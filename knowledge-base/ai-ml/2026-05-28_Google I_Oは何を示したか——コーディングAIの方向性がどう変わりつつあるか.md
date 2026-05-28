---
title: "Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-28
tags: [Google I/O, Gemini, Claude Code, AlphaFold, AlphaEvolve, AI coding, AI for science, DeepMind, agentic coding, Antigravity]
category: "ai-ml"
related: [6455, 3460, 3360, 3493, 3535]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-28T09:21:30.724038"
---

## 要約

MIT Technology Reviewの記事（2026年5月18日付）は、Google I/O 2026直前の状況を分析したもの。記事の核心は、基盤モデル競争においてGoogleが「明確な3位」に転落しているという評価だ。

【コーディング能力の後退】2025年3月のGemini 2.5 Pro登場時点ではトップ層の差は主観的な範囲だったが、現在はAnthropicのClaude CodeとOpenAIのCodexがGoogleのツールを「劇的に」上回っているとされる。事態の深刻さを示す指標として、DeepMindの一部エンジニアが社内ツールではなくClaude Codeの利用を余儀なくされているとThe Informationが報じた。対応策として、DeepMindに新たなAIコーディングチームが設置され、2024年ノーベル化学賞受賞者（AlphaFoldへの貢献）のJohn Jumperがそのチームに加わったと報告されている。I/Oではアジェンティックコーディングプラットフォーム「Antigravity」のアップデートが発表される可能性があるが、筆者は「劇的な変化は期待できない」と評価している。

【科学・ヘルスケア領域での強み】コーディングとは対照的に、科学AI分野ではGoogleが依然としてリードを保つ。2025年にはAI co-scientist（仮説立案・研究計画生成）とAlphaEvolve（数学・計算問題の反復的解探索）を公開済みで、スタンフォードの科学者からは「oracle」と呼ばれるほどの評価を得ている。医療AIについては、AI-powered Health Coachを一般公開する予定だが、フィットネス・ダイエット相談が主目的で、医療的判断への対応はOpenAIのChatGPT Health（2025年1月リリース）より保守的な設計とみられる。

【業界の力学と政治的文脈】同時期にオークランドで開催中のElon Musk対Sam Altman裁判、AnthropicとOpenAIの米国防総省（DoD）契約交渉、Google従業員600名（多数がDeepMind所属）によるDoD契約への抗議書簡など、AIのガバナンスと軍事利用に関する緊張が業界全体に広がっている。Googleはその翌日にDoD契約に署名しており、Demis Hassabisは「Nobel賞を持つ研究者」という中立的なイメージを維持しようとしているが、コントロバーシーを完全に回避するのは困難な状況にある。

【監査エージェント開発への示唆】Claude CodeがDeepMindエンジニアに選ばれた事実は、コーディングエージェントの品質が実務採用の決定的基準になっていることを示す。監査エージェント開発においても、LangGraphやReActベースのシステムを補完するコーディング支援ツールの選定では、ベンチマークより実使用でのアウトプット品質を優先すべきである。

## アイデア

- コーディング能力が基盤モデルの評判を決定する主要指標になっており、DeepMindエンジニア自身が社内ツールより競合（Claude Code）を選んだという事実は、エージェント型コーディングシステムの実用品質格差が公式ベンチマーク以上に大きいことを示唆する
- John JumperのようなAlphaFold由来のタンパク質構造解析の専門家がコーディングAIチームに投入されているのは、科学的推論能力とコード生成能力の統合が次世代AIエージェントの競争軸になりつつあることを示す
- AI co-scientistとAlphaEvolveはいずれも反復的仮説検証ループを持つシステムであり、監査エージェントにおける「証拠収集→仮説生成→検証」サイクルの設計に直接応用できるアーキテクチャパターンを提示している

## 前提知識

- **Gemini 2.5 Pro** (TODO: 読むべき)
- **Claude Code / Codex** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **agentic coding** → /deep_191 Generative UI: あらゆるプロンプトに対応するリッチでカスタムなビジュアル・インタラクティブUX
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_6455 Google I/OはAI駆動科学の方向性がいかに変化しているかを示した
- /deep_3460 人工科学者：AIが科学研究を自律的に推進する時代へ
- /deep_3360 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_3493 人工科学者：AIが科学研究を自律実行する時代へ——現状と課題
- /deep_3535 人工科学者：AIが科学研究をどう変えるか——マルチエージェント・自律研究システムの現状

## 原文リンク

[Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
