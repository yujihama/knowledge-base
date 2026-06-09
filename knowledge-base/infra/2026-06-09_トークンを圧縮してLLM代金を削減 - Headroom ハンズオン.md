---
title: "トークンを圧縮してLLM代金を削減 - Headroom ハンズオン"
url: "https://zenn.dev/ggmayer/articles/efa1eb9bd811ee"
date: 2026-06-09
tags: [Headroom, トークン圧縮, LLMプロキシ, Docker, Claude Code, Codex, OpenAI互換API, コスト削減]
category: "infra"
related: [3086, 2541, 6411, 6478, 2963]
memo: "[Zenn LLM] トークンを圧縮してLLM代金を削減 - Headroom ハンズオン"
processed_at: "2026-06-09T21:03:48.439707"
---

## 要約

HeadroomはLLMに送信するコンテキストを事前圧縮し、入力トークン量を削減するローカルプロキシツール。LLMモデル自体を軽量化するのではなく、Claude Code・Codex・CursorなどのAIコーディングエージェントが生成するログ、ツール出力、検索結果、RAG結果、会話履歴といった肥大化しやすい入力データをLLMへ渡す前に圧縮する点が特徴。

Docker Composeを用いたローカルプロキシ構成で導入できる。`ghcr.io/chopratejas/headroom:latest`イメージをポート8787で起動し、HuggingFaceトークン（HF_TOKEN）を環境変数として渡す。GUI用コンテナ（headroom-gui）はNode.js 22-alpineベースのDockerfileと、socatでポートフォワードするentrypoint.shを自作することで安定動作を実現している。GUIはlocalhost:3000で確認可能。

Codexからの接続設定は`config.toml`に`openai_base_url = "http://127.0.0.1:8787/v1"`を追記するだけで完結し、OpenAI API互換エンドポイントとして機能する。別コンテナからの場合は`http://headroom:8787/v1`に変更する。

実測値は圧縮対象コンテンツに対して約6%、全体では約3%の削減にとどまった。記事の考察によれば、日常的なコーディング作業では巨大JSON・構造化ログ・大量検索結果などHeadroomが得意とする入力が少なく効果が限定的となる。GUIダッシュボードではTokens Saved・Active Savings・By Strategy（圧縮戦略の内訳）・Cache Hitsを確認でき、どの戦略が機能しているかを把握できる。

効果が大きいユースケースとして、大量ログのLLM渡し、大きなJSONレスポンス処理、grep/検索結果の大量読み込み、テスト・エラーログの頻繁な解析、RAGやドキュメント検索結果の多用、長い会話履歴を維持したエージェント運用が挙げられる。監査エージェント開発への示唆として、内部統制チェックや証跡ログをLLMに大量投入するワークフローではHeadroomのような中間プロキシを挟むことでAPIコストを抑制できる可能性がある。特にReActループで繰り返しログを参照するエージェント構成との相性が良いと考えられる。

## アイデア

- LLMモデルではなくコンテキスト入力側を圧縮するアプローチは、モデル非依存でどのAPIにも適用できる汎用性がある
- socatを使ってlocalhostバインドのプロセスをコンテナ外公開する手法は、headless GUIツールのDocker化一般に応用できる
- By Strategyで圧縮戦略の内訳を可視化する設計は、LLM-as-judgeやRAGパイプラインのデバッグ・最適化サイクルに組み込める観測性（Observability）パターンの実装例

## 前提知識

- **OpenAI API互換エンドポイント** (TODO: 読むべき)
- **Docker Compose** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LLMトークン課金** (TODO: 読むべき)
- **リバースプロキシ** (TODO: 読むべき)

## 関連記事

- /deep_3086 なぜ、Claude CodeもCodexもエージェントではありえないのか？
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？
- /deep_6411 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する
- /deep_6478 Windows11 RTX 5090でAIエージェント用Qwen3.6-27B LLM環境構築
- /deep_2963 SOWでシンプルにClaude Codeを活用する

## 原文リンク

[トークンを圧縮してLLM代金を削減 - Headroom ハンズオン](https://zenn.dev/ggmayer/articles/efa1eb9bd811ee)
