---
title: "CloudflareスタックだけでブラウザゲームのNaive RAGシステムを構築する"
url: "https://zenn.dev/gearfried/articles/581b8730720b71"
date: 2026-04-13
tags: [RAG, Naive RAG, Cloudflare Workers, Vectorize, Workers AI, Gemma4, D1, Cron Trigger, 埋め込みモデル, ベクトルストア]
category: "infra"
related: [831, 1116, 1334, 861, 1420]
memo: "[Zenn LLM] Cloudflareで作るブラウザゲームのNaive RAGシステム"
processed_at: "2026-04-13T12:50:33.674716"
---

## 要約

ブラウザゲーム「魔人街のFFA」の開発者が、Cloudflareのサービス群のみを用いてNaive RAGベースの質問回答AIをゲームに組み込んだ実装事例。

**背景と課題**: 毎日アップデートを配信するゲームでは、頻繁にプレイするユーザーと数日ぶりのユーザーとの情報格差が生じやすい。従来は攻略Wikiやリリースノートがこのギャップをカバーするが、著者はメンテナンスコストの問題と、ゲームバランス上の「答え」を公式が明かしたくないという事情からそれらを避けた。代わりに、ゲーム内チャットログを自動的にナレッジベース化するRAGシステムを採用した。

**RAGの構成**: Naive RAGのパイプラインは以下の通り。①ゲーム内チャットを数百件単位でまとめてLLM（Workers AI上のGemma4 26B A4B）に投げ、攻略情報を抽出・要約する。②要約テキストを埋め込みモデルでベクトル化し、Cloudflare Vectorizeに保存する。③ユーザーからの質問チャットが来た際に、質問意図をベクトル化してVectorizeで類似検索を行い、関連する攻略情報を取得。④質問＋取得情報をLLMに渡して最終回答を生成する。

**Cloudflareスタックの全容**: データストレージにD1とDurable Objectを使用、チャンク化・ベクトル保存の定期処理にWorkers Cron Trigger（5分間隔）、ベクトルストアにVectorize、サーバーサイドロジックにWorkers、LLM推論にWorkers AIを使用する。LLMにはGemma4 26B A4Bを採用し、thinking機能をオフにしてもチャット用途には十分な品質を確認している。また、Workers AIの利用コスト（AI破産）を抑えるためにRate Limitを設定し、10秒間に10リクエストまでに制限している。

**設計上の特性**: チャットログをナレッジソースとすることで、新要素追加直後はAIが回答できず、コミュニティ内で攻略情報が共有されるにつれてAIも回答できるようになるという段階的な情報公開が実現される。これによりゲームの探索・発見の楽しみを損なわずに、情報格差を緩和できる。監査エージェント開発への示唆としては、外部ログや会話履歴をリアルタイムでナレッジ化するパターンが、監査証跡やコメントログのセマンティック検索に応用可能である点が挙げられる。

## アイデア

- チャットログを攻略情報のナレッジソースとして使うことで、公式が「答え」を明かさなくてもコミュニティの集合知がAIに蓄積されるという自律的なナレッジ構築モデル
- Cloudflare単一スタック（Workers / Vectorize / Workers AI / D1 / Cron Trigger）でRAGの全コンポーネントを完結させることで、外部サービス依存なしにサーバーレスRAGを低コストで運用できる構成
- Rate Limitをcron処理側に設けてLLM呼び出し頻度を制御することで、コスト爆発（AI破産）を防ぎながらバッチ型の継続的ナレッジ更新を実現する設計パターン

## 前提知識

- **RAG（検索拡張生成）** (TODO: 読むべき)
- **ベクトル埋め込み** (TODO: 読むべき)
- **Cloudflare Workers** (TODO: 読むべき)
- **Vectorize** (TODO: 読むべき)
- **Gemma** → /deep_168 Google Research 2025年振り返り：生成モデルの効率化・量子コンピューティング・科学的発見の加速

## 関連記事

- /deep_831 BERTの後継モデル登場：ModernBERTの紹介
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証

## 原文リンク

[CloudflareスタックだけでブラウザゲームのNaive RAGシステムを構築する](https://zenn.dev/gearfried/articles/581b8730720b71)
