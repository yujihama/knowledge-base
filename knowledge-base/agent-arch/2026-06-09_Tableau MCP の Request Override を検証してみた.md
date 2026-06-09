---
title: "Tableau MCP の Request Override を検証してみた"
url: "https://zenn.dev/cavernaria/articles/58e340d4951b28"
date: 2026-06-09
tags: [MCP, Tableau, Tool Scoping, Request Override, マルチテナント, Claude Code, HTTPヘッダー]
category: "agent-arch"
related: [430, 2688, 4520, 6126, 7591]
memo: "[Zenn LLM] Tableau MCP の Request Override を検証してみた"
processed_at: "2026-06-09T09:04:18.704201"
---

## 要約

Tableau MCP（Model Context Protocol サーバー）には、起動時の静的設定を変えずにリクエスト単位で一部の設定を上書きできる「Request Override」機能がある。Tool Scoping には3段階のレベル（①MCP本体の環境変数、②サイトレベルのREST API設定、③リクエストレベルのHTTPヘッダー）が存在し、Request Override は③にあたる。実装方法は、ツール呼び出し時のHTTPリクエストに `x-tableau-mcp-config` ヘッダーを付与するもので、HTTP トランスポートのみ対応（stdio 非対応）。上書き可能な変数は Tableau MCP 側で事前にオプトイン方式で許可する必要があり、環境変数 `ALLOWED_REQUEST_OVERRIDES` に変数名と制限タイプ（restricted/unrestricted）をセットする。

制限タイプ `restricted` では、現在のベースライン設定を「狭める方向」にしか上書きできない。たとえば `INCLUDE_DATASOURCE_IDS` が A, B, C の3件に設定されている場合、リクエスト側は A, B の2件に絞ることはできるが、新たな D を追加することは構造的に不可能。`unrestricted` では任意の値に上書きできる。

検証環境では Tableau Cloud 2026.2 を使用し、26個のデータソースのうち tamade_store_list 抽出・tamade_store_list_paypay 抽出・Superstore Datasource の3件をベースラインとして MCP 本体に設定。Claude Code を MCPクライアントとして、同一の Tableau MCP（127.0.0.1:3927）に対して2つの接続プロファイルを登録した。プロファイルA（tableau-retail）は `x-tableau-mcp-config: INCLUDE_DATASOURCE_IDS=<tamade1>,<tamade2>` ヘッダー付きで tamade 2件に絞り込まれ、プロファイルB（tableau-analyst）はヘッダーなしでベースラインの3件すべてが見える状態を確認した。

実運用上の示唆として、①②の静的設定だけでは「同一MCPに対してチームごとに異なるスコープを当てたい」マルチテナント要件に対応できないが、Request Override を使えば Tableau MCP は1台のまま、アプリ側がリクエストごとにヘッダーを付与するだけで対応可能。ただし PAT 認証は同時複数セッション不可という仕様があり、複数クライアントが同時に同一 MCP を共有する本番構成では OAuth 認証が必要になる点も判明した。

## アイデア

- MCPサーバーの設定をリクエスト単位で動的に上書きする仕組みは、監査エージェントが複数クライアント（部門・チーム）に対して同一インフラを共有しつつデータアクセス範囲を分離する設計に直接応用できる
- `restricted` タイプによりクライアント側がスコープを広げられない構造的保証は、LLMエージェントが意図せず権限逸脱するリスクをアーキテクチャレベルで抑制する設計パターンとして注目に値する
- PAT の同時接続不可という制約が `claude mcp list` の並行接続チェックと衝突する問題は、MCPクライアント実装の接続管理仕様を理解せずに設計するとマルチテナント環境で障害になりうることを示す実例

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **Tool Scoping** (TODO: 読むべき)
- **HTTPヘッダー** (TODO: 読むべき)
- **PAT認証** (TODO: 読むべき)
- **Tableau Cloud** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_7591 東京リージョンのPaaS「KamuiDash」を作ってみました

## 原文リンク

[Tableau MCP の Request Override を検証してみた](https://zenn.dev/cavernaria/articles/58e340d4951b28)
