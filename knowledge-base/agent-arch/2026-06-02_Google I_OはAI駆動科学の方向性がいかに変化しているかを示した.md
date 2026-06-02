---
title: "Google I/OはAI駆動科学の方向性がいかに変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-02
tags: [科学AI, エージェント科学, AlphaFold, WeatherNext, Gemini for Science, Co-Scientist, AlphaEvolve, 汎用推論モデル, recursive self-improvement, LLMエージェント]
category: "agent-arch"
related: [6370, 6733, 6251, 6299, 6710]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-02T09:16:25.836851"
---

## 要約

Google I/Oにおいて、Google DeepMindのCEOであるDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言は、科学AIに関するセグメントの締めとして行われ、同社の気象予測AI「WeatherNext」がジャマイカへの上陸前にハリケーン「メリッサ」の警報を事前提供し、人命救助に貢献した事例が紹介された直後だった。この対比は、現在の科学AIにおける2つのアプローチの緊張関係を浮き彫りにしている。

第1のアプローチは、AlphaFold（タンパク質構造予測）やWeatherNextのように、特定の科学問題を解くために設計・訓練された特化型ツールである。AlphaFoldはノーベル賞を受賞し、世界300万人以上の研究者に利用されており、関連技術を活用するGoogle子会社Isomorphic Labsは直近で20億ドルのシリーズB資金調達を完了した。

第2のアプローチは、LLMベースの汎用エージェントが人間の関与なしに最先端研究を遂行するというビジョンである。OpenAIは今週、汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したと発表しており、数学者からも「これまでの生成AIによる数学への最も意義ある貢献」と評価されている。

Googleはこの第2のアプローチへの傾注を示すため、「Gemini for Science」パッケージを発表した。これは、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」をはじめとする複数のLLMベース科学システムを統合したものである。Stanfordの遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」とCo-Scientistを評した（Nature Medicine掲載）。

リソース配分にも変化の兆しがある。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn JumperがAIコーディング分野に異動したことがLos Angeles Timesにより報道された。コーディング能力はエージェント科学システムの成功に不可欠であり、AnthropicやOpenAIとの競争上の観点からも合理的な判断と見られる。

GoogleはAI Co-Scientistという名称（AI Scientistではなく）を意図的に選択し、エージェントを人間科学者の「代替」ではなく「加速剤」として位置づけている。Hassabisは「今後10年程度はAIを科学者を支援するツールとして捉えるべきだが、それ以降はコラボレーターになりうる」と述べている。

監査エージェント開発への示唆：汎用推論モデルが数学的証明という厳密な論理領域で成果を上げた事実は、監査エージェントにおいても汎用LLMベースの推論が専用ツールに匹敵しうる可能性を示す。AlphaFold的な特化モデルとエージェント的な汎用推論の二軸設計は、監査AIアーキテクチャ（特化ツール呼び出しを組み込んだReActエージェント）の設計指針として参照できる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証したことは、特化型ではなく汎用エージェントが科学的発見を行える閾値に近づいていることを示す具体的な証拠である
- AlphaFoldのような特化型ツールとLLMエージェントは競合ではなく、エージェントが必要に応じて特化ツールをAPIとして呼び出す階層構造（ツール呼び出し型エージェント）として統合できる
- ノーベル賞受賞者をコーディングAI開発に異動させるという人材配置は、企業がどの技術に将来の競争優位を見出しているかを示す間接指標として読み取れる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **ツール呼び出し型エージェント** (TODO: 読むべき)

## 関連記事

- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6299 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI強化
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向

## 原文リンク

[Google I/OはAI駆動科学の方向性がいかに変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
