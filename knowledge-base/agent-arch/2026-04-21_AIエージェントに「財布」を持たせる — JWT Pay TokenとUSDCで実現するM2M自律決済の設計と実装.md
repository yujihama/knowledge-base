---
title: "AIエージェントに「財布」を持たせる — JWT Pay TokenとUSDCで実現するM2M自律決済の設計と実装"
url: "https://zenn.dev/evidai/articles/29c6fe5025438b"
date: 2026-04-21
tags: [JWT, EdDSA, M2M決済, Pay Token, USDC, JPYC, LangChain, Prisma, 楽観ロック, マルチエージェント, 予算委譲, 402 Payment Required]
category: "agent-arch"
related: [41, 858, 2255, 2251, 2298]
memo: "[Zenn LLM] AIエージェントに「財布」を持たせる — JWT Pay TokenとUSDCで実現するM2M自律決済の設計と実装"
processed_at: "2026-04-21T12:38:44.373548"
---

## 要約

AIエージェントがツールや有料APIを呼び出す際の「誰が払うか・いくら使えるか」という課題に対し、JWT（EdDSA/Ed25519署名）ベースのPay TokenとUSDC建て残高管理を組み合わせたM2M（Machine-to-Machine）自律決済アーキテクチャを提案・実装した記事。

従来の課題は3点：①APIキーをエージェントに渡すと全リソースへのアクセス権限が過剰になる、②フロントエンドがその都度ユーザーに確認すると自律性が損なわれる、③どのエージェントが何に使ったか監査できない。

Pay TokenはJWTペイロードにjti（トークンID）、buyerId（支払い責任者）、serviceId（呼び出し可能サービス制限）、limitUsdc（上限額・18桁精度）、buyerTag（エージェントセッション識別子・監査ログ用）、exp（有効期限）を格納する。署名アルゴリズムはRSA-PKCS1-v1_5（RS256）ではなくEdDSA（Ed25519）を採用し、署名サイズ64バイト（RS256の256バイトの1/4）、タイミング攻撃耐性、RFC 8037準拠という利点を持つ。

サーバー実装はHono（TypeScript）＋Prismaで構成。トークン発行時にDB上のTokenレコード（limitUsdc, usedUsdc, revoked等）を作成しJWT署名を付与。プロキシミドルウェアがエージェントリクエストのPay Tokenを検証し、残高チェック（悲観ロック）→実行→楽観ロックによるアトミックな課金記録（usedUsdcのincrementとChargeレコード作成をPrismaトランザクション内で実行）という流れで二重課金を防止する。残高超過時は402 Payment Requiredを返す。

日本円での入金にはPolygonチェーン上のERC-20トークンであるJPYC（1 JPYC≈1円）を活用。ユーザーがプラットフォームウォレットへJPYCを送金し、TXハッシュを申請するとethers.jsでオンチェーン検証（ERC-20 Transferイベントデコード）し、レート換算してUSDC残高に自動加算する。

マルチエージェント構成では、親エージェントが子エージェントに親残高の最大80%を上限としてサブトークンを委譲する予算委譲パターンを実装。エージェントが402を受信した際は「TOKEN_LIMIT_EXCEEDED」なら処理中断、「TOKEN_EXPIRED」なら自動リフレッシュという自律的なハンドリングが可能。LangChain BaseTool・AutoGenへの統合実装例も示す。課金データはQuickBooks・Xero・freeeへの会計仕訳自動同期にも対応。

監査エージェント開発への示唆：buyerTagによる操作主体の追跡とChargeレコードへの記録は、エージェントの費用対効果分析や不正利用検知に直結する。limitUsdcで明示的に権限範囲を絞る設計は、最小権限原則（Least Privilege）の実装例として内部統制観点でも参考になる。

## アイデア

- buyerTagフィールドをエージェントセッション識別子として設計することで、どのエージェントがいくら消費したかを監査ログに残せる点—これは監査AIシステムにおけるコスト追跡・責任主体の特定に直接応用できる
- 親エージェントが子エージェントに残高の80%上限でサブトークンを委譲する予算委譲パターン—LangGraphの階層エージェント設計と組み合わせることで、サブグラフごとに予算キャップを設けた制御可能なマルチエージェントが実現できる
- 402 Payment Requiredをエージェントの自律的な意思決定トリガーとして活用する設計—HTTPエラーコードをエージェントの状態遷移シグナルとして意味付けすることで、外部サービスとエージェントのインターフェース設計が標準化できる

## 前提知識

- **JWT / JWS** (TODO: 読むべき)
- **EdDSA / Ed25519** (TODO: 読むべき)
- **ERC-20 / Polygon** (TODO: 読むべき)
- **LangChain BaseTool** (TODO: 読むべき)
- **Prismaトランザクション** (TODO: 読むべき)

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_2251 The Colony Builder's Handbook — AIエージェントのためのソーシャルネットワーク入門
- /deep_2298 LLMベースの教育エージェントに関するスコーピングレビュー

## 原文リンク

[AIエージェントに「財布」を持たせる — JWT Pay TokenとUSDCで実現するM2M自律決済の設計と実装](https://zenn.dev/evidai/articles/29c6fe5025438b)
