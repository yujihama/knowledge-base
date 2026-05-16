---
title: "Gemini Live APIを用いてAI架電アプリを作ってみた"
url: "https://zenn.dev/milix_m/articles/ede75fba87c10b"
date: 2026-04-28
tags: [Gemini Live API, Twilio, WebSocket, FastAPI, 音声ストリーミング, audioop, μ-law, PCM変換, Docker, ngrok]
category: "infra"
related: [2590, 409, 1448, 1736, 2828]
memo: "[Zenn LLM] Gemini Live APIを用いてAI架電アプリを作ってみた"
processed_at: "2026-04-28T12:37:11.353245"
---

## 要約

Gemini Live APIとTwilioを組み合わせたAI架電アプリケーションの構築事例。フロントエンドはReact 19 + Vite 8 + React Router 7、バックエンドはPython 3.12上のFastAPI + Uvicorn（非同期対応）、DBはSQLite + SQLAlchemy（aiosqlite使用）、デプロイはDocker + Caddyのシングルコンテナ構成。

コア機能は「Geminiブリッジ」と呼ぶWebSocketブリッジ層で、TwilioのMedia Stream（WebSocket）とGemini Live API（WebSocket双方向音声ストリーミング）を中継する。両者の音声フォーマットが異なるため、標準ライブラリのaudioopを用いてμ-law 8kHz（Twilio側）↔ PCM 16kHz/24kHz（Gemini側）のリアルタイム変換を行う。

処理フローは以下の通り：(1) Web UIから架電操作 → (2) FastAPIがTwilio APIを呼び出し発信 → (3) 通話接続後、GeminiブリッジがTwilio Media StreamとGemini Live APIを双方向接続 → (4) 通話終了時にTwilioからFastAPIへWebhookで通知 → (5) 通話ログをDB更新。通話中はリアルタイムで状況確認でき、通話終了後は通常のGeminiモデルで通話内容の要約も生成可能。ユーザー側音声の文字起こしもブリッジ内で実施。

ローカル開発時はngrokでポート8000を外部公開し、TwilioからのWebhook・WebSocketを受信。UI上でプロンプト（AIの振る舞い）と発信先を自由に設定できる。

現状の課題として、応答遅延・相槌タイミングの不安定さ、ユーザー側音声の文字起こし精度の低さが挙げられている。監査エージェント開発への示唆として、WebSocketを介したリアルタイム音声ストリームと外部APIのブリッジ設計パターンは、電話ヒアリング自動化や監査対話ログ収集に応用可能。また音声フォーマット変換を薄いブリッジ層に閉じ込める設計は、異種プロトコル統合エージェントの参考になる。

## アイデア

- TwilioのMedia StreamとGemini Live APIはどちらもWebSocketベースだが音声フォーマットが異なり、ブリッジ層でμ-law 8kHz↔PCM 16/24kHzをリアルタイム変換する設計は、異種音声プロトコルを繋ぐ汎用パターンとして応用範囲が広い
- 通話中のリアルタイム文字起こしと、通話終了後の別モデルによる要約生成を分離することで、レイテンシと品質のトレードオフを使い分けている点が実装上の工夫として興味深い
- プロンプトをUI上で自由設定できる構成により、同じブリッジ基盤で用途（予約確認・調査・通知等）を切り替えられ、エージェントのペルソナ管理をインフラから分離する設計として参考になる

## 前提知識

- **Gemini Live API** (TODO: 読むべき)
- **Twilio Media Stream** (TODO: 読むべき)
- **WebSocket双方向通信** (TODO: 読むべき)
- **μ-law/PCM音声フォーマット** (TODO: 読むべき)
- **FastAPI非同期処理** (TODO: 読むべき)

## 関連記事

- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_2828 【実践】ハーネスエンジニアリング入門：セキュリティAIエージェント Warren を手元で動かして学ぶ

## 原文リンク

[Gemini Live APIを用いてAI架電アプリを作ってみた](https://zenn.dev/milix_m/articles/ede75fba87c10b)
