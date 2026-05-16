---
title: "13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026"
url: "https://zenn.dev/76hata/articles/llm-humaneval-coding-score-tier-2026"
date: 2026-05-11
tags: [HumanEval, EvalPlus, LLMベンチマーク, ローカルLLM, Gemma4, Claude, Qwen3, MoE, RTX3090, Ollama, pass@1, コーディング評価]
category: "ai-ml"
related: [2862, 2056, 3642, 4176, 4029]
memo: "[Zenn LLM] 13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026"
processed_at: "2026-05-11T12:13:17.125795"
---

## 要約

OpenAIが公開したPythonコーディングベンチマーク「HumanEval」の拡張版EvalPlusを用い、Claude APIモデル4種とRTX 3090（VRAM 24GB）上で動作するローカルLLM 9種、計13モデルのコーディング性能をpass@1指標で実測比較した記事。HumanEval（基本164問）とHumanEval+（同164問だが1問あたりのテストケースを数十〜数百に増強したエッジケース強化版）の両方でスコアを計測している。

主な結果として、Claude Opus 4.7がHumanEval 98.8%・HumanEval+ 96.3%で全体最高スコアを記録。Claude Opus 4.6は98.8%/93.9%でHumanEval+では4.7に劣後。Claude Sonnet 4.6とHaiku 4.5はともに98.2%/93.3%と完全同スコアであり、APIコストが約1/4のHaikuがコーディングタスクでは圧倒的コスト優位を示す。

ローカルLLMではGemma 4 26BがHumanEval 98.2%・HumanEval+ 95.1%を達成し、Claude Sonnet/Haikuを上回るエッジケース対応力を示した。RTX 3090（中古相場8〜12万円）さえあれば月額コストゼロでSonnet/Haikuクラスのコーディング性能が得られる点は実用上重要。一方Gemma 4 31Bは95.7%/92.7%と26Bより低スコアとなり、モデルサイズと性能の単純な比例関係が成立しないことを示した。

Qwen3 30B-A3B（MoEアーキテクチャ、実効パラメータ約3B）は50.6%/49.4%と最下位グループに留まり、パラメータ数30Bという表記に反しDense版Qwen3 14B（87.2%）を大幅に下回った。LiteLLM Proxy経由・temperature=0という呼び出し条件とMoEの相性が影響している可能性がある。Command-R 35BはRAG特化設計のため61.0%と低スコアで、用途に応じたモデル選択の重要性を示す。

実行環境はOllama + LiteLLM Proxyによるローカル推論とVPS上のClaude CLI（subprocess経由）を統一スクリプトで計測。量子化レベルや推論サーバ設定によってスコアが5〜10%変動し得る点、HumanEvalがPython関数実装能力のみを測定しRAG・日本語処理・エージェント動作は対象外である点に注意が必要。監査エージェント開発においては、コーディング生成サブタスクにHaiku 4.5を使うことでSonnet比でAPIコストを約75%削減しながら同等性能を維持できる可能性が示唆される。

## アイデア

- Gemma 4 26BがHumanEval+でClaude Sonnet 4.6・Haiku 4.5（93.3%）を上回る95.1%を達成しており、RTX 3090という単一GPUで商用APIと同等のコーディング性能が月額ゼロで実現できる
- MoEアーキテクチャ（Qwen3 30B-A3B）がDense版14B（87.2%）を大幅に下回る50.6%に留まった事例は、パラメータ数表記が実効性能を表さないことの具体的証拠であり、モデル選定基準の見直しを迫る
- Claude Haiku 4.5がSonnet 4.6と完全同スコア（98.2%/93.3%）でAPIコストは約1/4（入力$0.80 vs $3.00/1M tokens）という結果は、コーディングサブタスク特化のエージェント設計でHaikuを優先選択する根拠となる

## 前提知識

- **HumanEval** → /deep_1052 RTX 4080で挑む強化学習コードLLM — 実行フィードバックで1.5Bモデルを鍛える全記録
- **pass@1** → /deep_763 学習中LLMのダウンストリーム性能を高速・高精度に計測するプロービング手法
- **MoEアーキテクチャ** → /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- **量子化（GGUF/Q4_K_M等）** (TODO: 読むべき)
- **EvalPlus** (TODO: 読むべき)

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4029 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤

## 原文リンク

[13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026](https://zenn.dev/76hata/articles/llm-humaneval-coding-score-tier-2026)
