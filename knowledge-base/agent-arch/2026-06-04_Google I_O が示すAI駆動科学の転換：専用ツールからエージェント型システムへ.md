---
title: "Google I/O が示すAI駆動科学の転換：専用ツールからエージェント型システムへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-04
tags: [エージェント型AI, 科学AI, AlphaFold, Gemini for Science, AI Co-Scientist, AlphaEvolve, WeatherNext, LLM研究自動化, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-04T21:05:57.491914"
---

## 要約

Google I/O 2026にてDeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と述べた。その文脈は科学AIに関するセグメントであり、具体的には気象予測ソフトウェア「WeatherNext」がハリケーン「メリッサ」のジャマイカ上陸を事前警告し、人命救助に貢献した事例が紹介された。この発言は、科学AIにおける二つのアプローチの対立を浮き彫りにした。一つはWeatherNextやAlphaFold、AlphaGenome、AlphaEarth Foundationsのような特定科学問題に特化した専用ツール群。もう一つは、LLMベースのエージェント型システムが人手を介さずに最先端研究を実行できるようになるという方向性である。後者の代表例として、GoogleはGoogle I/OでGemini for Scienceパッケージを発表した。これは仮説生成AIの「AI Co-Scientist」やアルゴリズム最適化の「AlphaEvolve」を統合したブランドであり、研究者によるアクセス申請が開始された。同週にはOpenAIが汎用推論モデル（GPT-5.5系）を用いて重要な数学的予想を反証したと発表し、専用チューニング不要での研究貢献が現実化しつつあることを示した。人員面でも転換の兆候がある。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn JumperがAIコーディング分野に異動したことはLA Timesが報じており、エージェント科学の中核技術であるコーディング能力の強化を優先する戦略と解釈できる。AlphaFoldのタンパク質構造予測は世界300万人以上の研究者に利用され、関連会社Isomorphic Labsは20億ドルのシリーズB調達を完了するなど専用ツールへの需要は依然高い。しかしGoogleは公的イメージと一部リソースをエージェント型科学AIへシフトしつつある。Hassabisはエージェント型AIを「人間科学者の代替ではなく加速装置」として位置づけ、「AI Scientist」ではなく「AI Co-Scientist」という命名が意図的な選択と見られる。今後10年は「科学者を支援する道具」として機能し、それ以降は「協力者」になり得るとの見解を示している。監査エージェント開発への示唆として、仮説生成・検証・コーディングをエンドツーエンドで実行するエージェント構成が科学領域で現実化しつつあり、LangGraphやReActベースの監査エージェントにおいても同様のマルチステップ推論パイプラインの参考アーキテクチャとして注目に値する。

## アイデア

- 汎用推論モデル（OpenAIのGPT-5.5系）が専用チューニングなしで数学的予想を反証した事実は、専用科学ツールとエージェント汎用モデルの優位性境界が急速に変化していることを示す
- AI Co-ScientistとAlphaEvolveを統合したGemini for Scienceは、仮説生成→アルゴリズム最適化→実験設計までをエージェントがオーケストレーションする構成の実例であり、監査エージェントのマルチステップ推論設計に直接応用可能
- Jumperのコーディング部門異動は、エージェント科学においてコード生成・実行能力が中核コンピタンスになることを示唆し、LLM-as-judgeやself-playによる反復改善ループの重要性が増す

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **マルチエージェントオーケストレーション** → /deep_1561 リーダーシップクラスシステムにおける高スループット材料スクリーニングのためのマルチエージェントオーケストレーション

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/O が示すAI駆動科学の転換：専用ツールからエージェント型システムへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
