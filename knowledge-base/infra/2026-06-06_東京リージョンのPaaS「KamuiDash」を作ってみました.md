---
title: "東京リージョンのPaaS「KamuiDash」を作ってみました"
url: "https://zenn.dev/kamuidash/articles/444c138283e0c9"
date: 2026-06-06
tags: [PaaS, MCP, Claude Code, GitHub連携, 東京リージョン, CI/CD, PostgreSQL, コールドスタート]
category: "infra"
related: [2404, 2963, 1740, 430, 2688]
memo: "[Zenn LLM] 東京リージョンのPaaSを作ってみました"
processed_at: "2026-06-06T09:05:03.247342"
---

## 要約

長年のソフトウェアエンジニアとしての経験から、HerokuやRenderなど既存PaaSの課題（値上がり、リージョン問題、コールドスタート）を解決するため、東京リージョン特化のPaaS「KamuiDash」を開発・リリースした。GitHub連携のみでアプリをデプロイ・ホストできる個人開発・スタートアップ初期段階向けのサービスで、Preview版として公開済み。

主な機能は3つ：PostgreSQLデータベースの作成（同プロジェクト内DBからのデータコピー対応）、Webサーバーのホスト（Go/Python/Node.jsの3ランタイム対応、レプリカ数・インスタンスタイプ・環境変数・マイグレーションコマンド等を設定可能）、静的ファイルのホスト。GitHubリポジトリとの紐づけにより、git pushで自動デプロイが走るCD統合も備える。

競合との最大の差別化点はコールドスタートなし・無料プランの両立で、Freeプランでも1ヶ月間コールドスタートなしでサーバー・DBを利用可能。PoCや初期検証のユースケースを主なターゲットとしている。料金はドル建てで、他リージョン展開を見据えた設計。

LLM連携として、MCP（Model Context Protocol）とCLIを提供しており、Claude Code・Codex・CursorなどのAIコーディングツールからGUIを開かずにデプロイ状況確認などの操作が可能。これはデプロイ管理をAIエージェントのワークフローに組み込む実用的な取り組みであり、MCPによるインフラ操作の自動化という観点で注目に値する。監査エージェント開発においても、検証環境のプロビジョニングや管理をエージェントに委譲する際の参考アーキテクチャとなり得る。

## アイデア

- MCPとCLIを提供することでClaude CodeやCodexなどのAIエージェントからデプロイ操作を自然言語で制御できる設計は、インフラ操作のエージェント化の実例として参考になる
- 無料プランでもコールドスタートなしという設計は、コンテナの常時起動コストをサービス側が負担するモデルであり、初期ユーザー獲得とPaaSの単位経済性のトレードオフを示している
- 同一プロジェクト内DBからのデータコピー機能はステージング環境の構築を簡略化するアプローチで、PoCから本番へのシームレスな移行を想定した設計思想が見える

## 前提知識

- **PaaS** (TODO: 読むべき)
- **GitHub Actions / CD** (TODO: 読むべき)
- **MCP (Model Context Protocol)** → /deep_6357 LLMの拡張標準「MCP (Model Context Protocol)」入門：Pythonでカスタムサーバーを構築する
- **コンテナオーケストレーション** (TODO: 読むべき)
- **PostgreSQL** → /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2963 SOWでシンプルにClaude Codeを活用する
- /deep_1740 AIエージェントの安全性は『モデルの注意力』ではなく『ハーネスの設計』で守る
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」

## 原文リンク

[東京リージョンのPaaS「KamuiDash」を作ってみました](https://zenn.dev/kamuidash/articles/444c138283e0c9)
