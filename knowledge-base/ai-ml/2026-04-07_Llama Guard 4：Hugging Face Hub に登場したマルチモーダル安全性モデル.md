---
title: "Llama Guard 4：Hugging Face Hub に登場したマルチモーダル安全性モデル"
url: "https://huggingface.co/blog/llama-guard-4"
date: 2026-04-07
tags: [Llama Guard 4, safety model, multimodal, content moderation, pruning, MLCommons, prompt injection, jailbreak detection, dense model, Meta]
category: "ai-ml"
memo: "[HF Blog] Welcoming Llama Guard 4 on Hugging Face Hub"
processed_at: "2026-04-07T21:39:36.145845"
---

## 要約

MetaがLlama Guard 4を公開した。Llama 4 Scoutモデルから密結合(dense)アーキテクチャに枝刈り(pruning)された12Bパラメータのマルチモーダル安全性モデルで、24GB VRAMのシングルGPUで動作する。Llama 4 ScoutはMixture-of-Experts(MoE)構造（1共有エキスパート＋16ルーティングエキスパート）を持つが、Llama Guard 4ではルーティングエキスパートとルーターレイヤーを削除し、共有エキスパートのみを残すことでdenseモデルとして初期化している。追加の事前学習は行わず、マルチ画像（最大5枚）訓練データと人手アノテーションによる多言語データ（テキスト:マルチモーダル＝3:1）でポストトレーニングを実施。MLCommons hazard taxonomyに基づく14カテゴリ（暴力的犯罪S1、非暴力的犯罪S2、性犯罪S3、児童性的搾取S4、名誉毀損S5、専門アドバイスS6、プライバシーS7、知的財産S8、無差別兵器S9、ヘイトS10、自傷・自殺S11、性的コンテンツS12、選挙S13、コードインタープリタ悪用S14）を検出し、ユーザー側で検出対象カテゴリを除外設定可能。前バージョンのLlama Guard 3との比較では、英語でRecall +4%・F1 +8%、マルチ画像でRecall +20%・F1 +17%の改善を達成。テキストと画像の入力・出力の両方に対するモデレーションパイプラインをサポートし、ユーザー入力のフィルタリングとモデル生成レスポンスのフィルタリングを独立して適用できる。また、Llama Prompt Guard 2シリーズとして86Mと22Mパラメータの2モデルを同時公開。これらはプロンプトインジェクションおよびジェイルブレイクの検出に特化したバイナリ分類モデルで、前バージョンより軽量・高性能かつ敵対的攻撃に耐性のあるトークナイズを採用。HuggingFace transformersのプレビューリリース経由でpipeline APIおよびAutoModel APIで利用可能。

## アイデア

- MoEモデルをdenseモデルに枝刈りする手法：共有エキスパートの重みのみ保持することで、追加事前学習なしに小型・高速なモデルに変換できる点は、大規模モデルを特定タスク向けに効率化する実用的な蒸留代替手法として興味深い
- カテゴリ除外設定による柔軟なモデレーション：`excluded_category_keys`パラメータでチャットテンプレート生成時にシステムプロンプトを動的に変更し、不要カテゴリを除外できる設計は、用途特化の安全フィルターを構築する際の参考になる
- 入力・出力の双方向モデレーションパイプライン：ユーザーメッセージとアシスタント応答を同一モデルで評価できる構造により、エージェントシステムにおけるガードレールを単一モデルで実装できる点は、エージェントアーキテクチャとの統合設計において有用

## Yujiの取り組みへの示唆

監査エージェントシステムにおいて、LangGraphのノード間でLlama Guard 4をガードレールとして組み込むことで、LLMの入出力に対する安全性チェックを自動化できる。特にコードインタープリタ悪用(S14)やプライバシー(S7)カテゴリの検出は、監査データを扱うエージェントパイプラインのリスク管理に直接活用可能。また、LLM-as-judgeの評価フレームワークにおいて、安全性評価の一部をLlama Guard 4で代替・補完する構成も検討に値する。Llama Prompt Guard 2はエージェントへのプロンプトインジェクション対策として、入力バリデーション層に組み込める実用的なコンポーネントとなる。

## 原文リンク

[Llama Guard 4：Hugging Face Hub に登場したマルチモーダル安全性モデル](https://huggingface.co/blog/llama-guard-4)
