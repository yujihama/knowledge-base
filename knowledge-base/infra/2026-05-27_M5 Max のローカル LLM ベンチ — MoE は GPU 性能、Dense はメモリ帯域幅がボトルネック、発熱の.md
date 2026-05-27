---
title: "M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査"
url: "https://zenn.dev/kamo78/articles/ds4-m5max-benchmark"
date: 2026-05-27
tags: [Apple Silicon, M5 Max, ローカルLLM, MoE, DeepSeek, RTX 5090, thermal throttle, メモリ帯域幅, Ollama, mactop, ベンチマーク, Dense, Gemma4, Qwen3]
category: "infra"
related: [2056, 2062, 5266, 4176, 4332]
memo: "[Zenn LLM] M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査"
processed_at: "2026-05-27T09:01:55.504105"
---

## 要約

Apple M5 Max（40コアGPU / 128GB ユニファイドメモリ）上でローカル LLM 推論をテレメトリ計測し、ボトルネックを定量的に切り分けた検証記事。計測ツールは mactop（1Hz ロギング）および RTX 5090 側は nvidia-smi。

**MoE vs Dense のボトルネック差**
DeepSeek V4 Flash（MoE 284B-a13B / IQ2XXS 約81GB）のデコード中 DRAM 帯域使用率は最大 97 GB/s = 理論ピーク 614 GB/s の約16%にとどまる。MoE はトークンあたり活性化する expert が少なく（256 expert 中ごく一部）、1トークンあたり約 2.9 GB しかメモリから読み出されない。結果、Metal GPU の演算ユニットがボトルネックとなり、decode 34.1 tok/s を記録。一方 Gemma4 31B Dense は DRAM 577 GB/s（帯域使用率94%）と理論ピークに張り付き、decode 23 tok/s。「Apple Silicon = メモリ帯域がボトルネック」は Dense では正しいが MoE では成り立たない。

**Ollama 多モデル比較**
同条件で計測した結果、MoE 勢（ds4 / Qwen3.6 35B-a3B / gpt-oss 120B）はすべて帯域使用率 15–22% でGPU演算律速。Qwen3.6 35B-a3B Q4_K_M は 58 tok/s、gpt-oss 120B は 72 tok/s。Dense の Hermes3 70B は 11 tok/s で帯域使用率 46%、decode 2回目で GPU 温度 88°C / 周波数 1245 MHz（定格比-23%）まで落ちた。

**RTX 5090（WSL2）との比較**
32GB VRAM に収まる Qwen3.6 35B MoE と Gemma4 31B Dense で比較。decode は MoE 約 2.0x（58→118 tok/s）、Dense 約 2.8x（21.6→61 tok/s）。prefill 2k では Dense が 184→2,445 tok/s と約13倍に伸び、GDDR7 広帯域（公称約1.8 TB/s）の効果が大きい。

**熱ストレステスト（連続3分デコード）**
512トークンのデコードを冷却なしで連投した場合、RTX 5090 はクロック 1 MHz も低下せず MoE で 49°C・Dense で 64°C の平衡状態を維持。M5 Max は MoE（Qwen3.6）で開始 44°C から約1分で 98°C に達し、クロック 1620→1525 MHz、decode 速度 -13.1%（58.5→50.9 tok/s）。Dense（Gemma4）はより深刻で、クロックが 1299→690 MHz（ほぼ半減）、decode -29.8%（23.4→16.4 tok/s）、3分間で8反復しか回らなかった。

**実務的示唆**
ローカル LLM の体感速度評価には「ピーク tok/s」だけでなく持続負荷後の throttle 後速度を見ることが重要。MacBook Pro 筐体では特に Dense モデルで熱が深刻なボトルネックになる。Mac Studio 等の能動冷却筐体や dGPU 環境では持続スループットに大きな差が出る。監査エージェント等で長時間推論を行う場合は、筐体の冷却能力と持続スループットの両方を考慮したハードウェア選定が必要。

## アイデア

- MoE モデルはトークンあたりの活性 expert 数が少ないため DRAM 帯域を消費せず、Apple Silicon でも GPU 演算がボトルネックになるという構造的な非対称性
- 連続3分のデコードで M5 Max の Dense モデルがクロックほぼ半減（1299→690 MHz）・速度-30%という極端な throttle を示す一方、RTX 5090 が 64°C 平衡・クロック変動ゼロというデータで、持続スループット評価の重要性が定量的に明確化された
- DRAM 帯域使用率という単一の指標でモデルアーキテクチャ（MoE vs Dense）のボトルネックタイプを即座に識別できるテレメトリ手法（mactop + 1Hz ロギング）

## 前提知識

- **MoE (Mixture of Experts)** (TODO: 読むべき)
- **メモリ帯域幅律速** (TODO: 読むべき)
- **Thermal throttling** (TODO: 読むべき)
- **量子化 (IQ2XXS/Q4_K_M)** (TODO: 読むべき)
- **Unified Memory** (TODO: 読むべき)

## 関連記事

- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較
- /deep_2062 Dense vs MoE推論モデルの実力比較：Gemma 4, Phi-4, Qwen3を徹底検証
- /deep_5266 13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測

## 原文リンク

[M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査](https://zenn.dev/kamo78/articles/ds4-m5max-benchmark)
