---
title: "Pi Agent SDKを触ってみたメモ：LM Studio連携とカスタムプロバイダ実装"
url: "https://zenn.dev/nozomi_hiragi/articles/c4d874b96e2b35"
date: 2026-06-06
tags: [Pi Agent SDK, TypeScript, LM Studio, カスタムプロバイダ, AIエージェント, OpenAI互換API, ResourceLoader]
category: "agent-arch"
related: [1333, 3903, 4043, 1963, 1148]
memo: "[Zenn LLM] Pi Agent SDKを触ったのでメモ的な感じで"
processed_at: "2026-06-06T09:07:44.798303"
---

## 要約

Pi Agent SDK（@earendil-works/pi-coding-agent）を用いてAIエージェントを構築した際の実装メモ。PiはTypeScriptベースのエージェントフレームワークで、read/bash/edit/write/grep/find/lsといったファイル操作ツールが組み込み済みで、サクッとコーディングエージェントを作れる点が特徴。

セットアップでは、ResourceLoaderを用いてエクステンションやプロンプトを管理する。DefaultResourceLoaderをそのまま使うのが推奨で、プロンプトのカスタマイズはsystemPromptOverrideで行う。独自クラスを継承する方法は複雑になりがちで非推奨とされている。

イベントフックとして「before_agent_start」と「before_provider_request」が利用可能。前者ではシステムプロンプトの末尾に自動付与される「Current working directory:」の行を正規表現で削除するカスタマイズを実施。後者ではデフォルトの「developer」ロールを「system」ロールに書き換えることで、プロバイダ側のロール解釈を統一している。

セッション作成はresourceLoader.reload()後にcreateAgentSession()を呼び出し、customToolsで自作ツール、toolsで使用ツール一覧を指定する。会話はsession.prompt()で実行する。

LM Studio連携については、Piが標準でLM Studioプロバイダを提供していないため、公式パッケージカタログのコードを参考に自前実装。http://127.0.0.1:1234/api/v1/modelsからモデル一覧を取得し、type==="llm"のモデルのみをProviderModelConfigに変換。ProviderConfigにはname/baseUrl（/v1エンドポイント）/api（openai-completions）/apiKey/modelsを設定する。これによりOpenAI互換APIを持つローカルLLMをプロバイダとして利用できる。

著者は現在PiからOpenAI Agents SDKに移行済みであるが、Piは大半のエージェントユースケースをカバーできると評価している。監査エージェント開発への示唆としては、Piの組み込みツール群（特にbash/grep/find）はファイルベースの証跡収集や証拠チェックに転用可能であり、before_agent_startフックでシステムプロンプトを動的に制御するパターンは、監査フェーズ（計画・実施・報告）ごとにエージェントの振る舞いを切り替える設計に応用できる。

## アイデア

- before_agent_startフックでシステムプロンプトを動的書き換えするパターンは、エージェントのフェーズ管理（計画→実行→レビュー）に応用できる汎用的な制御手法
- OpenAI互換エンドポイント（/v1）を持つローカルLLMであれば同一プロバイダ実装で差し替え可能な設計は、モデル非依存アーキテクチャの実践例
- read/bash/edit/write等の組み込みツールセットはコーディングエージェント以外にも証跡収集・ログ解析エージェントへの転用が容易で、ツール設計の参考になる

## 前提知識

- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **TypeScript** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説
- **OpenAI Agents SDK** (TODO: 読むべき)
- **LM Studio** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- **システムプロンプト** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）

## 関連記事

- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_1963 C#でマルチモーダルLLMのHTTP通信を可視化する：画像のみ vs 画像+テキストのリクエスト構造比較
- /deep_1148 Bonsai-8B-mlx × Goose でフルローカルの AI エージェント環境を構築する

## 原文リンク

[Pi Agent SDKを触ってみたメモ：LM Studio連携とカスタムプロバイダ実装](https://zenn.dev/nozomi_hiragi/articles/c4d874b96e2b35)
