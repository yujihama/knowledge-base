---
title: "Hugging FaceがWitty Worksの包括的表現ライティングアシスタント開発を加速した事例"
url: "https://huggingface.co/blog/classification-use-cases"
date: 2026-04-10
tags: [SetFit, Sentence-Transformers, few-shot-learning, text-classification, mpnet-base-v2, contrastive-learning, KNN, logistic-regression, Azure]
category: "ai-ml"
memo: "[HF Blog] How Hugging Face Accelerated Development of Witty Works Writing Assistant"
processed_at: "2026-04-10T12:35:55.730171"
---

## 要約

Witty Worksは2018年設立のスタートアップで、多様性・包括性を促進するため、メールやLinkedInの投稿、求人広告などの文章中の非包括的表現を自動検出・修正するブラウザ拡張機能を開発している。英語・フランス語・ドイツ語に対応し、約2300語の非包括的語彙データベースを保有する。

初期アプローチはspaCyの転移学習モデルを用いたルールベース手法で、形態素解析・品詞タグ付け・固有表現抽出などの言語的特徴を活用して非包括的語を検出していた。この手法は語彙の85%に対しては有効だったが、文脈依存語（例：「fossil」が化石燃料を指す場合と人を指す場合）には対応できなかった。

Hugging Face Expert Acceleration Program（EAP）への参加を通じて、以下の3つの技術的改善が実現された。

1. **アーキテクチャ選択**: バニラTransformerによるトークン埋め込みから、Sentence Transformersによる文全体の埋め込みへ移行。Siamese networkとtriplet networkを組み合わせ、意味的に類似した文同士の距離を最小化する表現学習を実施。得られた文埋め込みをKNNまたはロジスティック回帰の入力として使用。

2. **ライブラリ選択**: SetFit（Sentence Transformers Fine-tuning）を採用。対照学習と文間意味的類似度を組み合わせることで、少数ラベルデータでの高精度分類を実現。従来は問題語1語あたり100〜200件のアノテーション済みデータが必要だったが、SetFit導入により15〜20件まで削減。これによりデータ収集・アノテーションコストを大幅に節約。

3. **モデル選択とデプロイ**: mpnet-base-v2とロジスティック回帰・KNNの組み合わせを採用。Google Colabでの初期検証後、追加最適化不要でAzureにデプロイ完了。最終的な分類精度は0.92を達成。

Witty Worksのリード・データサイエンティストElena Nazarenko氏は、HFエキスパートの支援により大規模データセット構築を回避でき、時間とコストを節約できたと述べている。CTOのLukas Kahwe Smith氏は、EAPはスタートアップにとって費用対効果の高いスパーリングパートナーだと評価している。

## アイデア

- SetFitによるfew-shot分類：1クラスあたり15〜20件のラベルデータで精度0.92を達成。大規模アノテーションなしに実用レベルの分類器を構築できる点は、データ収集コストが高い業務ドメインへの応用価値が高い
- 文脈依存語の処理にSentence Transformers（文全体の埋め込み）を使用し、KNN/ロジスティック回帰と組み合わせるアーキテクチャは、ルールベースと機械学習のハイブリッドとして実装・保守が容易
- バイアス管理の透明性確保のため意図的にトレーニングデータ数を絞り、人手レビューを維持するというアプローチは、説明可能性・監査可能性が求められるユースケースにおける設計指針として参考になる
## 関連記事

- /deep_161 鳥の音声で訓練されたAIが水中の謎を解明：Perch 2.0の転移学習
- /deep_369 視覚的In-Contextデモンストレーション選択の学習
- /deep_499 自己教師あり表現学習のためのガウス結合埋め込み（GJE/GMJE）
- /deep_281 時系列ファウンデーションモデルのフューショット学習：TimesFM-ICFの提案
- /deep_930 Ultrasound-CLIP: 超音波画像テキスト理解のためのセマンティック対照事前学習

## 原文リンク

[Hugging FaceがWitty Worksの包括的表現ライティングアシスタント開発を加速した事例](https://huggingface.co/blog/classification-use-cases)
