---
title: "Google I/Oが示すAI駆動科学の方向転換：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-05
tags: [Google DeepMind, Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-05T09:33:46.692535"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言の文脈となったのは、科学分野におけるAIの役割変化だ。

Google I/Oの科学AIセクションの目玉は、気象予測ソフトウェア「WeatherNext」がジャマイカに上陸したハリケーン・メリッサの事前警告を提供し、人命救助に貢献したという事例だった。しかしHassabisの示す将来像は、こうした専用ツールの延長線上にはない。

現在のAI科学アプローチは二極化している。第一は、AlphaFold（タンパク質構造予測、世界300万人以上の研究者が利用）やWeatherNext、AlphaGenome、AlphaEarth Foundationsのような特定問題に特化した専用ツール群。第二は、LLMベースの自律エージェントが人間の関与なしに最先端研究を実行するという将来像だ。

Googleは後者へのシフトを加速させている。その証拠として、AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング分野に異動したことが挙げられる。これはAnthropicやOpenAIとのコーディングツール競争への対応でもあるが、同時にコーディング能力がエージェント型科学研究システムの基盤となるため、戦略的な人材配置とも読める。

Google I/Oで発表された「Gemini for Science」は、仮説生成AIである「AI Co-Scientist」と、アルゴリズム最適化システム「AlphaEvolve」を統合したLLMベースのプラットフォームで、研究者からのアクセス申請受付が開始された。スタンフォード大学の遺伝学者Gary PeltzはNature Medicine誌でAI Co-Scientistを「デルポイの神託に相談するようだ」と評した。

OpenAIも同週、汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したと発表。数学者の一部によれば、これは生成AIが数学に対して行った最も重要な貢献とされる。専用モデルではなく汎用モデルによる科学的貢献は、エージェントによる科学研究の実現可能性を裏付けるものだ。

Googleはこれらのエージェントを「科学者の代替」ではなく「加速装置・共同研究者」として位置付けており、「AI Scientist」ではなく「AI Co-Scientist」という命名にもその姿勢が表れている。Hassabisは今後10年はAIを科学者を助けるツールとして捉え、それ以降は「コラボレーター」になりうると述べた。

監査エージェント開発への示唆：汎用LLMエージェントが仮説生成・アルゴリズム最適化・数学的証明反証を実現しつつある流れは、監査エージェントにも直接応用可能だ。特にAI Co-Scientistのような仮説生成アーキテクチャは、不正リスク仮説の自動生成や内部統制上の弱点発見に転用できるアプローチとして注目に値する。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専用モデルなしに数学予想の反証に成功したことは、特化型AIから汎用エージェントへの転換点を示す具体的証拠である
- AI Co-ScientistとAlphaEvolveを統合したGemini for Scienceのアーキテクチャは、仮説生成→実験設計→アルゴリズム最適化のループをエージェントで自動化する構造として、監査プロセスの自動化設計に応用できる
- ノーベル賞受賞者JumperのAIコーディング部門への異動は、コーディング能力がエージェント型科学研究の中核インフラであることを示しており、LLMのコード生成能力が科学エージェントの実用化を左右する鍵となる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **Gemini** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oが示すAI駆動科学の方向転換：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
