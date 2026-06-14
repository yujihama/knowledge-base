---
title: "多層プロンプトスキーマ（Hierarchical Prompt Schema）：LLMのルール矛盾をMermaid構造化で自動検出・解消する設計"
url: "https://zenn.dev/yoshi_katakura/articles/3b1952f0096a64"
date: 2026-06-14
tags: [HierarchicalPromptSchema, プロンプト設計, ConflictDetector, Mermaid, tool_use, Claude, マルチエージェント, Pydantic, 構造化出力]
category: "agent-arch"
related: [7797, 4475, 2254, 6359, 4330]
memo: "[Zenn LLM] 多層プロンプトスキーマ（Hierarchical Prompt Schema）"
processed_at: "2026-06-14T09:02:56.581389"
---

## 要約

LLMのシステムプロンプトは自然言語で記述されるため、複数のルールが矛盾してもコンパイルエラーが発生しない。本記事では、Soul-Twinプロジェクトで実装したHierarchical Prompt Schema（HPS）を解説する。実際の障害事例として、議長AIが指名禁止対象の副議長を26回連続で誤指名した問題が紹介されており、これはフラットなプロンプト構造においてLLMが矛盾するルールを独自解釈した結果である。

HPSは5層の優先度スキーマで構成される。Layer 1（絶対原則・最高優先度・変更不可）、Layer 2（Societyルール・起床・食事等のデフォルト）、Layer 3（役割・文脈）、Layer 4（フォーマット規則・字数・言語等）、Layer 5（個人ペルソナ・最も具体的）の順で、Layer 5が上位を上書き可能な継承構造を持つ。

実装面では、ConflictDetectorがClaude Haiku（claude-haiku-4-5-20251001）のtool_use機能を使って矛盾を構造化出力で検出する。矛盾の種類はdirect・conditional・role・implicit・temporalに分類され、severityはcritical・high・medium・lowの4段階で評価される。さらにSchemaConflictDetectorがスキーマ全体の矛盾を「HARD CONFLICT（修正必須）」と「EXPECTED OVERRIDE（正常な上書き）」に分類する。

最大の技術的特徴は、自然言語の代わりにMermaid図でルールをLLMに渡す点である。Geminiの指摘を踏まえ、Mermaid・LaTeX等の構造化表記の方がLLMには明瞭とし、解釈フェーズ→実行フェーズの2段階処理を強制する設計を採用した。比較テストでは、自然言語プロンプトと比較してMermaidスキーマは平均入力トークンが6,041から3,144へ約48%削減され、副議長誤指名が2件から0件に改善し、最終ターンの〔結論〕遵守は4/4を維持した。トークン削減は予想外の発見であり、構造化表記の方がLLMの処理効率が高いことを示唆する。

個々のプロンプトを超えてTWIN Societyのガバナンス階層にも拡張されており、society_rules.yamlでデフォルトルールを定義し、英語TWINのようにsociety_profileでhps_overridesキーを通じて言語等を上書きする仕組みも実装されている。全実装はSoul-Twin GitHubのbackend/app/prompt/以下に公開されており、UT94件全PASS・Claude Haikuでの統合テスト6/6 PASSを達成している。監査エージェント開発においては、複数エージェントが異なる権限・役割を持つ場合の優先度制御や矛盾検出に直接応用可能な設計パターンである。

## アイデア

- 自然言語プロンプトをMermaid図に変換してLLMに渡すことで、トークン数を約48%削減しつつルール遵守率を改善できる——構造化表記がLLMの内部処理に与える影響の実証
- LLMのtool_use機能をプロンプト矛盾の自動検出器として使う逆用的アプローチ：Claude自身が別のプロンプトの矛盾をcritical/high/medium/lowで構造化評価する
- EXPECTED_OVERRIDEとHARD CONFLICTを区別することで、意図的な上書き（英語TWINが日本語デフォルトを上書き）と真のバグを分離できる設計の明快さ

## 前提知識

- **Claude tool_use** (TODO: 読むべき)
- **Pydantic BaseModel** (TODO: 読むべき)
- **システムプロンプト設計** → /deep_5212 教育のライフサイクルを支えるAIエージェント入門：学校現場での設定から活用まで
- **Mermaid記法** (TODO: 読むべき)
- **マルチエージェント制御** (TODO: 読むべき)

## 関連記事

- /deep_7797 思考整理アプリを作る：LLMコスト設計からFlutter CustomPainterまでの技術全記録
- /deep_4475 採点基準v2改訂で「直感力9点」が認定された——LLM個人アセスメントプロンプト設計の実践記録
- /deep_2254 同僚の「細かすぎた」が機能になった──Cladeが育つ仕組み【v1.15.0】
- /deep_6359 仕様書に埋もれた「決まっていない意思決定」を、マルチエージェントで炙り出す
- /deep_4330 ブレインフライを抜けた先の景色 — 見えてきた1000時間の壁

## 原文リンク

[多層プロンプトスキーマ（Hierarchical Prompt Schema）：LLMのルール矛盾をMermaid構造化で自動検出・解消する設計](https://zenn.dev/yoshi_katakura/articles/3b1952f0096a64)
