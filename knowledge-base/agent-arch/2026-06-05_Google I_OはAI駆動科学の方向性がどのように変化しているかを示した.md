---
title: "Google I/OはAI駆動科学の方向性がどのように変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-05
tags: [Gemini for Science, AlphaFold, Co-Scientist, AlphaEvolve, WeatherNext, 自律型科学エージェント, recursive self-improvement, LLM-as-researcher]
category: "agent-arch"
related: [6783, 6370, 6733, 6435, 6510]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-05T21:15:11.813577"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEOのDemis Hassabisが「特化型AIツール」から「汎用エージェント型AI科学者」への移行を示唆する発言を行った。具体的には、気象予測ソフトウェアWeatherNextがハリケーン・メリッサのジャマイカ上陸を事前警告した実績を紹介しつつも、焦点は今後のエージェント型AIによる自律的な研究実行にあることが明確になった。

これまでGoogleはAlphaFold（タンパク質構造予測、Nobelprise受賞）、AlphaGenome（遺伝学）、AlphaEarth Foundations（地球科学）などの高度に特化したモデルを開発してきた。AlphaFoldは世界300万人超の研究者に利用されており、関連技術を活用するIsomorphic Labsは20億ドルのシリーズB資金調達を完了している。しかし、AlphaFoldの共同開発者でNobel賞受賞者のJohn JumperがAIコーディング部門に異動したことは、リソース再配置の具体的なシグナルとして注目される。

新発表の「Gemini for Science」パッケージは、仮説生成AIであるCo-Scientistとアルゴリズムhypothesisをコードとして最適化するAlphaEvolveを統合したLLMベースの科学研究支援スイートであり、研究者向けのアクセス申請受付が開始された。スタンフォードの遺伝学者Gary PeltzはCo-Scientistを「デルフォイの神託への相談」と評するなど、初期テスト参加者の評価は高い。

同時期にOpenAIは汎用推論モデル（GPT-5.5系）が数学的予想の反証に成功したと発表。これは数学者から「生成AIの数学への最も意義深い貢献」と評価されており、特化型でない汎用エージェントが独立した研究貢献を行い始めた事実を裏付ける。

Hassabisは「今後10年はAIを科学者を支援するツールと捉えるべき」と述べつつ、その先では「協調者」になり得ると示唆。コーディング能力が自律型科学エージェントの成功に直結するという認識のもと、GoogleはAIコーディング競争（Anthropic・OpenAI対比での劣位を意識）も念頭に置きながら、エージェント型科学AIへの軸足移動を進めている。監査エージェント開発の観点では、Co-ScientistやAlphaEvolveのような「仮説生成→検証→最適化」のループを持つ自律型エージェントアーキテクチャが、監査手続きの自動設計や異常仮説の生成タスクに応用できる可能性が示唆される。

## アイデア

- 特化型AIツール（AlphaFold等）から汎用LLMエージェントへのリソース移行が、Nobel賞受賞者の人事異動という具体的事実で裏付けられている点は、業界トレンドを読む上での重要なシグナル
- OpenAIの汎用推論モデルが数学的予想を反証したという事例は、特化型モデル不要論を補強するものであり、LLM-as-judgeやLLM-as-researcherという概念が実証フェーズに入りつつあることを示す
- Co-ScientistとAlphaEvolveの「仮説生成→アルゴリズム最適化」のアーキテクチャは、監査エージェントにおける「リスク仮説生成→検証手続き設計」のループに直接応用可能な設計パターンとして参照できる

## 前提知識

- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **マルチエージェントアーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_6783 Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6510 Google I/Oが示したAI駆動科学の転換：特化型ツールから汎用エージェントへ

## 原文リンク

[Google I/OはAI駆動科学の方向性がどのように変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
