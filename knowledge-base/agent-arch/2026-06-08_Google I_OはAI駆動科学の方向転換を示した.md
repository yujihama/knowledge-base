---
title: "Google I/OはAI駆動科学の方向転換を示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-08
tags: [Gemini for Science, AlphaFold, WeatherNext, AI Co-Scientist, AlphaEvolve, recursive self-improvement, agentic AI, 科学AI]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-08T09:18:55.817134"
---

## 要約

2026年のGoogle I/OキーノートでDeepMind CEO Demis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言が行われた文脈は、天気予報AI「WeatherNext」がジャマイカに上陸したハリケーン・メリッサの事前警告を発し、人命救助に貢献したという実績の紹介だった。この対比が、現在のAI科学の二つのアプローチの緊張関係を象徴している。

第一のアプローチは、AlphaFoldやWeatherNextのような特定科学問題に特化した専用ツールの開発だ。AlphaFoldはタンパク質構造予測でノーベル賞を受賞し、現在3,000万人以上の研究者に利用されている。関連会社Isomorphic Labsは新薬開発を目指し、直近で20億ドルのシリーズB資金調達を完了した。AlphaGenome（遺伝学）やAlphaEarth Foundations（地球科学）も昨夏リリースされており、特化型ツールの研究者需要は依然として高い。

第二のアプローチは、汎用LLMベースの自律的エージェントが科学研究を実行するビジョンだ。GoogleはGemini for Scienceパッケージを発表し、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」を統合。研究者が申請ベースでアクセス可能になった。スタンフォードの遺伝学者Gary PeltzはNature Medicine誌でCo-Scientistを「デルフォイの神託に相談するようだ」と表現した。同週、OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学予想を反証したと発表し、特化型ではない汎用エージェントが数学研究に独立した貢献を行えることを示した。

資源配分の変化も顕著だ。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門に異動したとLAタイムスが報道。これはAnthropicやOpenAIとのコーディングツール競争への対応でもあるが、コーディング能力がエージェント科学の基盤であることから、エージェント化への戦略的転換とも読める。

Hassabisは「今後10年はAIを科学者を助ける道具として考えるべきだ。その先はコラボレーターになるかもしれない」と述べ、「AI Co-Scientist」という命名（AI Scientistではなく）も人間中心のフレーミングを示している。ただし、真の科学的コラボレーターになるには独立した科学的能力が必要であり、シンギュラリティへの道程でAIが人間を超える科学者になる可能性も排除されていない。

監査エージェント開発への示唆：汎用推論モデルが専門分野（数学・科学）で特化型モデルなしに独立した知的貢献をし始めた事実は、監査エージェントにおいても特化型ファインチューニングより汎用LLM＋ReActループの組み合わせが有望であることを示す。AlphaEvolveのアルゴリズム自動最適化の手法は、監査ルールエンジンの自動改善に応用できる可能性がある。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学予想を反証した事例は、特化型モデルなしに一般エージェントが専門的知的貢献を行える転換点を示す
- AlphaEvolveのアルゴリズム自動最適化アプローチは、コード・ルール・戦略の自己改善ループを持つエージェントシステムの設計に直接応用可能
- GoogleがCo-Scientistの命名でAI Scientistを避けた意図的フレーミングは、AI能力が人間を超えることへの社会的受容コントロール戦略として注目に値する

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/OはAI駆動科学の方向転換を示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
