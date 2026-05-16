---
title: "Car-GPT: LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-03
tags: [LLM, 自動運転, Vision Transformer, Perception, Planning, End-to-End学習, マルチモーダル, DriveGPT4, PromptTrack]
category: "ai-ml"
related: [3582, 1527, 1297, 182, 1817]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-03T12:08:41.301902"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する可能性を解説したThe Gradientの解説記事（2024年3月）。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割するモジュラー型と、単一ニューラルネットワークですべてを代替するEnd-to-End学習の2方式が存在するが、どちらも完全自律走行を実現していない。そこに第三の候補としてLLMを位置づける。LLMの基礎として、テキストをトークン（数値）に変換するトークナイゼーション、EncoderとDecoderで構成されるTransformerアーキテクチャ、次単語予測タスクを説明した上で、自動運転への転用方法を整理する。入力はカメラ画像・LiDAR点群・RADAR点群などのセンサデータで、Vision Transformer（ViT）やVideo Vision Transformerにより「トークン化」できる。出力は知覚説明・行動指示（車線変更など）・Q&Aなど多様なタスクに対応可能。Perceptionタスクでは、GPT-4 VisionやHiLM-D、MTD-GPTが物体検出・追跡を実施し、PromptTrackがDETRとLLMを組み合わせてオブジェクトにIDを付与。Planningタスクでは、DriveGPT4やSurrealDriverなどが画像・BEV（Bird's Eye View）マップからテキストで「直進すべき」「譲るべき」といった行動計画を生成する。さらに生成AIを使ってトレーニングデータや代替シナリオを合成するDatagenユースケースや、シーンに対するQ&Aインターフェース構築も活発に研究されている。LLMを自動運転に組み込む利点として、巨大な学習データ（インターネット上のテキスト・画像）から蒸留された常識的知識の活用と、自然言語による説明可能性（なぜその行動を選んだか）の担保が挙げられる。一方、課題としてはリアルタイム推論のレイテンシ、センサデータのトークン化コスト、幻覚（Hallucination）によるミスの致命的リスクが残る。監査AIへの示唆としては、LLMが複雑なマルチモーダル入力（文書・画像・数値データ）を統合して意思決定の根拠を自然言語で説明するパラダイムは、監査エージェントが不正リスクの根拠を説明可能な形で出力する設計に直接転用できる。特にPlanningモジュールをLLMが担う構造は、ReActエージェントが証拠を観察して次の監査手続を選択するロジックと同型であり、DriveGPT4的なアーキテクチャ（画像→LLM→行動テキスト）を監査ワークフロー（証憑→LLM→監査意見）に読み替えることができる。

## アイデア

- 自動運転の4モジュール（Perception/Localization/Planning/Control）をLLMの入出力パイプラインに置き換えるアーキテクチャが、監査エージェントの証拠収集→リスク判断→手続選択の構造と同型である点
- LiDARやRADAR点群もVision Transformerでトークン化できるという発想は、非構造化センサデータを言語モデルに統一的に食わせる汎用フレームワークへの道を示しており、表・PDF・ログなど多様な監査証拠の統合処理にも応用可能
- LLMがPlanning層を担うことで「なぜ車線変更したか」を自然言語で説明できる点は、説明可能なAI（XAI）の実装として既存のブラックボックス型End-to-Endモデルに対する明確な優位性であり、規制対応が求められる領域（監査・金融など）に直接訴求できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークナイゼーション** → /deep_2269 VideoFlexTok：粗から細へのコース・トゥ・ファイン動画トークナイゼーション
- **BEV（Bird's Eye View）** (TODO: 読むべき)

## 関連記事

- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_182 AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ
- /deep_1817 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態

## 原文リンク

[Car-GPT: LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
