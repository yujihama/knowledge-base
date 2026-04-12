---
title: "Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合"
url: "https://huggingface.co/blog/trufflesecurity-partnership"
date: 2026-04-08
tags: [TruffleHog, シークレットスキャン, Hugging Face, セキュリティ, ClamAV, picklescan, API key leak, オープンソース]
category: "infra"
memo: "[HF Blog] Hugging Face partners with TruffleHog to Scan for Secrets"
processed_at: "2026-04-08T21:37:23.811020"
---

## 要約

Hugging FaceはTruffle Securityと提携し、オープンソースのシークレット検出ツール「TruffleHog」をプラットフォームのセキュリティパイプラインに統合した（2024年9月発表）。

TruffleHogは、コードリポジトリ内のパスワード・APIトークン・暗号化キーなどの機密情報を検出・検証するツールで、SaaSやクラウドプロバイダー向けの多数のデテクターを備える。「verified（検証済み）」シークレットとは、実際に認証プロバイダーに対して有効であることが確認されたもの。unverifiedは無効とは限らず、プロバイダーのダウンタイム等で検証失敗する場合もある。

今回の統合は2つの施策からなる。第1に、Hugging Faceの自動スキャンパイプラインへのTruffleHog追加。既存のClamAV（マルウェアスキャン）・picklescan（pickleファイルの悪意あるコードスキャン）に加え、`trufflehog filesystem`コマンドをリポジトリへの各プッシュ時に全新規・変更ファイルに対して実行する。検証済みシークレットが検出された場合、ユーザーにメール通知する。

第2に、TruffleHog側にネイティブのHugging Faceスキャナーを新設。`trufflehog huggingface`コマンドにより、モデル・データセット・Spacesのリポジトリ、PRやDiscussionコメントもスキャン可能。`--user`・`--org`・`--model`・`--dataset`・`--space`フラグで対象を絞り込める。認証は`--token`フラグまたは`HUGGINGFACE_TOKEN`環境変数で渡す。現時点ではLFSに格納されたファイルはスキャン対象外だが、対応予定。

実例として`mcpotato/42-eicar-street`モデルをスキャンしたところ、`token_leak.yml`の1行目に`hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`というHugging Faceトークンが検出された（unverified、スキャン所要時間2.18秒、trufflehog v3.81.10）。

将来的にはLFS対応が整い次第、`trufflehog huggingface`コマンドへの完全移行を予定している。

## アイデア

- 「verified vs unverified」の区別：プロバイダーのダウンタイムでverification失敗することがあるため、unverifiedも脅威として扱う設計思想が参考になる
- 自動スキャンパイプラインの多層構造：マルウェア・pickle・シークレットと異なる脅威ベクターを並列スキャンする設計は、AIシステムのCI/CDセキュリティ設計の雛形になる
- `trufflehog huggingface`コマンドによりユーザー自身が自組織のモデル・データセット全体をワンコマンドで監査できる点は、セルフサービス型のセキュリティ監査ツールとして優れた設計
## 関連記事

- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_1398 Hugging Face 倫理・社会ニュースレター #3: オープンMLにおける倫理的開放性
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_365 数学者の研究手法を変えるAIツール「Axplorer」——Axiom MathがPatternBoostを民主化

## 原文リンク

[Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合](https://huggingface.co/blog/trufflesecurity-partnership)
