---
title: "FalconモデルがHugging Faceエコシステムに登場"
url: "https://huggingface.co/blog/falcon"
date: 2026-04-10
tags: [Falcon, LLM, Apache2.0, Multi-Query-Attention, RefinedWeb, PEFT, LoRA, 量子化, bitsandbytes, HuggingFace]
category: "ai-ml"
memo: "[HF Blog] The Falcon has landed in the Hugging Face ecosystem"
processed_at: "2026-04-10T09:44:36.414031"
---

## 要約

Abu DhabiのTechnology Innovation Institute（TII）が開発したオープンソースLLMファミリー「Falcon」がHugging Faceエコシステムに統合された。Apache 2.0ライセンスで商用利用可能であり、Falcon-40BはリリースTimestamp（2023年6月）時点でOpen LLM Leaderboardのトップに位置し、LLaMA-65Bを上回る性能を持ちながらVRAM消費は約90GBと少ない。Falcon-7Bは約15GBで動作し、コンシューマー向けGPUでも推論・ファインチューニングが可能。2023年9月にはFalcon-180Bも公開され、PaLM-2に匹敵すると評価されている。

技術的な特徴として、学習データの80%以上にRefinedWeb（CommonCrawlを大規模重複排除・フィルタリングで精製した約1.5兆トークンのWebデータセット）を使用している点が挙げられる。GPT-3やPaLMのように多数のキュレーション済みデータソースを組み合わせる方式とは異なり、Web規模のデータ品質向上に特化した戦略を採る。TIIはRefinedWebの6000億トークン版をコミュニティ向けに公開している。

アーキテクチャ面では「Multi-Query Attention（MQA）」を採用しており、通常のMulti-Head Attentionが各ヘッドに個別のKey・Valueを持つのに対し、MQAは全ヘッドでKey・Valueを共有する。この設計により、自己回帰デコーディング時のK,Vキャッシュサイズが大幅に削減される（Falcon-7Bで20MB、LLaMA-7Bの1,100MBと比較）。推論スループットの向上とステートフルな最適化が可能になる。

Hugging Faceエコシステムとの統合では、transformersのpipeline APIによる推論、bitsandbytesを用いた8bit/4bit量子化（40Bモデルを45GB程度に圧縮）、PEFTライブラリを使ったLoRAファインチューニング、Text Generation Inferenceサーバーによる高速デプロイが提供されている。Instruct版（Falcon-7B-Instruct、Falcon-40B-Instruct）はインストラクション・会話データでファインチューニング済みで、即座にアシスタント用途に利用可能。Core ML変換によりM1 MacBook Proでのローカル実行も実証された。

## アイデア

- Multi-Query Attentionによるキャッシュサイズ削減（LLaMA比で50倍以上）は、長文脈の監査ドキュメント処理においてメモリボトルネックを緩和する有効な手法
- RefinedWebのように大規模Webデータを重複排除・品質フィルタリングで精製するアプローチは、ドメイン特化コーパス（監査基準文書など）の構築手法に応用できる
- LoRA+4bit量子化の組み合わせによりコンシューマーGPUでの40Bクラスモデルのファインチューニングが可能になった点は、ローカルLLMインフラ構築コストの劇的な低下を示す

## Yujiの取り組みへの示唆

Apache 2.0のFalconモデルは、Yujiが構築中のローカルLLMインフラ（RTX 3090）上で監査エージェントのバックボーンLLMとして活用できる候補。特にPEFT/LoRAによる監査ドメインへのファインチューニングと、bitsandbytesを用いた量子化による単一GPU運用の組み合わせは、LangGraphベースのエージェントシステムに組み込む際の実装参照として直接利用可能。また、LLM-as-judgeパイプラインにおける推論コスト削減にMulti-Query Attentionの特性が寄与する可能性がある。

## 原文リンク

[FalconモデルがHugging Faceエコシステムに登場](https://huggingface.co/blog/falcon)
