---
title: "Mac mini M4 Pro / M4 Max でローカル LLM を動かす：VRAM 早見表と GGUF 量子化の選び方"
url: "https://zenn.dev/runlocal/articles/a506b0c8d57313"
date: 2026-05-21
tags: [GGUF, Ollama, llama.cpp, Apple Silicon, 統一メモリ, 量子化, ローカルLLM, M4 Pro, Q4_K_M]
category: "infra"
related: [3653, 4744, 6069, 5805, 4332]
memo: "[Zenn LLM] Mac mini M4 Pro / M4 Max でローカル LLM を動かす：VRAM 早見表と GGUF 量子化の選び方"
processed_at: "2026-05-21T09:04:51.422613"
---

## 要約

Apple Silicon の統一メモリ（Unified Memory）は CPU と GPU が同一メモリプールを共有するが、macOS の `recommendedMaxWorkingSetSize` 制約により GPU が実際に使えるのは搭載メモリの約 66〜75% に限られる。M4 Pro 24GB では実用 VRAM は約 16GB、48GB では約 36GB、M4 Ultra 64GB では約 48GB が安全圏となる。メモリ帯域は M4 Pro が 273 GB/s、M4 Max が 546 GB/s、M4 Ultra が 1092 GB/s であり、同一モデルでも M4 Pro と M4 Max/Ultra では推論速度が 2〜4 倍異なる点に注意が必要。

GGUF 量子化については Q4_K_M がデフォルト推奨（FP16 比 30%サイズ、品質劣化はほぼ体感不可）。VRAM に 1.3 倍以上余裕があれば Q5_K_M または Q8_0 に上げて品質を確保し、逆に乗らない場合は IQ3_M → Q2_K の順でフォールバックする。

構成別の実用モデルとしては、M4 Pro 24GB（~16GB VRAM）では Qwen 3.5 9B（Q4_K_M で 6.5GB）・Phi-4 14B（9.5GB）が快適に動作し、Mistral Small 3.2（14GB）はギリギリ。M4 Pro/Max 48GB（~36GB VRAM）では Gemma 4 27B（17GB）・Qwen 3.6 35B-A3B（21GB）がスイートスポット、70B クラスは IQ3_M（32GB）で辛うじて動作。M4 Ultra 64GB（~48GB VRAM）で初めて Qwen 3.5 72B が Q4_K_M（44GB）で実用速度（10 tok/s 以上）に達する。128GB 以上の Ultra では 70B〜120B 帯がベストで、GLM 4.6 の Q2_K（105GB）が視野に入る程度。

`sudo sysctl iogpu.wired_limit_mb=20480` で GPU 割当上限を一時的に引き上げることは可能だが、OS メモリ枯渇によるフリーズリスクがあるため非推奨。llama.cpp / ollama / LM Studio いずれを使用してもこのメモリ制約は共通であるため、モデル選定前に実用 VRAM の上限を把握することが無駄なダウンロードを防ぐ近道となる。監査エージェント開発においてローカル LLM を使う場合、M4 Pro 24GB では推論モデル（DeepSeek R1 7B）や Phi-4 14B 程度が現実的な選択肢となる。

## アイデア

- macOS の `recommendedMaxWorkingSetSize` による GPU 割当制限（66〜75%）は見落とされがちな制約であり、搭載メモリ量≠使用可能 VRAM という非自明な事実を定量的に整理している点
- メモリ帯域（273 / 546 / 1092 GB/s）が推論 token/s に直結するため、同一 VRAM 容量でも M4 Pro と M4 Max/Ultra で最大 4 倍の速度差が生じるというトレードオフの明示
- Q4_K_M をデフォルトとし、VRAM 余剰時は Q8_0 へのアップグレード、不足時は IQ3_M → Q2_K へのフォールバックという段階的量子化戦略の実用的フレームワーク

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **統一メモリ (Unified Memory)** (TODO: 読むべき)
- **Apple Silicon GPU** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_4744 LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開
- /deep_6069 Gemma 4 E4BをMacでローカル量子化してみた（llama.cpp + Q4_K_M）
- /deep_5805 AIの量子化とは何か？──組み込みエンジニアの視点で整理する
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測

## 原文リンク

[Mac mini M4 Pro / M4 Max でローカル LLM を動かす：VRAM 早見表と GGUF 量子化の選び方](https://zenn.dev/runlocal/articles/a506b0c8d57313)
