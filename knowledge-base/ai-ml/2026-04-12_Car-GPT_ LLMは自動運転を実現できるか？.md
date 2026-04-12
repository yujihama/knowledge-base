---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-12
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Chain-of-Thought, Perception, Planning, Diffusion Model, PromptTrack, GPT-Driver]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-12T09:25:06.274568"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に適用する可能性をThe Gradient誌が解説したもの（2024年3月）。自動運転の従来アーキテクチャは「モジュール型」（Perception→Localization→Planning→Controlの分離構成）であり、2010年代にはこの設計が主流だった。その後、単一ニューラルネットワークで操舵・加速を直接予測する「End-to-End学習」が注目されたが、ブラックボックス問題が残る。LLMはこの文脈で第三の選択肢として浮上している。

LLMの基本構造として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoderまたは純Decoder構成のTransformerアーキテクチャ、そしてNext-Word Predictionという出力機構が説明される。GPT系モデルは純Decoder型。

自動運転への適用では、入力をカメラ画像・LiDAR点群・RADAR点群などに拡張し、Vision Transformer（ViT）でトークン化する。研究が活発な領域は4つ：①Perception（環境認識・物体検出）、②Planning（行動決定）、③Generation（学習データ生成・シナリオ拡張）、④Q&A（チャット型インターフェース）。

具体的なモデルとして、HiLM-DやMTD-GPTが動画含む物体検出に対応。PromptTrackはDETR検出器とLLMを組み合わせ、物体への一意ID割り当て（4D Perception相当）を実現。Planning領域ではGPT-Driverがシーン記述からCoT（Chain-of-Thought）推論で運転判断を生成し、PromptDriverはゼロショットでLLMを運転エージェントとして機能させる。DriveCoT、DiMA等もPlanning研究の代表例として挙げられる。

データ生成面では拡散モデル（Diffusion Model）との組み合わせが鍵で、テキスト記述から現実的なドライビングシナリオを生成することで学習データ不足を補う。Q&A応用ではDriveVLM等がマルチモーダル入力に基づきドライバーへの説明生成や意思決定の根拠提示を行う。

監査エージェント開発への示唆：LLMをPlanning層に組み込みCoTで判断根拠を自然言語で出力する設計は、監査エージェントの「判断の説明可能性」要件と構造的に同一。GPT-DriverやPromptDriverのゼロショット推論アプローチは、少数事例しかない監査シナリオへのLLM適用設計の参考になる。

## アイデア

- GPT-DriverがChain-of-Thought推論でPlanning判断を自然言語として出力する設計は、監査エージェントの意思決定説明可能性と同一の構造問題を解いており、実装パターンを転用できる
- PromptTrackのDETR＋LLM統合アーキテクチャは、構造化出力（物体ID）と自然言語推論を同一モデルで扱う手法として、Pydantic＋LangGraphによるエージェント出力設計に応用可能
- 拡散モデルによるシナリオ生成でレアケースの学習データを補う手法は、監査でも稀な不正パターンの合成データ生成に転用できる可能性がある

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **Chain-of-Thought推論** (TODO: 読むべき)
- **DETR** (TODO: 読むべき)
- **Diffusion Model** → [データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク](../ai-ml/2026-04-06_データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡.md)

## 関連記事

- [DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化](../ai-ml/2026-04-09_DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化.md)
- [🤗 Transformersでネイティブサポートされる量子化スキームの概要](../infra/2026-04-09_🤗 Transformersでネイティブサポートされる量子化スキームの概要.md)
- [🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング](../ai-ml/2026-04-10_🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング.md)
- [高忠実度画像圧縮のためのノイズ制約拡散（NC-Diffusion）フレームワーク](../ai-ml/2026-04-10_高忠実度画像圧縮のためのノイズ制約拡散（NC-Diffusion）フレームワーク.md)
- [階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由](../agent-arch/2026-04-07_階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由.md)

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
