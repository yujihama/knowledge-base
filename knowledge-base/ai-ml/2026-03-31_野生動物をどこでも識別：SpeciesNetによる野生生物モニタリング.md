---
title: "野生動物をどこでも識別：SpeciesNetによる野生生物モニタリング"
url: "https://research.google/blog/where-wild-things-roam-identifying-wildlife-with-speciesnet/"
date: 2026-03-31
tags: [CNN, transfer-learning, fine-tuning, computer-vision, open-source, wildlife-monitoring, MegaDetector, Google-Earth-AI]
category: "ai-ml"
memo: "[Google AI Blog] Where wild things roam: Identifying wildlife with SpeciesNet"
related: [1564, 214, 1492, 1449, 161]
processed_at: "2026-03-31T09:11:56.173390"
---

## 要約

SpeciesNetはGoogleが開発した野生生物識別AIモデルで、2025年にオープンソース化されてから1年が経過し、世界中の研究・保全プロジェクトで活用されている。モデルは哺乳類・鳥類・爬虫類を含む2,498カテゴリを分類可能で、6,500万枚以上のラベル付き画像で学習されている。アーキテクチャは畳み込みニューラルネットワーク（CNN）を採用し、照明・角度・距離が異なる条件下での種レベルの識別を実現。動物含有画像の検出率は99.4%、種レベルへの分類は83%のケースで実施され、その予測精度は94.5%。処理速度は標準ラップトップで1日約30,000枚、低価格帯ゲーミングGPUで250,000枚以上。MegaDetectorという別のオープンソースモデルと連携し、画像内の動物領域を特定してからSpeciesNetが種を識別する2段階パイプラインを構成する。Wildlife Insightsプラットフォーム（約2億枚の人間検証済み画像を保有）と統合されており、ユーザーがラベル付けした画像が再びモデルの学習データにフィードバックされる自己強化サイクルを持つ。具体的な活用事例として、タンザニアのSnapshot Serengetiプログラムでは1,100万枚の画像を数日で処理（従来は市民科学者が数十年かかる量）、オーストラリアのWildObsはmusky rat-kangarooやorange-footed scrubfowlなど既存ラベルにない固有種に対してファインチューニングを実施、アイダホ州魚類野生生物局は数百台のカメラトラップからのデータ処理ワークフローに組み込み人間の最終確認の前段として活用。The Nature ConservancyのAnimlやデスクトップツールAddaxAIなどのサードパーティプラットフォームにも統合されており、エコシステムが拡大中。Google Earth AIコレクションの一部として位置付けられ、地理空間AIツール群との統合も進む。

## アイデア

- 6,500万枚規模のドメイン特化データセットで学習したモデルを地域固有種にファインチューニングするアプローチは、監査ドメインでの汎用LLMを特定業種・規制環境に適応させる手法と構造的に同じであり、少量の専門ラベルデータで高精度を達成するパターンとして参考になる
- MegaDetector（物体検出）→SpeciesNet（種分類）の2段階パイプラインは、粗いフィルタリングで処理対象を絞り込んでから高精度モデルを適用するアーキテクチャパターンで、大量文書処理における前処理段階の設計に応用できる
- 人間検証済みラベルが次世代モデルの学習データに還流するフライホイール構造（Wildlife Insights ↔ SpeciesNet）は、LLM-as-judgeによる継続的な品質改善ループと同様の考え方であり、RLAIF設計の具体的な実装参考例となる

## 関連記事

- /deep_1564 自己教師あり単眼深度推定のための適応的深度変換スケール畳み込み（DcSConv）
- /deep_214 画像シャープニングによる効率的な先制的ロバスト化
- /deep_1492 タンパク質への深層学習：プロテイン言語モデルの仕組みと応用
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_161 鳥の音声で訓練されたAIが水中の謎を解明：Perch 2.0の転移学習

## 原文リンク

[野生動物をどこでも識別：SpeciesNetによる野生生物モニタリング](https://research.google/blog/where-wild-things-roam-identifying-wildlife-with-speciesnet/)
