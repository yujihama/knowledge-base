---
title: "ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成"
url: "https://zenn.dev/yay1/articles/80f6461bef92c6"
date: 2026-04-22
tags: [vLLM, LiteLLM, ngrok, OpenWebUI, HuggingFace ChatUI, Qwen3, Swallow, Docker, ローカルLLM, マルチモデル]
category: "infra"
related: [2403, 2404, 2257, 394, 524]
memo: "[Zenn LLM] 簡単にローカルモデルをデモする"
processed_at: "2026-04-22T12:09:10.528377"
---

## 要約

ローカル環境で動かすLLMを外部にデモ公開するための実用的なスタックを解説した記事。バックエンドにvLLMとLiteLLMを、フロントエンドにHuggingFace ChatUIまたはOpenWebUIを使い、ngrokで外部公開する構成。

vLLMは複数GPUを使い分けて複数モデルを並列起動する。具体的には、CUDA_VISIBLE_DEVICES=1でtokyotech-llm/Qwen3-Swallow-8B-RL-v0.2をポート8500、CUDA_VISIBLE_DEVICES=2でGPT-OSS-Swallow-20B-RL-v0.1をポート8501で起動する。各モデルはtmuxセッションで管理され、ログはlogsディレクトリに出力される。Qwen3系モデルはreasoning-parserオプションでqwen3を指定し、推論トークンのパース対応を行っている。

vLLMで複数モデルを起動するとポートが分散するため、LiteLLMプロキシで統合する。litellm_config.yamlに各モデルのエンドポイントをopenai互換形式で定義し、Dockerコンテナとして起動することでlocalhost:4000に全モデルのAPIを集約する。DockerからホストのvLLMへアクセスするためhost.docker.internal経由のアドレスを使用。curl /v1/modelsで集約確認が可能。

フロントエンドはHuggingFace ChatUIとOpenWebUIの2択。ChatUIはシンプルで、ngrokのBasic認証との相性が良い。OpenWebUIは2モデル同時推論、パラメータ調整、ユーザー管理、コード実行、Web検索、ツールユースなど高機能だが、ngrokのBasic認証と組み合わせるとChromeでページ遷移のたびに認証を求められる問題がある。

外部公開はngrokを使用し、httpsでlocalhostを公開。Basic認証が必要なデモ環境ではChatUI、認証不要の内部共有ではOpenWebUIが適しているという実用的な使い分け指針が示されている。監査AIや社内デモ用途で自社モデルを安全に試験公開する際のリファレンス構成として参考になる。

## アイデア

- LiteLLMプロキシによる複数vLLMエンドポイントの統合は、マルチモデル環境でのAPI管理を大幅に簡素化する——複数ポートを1ポートに集約することでフロントエンド側の実装を単純化できる
- ngrokのBasic認証とOpenWebUIの相性問題（Chromeでページ遷移ごとに認証要求）は、デモ環境設計時に注意が必要な実務的知見
- tmuxセッションとCUDA_VISIBLE_DEVICESの組み合わせによる複数モデルの並列管理は、マルチGPU環境でのモデル分離運用の典型パターンとして応用範囲が広い

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **LiteLLM** → /deep_827 smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ
- **Docker** → /deep_584 ScreenSuite - GUIエージェント向け最も包括的な評価スイート
- **OpenAI互換API** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **ngrok** (TODO: 読むべき)

## 関連記事

- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ

## 原文リンク

[ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成](https://zenn.dev/yay1/articles/80f6461bef92c6)
