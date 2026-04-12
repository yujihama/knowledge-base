---
title: "Rocket Money × Hugging Face: 本番環境における揮発性MLモデルのスケーリング事例"
url: "https://huggingface.co/blog/rocketmoney-case-study"
date: 2026-04-09
tags: [BERT, テキスト分類, Hugging Face Inference API, モデルサービング, MLOps, GCP, トランザクション分類, 本番ML]
category: "infra"
memo: "[HF Blog] Rocket Money x Hugging Face: Scaling Volatile ML Models in Production​"
related: [1574, 117, 1489, 1645, 396]
processed_at: "2026-04-09T21:47:59.010104"
---

## 要約

Rocket Money（旧Truebill）は、ユーザーの銀行口座からトランザクションデータを収集し、加盟店・サービスの検出・分類を行うパーソナルファイナンスアプリ。月1億件以上のトランザクションを処理するこのシステムで、従来のRegexベースの正規化器と決定テーブルによる分類手法が、クラス数増加（4,000以上）とともに限界を迎えた。

その後、BERTファミリーモデルをベースにしたテキスト分類システムを構築。GCP上のウェアハウスでオフライン評価を実施し、Retoolでラベリングキューやゴールドスタンダード検証データセット・ドリフト検出モニタリングツールを整備した。モデルがオフラインで高性能を示した後、MLOpsチームを持たない小規模組織として、サービング基盤を内製ではなく外部調達する判断を行った。

候補として、内製プロトタイプ・AWS SageMaker・Hugging Face Inference APIを3ヶ月間比較評価した。GCPベースのパイプラインとの連携においてSageMakerは手間がかかる一方、Hugging FaceはセットアップがシンプルでGCPとの親和性も高く、1週間以内にトラフィックの一部を処理できた。段階的なトラフィック増加と最悪ケースを想定した負荷試験を経て、最終的にHugging Faceを採用。

本番移行後は、旧Regexシステムとのスプリットテストで新規ユーザーを50%ずつ振り分け、有料ユーザー継続率・エンゲージメントなどビジネス指標でMLモデルが優位であることを確認してから段階的に100%へ移行（約2ヶ月）。クラス数を増やした第2世代モデルへの切り替え時にアウテージが発生、キャッシュ問題による旧モデルの応答継続などのインシデントも経験しつつ、両社共同で解決した。

Hugging Face側との共有Slackチャンネルを設置し、技術課題への迅速対応と能動的な問題解決を評価。MLエンジニア小規模チームでも本番グレードのサービングを実現した好事例として位置付けられる。

## アイデア

- MLOpsチームなしでBERTベース本番推論を実現するために、モデルサービング基盤を外部調達（Buy vs Build）する意思決定フレームワーク
- 4,000以上のクラスを持つ多クラステキスト分類において、クラス追加コストとビジネス価値のトレードオフを定量評価する設計思想
- A/Bテストをモデル精度だけでなく有料ユーザー継続率などビジネスメトリクスと組み合わせて評価することで、段階的なトラフィック移行の意思決定を確実にするアプローチ
## 関連記事

- /deep_1574 HuggingFace ViTモデルをVertex AIにデプロイする
- /deep_117 DariMis: YouTubeにおけるダリ語偽情報検出のためのハーム認識モデリング
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する
- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け

## 原文リンク

[Rocket Money × Hugging Face: 本番環境における揮発性MLモデルのスケーリング事例](https://huggingface.co/blog/rocketmoney-case-study)
