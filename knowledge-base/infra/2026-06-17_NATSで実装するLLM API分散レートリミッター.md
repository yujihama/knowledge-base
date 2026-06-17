---
title: "NATSで実装するLLM API分散レートリミッター"
url: "https://zenn.dev/moridev/articles/8ff6da3dd48a91"
date: 2026-06-17
tags: [NATS, JetStream, NATS KV, 分散レートリミッター, CAS, RPM制御, LLM API, マルチワーカー, asyncio]
category: "infra"
related: [6269, 8475, 5392, 7516, 7066]
memo: "[Zenn LLM] NATS で実装する LLM API 分散レートリミッター"
processed_at: "2026-06-17T09:05:36.524873"
---

## 要約

複数ワーカーからLLM APIを並列呼び出しする際、単一プロセスのasyncio.Semaphoreではサービス全体のRPMやトークン上限を制御できない問題に対し、NATS JetStreamとNATS KVを組み合わせた分散レートリミッターの実装方法を解説する記事。

Redisを使う従来構成との最大の違いは、ジョブキュー（JetStream）と共有KVストア（NATS KV）を同一のNATSインフラに集約できる点。Redis構成ではMQ＋Redisの2系統が必要だが、NATS構成では1系統に統一できる。

競合制御の仕組みも異なる。RedisはLuaスクリプトで「get→判定→set」をアトミックに実行できるが、NATS KVにはその機能がない。代わりにCAS（Compare-and-Swap）ループを使い、kv.update()に読み取り時のrevisionを渡すことで、他ワーカーによる更新を検出してリトライする。試行上限は10回、試行間隔0.01秒を設定し無限ループを防止する。

ウィンドウ管理はキー名に時刻（例: rpm.20260526T1000）を埋め込む方式を採用。分が変わると自動的に別キーを参照し、バケットのTTL=60秒設定により古いキーが自動削除される。

NATS KVへのアクセス集中を緩和するため、BatchingRateLimiterを導入。ワーカーがbatch_size=10分の利用枠をまとめて借り、ローカルのLocalLeaseで消費管理することで、KVアクセス頻度を約1/10に削減できる。ただし未使用分は共有ストアへ返却されず、ワーカー数×batch_sizeがmax_rpmを大幅に下回るよう設計する必要がある。またウィンドウ境界をまたいで枠を持ち越せないため、ローカルリースに借りた時点のウィンドウを記録し、変わったら破棄・再取得する。

管理対象の利用枠は同時実行数・RPM・ITPM・OTPMの4種類。RPM/ITPM/OTPMはウィンドウキー方式とバケットTTLで自然に管理できる。一方、同時実行数はゲージ（増減する現在値）のため、固定キー名で別バケット（TTLなしまたは長め）に分離する必要がある。ワーカークラッシュ時の減算漏れ対策として、リースIDと短いTTLの別バケットで管理し、期限切れリースを定期的に回収する設計が推奨される。

監査エージェント開発への示唆：複数の監査ワーカーがAnthropicやOpenAI APIを並列呼び出しする場合、このNATS KV＋CASループによる分散レートリミッターパターンはそのまま適用可能。LangGraphのノード実行タスクをJetStream pull consumerで受け取り、max_deliver=5のリトライ上限とterm()によるデッドレター設計を組み合わせることで、API制限起因の失敗ジョブを適切にハンドリングできる。

## アイデア

- NATS KVのCASループによる競合制御は、Redisのトランザクションスクリプトと等価な安全性を提供しつつ、インフラを1系統に統一できる設計パターン
- BatchingRateLimiterによるローカルリース方式は、共有ストアへのアクセス頻度を1/batch_sizeに削減するトレードオフ設計で、LLM APIの高頻度呼び出し環境に有効
- 同時実行数（ゲージ）とRPM/トークン数（累積カウンター）ではTTL戦略が根本的に異なるため、KVバケットを分離して管理する必要があるという設計原則

## 前提知識

- **NATS JetStream** (TODO: 読むべき)
- **分散レートリミット** (TODO: 読むべき)
- **CAS（Compare-and-Swap）** (TODO: 読むべき)
- **asyncio** → /deep_35 AIエージェントの出力を代謝で管理する — Metabolic Agent Executionの設計
- **RPM/TPM制御** (TODO: 読むべき)

## 関連記事

- /deep_6269 開発しながらLoRAデータが自動で貯まる仕組み「M2LoRA」を作った
- /deep_8475 複数ワーカーで LLM API のレート制限を扱う設計案
- /deep_5392 書籍OCRにLLMを組み合わせて精度向上と文書構造化を実現した記録
- /deep_7516 広告コピー10案を一括生成するLLMシステムの実装【Google/Meta/X対応】
- /deep_7066 乗り換え検討用：主要LLM API料金を9社・3階層（フラッグシップ/mini/nano）で比較 2026年5月更新

## 原文リンク

[NATSで実装するLLM API分散レートリミッター](https://zenn.dev/moridev/articles/8ff6da3dd48a91)
