---
title: "Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ"
url: "https://huggingface.co/blog/skops"
date: 2026-04-11
tags: [scikit-learn, Hugging Face Hub, MLOps, モデルカード, モデルホスティング, Skops, joblib, pickle]
category: "infra"
memo: "[HF Blog] Introducing Skops"
related: [396, 1645, 428, 173, 1648]
processed_at: "2026-04-11T21:08:03.808882"
---

## 要約

SkopsはHugging Faceが開発したPythonライブラリで、scikit-learnモデルのHugging Face Hubへのホスティング、モデルカードの自動生成、チームコラボレーションを目的としている。主要機能は3つに分かれる。(1) hub_utils: モデルのシリアライズ（pickle/joblib対応）、ローカルリポジトリの初期化（hub_utils.init）、Hub へのアップロード（hub_utils.push）、ダウンロード（hub_utils.download）、環境更新（hub_utils.update_env）を提供。init時にscikit-learnバージョン、タスク種別（例: tabular-classification）、サンプル入力データを設定ファイルに記録し、推論ウィジェットの有効化やモデル検索性向上に活用される。(2) card: Card クラスによるモデルカードの自動生成。metadata_from_config()で設定ファイルからメタデータを抽出し、add()メソッドでモデル説明・制限事項・引用情報・サンプルコードを追加、add_metrics()でaccuracy・F1スコア等の評価指標をテーブル形式で記録、add_plot()で混同行列等の図を埋め込める。最終的にREADME.mdとして保存され、Hugging Face Hubの標準フォーマット（YAMLフロントマター＋Markdown）に準拠する。(3) セキュリティ面：Hub上でのモデル共有において、環境要件（requirements）を明示することで再現性を担保し、リポジトリをprivateにすることでアクセス制御も可能。ブログ記事は2022年8月12日公開で、乳がんデータセットでDecisionTreeClassifierを訓練する具体的なエンドツーエンドの例を提示している。scikit-learnエコシステムをMLOpsの標準的なワークフローに統合するための橋渡しツールとして位置づけられる。

## アイデア

- モデルカードの自動生成機能（metadata_from_config）は、モデルの再現性・説明責任を構造化されたフォーマットで担保する設計で、監査文脈における証跡管理の自動化と親和性が高い
- hub_utils.init が環境要件・タスク種別・サンプル入力を設定ファイルに一元管理する設計は、複数モデルを管理するMLOpsパイプラインにおけるバージョン管理・依存関係追跡の参考になる
- add_metrics()でF1・accuracyをテーブルとしてモデルカードに埋め込む仕組みは、評価結果の改ざん防止や第三者検証を想定した監査証跡フォーマットとして応用できる
## 関連記事

- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する
- /deep_428 ゼロからGPUへ: 本番環境対応CUDAカーネルの構築とスケーリングガイド
- /deep_173 「平面を作るモデル」から紐解く機械学習と行列
- /deep_1648 scikit-learnのLinearRegression実装を追う: Ordinary Least Squares入門

## 原文リンク

[Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ](https://huggingface.co/blog/skops)
