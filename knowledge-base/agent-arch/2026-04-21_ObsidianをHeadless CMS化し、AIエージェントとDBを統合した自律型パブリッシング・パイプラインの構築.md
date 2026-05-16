---
title: "ObsidianをHeadless CMS化し、AIエージェントとDBを統合した自律型パブリッシング・パイプラインの構築"
url: "https://zenn.dev/hideki_tamae/articles/5a0e8f92293c6d"
date: 2026-04-21
tags: [n8n, Obsidian, Claude 3.5 Sonnet, PostgreSQL, Cloudflare Tunnel, Headless CMS, 自動化パイプライン, Web3]
category: "agent-arch"
related: [2404, 1962, 1915, 4]
memo: "[Zenn LLM] # 【完全自動化】ObsidianをHeadless CMS化し、AIエージェントとDBを統合した「自律型パブリッシング・パイプライン」の構"
processed_at: "2026-04-21T12:36:24.777049"
---

## 要約

本記事は、Obsidian・n8n・Claude 3.5 Sonnet・PostgreSQL・Cloudflare Tunnelを組み合わせた完全自動パブリッシングパイプラインの構築記録である。筆者はMarkdownファイルをObsidianの特定フォルダに配置するだけで、記事の公開からDB登録・ファイル整理までを無人で完結させるシステムを1.5日で実装した。

パイプラインの処理フローは6段階で構成される。①Cronによる定期トリガーで処理を起動、②Cloudflare Tunnel経由でローカルのObsidian REST APIにアクセスしMarkdownを取得、③Claude 3.5 SonnetがMarkdown本文を解析してTitle・Slug・ReadTime・ハッシュタグをJSON形式で構造化、④Web3パブリッシングプラットフォーム「Paragraph」へ自動投稿、⑤PostgreSQLへの全データ永続化、⑥処理済みファイルの別フォルダへの物理移動による状態管理。

技術的な難所として3点が挙げられている。第一に、長文Markdownに含まれる記号・改行・カンマがPostgreSQLへのINSERT時にパースエラーを引き起こすため、データを物理的に隔離する装填メカニズムを独自実装した。第二に、クラウド（n8n）からローカル環境（Obsidian）へのセキュアな双方向通信をCloudflare TunnelとBearerトークンで実現した。第三に、投稿成否に基づくファイルの物理移動により二重投稿を防ぐ循環型キューを設計した。

日本語ファイルパスのAPI送信には`encodeURI()`によるURLエンコードを使用し、HTTPヘッダー・URL双方での安全な送受信を確保している。システムの評価指標として、設計複雑度92/100・データ堅牢性85/100・希少性95/100が挙げられており、生産性向上は記事1本あたり20分の手作業を0分に削減（1,500%向上、年間30時間超の創出）と試算されている。

監査エージェント開発への示唆としては、n8nとCloudflare Tunnelを用いたクラウド↔ローカル間の安全なハイブリッド接続パターンが参考になる。LangGraphベースのエージェントがローカルLLMやローカルDBにアクセスする際の通信設計として、同様のトンネリング+Bearer認証方式を採用できる。また、処理済みアイテムを物理移動で状態管理する循環型キュー設計は、監査エージェントのタスク管理における冪等性保証の実装パターンとして応用可能である。

## アイデア

- Obsidianをファイルドロップ型のHeadless CMSとして機能させ、ローカルREST APIとCloudflare Tunnelでクラウドワークフロー(n8n)と接続するハイブリッドアーキテクチャ
- LLMによるメタデータ構造化をパイプラインの中間処理として挟み、非構造化Markdownを後続DBやAPIが扱えるクリーンなJSONに変換するデータバリデーション層の設計
- 処理済みファイルを別フォルダへ物理移動することで状態をファイルシステム上に表現し、二重処理を数学的に防ぐ循環型キューの実装（DBを使わないステート管理の代替手法）

## 前提知識

- **n8n** (TODO: 読むべき)
- **Cloudflare Tunnel** (TODO: 読むべき)
- **REST API** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **PostgreSQL** → /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する
- **Claude API** → /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- /deep_1915 MCP（Model Context Protocol）実践ガイド——PythonでAIエージェントにツールを接続する
- /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する

## 原文リンク

[ObsidianをHeadless CMS化し、AIエージェントとDBを統合した自律型パブリッシング・パイプラインの構築](https://zenn.dev/hideki_tamae/articles/5a0e8f92293c6d)
