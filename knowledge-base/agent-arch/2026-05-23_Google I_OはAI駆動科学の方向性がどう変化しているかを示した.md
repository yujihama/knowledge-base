---
title: "Google I/OはAI駆動科学の方向性がどう変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-23
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律科学エージェント, 汎用推論モデル, recursive self-improvement]
category: "agent-arch"
related: [6370, 6140, 6170, 6049, 5984]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-23T21:00:37.350002"
---

## 要約

2026年5月のGoogle I/OでDeepMind CEO Demis Hassabisは「特異点の麓に立っている」と宣言した。その文脈は科学向けAIの二つのアプローチの対比にある。一つは特化型AIツール（WeatherNext、AlphaFold、AlphaGenome等）、もう一つはLLMベースの汎用エージェントが自律的に研究を実行するアプローチだ。WeatherNextは2025年のハリケーン・メリッサ（ジャマイカに壊滅的上陸）に対し事前警報を発し、人命救助に貢献した実績ある特化ツールだが、Hassabisはその発表の場でも「特異点」という大きな言葉を使った。Googleが発表したGemini for Scienceパッケージは、LLMベースの仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を統合したもので、研究者は現在アクセス申請可能。Co-Scientistは早期テスト参加者のスタンフォード遺伝学者Gary Peltzに「デルフォイの神託に相談するようだ」と評された。一方、業界全体でもエージェント型研究の進展が顕著で、OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表した。これは数学者らから生成AIによる数学への最も意味ある貢献と評価されている。リソース配分の変化も見られ、AlphaFoldでノーベル賞を受賞したGoogle fellowのJohn JumperがAIコーディング分野に移行したことが報じられており、コーディング能力がエージェント科学システムの核心能力であることを踏まえると、汎用エージェント科学への戦略的シフトを示唆する。AlphaFoldはなお300万人以上の研究者が利用し、関連会社Isomorphic Labsは20億ドルのシリーズB調達を完了しており特化ツールの廃棄ではない。ただしエージェントシステムは必要に応じてAlphaFold等の特化ツールを呼び出す設計が可能で、両者は排他的ではない。監査エージェント開発の観点では、「汎用推論モデルが専門外のドメインで独立した研究貢献をする」という実績が重要で、特化ファインチューニングなしにReActや推論能力だけで専門的アウトプットを出せる可能性を示している。また、AI Co-Scientistという命名に見られるように「補助者」ポジショニングを取りながら実質的な自律性を高めるロードマップは、監査AIの社会的受容設計の参考になる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が特化訓練なしで数学的予想を反証したことは、特化ファインチューニングvs汎用推論の設計論争に対する実証的なデータ点になる
- エージェントシステムが必要に応じてAlphaFold等の特化ツールをツールコールする設計は、監査エージェントが会計基準DBや規制検索APIを呼び出すアーキテクチャと同型であり、構造的示唆がある
- 科学分野では実験による検証が必要なため数学よりAIの自律貢献が難しいという指摘は、監査でも帳票・証跡という物理的検証が残る点と並行しており、AIが補完できる範囲の境界論として参考になる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **recursive self-improvement** (TODO: 読むべき)
- **ツールコール** → /deep_1243 Claude Codeが「バカになった」は気のせいじゃない — 23万ツールコールが示す品質低下の正体

## 関連記事

- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6140 Google I/O 2026のAI発表を読むエンジニア・研究視点
- /deep_6170 Google I/O 2026に向けた期待：コーディングAIの挽回、科学AI、業界ドラマ
- /deep_6049 Google I/O 2026で注目すべき3つのポイント：コーディングAIの巻き返しと科学AI
- /deep_5984 Google I/O 2026で何を期待するか：コーディングAIでの巻き返しと科学AIの強み

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
