---
title: "Bonsai-8B-mlx × Goose でフルローカルの AI エージェント環境を構築する"
url: "https://zenn.dev/geeknees/articles/52f2b7ca6b81e4"
date: 2026-04-09
tags: [MLX, Bonsai-8B, Goose, ローカルLLM, OpenAI互換API, Apple Silicon, AIエージェント, Custom Provider]
category: "infra"
memo: "[Zenn LLM] Bonsai-8B-mlx × Goose でフルローカルの AI エージェント環境を作る"
processed_at: "2026-04-09T12:39:58.112332"
---

## 要約

Mac（Apple Silicon、M1・16GB メモリ）上で完全ローカルの AI エージェント環境を構築する方法を解説した記事。使用するコンポーネントは PrismML が公開する Bonsai-8B-mlx（MLX フォーマットの 8B パラメータ LLM）と、Block（Square 親会社）が開発するオープンソース AI エージェントフレームワーク Goose の 2 つ。

Bonsai-8B-mlx は Apple の機械学習フレームワーク MLX を使い、Apple Silicon の Unified Memory 上で直接推論する。mlx_lm.server コマンドでポート 8081 に OpenAI 互換 HTTP サーバーとして起動でき、/v1/models・/v1/chat/completions エンドポイントを提供する。モデル ID は /v1/models では「models/Bonsai-8B-mlx」と表示されるが、chat completion レスポンスには「default_model」と返るため、Goose 登録時は「default_model」を使う必要がある。

Goose は CLI とデスクトップ GUI を持つコーディングエージェントで、Custom Provider 機能により OpenAI 互換 API であればローカル LLM を含む任意のバックエンドを登録できる。設定は GUI の Settings → Providers から行うか、~/.config/goose/custom_providers/ 以下に JSON ファイルを置く方法で管理できる。Streaming Support は初期段階では off にすることが推奨されており、on のままにするとレスポンスが途中で切れる問題が発生する。

トラブルシューティングとして 3 点が整理されている。①API URL をルート（/）ではなく /v1/chat/completions に設定しないと 404 レスポンスを JSON パースしようとしてエラーになる。② モデル名の不一致（Bonsai-8B-mlx と指定すると Model not found になるため default_model を使う）。③ ストリーミングを off にしてレスポンス切断を防ぐ。

実用上の制限として、日本語応答の品質が低いこと、Tool 呼び出し（関数呼び出し）が不安定で完了しないケースがあること、16GB Unified Memory での CPU・メモリ負荷が高いことが挙げられている。クラウド API を一切使わないオフライン環境での AI エージェント動作を優先する用途向けのセットアップであり、本番利用よりも検証・プライバシー重視の実験環境として位置付けられる。

## アイデア

- OpenAI 互換 API レイヤーを挟むことで、モデルを差し替えても上位のエージェントフレームワーク（Goose, LangGraph 等）を無修正で使い回せる疎結合アーキテクチャの実例
- mlx_lm.server の /v1/models と chat completion レスポンスでモデル ID が異なる（models/Bonsai-8B-mlx vs default_model）という非自明な仕様差は、OpenAI 互換を謳うローカルサーバー全般に潜む互換性の落とし穴として注意すべき点
- Tool 呼び出しの不安定性は 8B 規模モデルの function calling 能力の限界を示しており、エージェントの信頼性には LLM の instruction-following 精度がボトルネックになることを示す実験的根拠
## 関連記事

- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- /deep_1493 Apple SiliconでCore MLを使ってStable Diffusionを動かす
- /deep_1143 AIがスマホで動く時代が来た — エッジAIとは何か、何が変わるのか、Bonsai 8Bを動かしてみた

## 原文リンク

[Bonsai-8B-mlx × Goose でフルローカルの AI エージェント環境を構築する](https://zenn.dev/geeknees/articles/52f2b7ca6b81e4)
