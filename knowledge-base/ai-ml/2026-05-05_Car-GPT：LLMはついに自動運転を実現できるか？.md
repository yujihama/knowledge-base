---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-05
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, Perception, Planning, DriveLM, マルチモーダル]
category: "ai-ml"
related: [3582, 1527, 1297, 182, 1817]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-05T12:54:24.008656"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を概説した解説記事（2024年3月）。自動運転の歴史的アプローチとして、従来のモジュラー型（Perception・Localization・Planning・Controlの4段階分離）とEnd-to-End学習（単一ニューラルネットで操舵・加速を直接予測）を対比した上で、LLMが第三の解答となり得るかを検討する。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ、および次単語予測タスクを平易に説明。Vision Transformerを用いれば画像・LiDAR点群・RADARデータも同様にトークン化可能であり、Transformerブロック自体はモダリティ非依存であることを指摘する。

自動運転へのLLM応用として2023年時点の主要研究領域は4つ：①Perception（環境記述・物体検出）、②Planning（行動決定・軌跡生成）、③Generation（学習データ・シナリオの拡散モデルによる生成）、④Q&A（シナリオベースの対話インターフェース）。

Perceptionでは、GPT-4 Visionによる物体検出に加え、HiLM-D・MTD-GPT（画像・動画対応）、PromptTrack（DETRとLLMを組み合わせてオブジェクトIDを追跡）などが紹介される。Planningでは、DriveVLM・UniAD・VAD・DriveLMといったモデルが、鳥瞰図や多視点画像を入力として自然言語で行動理由を説明しながら軌跡を出力する。特にDriveLMはシーングラフを用いた視覚的Q&Aを自動運転に導入している。

一方で課題も明示されており、①リアルタイム推論の計算コスト（GPT-4の応答速度は自動運転の要求に不十分）、②LLMのハルシネーション（存在しない物体を「見る」リスク）、③学習データの偏り（インターネット上の一般テキストと道路環境の乖離）、④センサーデータの直接処理能力の未成熟、が挙げられる。

監査エージェント開発への示唆：LLMを意思決定モジュールに組み込みながら自然言語で理由を出力させる設計（DriveLMのQ&A方式）は、監査エージェントが判断根拠を説明可能な形で記録する仕組みとほぼ同型。また、End-to-End化のブラックボックス問題とモジュラー型の解釈性トレードオフは、監査AIの説明責任設計でも直面する課題と対応する。

## アイデア

- Vision TransformerによってLiDAR・RADAR・カメラデータを統一的にトークン化し、単一Transformerで処理するモダリティ非依存アーキテクチャは、センサー融合の複雑性を大幅に削減する可能性がある
- DriveLMのシーングラフ＋視覚的Q&Aアプローチは、エージェントが行動根拠を自然言語で出力する設計の実用例であり、説明可能なエージェント全般に転用できる
- ハルシネーション問題は自動運転では安全上の致命的リスクになるため、LLMの確信度校正（calibration）やフォールバック機構の設計がLLMエージェント全般の信頼性確保における核心的課題であることを再確認させる

## 前提知識

- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開

## 関連記事

- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
