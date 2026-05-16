---
title: "1-bit 8B×8アンサンブル vs Q4×1：RTX 4080でHumanEval実測比較"
url: "https://zenn.dev/seeda_yuto/articles/bonsai-8b-vs-qwen-q4-humaneval"
date: 2026-05-11
tags: [ローカルLLM, 量子化, 1-bit量子化, HumanEval, QAT, アンサンブル, llama.cpp, Ollama, RTX 4080, Bonsai-8B, Qwen3, ベンチマーク, VRAM最適化]
category: "infra"
related: [4332, 3642, 3653, 3909, 4331]
memo: "[Zenn LLM] 「1-bit 8B×8 と Q4×1 の比較がないと意味ないだろ」と言われたのでRTX 4080で実測した"
processed_at: "2026-05-11T21:33:31.801200"
---

## 要約

前回記事でBonsai-8B（1-bit量子化モデル）を16GB GPU上に8プロセス並列起動した実験に対し、「同じVRAM予算でQ4の1台と比較しないと意味がない」というコメントを受けて実施した追検証。RTX 4080（16GB VRAM）上でHumanEval 164問を用い、4構成を比較した。

比較対象はA: Qwen3-8B Q4_K_M×1（VRAM約9.4GB）、B: Bonsai-8B×1（約1.9GB）、C: Bonsai×8 worker-per-problem（約15.2GB、問題間並列）、D: Bonsai×8 true fanout（約15.2GB、問題内並列・best-of-8）の4構成。評価軸としてpass@1（精度）、tok/s（スループット）、QAT（Quality-Adjusted Throughput＝pass_rate×tok/s）の3軸を設定した。QATは「1秒あたり何個の正しい解を吐けるか」を示す合成指標。

結果はpass@1でQwen3-8B Q4が95.7%（157/164問）と圧勝。Bonsai×8のtrue fanout（D）でも90.2%（148問）にとどまり、16GBに8台載せた1-bitモデルでもQ4単騎の精度を超えられなかった。一方QATではBonsai×8 worker-per-problem（C）が227と、Qwenの85に対して2.66倍。Bonsai単体が212 tok/sで動き、8台並列で実効253 tok/sを達成した。

失敗問題の集合演算では、164問中5問が両モデル共通の失敗問題（HumanEval 3,5,21,22,28）であり、問題自体の難易度に起因する。Bonsai単体→×8でのアンサンブル精度ゲインは+1.2pp（実質2問分）で誤差に近く、同モデルのtemperature diversityでは本質的な多様性が出ないことが確認された（0.2で不正解の問題は高温で8発打っても似た間違え方をする）。

C（問題間並列）とD（問題内並列）の比較では、Dはwall timeが455秒とCの83秒に対して約5.5倍かかりQATで劣る。問題レベルで並列化しないため、8ワーカーあっても実質1台分×8倍の時間がかかる構造的な問題。

実用上の使い分けは明確で、チャットアプリにはQwen3-8B Q4（95.7%の質が直接ユーザー体験に影響）、CI・評価・大量生成バッチ処理にはBonsai×8 worker-per-problem（同じ時計時間で2.66倍の正答を生成可能）が適切。同モデルアンサンブルでの精度向上はコスパが悪く、異アーキテクチャ（Qwen+Phi-4+Gemma等）のheterogeneous ensembleが次の検討課題として示された。

監査エージェント開発への示唆：大量の監査ルール判定や証跡評価バッチ処理ではBonsai×8型のQAT最大化戦略が有効。ただし判断の質が直接リスク評価に影響するケースではQ4モデルの精度優位性を優先すべき。

## アイデア

- QAT（Quality-Adjusted Throughput＝pass_rate×tok/s）という合成指標で、精度とスループットのトレードオフを単一数値に落とし込む評価フレームワークが実用的
- 同モデルの温度多様性アンサンブルは+1.2pp程度の精度ゲインしか生まず、異アーキテクチャのheterogeneous ensembleの方が失敗モードの多様性を確保できるという実証
- 1-bit量子化モデルを同一GPU上に8並列展開することでバッチ処理スループットをQ4単体の2.66倍にする「問題間並列」戦略は、精度より処理量が求められるCI・評価パイプラインに直接応用可能

## 前提知識

- **量子化（Q4/1-bit）** (TODO: 読むべき)
- **HumanEval** → /deep_1052 RTX 4080で挑む強化学習コードLLM — 実行フィードバックで1.5Bモデルを鍛える全記録
- **pass@k** → /deep_4150 JURY-RL：ラベルなしRLVRのための「投票で提案、証明で決定」フレームワーク
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **best-of-N sampling** (TODO: 読むべき)

## 関連記事

- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る

## 原文リンク

[1-bit 8B×8アンサンブル vs Q4×1：RTX 4080でHumanEval実測比較](https://zenn.dev/seeda_yuto/articles/bonsai-8b-vs-qwen-q4-humaneval)
