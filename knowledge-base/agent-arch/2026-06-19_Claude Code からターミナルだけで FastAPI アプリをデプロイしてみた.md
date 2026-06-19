---
title: "Claude Code からターミナルだけで FastAPI アプリをデプロイしてみた"
url: "https://zenn.dev/kamuidash/articles/6a673850634039"
date: 2026-06-19
tags: [MCP, Claude Code, FastAPI, KamuiDash, PaaS, 自律デプロイ, uvicorn]
category: "agent-arch"
related: [7591, 430, 2688, 4520, 6126]
memo: "[Zenn LLM] Claude Code からターミナルだけで、FastAPI アプリをデプロイしてみた"
processed_at: "2026-06-19T09:05:02.283054"
---

## 要約

KamuiDash という PaaS が提供する MCP サーバーを利用し、Claude Code（AI エージェント）との対話のみで FastAPI アプリの作成・GitHub への push・本番デプロイを完結させた事例。ブラウザのダッシュボード操作は GitHub リポジトリと KamuiDash の連携時のワンタップのみで、それ以外の全操作を CLI と Claude Code から実行している。

技術スタックは kamui CLI（v0.1.18）、Claude Code（v2.1.x）、GitHub CLI（gh v2.88.x）。MCP 接続は `kamui mcp setup --register` コマンドで Personal Access Token をファイル経由で Claude Code に登録する安全な方法を採用。接続後は `claude mcp list` で `kamui: https://api.kamui-platform.com/mcp (HTTP) - Connected` と確認できる。

アプリ本体は最小構成の FastAPI：`GET /` で Hello メッセージと `region: tokyo` を返し、`GET /health` で `status: ok` を返す。KamuiDash の Python ランタイムが `python main.py` で起動する仕様のため、uvicorn を `main.py` 内から環境変数 `PORT`（デフォルト 8000）を読んで起動する形式で実装。依存パッケージは `fastapi` と `uvicorn[standard]` のみ。Claude Code が `git init`・コミット・`gh repo create`・`git push` まで自律実行した。

デプロイは MCP ツール経由で `create_project`（Free プラン / 東京リージョン）→ `create_app`（Python / pip install / python main.py / レプリカ1）の順に実行。ビルド中は `list_deploy_runs` でステータスを追跡し、失敗時は `get_deploy_run_logs`、起動後は `get_app_logs` でログを確認する。全操作が MCP 経由のため、ブラウザ不要で状況把握が可能。

デプロイ成功後の疎通確認では東京リージョンの公開 URL に curl を3回実行し、全て HTTP 200 を確認。初回は TLS 接続確立込みで約 1.13 秒、2回目以降は約 0.13 秒で安定。KamuiDash は無料プランでもアプリをスリープさせない設計のため、コールドスタートによる数十秒待機は発生しない。

監査エージェント開発への示唆：MCP による操作インターフェースの統一は、エージェントが外部サービス（デプロイ基盤・ログ収集・監査証跡）を自律的に操作する際の設計パターンとして参考になる。`create_project`・`list_deploy_runs`・`get_app_logs` のように操作を粒度の細かいツールとして分解し、エージェントが状態遷移を自律追跡する構成は、監査エージェントの外部システム連携設計にそのまま応用できる。

## アイデア

- MCP サーバーを PaaS 側が提供することで、AI エージェントがデプロイ・ログ確認・状態追跡を自律的にツール呼び出しで実行できる。エージェントが外部サービスを操作する際の API 設計のモデルケースになる
- `list_deploy_runs` → `get_deploy_run_logs` → `get_app_logs` という状態遷移の自律追跡パターンは、エージェントが長時間タスクの進捗を自己監視する ReAct ループの具体実装として参考になる
- Dockerfile や CI 設定なしで本番デプロイを完結させる「Vibe Coding → 即本番」のフローは、プロトタイプ検証サイクルを大幅に短縮する可能性がある。監査エージェントの PoC デプロイでも同様のアプローチが有効

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **PaaS** → /deep_7591 東京リージョンのPaaS「KamuiDash」を作ってみました
- **uvicorn** (TODO: 読むべき)

## 関連記事

- /deep_7591 東京リージョンのPaaS「KamuiDash」を作ってみました
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[Claude Code からターミナルだけで FastAPI アプリをデプロイしてみた](https://zenn.dev/kamuidash/articles/6a673850634039)
