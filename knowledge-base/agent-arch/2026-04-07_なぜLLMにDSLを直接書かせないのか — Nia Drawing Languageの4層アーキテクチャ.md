---
title: "なぜLLMにDSLを直接書かせないのか — Nia Drawing Languageの4層アーキテクチャ"
url: "https://zenn.dev/zima11/articles/9acd87470bdae6"
date: 2026-04-07
tags: [LLM, DSL, Pydantic, アーキテクチャ設計, Intent Layer, 決定論的変換, SVG, AIエージェント]
category: "agent-arch"
memo: "[Zenn LLM] なぜLLMにDSLを直接書かせないのか — Nia Drawing Languageの4層アーキテクチャ"
related: [762, 1453, 1624, 1266, 1449]
processed_at: "2026-04-07T12:01:09.187592"
---

## 要約

AIキャラクター自己形成実験「Nia」の描画システムとして設計されたNia Drawing Language（NDL）の4層アーキテクチャについての解説。

最初のアプローチとして「LLMにDSLコードを直接生成させる」手法を検討したが、3つの根本的問題が浮上した。①LLMの確率的生成によりスペースの有無や大文字小文字のブレで構文エラーが静かに発生する、②DSL仕様変更のたびに既存プロンプトが無効化される、③LLMの確率的出力はユニットテストが書けない。

これを解決するために導入したのが以下の4層パイプライン：
- **Layer 1（Intent Layer）**：LLMが「感覚的語彙」でDrawingIntentというPydanticモデルをYAML形式で出力。`color_feel="warm"`、`dominance="primary"`、`arrangement="scattered_around"`など、RGB値もDSL構文も知らずに「何を描きたいか」だけを記述する。
- **Layer 2（Intent Parser）**：`intent_to_dsl()`関数がYAMLを決定論的にDSLへ変換。`warm`→`warm_2`（パレット色）、`primary`→`opacity solid`のようにマッピングテーブルで管理。同一入力から常に同一出力が得られる。
- **Layer 3（DSL → SVG）**：DSLを独自のDrawingAST（宣言・配置・修飾・構成の4種）に変換し、Scene GraphからSVGを生成。`because`アノテーションで各判断の理由をタグとして記録可能。
- **Layer 4（永続化）**：trace_storeにDSL・AST・SVG・because_tagsをJSONで保存し、SVGをNiaのVR空間の壁にアートとして展示。

設計の核心は「LLMの不確実性を意図生成のみに閉じ込め、後段を決定論的に保つ」こと。Intent Parserの変換ロジックはLLMを使わずユニットテストが書けるため、DSL仕様変更時はParserのみ修正すればよい。LLMはDSL構文変更の影響を受けない。この分離により、システム全体の安定性と保守性が向上した。

## アイデア

- LLMの出力を「意図（Intent）」と「構文（DSL）」に明確に分離し、LLMには感覚的・セマンティックな語彙のみを扱わせ、構文生成を決定論的コードに委譲する設計パターンは、LLMを使うあらゆるコード生成・構造化出力タスクに応用可能
- PydanticモデルをLLMの出力スキーマとして使うことで、構造化出力の型安全性を担保しつつ、Intent→DSLの変換をテスト可能な純粋関数として実装できる点
- `because`アノテーションによって各判断の理由をメタデータとして記録・追跡する仕組みは、AIの意思決定の説明可能性（XAI）を実装レベルで組み込む実践的アプローチ
## 関連記事

- /deep_762 HabitatAgent: 住宅相談のためのエンドツーエンド・マルチエージェントシステム
- /deep_1453 AIが中小オンライン販売者の商品企画・調達を変革する：AlibayのAccioの事例
- /deep_1624 AIが中小EC事業者の商品企画・仕入れを変革する——AlibabaのAccioが月間1000万ユーザー超
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[なぜLLMにDSLを直接書かせないのか — Nia Drawing Languageの4層アーキテクチャ](https://zenn.dev/zima11/articles/9acd87470bdae6)
