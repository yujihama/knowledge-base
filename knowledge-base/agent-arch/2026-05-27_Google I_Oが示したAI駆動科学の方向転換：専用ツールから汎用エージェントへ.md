---
title: "Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-27
tags: [Google DeepMind, Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 汎用エージェント, 科学AI, recursive self-improvement, OpenAI]
category: "agent-arch"
related: [6461, 6370, 6585, 3430, 6435]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-27T09:16:21.659513"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言の文脈は科学AIセッションであり、ハリケーン・メリッサの上陸を事前予測して人命救助に貢献した気象予測ソフト「WeatherNext」の紹介と組み合わさることで、AI科学の2つのアプローチ間の緊張が浮き彫りになった。

第1のアプローチは、特定の科学的問題を解くために設計・訓練された専用ツール（WeatherNext、AlphaFold、AlphaGenome、AlphaEarth Foundationsなど）。第2は、LLMベースの汎用エージェントシステムが人間の関与なしに最先端研究を実行するというビジョンである。

Googleは専用ツール開発を完全に放棄したわけではない。AlphaFoldはノーベル賞を獲得し、現在300万人以上の研究者が利用。Isomorphic Labsは20億ドルのシリーズB調達に成功している。しかし方向転換の兆候も明確だ。AlphaFold共同開発者でノーベル賞受賞者のJohn Jumperは現在、科学特化ツールではなくAIコーディング分野で作業しているとLA Timesが報道。コーディング能力はAnthropicやOpenAIに後れを取っているという競争上の理由もあるが、エージェント型科学AIへの優先転換の意味合いも持つ。

今回発表された「Gemini for Science」パッケージは、仮説生成AI「Co-Scientist」やアルゴリズム最適化「AlphaEvolve」など複数のLLMベース科学システムを統合。研究者はアクセス申請が可能になった。Co-Scientistについてスタンフォード大学の遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」と評した。

同週、OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学予想を反証したと発表。数学者の間では生成AIが数学に与えた最も重要な貢献とされる。専用モデルでなく汎用エージェントが独立した研究貢献を行えるなら、科学全般への応用も視野に入る（ただし科学では実験的検証が必要なため難易度は高い）。

Googleはエージェントを人間科学者の「補助者」として位置づけており、名称を「AI Scientist」ではなく「AI Co-Scientist」としているのは意図的とみられる。Hassabisは「今後10年はAIを科学者を助ける道具として考えるべき。その先は不確実だが、協力者に近い存在になるかもしれない」と述べている。

監査エージェント開発への示唆：科学分野でのエージェント化と同様に、監査領域でも「特定の監査手続き専用ツール」から「汎用推論エージェントによる自律的な監査計画・実行」へのシフトが中長期的に予想される。Co-ScientistのようなLLMベース仮説生成能力は、リスク評価や不正パターン発見に転用可能な設計思想を持つ。

## アイデア

- 専用科学AIツール（AlphaFold等）と汎用LLMエージェントの性能収束点：AlphaFoldなしにはタンパク質構造予測ができないエージェントが、いつ専用ツールを不要にするかという問いは、監査AIにおける「特化型ルール検出エンジン vs. 汎用推論エージェント」の設計判断にも直結する
- ノーベル賞受賞者John Jumperのコーディング分野への配置転換は、汎用コード生成能力がドメイン特化科学AIより戦略的優先度が高いという判断を示しており、「コード生成＝科学エージェントの基盤能力」という考え方が業界標準になりつつある
- OpenAIの汎用推論モデルが数学予想を反証したことで、「専門訓練なしでも独立した知的貢献が可能」という前例が生まれた。これはLLM-as-judgeやReActベースのエージェントが監査判断を下す際の正当性議論に影響する

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性

## 原文リンク

[Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
