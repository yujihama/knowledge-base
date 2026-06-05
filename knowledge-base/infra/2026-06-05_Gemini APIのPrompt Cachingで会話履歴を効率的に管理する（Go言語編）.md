---
title: "Gemini APIのPrompt Cachingで会話履歴を効率的に管理する（Go言語編）"
url: "https://zenn.dev/yamitake/articles/gemini-prompt-caching-go"
date: 2026-06-05
tags: [Gemini, Context Caching, Prompt Caching, Go, Vertex AI, 会話履歴管理, Redis, PostgreSQL, トークンコスト最適化]
category: "infra"
related: [2960, 2, 5906, 3898, 5034]
memo: "[Zenn LLM] Gemini APIのPrompt Cachingで会話履歴を効率的に管理する（Go言語編）"
processed_at: "2026-06-05T09:20:37.003094"
---

## 要約

GeminiのContext Caching（Prompt Caching）をGo言語で実装し、LLMアプリケーションの会話履歴管理を効率化する手法を解説した記事。通常のAPI呼び出しでは毎リクエストにシステムプロンプト＋全会話履歴を送信するため、会話が長くなるほどトークン数が線形増加しコスト・レイテンシが悪化する。Context Cachingはこの問題を解決するために、頻繁に参照されるコンテキスト（システムプロンプト＋過去会話）をサーバー側にキャッシュし、以降のリクエストにはキャッシュIDのみを渡す仕組み。キャッシュ部分の入力トークンコストは約75%割引となり、ヒット時のレイテンシも削減される。実装面では、`cloud.google.com/go/vertexai/genai`パッケージの`CreateCachedContent`でキャッシュを作成（有効期限TTL付き）し、`GenerativeModelFromCachedContent`でキャッシュを参照したモデルを取得する。キャッシュには最低32,768トークンが必要で、Gemini 1.5 Proの上限100万トークンに対してキャッシュ対象の目安は50万トークンとしている。会話履歴の永続化戦略として、規模別に3パターンを提示：小〜中規模はPostgreSQL/MySQLでRDB管理、大量セッション・高頻度アクセスはRedis＋gzip圧縮（TTL 24時間）、超大規模は「Geminiキャッシュ→Redis→PostgreSQL（30日）→Cloud Storage（長期アーカイブ）」の4層階層化ストレージ。コンテキストウィンドウ超過対策として、最新20件はそのまま渡し、古い履歴はLLMで要約してから結合する`GetOptimizedHistory`パターンも実装している。キャッシュ有効期限は5分前倒しで更新チェックすることで失効リスクを低減。コスト試算ではexpectedQueriesが一定数を超えるとキャッシュ利用が有利になる分岐点がある。監査エージェントへの示唆として、長いシステムプロンプト（監査基準・内部統制ルール等）を複数ターン再利用する場面でContext Cachingは直接適用可能であり、LangGraphの会話ノードでのトークンコスト制御に活用できる。

## アイデア

- キャッシュ最低32,768トークンという下限制約が、システムプロンプトの設計粒度（薄いvs厚い）に直接影響する点が実装上の重要な判断基準になる
- 4層階層化ストレージ（Geminiキャッシュ→Redis→RDB→GCS）は、監査ログの保持期間ポリシーと親和性が高く、エビデンス管理基盤にそのまま転用できる設計パターン
- 古い会話をLLMで要約して最新履歴と結合する`GetOptimizedHistory`は、長期監査セッション（四半期をまたぐ往査など）でのコンテキスト圧縮に応用できる

## 前提知識

- **Gemini API / Vertex AI** (TODO: 読むべき)
- **Context Caching / Prompt Caching** (TODO: 読むべき)
- **トークン課金モデル** (TODO: 読むべき)
- **Redis TTL** (TODO: 読むべき)
- **Go genai SDK** (TODO: 読むべき)

## 関連記事

- /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- /deep_5906 Kagentでコンテキストエンジニアリングを導入してみた — トークン消費を16万→8万に削減
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_5034 自己同一性を前提としない体系「顕現論（Aletheics）」をLLMに与えて哲学談義すると面白い

## 原文リンク

[Gemini APIのPrompt Cachingで会話履歴を効率的に管理する（Go言語編）](https://zenn.dev/yamitake/articles/gemini-prompt-caching-go)
