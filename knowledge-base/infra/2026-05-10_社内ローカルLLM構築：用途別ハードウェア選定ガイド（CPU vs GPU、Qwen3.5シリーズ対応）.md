---
title: "社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）"
url: "https://zenn.dev/shineos/articles/local-ai-model-deployment-guide-2026"
date: 2026-05-10
tags: [ローカルLLM, Qwen3.5, Ollama, 量子化, GPU選定, Whisper, SDXL, ハードウェア構成, CPU推論]
category: "infra"
related: [3642, 4332, 4043, 4472, 3810]
memo: "[Zenn LLM] 【AI開発】社内でローカルLLMを構築したい。最高スペックのサーバーを買えば良いのか？｜用途別ハードウェア選定ガイド"
processed_at: "2026-05-10T09:34:53.843670"
---

## 要約

クラウドAPIコスト増大やデータプライバシー懸念を背景に、社内ローカルLLM構築の需要が高まっているが、「最高スペックのGPUサーバーを買えば良い」は誤りである。本記事は2026年3月時点のQwen3.5シリーズを例に、用途別ハードウェア選定基準を整理する。

最大のポイントは「LLM推論にGPUは必須ではない」という点。Qwen3.5 9Bをq4_K_M量子化（4bit）で実行すると、RAM約6.6GBのみで動作し、Intel Core i7相当のCPUで5〜20 tokens/秒を実現できる。社内FAQやバッチ文書要約など、リアルタイム性が不要な用途ではGPUは不要。

CPU vs GPUの比較では、CPUのみ構成が初期投資5〜15万円・消費電力50〜150Wで済む一方、GPUありは20〜100万円以上・200〜700Wを要するが推論速度は10〜50倍に向上する。

用途別要件は以下の通り。汎用LLM低頻度：CPU+32GB RAMで5〜15万円。汎用LLM高頻度：RTX 4070（12GB）で25万円程度。音声認識（Whisper Large v3 Turbo）：RTX 4060（8GB）で15〜25万円、リアルタイム処理には必須。画像生成（SDXL/Flux）：CPUは不可、RTX 4080（16GB）以上で30〜50万円。画像認識（Qwen3.5-VL）：RTX 4090（24GB）で40〜80万円。コード生成高頻度（Qwen3.5 27B）：RTX 4080で30〜50万円。

推奨アプローチは段階的スケールアップ。まずOllamaでCPU検証（`ollama run qwen3.5:9b-q4_K_M`）を行い、5 tokens/秒以上なら運用可能と判断。不足する場合のみGPUを追加する。H100（1台200万円・700W）のようなハイエンドは、100B超の大規模モデル学習や動画処理でなければ過剰投資となる。

Qwen3.5シリーズはAlibaba Qwenチームが2026年2月にリリース。201言語対応、最大256Kトークンコンテキスト、Apache 2.0ライセンスで商用利用可能。MoEアーキテクチャのQwen3.5-35B-A3Bは32B相当の性能を低VRAMで実現する点も注目。

監査エージェント開発への示唆：内部監査向けRAGシステムや文書要約エージェントは低頻度・バッチ処理が多く、CPU構成（10〜15万円）から始めてOllamaで検証するアプローチが費用対効果の観点から最適。機密データを扱う監査用途ではローカルLLMのプライバシー優位性は大きく、量子化モデルであれば既存PCスペックで試験運用が可能。

## アイデア

- テキスト生成に限定すれば量子化（q4_K_M）でCPUのみ実用運用が可能であり、監査文書の非同期バッチ要約ならGPU投資ゼロで始められる
- MoEアーキテクチャ（Qwen3.5-35B-A3B）が32B相当の能力を低VRAM（A3B=Active 3B）で実現する設計は、エッジ・オンプレ環境での大規模モデル活用の新たな方向性を示す
- 段階的スケールアップ戦略（CPU検証→GPU追加）はエージェントシステムの本番移行判断にも応用でき、5 tokens/秒という具体的な閾値がGo/No-Goの定量基準として機能する

## 前提知識

- **量子化（GGUF/Q4/Q8）** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **VRAM容量とモデルサイズ** (TODO: 読むべき)
- **Whisper** → /deep_128 WAXAL: アフリカ言語音声技術のための大規模オープンリソース
- **Stable Diffusion** → /deep_1211 LCM LoRAによるSDXLの4ステップ高速推論

## 関連記事

- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_4472 7年前のChromebookでローカルLLMは動くのか？ Trillim + Ternary Bonsai を Crostini で試す
- /deep_3810 64GB RAM & Podman と格闘しながら専用 ChatGPT を立てた話

## 原文リンク

[社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）](https://zenn.dev/shineos/articles/local-ai-model-deployment-guide-2026)
