---
title: "FetchがHugging FaceとAWSを活用してAIツールを統合し、開発時間を30%削減"
url: "https://huggingface.co/blog/fetch-eap-case-study"
date: 2026-04-10
tags: [Hugging Face, AWS SageMaker, AWS Inferentia, Transformers, Document AI, エンティティ解決, セマンティック検索, MLOps, シャドウパイプライン]
category: "infra"
memo: "[HF Blog] Fetch Consolidates AI Tools and Saves 30% Development Time with Hugging Face on AWS"
related: [1015, 303, 1578, 1448, 1529]
processed_at: "2026-04-10T12:37:26.215896"
---

## 要約

Fetchはショッピングリワードアプリを運営する消費者向け企業で、月間アクティブユーザー1,800万人、1日1,100万枚のレシートを処理する規模を持つ。従来はサードパーティのブラックボックスAIソリューションを使用してレシートのスキャン・処理を行っていたが、ビジネスパートナーが求める顧客エンゲージメントの詳細なデータを提供できないという課題があった。コンピュータビジョン科学者のBoris Koganが主導し、12ヶ月の計画を8ヶ月で完了させ、AWS上で自社のML・AIモデルを構築した。技術スタックはAmazon SageMaker（モデルの構築・学習・デプロイ）とAWS Inferentiaアクセラレータ（深層学習推論の高性能・低コスト処理）を中心に構成。Hugging FaceのExpert Acceleration Program（EAP）を通じてHugging FaceのMLエンジニアYifeng Yinがアドバイザリーとして参画し、TransformersモデルやDocument AIモデルの活用方法を指導した。具体的な成果は、開発時間30%削減、レシート処理レイテンシ50%削減、モデルのトレーニング時間が従来の数日〜数週間から数時間へ短縮。移行プロセスでは「シャドウパイプライン」を構築し、本番の1,100万枚/日のレシート処理を継続しながら新MLパイプラインの結果を並行検証することでリスクを排除した。エンティティ解決とセマンティック検索の精度も向上し、ブラックボックス依存から脱却することでビジネスリスクを低減。オープンソースのTransformersモデルを活用することで、従来は訓練が困難だったモデルを短期間で実用化できた点が技術的な核心である。

## アイデア

- シャドウパイプライン戦略：本番システムを停止せず新MLパイプラインを並行稼働させ、出力を旧システムと比較検証してからカットオーバーする手法は、大規模AIシステム移行のリスク管理として汎用性が高い
- ブラックボックスAIからの脱却コスト：サードパーティAIへの依存はデータ粒度・制御性・ビジネスリスクのトレードオフを生む。自社モデル化によりデータの可視性が向上し、パートナーへの詳細レポートが可能になった
- Hugging Face EAPのアドバイザリーモデル：コードを書くのではなくナレッジトランスファーに特化した支援形態が開発者チームの自律性を高めつつ30%の効率改善をもたらした点は、企業へのAI導入支援モデルとして参考になる
## 関連記事

- /deep_1015 Transformersドキュメントの再設計：混乱を整理する
- /deep_303 Sentence TransformersがHugging Faceに移管——月間100万ユーザーの埋め込みライブラリが新体制へ
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング

## 原文リンク

[FetchがHugging FaceとAWSを活用してAIツールを統合し、開発時間を30%削減](https://huggingface.co/blog/fetch-eap-case-study)
