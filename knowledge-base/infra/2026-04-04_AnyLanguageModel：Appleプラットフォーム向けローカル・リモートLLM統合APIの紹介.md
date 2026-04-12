---
title: "AnyLanguageModel：Appleプラットフォーム向けローカル・リモートLLM統合APIの紹介"
url: "https://huggingface.co/blog/anylanguagemodel"
date: 2026-04-04
tags: [Swift, MLX, Apple-Silicon, llama.cpp, Ollama, Foundation-Models, HuggingFace, LLM-API]
category: "infra"
memo: "[HF Blog] Introducing AnyLanguageModel: One API for Local and Remote LLMs on Apple Platforms"
processed_at: "2026-04-04T09:10:20.428155"
---

## 要約

AnyLanguageModelは、HuggingFaceが発表したSwiftパッケージで、Appleプラットフォーム上でのLLM統合の摩擦を解消することを目的としている。現状、Apple開発者がAIアプリを構築する際はCore ML、MLX、Apple Foundation Models、クラウドAPIなど複数の異なるAPIを組み合わせる必要があり、各統合に多大なコストがかかっていた。

本ライブラリの核心的なアプローチは、AppleのFoundation Modelsフレームワークをベースとして採用し、`import FoundationModels`を`import AnyLanguageModel`に差し替えるだけで複数のバックエンドに切り替えられる互換APIを提供することである。対応プロバイダーは、Apple Foundation Models（macOS 26+/iOS 26+）、Core ML（Neural Engine加速）、MLX（Apple Siliconでの量子化モデル）、llama.cpp（GGUFモデル）、Ollama（ローカルHTTP API）、OpenAI・Anthropic・Google GeminiなどのクラウドAPI、さらにHugging Face Inference Providersと多岐にわたる。

アーキテクチャ上の重要な工夫として、Swift 6.1のパッケージトレイト機能を活用した依存関係の最小化がある。`traits: ["MLX"]`のように使用するバックエンドのみを宣言することで、不要な依存を排除できる。デフォルトでは重量級の依存は含まれず、クラウドプロバイダーはURLSessionのみで動作する。

Foundation ModelsのAPIを基盤として選んだ理由として、Swiftのマクロを活用した人間工学的な設計、セッション・ツール・生成という抽象化がLLMの実動作と適合している点、全Apple開発者が習得するAPIであるため学習コストが低い点が挙げられている。

現時点ではApple Foundation ModelsがImage入力未対応であるため、Anthropic等のビジョンモデル向けにAPIを独自拡張し画像送信をサポートしている。将来のApple実装との競合リスクを認識した上で、DeprecationWarningで対処する方針を明示している。

今後の開発予定として、全プロバイダーへのツール呼び出し対応、MCPインテグレーション、構造化出力のGuided generation、ローカル推論の性能最適化が計画されており、最終的にはAppleプラットフォーム上でのシームレスなエージェントワークフロー構築基盤を目指している。デモアプリとしてchat-ui-swiftも公開されており、Apple Intelligence統合・HuggingFace OAuth認証・ストリーミング応答・チャット永続化が実装されている。現在のバージョンは0.4.0でpre-1.0段階。

## アイデア

- 「既存の優れたAPIをベースとして採用し、importの差し替えのみで複数バックエンドに対応する」という設計思想は、抽象化レイヤーの肥大化を避けつつ互換性を確保する実用的アプローチ
- Swift 6.1のパッケージトレイト機能による依存関係の選択的包含は、マルチバックエンドライブラリの依存肥大化問題に対するクリーンな解決策
- Apple Foundation ModelsのAPIが未対応の機能（画像入力）に対し、将来の公式実装と競合するリスクを承知の上でAPIを先行拡張するというプラグマティックな意思決定
## 関連記事

- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_859 Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル
- /deep_400 GGMLとllama.cppがHugging Faceに参加——ローカルAIの長期的発展を支える体制へ

## 原文リンク

[AnyLanguageModel：Appleプラットフォーム向けローカル・リモートLLM統合APIの紹介](https://huggingface.co/blog/anylanguagemodel)
