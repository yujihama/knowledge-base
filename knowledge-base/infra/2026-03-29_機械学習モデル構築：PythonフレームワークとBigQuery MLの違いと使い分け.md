---
title: "機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け"
url: "https://zenn.dev/e_agency/articles/f8105cc3fbfbd1"
date: 2026-03-29
tags: [BigQuery ML, scikit-learn, Google Cloud, SQL, 機械学習, Vertex AI, データパイプライン, MLOps]
category: "infra"
memo: "[Zenn 機械学習] 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け"
processed_at: "2026-03-29T22:44:54.193304"
---

## 要約

BigQuery上のデータを用いた機械学習において、Pythonフレームワーク（scikit-learn等）とBigQuery ML（BQML）の2つのアプローチを5つの観点で比較・整理した記事。

**1. データ移動のアーキテクチャ**：Pythonでは学習前にBigQueryからデータをメモリへ抽出する必要があり、数十GB〜TBクラスではメモリ不足や転送コストが問題になる。BQMLはBigQueryの内部で直接学習を実行するため、ペタバイト級のデータでもデータ移動ゼロで処理でき、セキュリティ・ガバナンス面でも有利。

**2. 必要スキルセット**：Pythonアプローチはscikit-learn/TensorFlow/PyTorchの専門知識と環境構築スキルが必要で、データサイエンティスト・MLエンジニア向け。BQMLは`CREATE MODEL`というSQL文のみで、モデル作成・評価・推論まで完結するため、データアナリストやSQLが書けるマーケターでも実践可能。

**3. 柔軟性と対応アルゴリズム**：Pythonは最新OSSアルゴリズム、カスタム損失関数、LLMファインチューニング等に対応し柔軟性は無制限。BQMLは線形回帰・ロジスティック回帰・XGBoost・K-means・ARIMA_PLUSなど実務頻出アルゴリズムをカバーし、ビジネス用途の約8割に対応。

**4. デプロイ・運用**：Pythonカスタムモデルは推論APIサーバー開発・Docker化・Vertex AI Endpointsへのデプロイ等、周辺エンジニアリング工数が大きい。BQMLはモデルがBigQuery内にオブジェクトとして保存され、`ML.PREDICT`関数をSQLで呼ぶだけでバッチ推論が実行可能。dbt・Dataformや既存スケジュールクエリへのSQL追加だけでPoC→本番化のリードタイムを大幅短縮できる。

**5. 使い分けの指針**：非構造化データ・最新手法・超低レイテンシAPIが必要な場合はPython、データがすでにBigQueryに集約済み・チームがアナリスト中心・数日〜数週間での本番化が目標・データ外部持ち出し制約がある場合はBQMLを選択。まずBQMLで小さく始め、高度要件が出てきたらPythonへ移行するアプローチが有効とされる。

**補足**：BigQuery Data Science Agentに「予測モデルを作って」と指示するとPython（scikit-learn）コードが生成されやすいため、BQMLを使わせるには「BigQuery MLで」と明示的に指定する必要がある。

## アイデア

- 「データを動かすか、プログラムを動かすか」というアーキテクチャ思想の対比が明快で、データ量・セキュリティ要件に応じた技術選択の判断軸として汎用性が高い
- BQMLの`ML.PREDICT`をdbt/Dataformに組み込むパターンは、既存データパイプラインへのML組み込みコストを最小化する実用的なアプローチ
- LLMエージェント（Data Science Agent）がデフォルトでPythonコードを生成する傾向があるという観察は、エージェントの出力制御にはプロンプトでの手法明示が不可欠であることを示す具体例

## Yujiの取り組みへの示唆

監査エージェントシステムにおいて、BigQueryに集約された監査データ（取引ログ・仕訳データ等）に対して異常検知や分類モデルを構築する場面でBQMLは有力な選択肢になりえる。データを外部に持ち出さずにSQL内でモデル実行できる点は、監査データのガバナンス・機密保持要件と親和性が高い。また、LangGraphベースのエージェントからBQML（`ML.PREDICT`）を呼び出すツールをPydanticでスキーマ定義すれば、エージェントによる自律的な異常スコアリングパイプラインを最小コストで構築できる。

## 原文リンク

[機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け](https://zenn.dev/e_agency/articles/f8105cc3fbfbd1)
