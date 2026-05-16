---
title: "Azure ML パイプラインコンポーネントバッチデプロイで CLI から Python SDK v2 に移行したらハマった話"
url: "https://zenn.dev/aklzo/articles/0c48026d8a3c50"
date: 2026-05-06
tags: [Azure ML, Python SDK v2, バッチエンドポイント, PipelineComponentBatchDeployment, azure-ai-ml, CI/CD, @latest, 匿名コンポーネント]
category: "infra"
related: [423, 6, 3378, 1740, 1428]
memo: "[Zenn 機械学習] Azure ML パイプラインコンポーネントバッチデプロイで CLI から Python SDK v2 に移行したらハマった話"
processed_at: "2026-05-06T12:26:26.786210"
---

## 要約

Azure Machine Learning でバッチ推論パイプラインを CLI（az ml batch-deployment create）から Python SDK v2（azure-ai-ml 1.32.0）に移行した際、`@latest` によるモデル自動更新が2回目以降に機能しなくなる問題の原因調査と対処法をまとめた記事。

問題の根本は `_batch_deployment_operations.py` の `begin_create_or_update` 内の分岐にある。`ModelBatchDeployment` では `upload_dependencies` が呼ばれ `@latest` がAPIで解決されるが、`PipelineComponentBatchDeployment` では `_validate_component` のみが呼ばれる。この `_validate_component` はコンポーネントが既存登録済みかを `get()` で確認し、FOUND なら `@latest` 解決をスキップする。

CLI が「毎回 `@latest` を解決できていた」理由は CLI 固有の機能ではなく、YAML インライン定義時に生成される「匿名コンポーネント」の構造による副次効果だった。匿名コンポーネントは Python オブジェクト上では `version="1"` だが、ワークスペース登録時のバージョンは YAML 内容のコンテンツハッシュ（例: `abc123...`）になる。そのため `get("azureml_anonymous", "1")` は常に NOT FOUND となり、毎回 `create_or_update` → `@latest` 解決が走る。

一方、名前付き＋固定バージョンのコンポーネントは初回のみ NOT FOUND で登録・解決され、2回目以降は FOUND となり `@latest` 解決がスキップされる。auto_increment（name あり・version なし）の場合も DEFAULT ラベルで最新バージョンが取得され FOUND 扱いとなる。

CLI は内部で同一実装の vendored SDK を使用しており、コードレベルでの差異はない。挙動の差はコンポーネント定義の方法（匿名 vs 名前付き）に起因する。

SDK v2 で `@latest` を毎回解決するには3つの方法がある。①コンポーネントを匿名（name/version なし）にしてインライン定義する。②`deployment.component.version = str(int(time.time()))` のように実行ごとにバージョンを動的に変更する。③`ml_client.components.create_or_update(component)` で事前にコンポーネントを明示登録し、解決済み ARM ID をデプロイに渡す。監査エージェント等の CI/CD パイプラインでモデルを自動更新したい場合は方法②または③が確実で意図が明確。

## アイデア

- CLIとSDKが同一の vendored コードを使いながら挙動が異なる原因が「匿名コンポーネントのバージョン管理構造の副次効果」という点は、APIの設計意図を超えた暗黙の依存を示す好例
- コンテンツハッシュをバージョン識別子として使う匿名コンポーネントの設計は、冪等性を担保する一方で `get()` による存在チェックと不整合を生じさせるトレードオフが興味深い
- モデルバージョン自動更新を実現する3つの方法のうち、方法③（事前登録＋ARM ID直渡し）は意図を明示的にコードで表現できる点で、CI/CDの可観測性・デバッグしやすさの観点から最も優れた設計

## 前提知識

- **Azure Machine Learning** (TODO: 読むべき)
- **バッチエンドポイント** (TODO: 読むべき)
- **Python SDK v2 (azure-ai-ml)** (TODO: 読むべき)
- **パイプラインコンポーネント** (TODO: 読むべき)
- **ARM ID** (TODO: 読むべき)

## 関連記事

- /deep_423 Hugging FaceとVirusTotal、AIセキュリティ強化に向けて協業を発表
- /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- /deep_3378 Claude Code の Monitor ツール完全ガイド — バックグラウンドプロセスをリアルタイム監視する仕組み
- /deep_1740 AIエージェントの安全性は『モデルの注意力』ではなく『ハーネスの設計』で守る
- /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線

## 原文リンク

[Azure ML パイプラインコンポーネントバッチデプロイで CLI から Python SDK v2 に移行したらハマった話](https://zenn.dev/aklzo/articles/0c48026d8a3c50)
