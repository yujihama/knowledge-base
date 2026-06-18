---
title: "複数ワーカーで LLM API のレート制限を守る: lease 方式と共有ストア直接管理の選び方"
url: "https://zenn.dev/moridev/articles/4706a8151be94f"
date: 2026-06-18
tags: [レート制限, 分散システム, LLM API, Redis, GCRA, token bucket, lease, LiteLLM, asyncio, RPM]
category: "agent-arch"
related: [8475, 8551, 6269, 5392, 7516]
memo: "[Zenn LLM] 複数ワーカーで LLM API のレート制限を守る: lease 方式と共有ストア直接管理の選び方"
processed_at: "2026-06-18T09:03:37.529605"
---

## 要約

複数のワーカー・コンテナから同一の LLM API を呼び出す場合、プロセス内の asyncio.Semaphore だけではサービス全体の RPM・トークン上限を守れない。本記事は Redis や NATS KV などの共有ストアを使った分散レート制限の設計、特に「lease（リース）方式」の落とし穴と正しい使い方を解説する。

lease とは、ワーカーが一定期間分の利用枠をまとめて共有ストアから確保し、TTL 内はローカルカウンターで消費する方式。リクエストごとに CAS（Compare-and-Swap）する方式と比較して共有ストアへのアクセス頻度を大幅に削減できる。

最大の落とし穴は「lease の TTL と API 側の基準時間（RPM の 60 秒など）を同一視すること」。例えば RPM=50 の API に対し TTL=30 秒・割当=50 リクエストの lease を設計すると、有効 RPM は 100 となり上限の 2 倍を許可してしまう。TTL を 60 秒に合わせても、lease は「総量」しか管理せず「いつ送るか」は制御しないため、50 リクエストを 1 秒以内に集中送信すれば 429 が発生する。

対策は 2 つに分けて考える。①TTL に比例して割当量を換算する（TTL=30 秒なら RPM50 の半分の 25 リクエストを割り当てる）、②ワーカー内で LocalPacer を使い送信間隔をならす（25 req / 30 sec = 1.2 秒間隔）。lease が「総量」、pacer が「タイミング」を担う役割分担が重要。さらに実運用では安全率 0.8 をかけて configured_rpm=40 として運用することで 429 によるリトライを抑制する。

より厳密な制御が必要な場合は lease を使わず、共有ストア上で直近 60 秒のウィンドウを直接管理するか、token bucket の状態（最終補充時刻・残トークン・補充速度）を共有ストアに保持する方式を選ぶ。ただしリクエストごとに共有ストアへの読み書きと CAS 競合が発生するトレードオフがある。

既製ライブラリとしては limits（Redis/etcd 対応・コスト重み付け可）、pyrate-limiter（token bucket/leaky bucket）、redis-cell（Redis モジュール・GCRA 方式）が利用可能。LLM ゲートウェイとしては LiteLLM（複数プロバイダのレート制限を一元管理）が実務的な第一選択肢となる。自前実装が正当化されるのは共有ストアへのアクセスを極小化したい高頻度バッチ処理に限られる。

監査エージェント開発への示唆：LangGraph を使った並列エージェントから同一 LLM API を呼び出す構成では、このレート制限設計が直接適用できる。lease + pacer の組み合わせにより、Redis 等の共有ストアへの負荷を抑えながら安定したスループットを確保できる。

## アイデア

- lease の TTL と API 側の基準時間（RPM の 60 秒）は別概念であり、TTL が短ければ割当量も比例縮小しなければ実効 RPM が倍増するという反直感的な落とし穴
- lease（総量制御）と pacer（タイミング制御）を明示的に役割分担することで、設計の責任範囲が明確になり独立してチューニングできる
- GCRA（Generic Cell Rate Algorithm）は token bucket と等価でありながら単一の状態変数から次の送信可能時刻を計算できるため、共有ストア上での実装が簡潔になる

## 前提知識

- **RPM / token bucket** (TODO: 読むべき)
- **Redis CAS** (TODO: 読むべき)
- **asyncio.Semaphore** (TODO: 読むべき)
- **GCRA** (TODO: 読むべき)
- **sliding window** (TODO: 読むべき)

## 関連記事

- /deep_8475 複数ワーカーで LLM API のレート制限を扱う設計案
- /deep_8551 NATSで実装するLLM API分散レートリミッター
- /deep_6269 開発しながらLoRAデータが自動で貯まる仕組み「M2LoRA」を作った
- /deep_5392 書籍OCRにLLMを組み合わせて精度向上と文書構造化を実現した記録
- /deep_7516 広告コピー10案を一括生成するLLMシステムの実装【Google/Meta/X対応】

## 原文リンク

[複数ワーカーで LLM API のレート制限を守る: lease 方式と共有ストア直接管理の選び方](https://zenn.dev/moridev/articles/4706a8151be94f)
