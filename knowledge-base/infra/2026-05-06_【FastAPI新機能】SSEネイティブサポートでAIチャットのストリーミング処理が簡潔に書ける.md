---
title: "【FastAPI新機能】SSEネイティブサポートでAIチャットのストリーミング処理が簡潔に書ける"
url: "https://zenn.dev/team_nishika/articles/e57cc1f621bcd1"
date: 2026-05-06
tags: [FastAPI, SSE, Server-Sent Events, EventSourceResponse, Pydantic, LLMストリーミング, AsyncIterable]
category: "infra"
related: [3231, 2951, 2950, 1736, 797]
memo: "[Zenn LLM] 【FastAPI新機能】SSEネイティブサポートでAIチャットの処理が楽に書ける"
processed_at: "2026-05-06T12:47:51.015063"
---

## 要約

FastAPI 0.135.0（2026-03-01リリース）にて、SSE（Server-Sent Events）のネイティブサポートが追加された。具体的には `fastapi.sse` モジュールとして `EventSourceResponse` と `ServerSentEvent` が公式に組み込まれた。

従来のSSE実装では `StreamingResponse` を使い、手動でJSONシリアライズ・イベントフォーマット構築を行う必要があったが、新機能では戻り値型を `AsyncIterable[PydanticModel]` と宣言するだけで、PydanticのRust実装（pydantic-core）による自動バリデーション＆シリアライズが適用される。`json.dumps()` を明示的に呼ぶ必要がなくなり、コード量が大幅に削減される。

イベント種別の制御が必要な場合は `ServerSentEvent` オブジェクトを yield することで、`event` / `id` / `retry` などSSEプロトコルの各フィールドを個別に指定できる。LLMストリーミングで慣例的に使われる `[DONE]` センチネル値の送信には `raw_data` パラメータを使うことでJSONエンコードをスキップして文字列をそのまま送信可能。

インフラ面では、keep-aliveのpingとキャッシュ制御ヘッダー（`Cache-Control: no-cache`）、Nginxリバースプロキシのバッファリング抑止ヘッダー（`X-Accel-Buffering: no`）がデフォルトで自動付与される。プロキシ環境下でSSEが詰まる問題をゼロコンフィグで回避できる点は運用上重要。

接続断からの再接続時には、クライアントが最後に受信したイベントIDを `Last-Event-ID` HTTPヘッダーで送信する仕様（SSE標準）をそのまま活用でき、サーバー側でストリームの途中再開が実装しやすい。

フロントエンド側はTypeScriptの標準 `EventSource` APIを使い、`addEventListener('token', ...)` / `addEventListener('done', ...)` のようにイベント種別ごとにハンドラを分けて記述できる。

監査エージェント開発への示唆：LangGraphベースのエージェントが長時間推論を行う際、中間ステップや思考ログをリアルタイムでフロントエンドに配信するユースケースに直接適用できる。`event` フィールドで `thinking` / `tool_call` / `result` 等のイベント種別を分類することで、エージェントの実行状態をUIで可視化するコードが大幅に簡潔になる。

## アイデア

- 戻り値型 `AsyncIterable[PydanticModel]` の宣言だけでシリアライズが完結する設計は、OpenAPIスキーマ自動生成とストリーミングを同時に実現する点で型駆動設計の好例
- `raw_data` による `[DONE]` センチネル送信とイベント種別分類の組み合わせは、LLMエージェントの多段階実行状態（thinking→tool_call→result）をフロントに伝達するプロトコル設計に転用できる
- Nginx `X-Accel-Buffering: no` の自動付与など、プロキシ環境の落とし穴をフレームワーク側が吸収する設計方針は、AIアプリのプロダクション展開コストを下げる重要なアプローチ

## 前提知識

- **Server-Sent Events (SSE)** (TODO: 読むべき)
- **FastAPI / Starlette** (TODO: 読むべき)
- **Pydantic v2** (TODO: 読むべき)
- **AsyncGenerator / AsyncIterable** (TODO: 読むべき)
- **LLMトークンストリーミング** (TODO: 読むべき)

## 関連記事

- /deep_3231 LLMルーターの自動プロファイル選択をrule-basedでどこまでやるか—CodeRouter v1.6 auto_router
- /deep_2951 CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_797 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：フルファクトリアル・クロスバックエンド手法

## 原文リンク

[【FastAPI新機能】SSEネイティブサポートでAIチャットのストリーミング処理が簡潔に書ける](https://zenn.dev/team_nishika/articles/e57cc1f621bcd1)
