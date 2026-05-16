---
title: "SOWでシンプルにClaude Codeを活用する"
url: "https://zenn.dev/chihaso/articles/2d613b6ac154e8"
date: 2026-04-25
tags: [Claude Code, SOW, カスタムコマンド, Human-in-the-loop, プロンプト設計, Codex, GitHub連携, MCP]
category: "agent-arch"
related: [430, 2688, 2404, 2140, 2541]
memo: "[Zenn LLM] SOWでシンプルにClaude Codeを活用する"
processed_at: "2026-04-25T12:53:42.864715"
---

## 要約

本記事は、Claude CodeやCodexをより効果的に活用するための「SOW（Statement of Work / Scope of Work）」という手法を紹介する実践的なガイドである。著者は8ヶ月間、AIへの指示出しをほぼSOW一本で運用しており、その具体的なワークフローを公開している。

SOWとは「作業明細書」のことで、「〇〇のSOWを作って」とAIに指示するだけで、実装手順・スコープ・完了条件を含む構造化されたドキュメントを自動生成させることができる。GitHubのissue URLやJiraのURLを渡すだけで、MCPやCLIを通じてコメントも含めた情報を取得し、既存コードを踏まえた詳細な作業計画書を出力する点が特徴的。

著者は2つのカスタムコマンドを`~/.claude/commands/`配下にグローバル設定として保存し、複数リポジトリで共用している。`/create_sow <URL or 説明文>`でSOWを`./tmp/sow`ディレクトリに生成し、`/do_sow <SOWパス>`で1フェーズずつ実行・承認・進捗反映のサイクルを回す。

具体的なSOW出力例として、RailsバックエンドのPOST APIとReactフロントエンドのフォームコンポーネント実装を含む案件が示されており、ルーティング・コントローラー・モデルメソッド・Request Spec・Model Spec・TypeScript型チェック・RuboCopまでチェックボックス付きで列挙されている。完了条件も「25 examples, 0 failures」「61 files, no offenses」のように定量的に記述される。

SOW活用の主なメリットは3点：(1)最初のプロンプトをゼロから考える必要がなくなる、(2)Dry-runとして事前に作業内容を人間がレビューできる、(3)トークン上限で会話が途切れた際も「ここまでをSOWに反映」→新セッションで`/do_sow`するだけで再開できる。

監査エージェント開発への示唆として、SOWはLangGraphのようなエージェントが実行する前に「タスク計画フェーズ」を明示的に分離するパターンと本質的に同じ構造を持つ。人間がSOWをレビュー・修正する工程は、Human-in-the-loopのチェックポイントとして機能しており、エージェントの自律的な実行に先立つ計画承認フローの設計に直接応用できる。

## アイデア

- SOWを「エージェントへのDry-run」として使うことで、コード差分レビューより認知負荷の低い事前検証ループを実現している点
- グローバルな`~/.claude/commands/`にコマンドを置くことでリポジトリ横断の再利用を実現し、コマンド自体をソフトウェアとして管理する発想
- トークン上限による会話切断の問題を、SOWへの進捗書き戻し＋新セッション再開という外部ストレージ活用で解決しているアーキテクチャパターン

## 前提知識

- **Claude Code カスタムコマンド** (TODO: 読むべき)
- **SOW（Statement of Work）** (TODO: 読むべき)
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？

## 原文リンク

[SOWでシンプルにClaude Codeを活用する](https://zenn.dev/chihaso/articles/2d613b6ac154e8)
