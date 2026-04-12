---
title: "Vibe Coding XR：XR BlocksとGeminiによるAI+XRプロトタイピングの高速化"
url: "https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/"
date: 2026-03-29
tags: [Gemini, XR Blocks, WebXR, vibe-coding, system-prompt-engineering, LLM-code-generation, Android XR, three.js, LiteRT, context-grounding]
category: "agent-arch"
memo: "[Google AI Blog] Vibe Coding XR: Accelerating AI + XR prototyping with XR Blocks and Gemini"
processed_at: "2026-03-29T22:54:21.815600"
---

## 要約

GoogleのResearchチームが発表した「Vibe Coding XR」は、大規模言語モデル（Gemini）と自社開発のオープンソースフレームワーク「XR Blocks」を組み合わせ、自然言語プロンプトから60秒以内にインタラクティブなAndroid XRアプリを生成するラピッドプロトタイピングワークフローである。

技術的基盤として、XR BlocksはWebXR・three.js・LiteRT.jsを用いたウェブベースのフレームワークであり、空間認識（depth sensing）、ハンドインタラクション、物理シミュレーションなどの複雑なサブシステムを統合管理する。Geminiには専用のシステムプロンプトが設計されており、XR Blocksのアーキテクチャ、コードテンプレート、ルームスケールXR環境のベストプラクティス（空間レイアウト・スケール・インタラクション距離等）が「教示」されている。このコンテキストグラウンディングにより、Geminiのハルシネーションを抑制し、有効なAPI呼び出しと設計パターンへの準拠を実現している。

ワークフローはGemini Canvasのインターフェース上で動作し、ユーザーはChromeブラウザ（デスクトップまたはAndroid XRヘッドセット）からテキストまたは音声でプロンプトを入力する。Geminiがマルチステップ計画と高度な推論によってシーン構成・知覚設定・インタラクション設計を行い、コードを生成する。デスクトップではXR Blocks内蔵のシミュレータで動作確認が可能であり、同一コードをAndroid XRデバイス（Samsung Galaxy XR等）に直接デプロイできる。

実証例として、数学チュータリング（四面体・立方体・正八面体でオイラーの定理を3D可視化）、物理実験（天秤に異なる重りを配置してバランスを学習）、化学実験シミュレーション（メタン・エチレン・アセチレンの燃焼を体積可視化）、シュレーディンガーの猫（量子重ね合わせ状態をピンチジェスチャーで操作）など、教育用途の多様なプロトタイプが生成されている。

ACM CHI 2026（2026年）でのデモ発表が予定されており、現在ライブデモとGitHubリポジトリが公開されている。

## アイデア

- 専用システムプロンプトにドメイン固有のコードテンプレートとアーキテクチャ仕様を埋め込むことで、LLMのハルシネーションを抑制しつつ特定ドメインの高品質コード生成を実現するアプローチ——これは「ドメイン特化コンテキストグラウンディング」として汎用的なエージェント設計パターンになりえる
- デスクトップシミュレータ→実機デプロイという「段階的検証パイプライン」を自動化することで、プロンプトから動作確認済みアプリまでのサイクルを60秒以下に圧縮している点——開発フィードバックループの極限短縮
- GeminiのLong-context能力を活用してフレームワーク全体のソースコードとテンプレートをコンテキストウィンドウに収め、外部ツール呼び出しなしでアーキテクチャ整合性を維持している設計——RAGを使わずコンテキスト直接注入で解決する判断

## Yujiの取り組みへの示唆

監査エージェント開発において、Vibe Coding XRの「ドメイン固有システムプロンプト＋コードテンプレートのコンテキスト注入」手法は直接応用可能である。LangGraphのノード定義やPydanticスキーマをシステムプロンプトに埋め込むことで、監査ワークフロー生成エージェントのハルシネーション抑制と有効なAPI呼び出しの保証が期待できる。また、60秒以内でプロトタイプを生成するラピッドバリデーションの思想は、監査手続きの自動設計エージェントをテストする際の「仮説→即実装→即検証」サイクルの設計指針として参考になる。

## 原文リンク

[Vibe Coding XR：XR BlocksとGeminiによるAI+XRプロトタイピングの高速化](https://research.google/blog/vibe-coding-xr-accelerating-ai-xr-prototyping-with-xr-blocks-and-gemini/)
