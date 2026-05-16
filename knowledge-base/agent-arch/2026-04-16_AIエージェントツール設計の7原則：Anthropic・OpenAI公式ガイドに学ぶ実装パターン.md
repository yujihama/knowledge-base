---
title: "AIエージェントツール設計の7原則：Anthropic・OpenAI公式ガイドに学ぶ実装パターン"
url: "https://zenn.dev/0h_n0/articles/c1f033224797db"
date: 2026-04-16
tags: [ツール設計, ACI, 冪等性, Poka-yoke, Tool Search Tool, strict mode, Function Calling, MCP, LLMエージェント]
category: "agent-arch"
related: [1475, 12, 430, 88, 1784]
memo: "[Zenn LLM] AIエージェントツール設計の7原則：Anthropic・OpenAI公式ガイドに学ぶ実装パターン"
processed_at: "2026-04-16T12:46:33.974231"
---

## 要約

AnthropicとOpenAIの公式ドキュメントをもとに、AIエージェントのツール設計における7つの原則を体系化した実装ガイド。Anthropicは「SWE-benchエージェント構築においてプロンプト全体よりツール設計に多くの時間を費やした」と報告しており、ツール設計がエージェントの信頼性を左右する最重要要素として位置づけている。

7原則の概要：①単一責任（Atomicity）：1ツール1機能を徹底し、「God Tool」を避ける。Gemini ADK公式ガイドによれば、単一責任化によりバリデーションエラーのカテゴリ全体を排除できる。②冪等性（Idempotency）：idempotency_keyを用いてリトライ時の副作用重複（二重課金等）を防止する。③セマンティック明確性（Documentation as Code）：docstringをLLMへの指示書として設計し「USE THIS TOOL / DO NOT USE」を明記する。Tool Use Examplesを1〜5個追加するとパラメータ精度が72%→90%に向上（Anthropic内部テスト）。④スキーマ制約（Schema Enforcement）：OpenAIのstrict modeを常時有効化し、enumによる選択肢制限、フラット構造、additionalProperties:falseを徹底する。⑤エラー防止設計（Poka-yoke）：相対パスを絶対パスに変更するといった構造的制約でモデルの誤りを排除する。エラーメッセージには「次にLLMが取るべきアクション」を含め自己修正ループを促進する。⑥コンポーザビリティ（Composability）：ツール間でID体系・データ形式を統一し、あるツールの出力が別ツールの入力として自然に使える設計にする。⑦動的ツール管理（Tool Search Tool）：ツール数増加時のコンテキスト肥大化問題に対し、Anthropicの「Tool Search Tool」や自作のベクトル検索で必要なツールを動的に取得する。コンテキスト使用量85%削減、トークン消費37%削減の効果が報告されている（Anthropic公式）。

ACIという概念も重要：Anthropicはエージェントとツールの接点を「Agent-Computer Interface（ACI）」と命名し、人間向けUIと同等の設計配慮が必要と述べている。モデルに親和的なフォーマット、最小限のオーバーヘッド、推論のための余白確保が設計指針となる。監査エージェント開発への示唆として、LangGraphでReActループを構成する際のツール設計にこれらの原則を適用することで、ツール選択ミスや不正なパラメータ生成を構造的に抑制できる。特にPoka-yoke設計とエラーメッセージの指示的な記述は、長い推論ループでの自己修正能力を高める。

## アイデア

- ツールのdocstringを「人間向けドキュメント」ではなく「LLMへの指示書」として設計するという視点の転換：USE THIS TOOL / DO NOT USEパターンにより、類似ツール間の選択精度を構造的に向上させる
- Poka-yoke（ポカヨケ）の概念をAIツール設計に転用：相対パス→絶対パスへの変更1つで成功率が大幅改善したというAnthropicの事例は、モデルの確率的挙動を設計で補う発想として監査ログ検索ツール等にも直接応用できる
- 10ツール超はTool Search Toolで動的管理するという閾値設計：コンテキスト85%削減という数値とともに、ツール数を制限するアーキテクチャ判断基準が明示されており、大規模エージェントシステムのスケーリング戦略として実用的

## 前提知識

- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **JSON Schema** (TODO: 読むべき)
- **冪等性** (TODO: 読むべき)
- **LangGraph / ReAct** (TODO: 読むべき)
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える

## 関連記事

- /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[AIエージェントツール設計の7原則：Anthropic・OpenAI公式ガイドに学ぶ実装パターン](https://zenn.dev/0h_n0/articles/c1f033224797db)
