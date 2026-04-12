---
title: "Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ"
url: "https://huggingface.co/blog/storage-buckets"
date: 2026-03-31
tags: [HuggingFace, StorageBuckets, Xet, オブジェクトストレージ, fsspec, huggingface_hub, MLOps, チェックポイント管理]
category: "infra"
memo: "[HF Blog] Introducing Storage Buckets on the Hugging Face Hub"
processed_at: "2026-03-31T09:01:51.830690"
---

## 要約

Hugging Face は2026年3月10日、Hub上でS3ライクなオブジェクトストレージ「Storage Buckets」を一般公開した。従来のモデル・データセットリポジトリはGitベースのバージョン管理を前提としており、学習チェックポイント・オプティマイザ状態・処理途中のデータシャード・エージェントトレースなど、頻繁に上書きされる中間成果物の保管には不向きだった。Bucketsはこの課題に対応した非バージョン管理型ストレージで、ユーザー・組織の名前空間配下に置かれ、`hf://buckets/username/bucket-name` 形式でアドレス指定できる。

技術的な基盤としてXet（Hugging Faceのチャンクベースストレージバックエンド）を採用しており、ファイルをモノリシックなblobとして扱わずコンテンツをチャンク単位に分割・重複排除する。連続するチェックポイント間でモデルの一部が変化していない場合、差分バイトのみ転送されるため、帯域幅・転送時間・ストレージコストが削減される。Enterpriseプランでは重複排除後のサイズに基づく課金となる。

操作方法はCLI（`hf`コマンド）とPython（`huggingface_hub` v1.5.0以降）の両方から可能。`hf buckets create`でバケット作成、`hf buckets sync`でローカルディレクトリとの同期、`--dry-run`オプションで実行前の確認、`--plan`でプラン保存と後適用が行える。Pythonでは`create_bucket`・`sync_bucket`・`list_bucket_tree`などのAPIが提供され、JavaScriptは`@huggingface/hub` v2.10.5以降で対応。

fsspecとの統合により`HfFileSystem`を経由してpandas・Polars・Daskなどのライブラリが`hf://`パスを直接読み書きできる。追加設定不要で既存データワークフローへの組み込みが可能。

またAWS・GCPとのパートナーシップによる「Pre-warming」機能を提供し、コンピュートが稼働するクラウドリージョン近くにデータを事前配置することで、分散学習時のデータ転送レイテンシを低減する。

ロードマップとしてBucketsと従来のバージョン管理リポジトリ間の直接転送（最終チェックポイントをモデルリポジトリへ昇格、処理済みシャードをデータセットリポジトリへコミット）が予定されている。Jasper・Arcee・IBM・PixAIがプライベートベータに参加し、フィードバックを提供した。

## アイデア

- Xetのチャンク重複排除により、連続チェックポイントの差分のみ転送・保存できる点は、大規模学習ランのコスト管理において実用的な最適化手段となる
- fsspec統合によりpandas・Polars等の既存ライブラリがhf://パスをそのまま扱えるため、データパイプラインのストレージバックエンドをコード変更なしにBucketsへ切り替え可能
- エージェントのトレース・メモリ・共有ナレッジグラフの保存先として明示的に設計されており、マルチエージェント系システムの中間状態管理ユースケースが公式に想定されている
## 関連記事

- /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- /deep_900 ファイルからチャンクへ：HuggingFaceストレージ効率の改善
- /deep_771 チャンクからブロックへ：Hugging Face Hubにおけるアップロード・ダウンロードの高速化
- /deep_713 XetストレージがHugging Face Hubに導入された：LFSからコンテンツ定義チャンキングへの移行
- /deep_521 ParquetのContent-Defined Chunking（CDC）によるHugging Face Hub上のデータ転送最適化

## 原文リンク

[Hugging Face Hub に Storage Buckets が登場 — S3ライクなミュータブルオブジェクトストレージ](https://huggingface.co/blog/storage-buckets)
