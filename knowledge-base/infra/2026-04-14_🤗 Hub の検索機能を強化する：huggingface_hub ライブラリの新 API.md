---
title: "🤗 Hub の検索機能を強化する：huggingface_hub ライブラリの新 API"
url: "https://huggingface.co/blog/searching-the-hub"
date: 2026-04-14
tags: [huggingface_hub, HfApi, ModelFilter, ModelSearchArguments, AttributeDictionary, Hub検索, プログラマブル検索]
category: "infra"
related: [1486, 767, 402, 768, 583]
memo: "[HF Blog] Supercharged Searching on the 🤗 Hub"
processed_at: "2026-04-14T12:07:38.732448"
---

## 要約

huggingface_hub ライブラリに追加された ModelSearchArguments・DatasetSearchArguments・ModelFilter の3クラスにより、Hugging Face Hub 上のモデル・データセット検索をプログラマブルかつ直感的に行えるようになった。

従来の課題は、HfApi.list_models() に渡すクエリパラメータの書式を「暗記」する必要があった点にある。たとえばGLUEデータセットで絞り込む際は 'dataset:glue' という特定の文字列フォーマットが必要で、試行錯誤が避けられなかった。

新機能の中核は ModelSearchArguments クラスで、Hub が受け付ける全パラメータをネスト辞書として保持し、タブ補完で探索できる。model_args.pipeline_tag.TextClassification → 'text-classification'、model_args.dataset.glue → 'dataset:glue' のように、人間が読みやすい属性名から正しい API 文字列が得られる。これにより IDE を離れずに正しいクエリを構築できる。

より複雑な AND 条件検索には ModelFilter クラスを使う。task・trained_dataset・library をリストで渡すことで、「text-classification かつ zero-shot-classification、Multi NLI かつ GLUE で学習済み、PyTorch かつ TensorFlow 対応」といった多条件絞り込みを1オブジェクトで表現できる。実際にこの条件で検索すると Jiva/xlm-roberta-large-it-mnli のみが返され、クエリの精度が確認できる。

実装上の仕組みは AttributeDictionary という独自クラスで、fastcore ライブラリの AttrDict を拡張したもの。通常の辞書をベースに、全キーへのタブ補完・ネスト辞書の連鎖アクセス（model_args.dataset.glue）・キー削除（del model_args[key]）をサポートする。JavaScript の object クラスの挙動に近く、API レスポンスのような深いネスト構造の探索的プログラミングに適している。

DatasetFilter・DatasetSearchArguments も同様に実装されており、データセット検索にも同じパターンが使える。api.list_models(filter=(...)) と api.list_datasets(filter=...) の両方で統一的なインターフェースが提供される。

監査エージェント開発への示唆：Hub 上に公開されている監査・コンプライアンス関連モデルやデータセットをプログラムで体系的に収集・評価するパイプラインを構築する際、この API を使えば条件指定の精度が上がり、モデル選定の自動化が容易になる。

## アイデア

- AttributeDictionary による「タブ補完可能な辞書」というパターンは、複雑な設定オブジェクト（LangGraph のノード設定や Pydantic モデルのスキーマ探索）にも応用できる探索的プログラミングの設計手法
- ModelFilter の多条件 AND 検索は、監査エージェントが使用するモデルの要件仕様（タスク・学習データ・フレームワーク）をコードとして宣言的に管理する手段になり得る
- api.model_info('model_id') でモデルメタデータをプログラムで取得できるため、Hub 上モデルの定期スキャン・品質監視パイプラインを自動化できる

## 前提知識

- **huggingface_hub** → /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- **HfApi** (TODO: 読むべき)
- **Hugging Face Hub** → /deep_187 Community Evals: ブラックボックスリーダーボードから脱却するHugging Faceの分散型評価システム
- **タブ補完 / AttributeDict** (TODO: 読むべき)
- **pipeline_tag** (TODO: 読むべき)

## 関連記事

- /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- /deep_767 Hugging Face Hub に3つの新サーバーレス推論プロバイダー追加：Hyperbolic、Nebius AI Studio、Novita
- /deep_402 Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ
- /deep_768 Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合
- /deep_583 Featherless AIがHugging Face Inference Providersに統合 — サーバーレスで膨大なモデルカタログにアクセス可能に

## 原文リンク

[🤗 Hub の検索機能を強化する：huggingface_hub ライブラリの新 API](https://huggingface.co/blog/searching-the-hub)
