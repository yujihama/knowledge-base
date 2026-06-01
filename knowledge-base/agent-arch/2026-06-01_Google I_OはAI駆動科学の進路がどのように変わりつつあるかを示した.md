---
title: "Google I/OはAI駆動科学の進路がどのように変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-01
tags: [エージェント型AI, 科学AI, AlphaFold, WeatherNext, Gemini for Science, AI Co-Scientist, AlphaEvolve, 汎用推論モデル, 再帰的自己改善, Google DeepMind]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-01T09:16:27.330274"
---

## 要約

2026年5月のGoogle I/Oで、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と述べた。この発言の文脈は科学AI領域であり、同社の気象予測ソフトウェア「WeatherNext」がジャマイカに上陸したハリケーン・メリッサの事前警告を提供し、人命救助に貢献したという事例が紹介された。

記事は、科学AIの2つのアプローチの緊張関係を軸に展開する。一方は「特化型AIツール」—AlphaFold（タンパク質構造予測、ノーベル賞受賞、300万人以上の研究者が利用）、WeatherNext、AlphaGenome、AlphaEarth Foundationsなど、特定の科学問題を解くよう設計・訓練されたシステム。もう一方は「エージェント型LLMシステム」—自律的に最先端研究を実行できる汎用推論モデルベースのアプローチである。

リソースと優先度の移行を示す具体的な証拠として、AlphaFold開発でノーベル賞を受賞したGoogleフェローのJohn Jumperが現在はAIコーディング部門に異動していることが挙げられる。Googleがコーディングツールでの競争力回復（AnthropicやOpenAIへの対抗）を優先している背景があるが、コーディング能力はエージェント型科学システムにも不可欠であるため、この人事はエージェント科学への傾注を示すとも解釈できる。

今週の業界動向として、OpenAIの汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したことも報告された。数学者の一部はこれを生成AIの数学分野への最も意味ある貢献と評価しており、科学ドメインへの波及可能性を示唆している。

GoogleはI/Oで「Gemini for Science」パッケージを発表。仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を統合し、研究者からのアクセス申請受付を開始した。StanfordのGary Peltz遺伝学者はAI Co-Scientistをデルフォイの神託に喩えるほど高く評価している。

Hassabisは今後10年は「AIを科学者を助ける驚異的なツール」として位置づけ、その後は「コラボレーター」になりうるとDaedalus誌インタビューで述べた。AI Co-Scientistという命名（AI Scientistではなく）にも人間中心の協働フレーミングが意図的に反映されている。

監査エージェント開発への示唆：汎用推論モデルが特化型システムなしに数学的証明を覆せるなら、監査ドメインでも特化ファインチューニングよりもReAct型の汎用エージェント設計の優位性が高まりうる。また、科学AIにおけるCo-Scientist的な「人間とAIの協働ループ」設計思想は、監査エージェントの人間レビュー組み込みアーキテクチャに直接応用できる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証できたという事実は、特化型モデルを構築せずとも科学的貢献が可能であることを示し、特化型vs汎用エージェントの費用対効果の議論を根本から変える可能性がある
- AlphaFoldのノーベル賞受賞者Jumperがコーディング部門に異動という人事は、企業戦略レベルで「特化科学ツール開発」から「エージェント基盤（コーディング能力）構築」へのリソースシフトを示す経営判断の指標として注目に値する
- Gemini for ScienceにおけるCo-Scientistの設計思想（仮説生成→実験→検証の自律ループを人間監督下で行う）は、監査エージェントにおけるリスク仮説生成→証拠収集→判断のReActループ設計に直接転用可能なアーキテクチャパターンを提供する

## 前提知識

- **LLMエージェント（ReAct）** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善（RSI）** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **RAG / ツール呼び出し** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/OはAI駆動科学の進路がどのように変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
