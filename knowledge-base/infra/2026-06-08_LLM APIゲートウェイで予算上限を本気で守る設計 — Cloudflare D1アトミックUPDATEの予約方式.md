---
title: "LLM APIゲートウェイで予算上限を本気で守る設計 — Cloudflare D1アトミックUPDATEの予約方式"
url: "https://zenn.dev/beki/articles/0170717cc81f3e"
date: 2026-06-08
tags: [LLM-gateway, Cloudflare-D1, SQLite, budget-management, Race-Condition, atomic-UPDATE, TypeScript, Cloudflare-Workers, cost-control, multi-tenant]
category: "infra"
related: [7758, 3898, 6527, 7375, 3095]
memo: "[Zenn LLM] LLM API ゲートウェイで予算上限を本気で守る設計 — Cloudflare D1 アトミック UPDATE の予約方式"
processed_at: "2026-06-08T21:04:36.785091"
---

## 要約

LLM APIの予算管理における並行リクエスト下のRace Conditionを、Cloudflare D1（SQLiteベース）のアトミック条件付きUPDATEで根治する設計を解説した記事。月予算10,000ドル・残り100ドルの状態に並行50リクエストが着弾すると、ナイーブな実装では全リクエストが「残予算100ドルOK」と判定して全通過し、実際には10,100ドルの消費になる典型的なRead-Modify-Write競合が発生する。解法として「予約方式」を採用：リクエスト着弾時に最大コスト見積もり分をreserved_usd_microに加算するUPDATE文のWHERE句に予算チェック条件（reserved + spent + max_cost ≤ cap）を組み込むことで、予算判定と予約を1文で原子的に実行。changes()が0なら予算不足として即429拒否する。上流LLM API応答後は実コストでCommit（予約解除＋実コスト記録）または失敗時はRelease（予約解除のみ）で3段階のライフサイクルを管理する。SQLiteの書き込みがプライマリで直列化される特性により、追加ロック機構なしでアトミックUPDATEが成立する。多段予算（組織×チーム×メンバー）は各階層へ逐次Reserveし、失敗時に直前までをReleaseするロールバックで対応可能。プロダクション考慮事項として冪等性設計も提示：budget_reservationsテーブルにrequest_idをPKとしてapply_nonceマーカーを持たせ、db.batch()で2文を1トランザクション実行することでWorkerクラッシュ時の片方適用による不整合を防ぐ。p99レイテンシは単段UPDATEで数十ms、5段逐次で数百ms以内であり、LLM APIの秒オーダー応答に対して実用的な追加コストに収まる。監査エージェント開発への示唆：エージェントの並列実行・繰り返し呼び出しが1件20〜50ドル規模になると1回の暴走で数千ドル超過が起こりうる。予算ゲートウェイをエージェントオーケストレーション層の前段に置く設計は、LangGraph等のマルチエージェント構成でのコスト制御アーキテクチャとして直接応用可能。

## アイデア

- WHERE句に予算チェック条件を埋め込んだ条件付きUPDATE1文で、予算判定と予約を原子的に実現する発想はSQLiteの直列化特性を活かした最小実装
- reserved + spent ≤ capの不等式で「予約中」という中間状態を管理することで、追加インフラ（Redis、分散ロック等）なしにRace Conditionを防げる
- apply_nonceマーカーパターンとdb.batch()による2文トランザクションで冪等性を保証し、Workerのリトライや上流タイムアウト後の二重実行を防ぐ設計

## 前提知識

- **ACID / アトミックトランザクション** (TODO: 読むべき)
- **Read-Modify-Write競合** (TODO: 読むべき)
- **Cloudflare Workers / D1** (TODO: 読むべき)
- **SQLite直列化書き込み** (TODO: 読むべき)
- **冪等性設計** → /deep_7338 LLMの出力を追跡可能にする：正規化・ハッシュ・状態遷移の設計

## 関連記事

- /deep_7758 Claudeが2時間ごとに世界を1日進める物語サイトを作った（完結したら永久停止）
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_6527 競馬予想MLでデータリーケージを正攻法で潰した話 — race_dateフィルタを4箇所に入れて気づいたこと
- /deep_7375 学生が個人開発でLightGBM競馬予想アプリを運用してわかったこと
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる

## 原文リンク

[LLM APIゲートウェイで予算上限を本気で守る設計 — Cloudflare D1アトミックUPDATEの予約方式](https://zenn.dev/beki/articles/0170717cc81f3e)
