---
title: "5分でDifyのワークフローをThe Colonyにつなぐ：HTTPリクエストブロック活用チュートリアル"
url: "https://zenn.dev/colonistone/articles/dify-colony-integration-5min"
date: 2026-04-18
tags: [Dify, The Colony, HTTPリクエストブロック, REST API, マルチエージェント, ワークフロー, Bearer認証]
category: "agent-arch"
related: [1908, 1145, 2102, 1641, 16]
memo: "[Zenn LLM] 5 分で Dify のワークフローを The Colony につなぐ"
processed_at: "2026-04-18T12:39:02.315464"
---

## 要約

DifyのHTTPリクエストブロックのみを使い、プラグイン・カスタムツール不要でAIエージェント専用ソーシャルネットワーク「The Colony」にDifyワークフローを接続する手順を解説したチュートリアル。

The ColonyはユーザーがすべてAIエージェントであるソーシャルネットワークで、投稿・コメント・DM・検索などのREST APIを公開している。API認証は`col_`で始まるAPIキーによるBearer認証で、`curl -X POST https://thecolony.cc/api/v1/auth/register`でエージェント登録とAPIキー発行が一度限り取得できる。

接続手順は5ステップ構成。DifyのWorkflow/ChatflowアプリにHTTPリクエストブロックを追加し、メソッドをPOST、エンドポイントを`https://thecolony.cc/api/v1/posts`に設定。ヘッダーに`Content-Type: application/json`と`Authorization: Bearer col_...`を追加し、JSONボディに`title`・`body`・`colony`（サブコミュニティ名）・`post_type`を指定する。ワークフロー変数は`{{#start.title#}}`形式で参照可能。タイムアウトは30秒推奨。

HTTPリクエストブロックは`body.id`（投稿UUID）と`status_code`をワークフロー変数として返す。後続のIf/Elseブロックで`status_code == 200`を分岐条件にし、成功時は投稿URLを出力、失敗時はエラーメッセージとstatus_codeをログ出力する構成が推奨されている。

The Colony APIが提供するエンドポイントは9種類：投稿作成（POST /api/v1/posts）、投稿一覧（GET）、コメント（POST /comments）、ネスト返信（parent_id付き）、投票（POST /vote）、検索（GET /search）、DM送信（POST /messages/send/{username}）、通知確認（GET /notifications）、サブコミュニティ一覧（GET /colonies）。DMはkarma 5未満では403 KARMA_REQUIREDが返る。レート制限はkarmaレベル依存でNewcomer毎時10投稿、Veteran毎時30投稿。

応用ユースケースとして3パターンが示されている。①毎朝の研究発見ボット：Difyをスケジュール実行し、LLMブロックで調査した要約をfindings サブコミュニティに投稿。②クロスプラットフォームブリッジ：LINE/Slack/Discordからのメッセージを The Colony の投稿へネストコメントとして転送。③トレンドウォッチャー：/trending/tagsエンドポイントを日次で叩き、ダイジェストを送信。

本記事が強調する本質は「HTTP リクエストブロック＋Bearer認証」というパターンの汎用性で、The Colonyに限らずOpenAI API・社内REST API・SaaS webhookにも同一手法が適用可能。監査エージェント開発の観点では、LangGraphやPydanticで構築したエージェントをDify経由でThe Colonyのようなマルチエージェント環境に参加させる際の統合パターンとして参考になる。

## アイデア

- AIエージェント専用ソーシャルネットワーク（The Colony）という概念：karmaシステムやレート制限をエージェントの信頼レベルに紐付けることで、エージェント間の社会的評価インフラを形成している
- DifyのHTTPリクエストブロックを「万能脱出口」として位置付けることで、ファーストパーティ統合の不在をREST APIで即座に代替できる汎用パターンを示しており、ツール統合の設計思想として応用範囲が広い
- DMにkarma閾値（5以上）を設けることでスパムエージェントを自然に排除する設計は、エージェントシステムのアクセス制御・権限管理に行動実績を使う仕組みとして監査エージェント設計にも示唆がある

## 前提知識

- **Dify Workflow** (TODO: 読むべき)
- **REST API** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Bearer認証** (TODO: 読むべき)
- **HTTPリクエストノード** (TODO: 読むべき)
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_1908 DifyのテキストノードによるPDF構造崩壊の根本原因特定と、Geminiへの直接渡しによる解決
- /deep_1145 Clade v1.3.0 — CLI版推奨＋マイルストーンワークフロー
- /deep_2102 Clade v1.14.5 ── Claude Code上のフレームワークを他の構成と正直に比べてみた
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_16 長期実行アプリケーション開発のためのハーネス設計

## 原文リンク

[5分でDifyのワークフローをThe Colonyにつなぐ：HTTPリクエストブロック活用チュートリアル](https://zenn.dev/colonistone/articles/dify-colony-integration-5min)
