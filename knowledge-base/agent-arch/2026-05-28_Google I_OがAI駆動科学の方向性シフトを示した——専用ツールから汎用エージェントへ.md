---
title: "Google I/OがAI駆動科学の方向性シフトを示した——専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-28
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, 汎用推論モデル, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-28T21:12:40.535241"
---

## 要約

Google I/OのキーノートでDeepMind CEOのDemis Hassabisは「特異点の麓に立っている」と表明した。この発言の文脈は天気予報ソフト「WeatherNext」によるハリケーン・メリッサの早期警報事例であり、専用AIツールの実績と汎用エージェント型AIへの熱狂との間の緊張関係を象徴している。

現在のAI科学アプローチは2つの流れに分かれる。第1は、AlphaFoldやWeatherNextのような特定科学問題に特化した専用ツール。AlphaFoldはタンパク質構造予測で世界300万人以上の研究者に利用され、関連技術を展開するIsomorphic Labsは20億ドルのシリーズB資金調達を完了した。第2は、LLMベースの汎用エージェントシステムで、最小限の人間関与で研究プロジェクトを自律実行できることを目指す。

Googleは後者への傾斜を明確にしつつある。Google I/Oでの主要発表は「Gemini for Science」パッケージで、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」をLLMベースの科学システム群として統合。現在は研究者が申請制でアクセス可能。スタンフォードの遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」とCo-Scientistを評価した。

リソース配分にも変化の兆候がある。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門に異動したと報じられた。これはAnthropicやOpenAIに対するコーディングツールの競争力強化が主因とも見られるが、コーディング能力がエージェント型科学システムの根幹であることから、エージェント科学へのシフトとも解釈できる。

OpenAIも今週、汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表。数学者の間でも生成AIの数学への最も重大な貢献と評価されており、専用化なしの汎用エージェントが独立した研究貢献を行い始めている証左とされる。

Hassabisは「今後10年はAIを科学者を助けるツールとして捉えるべき」と述べつつ、その先では「コラボレーター」になり得るとも示唆。Gemini for Scienceは専用ツールを排除するのではなく、エージェントが必要に応じてAlphaFold等を呼び出す設計であり、両者は共存する。ただしpublic imagingおよびリソース配分の重心は、特化型ツール開発から自律エージェント型科学へと移行しつつある。

監査エージェント開発への示唆：LLMベース汎用エージェントが専門領域（数学・科学）で独立した研究貢献を始めているという事実は、監査AI分野においてもReActやLangGraphによる自律的な証拠収集・リスク仮説生成エージェントの実用化水準が近づきつつあることを示唆する。Co-Scientistのような「仮説生成→検証」ループ設計は、監査における「リスク仮説→手続設計」フローと構造的に類似しており、参照価値が高い。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専用化なしに数学的予想を反証した事実は、ドメイン特化ファインチューニングなしで高度な知識労働が可能になるという設計思想の転換点を示す
- Co-Scientistの「仮説生成→検証」ループ設計は監査エージェントの「リスク仮説→監査手続設計→証拠評価」フローに直接応用できる構造的アナロジーを持つ
- John Jumperのコーディング部門異動が示すように、コーディング能力の強化はエージェント型科学システムの根幹インフラであり、コード生成精度がエージェント科学の性能上限を規定するという認識が業界に定着しつつある

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/OがAI駆動科学の方向性シフトを示した——専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
