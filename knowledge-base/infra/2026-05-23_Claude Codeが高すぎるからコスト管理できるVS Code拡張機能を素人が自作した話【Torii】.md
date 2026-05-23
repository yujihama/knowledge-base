---
title: "Claude Codeが高すぎるからコスト管理できるVS Code拡張機能を素人が自作した話【Torii】"
url: "https://zenn.dev/2dachs/articles/8b37c3fa916f8d"
date: 2026-05-23
tags: [VS Code拡張機能, Claude Code, コスト管理, マルチプロバイダー, Ollama, Cline SDK, @cline/agents, 個人開発, エージェントループ, React, Node.js]
category: "infra"
related: [4473, 4753, 2950, 4619, 2404]
memo: "[Zenn LLM] Claude Codeが高すぎるからコスト管理できるVS Code拡張機能を素人が自作した話【Torii】"
processed_at: "2026-05-23T09:09:03.178376"
---

## 要約

Claude CodeのProプラン（5時間セッション・週次制限）に頻繁に引っかかった個人開発者が、コスト可視化とマルチプロバイダー対応を備えたVS Code拡張機能「Torii（鳥居）」をClaude Codeで自作した事例。

Toriiの主要機能は4つ。①コスト透明性：1会話ごとのコストをリアルタイム表示し、月間合計を円換算（為替レート自動取得）でバー表示。プロジェクト別・グローバル別の予算管理も可能。②マルチプロバイダー対応：OpenAI・Anthropic・DeepSeek・Google Gemini・Ollama（ローカル）を切り替え可能で、用途・予算に応じた自動ルーティングを実装。③プライバシー自動保護：APIキーやパスワード等の機密キーワードを含むプロンプトを自動でOllamaに転送し、クラウド送信を防止。④エージェントループ（Pro機能）：ファイル読み書き・コマンド実行を自律的に繰り返すループを実装し、実行前のワンクリック承認UIと危険コマンドの自動ブロックを装備。

アーキテクチャはVS Code拡張機能の標準的な2プロセス構成（Extension Host＋Webview）をベースに、React製WebviewとNode.js製Extension Host間をpostMessageで繋ぎ、さらにExtension Hostと127.0.0.1上のExpressサーバーをSSE/HTTPで接続する3層構造。エージェントループはゼロから実装を試みたが、同じ質問の繰り返しやプロジェクトファイル不読取りの問題で約1週間を消費。2025年5月14日にCline SDKがOSS化されたタイミングで@cline/agentsを採用し、read_file・write_file・run_command等のツール定義に集中できた。

承認フローはAIのrun_command呼び出し→agentLoopのPromise待機→SSEでWebview通知→承認UI表示→Approve/Cancel→ループ継続/中断という経路を実装。WebviewとExtension Hostの別プロセス性に起因するpostMessage→SSE→HTTP POSTの双方向通信が実装上の最大の難所だった。

価格はチャットモード・予算管理・コスト表示・マルチプロバイダー対応が無料（OSS・MIT）、エージェントループ・ストリーミング応答がPro版¥980/月（7日間無料トライアル付き）。APIの従量課金は別途必要だが、DeepSeekやOllamaを使えば実質ほぼ無料で運用可能。VS Code Marketplaceで「Torii」検索またはext install pettal.toriiでインストール可能。Lemon Squeezy審査完了まではPro版もベータとして無料開放中。

## アイデア

- 機密キーワードを含むプロンプトを自動検出してOllamaにルーティングするプライバシー保護機構：クラウドAPIとローカルLLMをポリシーベースで自動振り分けする設計は、監査ログや機密文書を扱う監査エージェントでも応用可能
- @cline/agentsのOSS化によりゼロ実装の1週間のロスを解消：エージェントループの安定した共通基盤の存在が個人開発の生産性に与える影響の大きさを示す実例
- WebviewとExtension Host間のpostMessage→SSE→HTTP POSTという三段階の双方向通信による承認フロー：AIの自律実行とユーザー承認を組み合わせたヒューマン・イン・ザ・ループの実装パターン

## 前提知識

- **VS Code Extension API** (TODO: 読むべき)
- **Cline SDK / @cline/agents** (TODO: 読むべき)
- **SSE（Server-Sent Events）** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **LLM APIルーティング** (TODO: 読むべき)

## 関連記事

- /deep_4473 WantedlyのPlaywright自動化で3回連続404——CDPセッション越しにフォームへ辿り着くまでの1時間
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_4619 ワークフロー象限とReAct象限の間のグラデーション — 設計フェーズと運用フェーズがスキル設計位置を決める
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門

## 原文リンク

[Claude Codeが高すぎるからコスト管理できるVS Code拡張機能を素人が自作した話【Torii】](https://zenn.dev/2dachs/articles/8b37c3fa916f8d)
