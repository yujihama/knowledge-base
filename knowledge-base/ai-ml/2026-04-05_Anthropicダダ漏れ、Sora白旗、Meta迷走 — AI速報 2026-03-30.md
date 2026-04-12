---
title: "Anthropicダダ漏れ、Sora白旗、Meta迷走 — AI速報 2026-03-30"
url: "https://zenn.dev/yokoi_ai/articles/ai-general-daily-2026-03-30"
date: 2026-04-05
tags: [Claude-Mythos, Capybara, GPT-5.3-Codex, Sora, Llama, MCP, CVE, Agentic-Storefronts, Mistral-Small-4, Gemini]
category: "ai-ml"
memo: "[Zenn 機械学習] Anthropicダダ漏れ、Sora白旗、Meta迷走 — AI速報 2026-03-30"
related: [868, 826, 892, 430, 861]
processed_at: "2026-04-05T09:00:36.284466"
---

## 要約

2026年3月最終週のAI業界主要動向をまとめた記事。①Anthropicの未発表モデル「Claude Mythos/Capybara」のブログ原稿が未保護データストアから漏洩。Opusの上位ティアに位置し、コーディング・学術推論・サイバーセキュリティで「劇的に高いスコア」と記載。Anthropic自身が「前例のないサイバーセキュリティリスク」と警告するレベルの能力を持つとされ、Opus 4.6がFirefoxの脆弱性を2週間で22件発見した実績の上位モデルとされる。②OpenAIがSora公開APIを30日猶予で廃止。理由は「動画生成のスケール化は経済的に持続不可能」と公式表明。テキスト・コード生成と異なり動画生成は計算コストが桁違いに重く、収益化が困難と判断。③MetaのLlama後継「Avocado」が性能問題で5月以降に延期。内部テストでGemini 2.5〜3.0相当に留まり、論理推論・コーディング・エージェント性能で劣後。暫定措置としてGoogle Geminiのライセンス取得を検討中との報道。1,350億ドルのAI投資にもかかわらず自社モデルが競合に追いつけない状況。④OpenAIがGPT-5.3-Codexを全プラットフォーム展開。Codexアプリ・CLI・IDE拡張・Codex Cloudで利用可能。GPT-5汎用スタックとCodex専用スタックを統合し、週間アクティブユーザーは200万超・年初比5倍。PythonツールチェーンのAstral（uv/Ruff/ty）も買収しCodexチームに統合。⑤ShopifyがChatGPT・Google AI Mode・Microsoft Copilot・Gemini内での直接販売を「Agentic Storefronts」として実装。⑥Palo Alto Networks Unit 42がMCP（Model Context Protocol）実装の攻撃経路を文書化。60日間で30件のCVEが登録され、ツール呼び出し機構そのものが攻撃面になることを示した。⑦小ネタとして、Mistral Small 4（22B、Apache 2.0）、Anthropic Institute設立、Gemini 3.1 ProがAI Intelligence Index首位タイ（57点）など。

## アイデア

- MCPに60日間で30件のCVEが登録されたという事実は、エージェントのツール呼び出し機構が攻撃面になるという構造的問題を示しており、エージェント設計においてMCP経由のツール実行を信頼境界としてどう扱うかの設計原則が急務になっている
- OpenAIのSora API廃止は『スケール可能なAIサービス』の経済合理性に限界があることを公式に認めた事例であり、コスト構造を無視したサービス設計の危うさを示す具体的な失敗例として参照価値が高い
- Metaが自社LlamaシリーズでなくGoogle Geminiのライセンス取得を検討するという報道は、1,350億ドル規模の投資でも差別化できないフロンティアモデル開発の集中化を示しており、オープンソース戦略の転換点として業界構造上の重要な変化点となりうる
## 関連記事

- /deep_868 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：完全要因計画クロスバックエンド手法
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_892 重み空間モデルマージによる大規模言語モデルの壊滅的忘却対策と指示追従能力の改善
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力

## 原文リンク

[Anthropicダダ漏れ、Sora白旗、Meta迷走 — AI速報 2026-03-30](https://zenn.dev/yokoi_ai/articles/ai-general-daily-2026-03-30)
