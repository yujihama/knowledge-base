---
title: "Google I/Oが示したAI科学研究の方向転換：特化ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-25
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, Google DeepMind]
category: "agent-arch"
related: [6461, 6370, 3430, 6435, 6391]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-25T21:03:24.816630"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓にいる」と発言した。その文脈は科学AIの進化を論じるセッションであり、特化型AIツールと汎用エージェント型AIという2つのアプローチの分岐点を象徴していた。

特化型AIの代表例として、WeatherNextは2025年にジャマイカを直撃したハリケーン・メリッサの上陸を事前予測し、人命救助に貢献した。AlphaFoldはタンパク質構造予測で世界3百万人以上の研究者に利用され、John Jumper氏のノーベル賞受賞をもたらした。AlphaGenome（遺伝学）やAlphaEarth Foundations（地球科学）も2025年夏にリリースされた。Isomorphic LabsはAlphaFoldを創薬に応用し、20億ドルのシリーズB資金調達を完了している。

一方、Google I/Oの主要発表はエージェント型科学AIを束ねた「Gemini for Science」パッケージだった。仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を含み、一般研究者へのアクセス申請受付が開始された。StanfordのGary Peltz遺伝学者は「デルポイの神託に相談するようだ」とNature Medicine誌に記した。

方向転換の具体的兆候として、AlphaFoldでノーベル賞を受賞したGoogle Fellow John JumperがAIコーディング分野に異動したとLos Angeles Timesが報じた。AnthropicやOpenAIとのコーディングツール競争でのGoogle劣勢が背景とされるが、コーディング能力がエージェント型科学AIの基盤でもあるため、優先シフトを示す。

同週にOpenAIは汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表。数学者の間でも生成AIによる最大貢献と評価されており、専門特化なしに研究貢献が可能であることを示した。Google Cloud主任科学者Pushmeet KohliはDaedalus誌でAIが「科学を支援するだけでなく科学を行う」段階に移行しつつあると論じた。

Hassabisは短期的には「AIは科学者を助くツール」、長期的には「コラボレーター」と位置づける慎重な表現を使いつつ、「AI Co-Scientist」という名称選択にも人間中心の姿勢が現れている。ただしエージェント型科学AIが特化ツールを置き換えるのではなく、必要時にAlphaFold等を呼び出す形での統合も設計上可能であり、両者は排他的ではない。

監査エージェント開発への示唆：仮説生成→検証→改善のループをエージェントが自律実行するAI Co-Scientistの構造は、監査証拠収集・リスク仮説生成・手続立案をエージェントが反復実行する監査AIアーキテクチャと構造的に同型である。AlphaEvolveのようなアルゴリズム自己最適化は、監査サンプリング戦略や異常検知モデルの動的改善に応用できる可能性がある。

## アイデア

- エージェント型科学AIは専門特化ツール（AlphaFold等）をAPIとして呼び出す設計が可能で、両アプローチは置換ではなく統合関係にある点が監査AIの道具立て設計に示唆を与える
- OpenAIの汎用推論モデルが数学的予想を反証したように、専門訓練なしの汎用モデルが研究貢献できるなら、監査ドメイン特化なしのLLMでも高度な監査判断が可能になる閾値が近い可能性がある
- Jumperのコーディング分野異動はコーディング能力がエージェント型研究AIの核心であることを示しており、LLMによるコード生成・実行ループが科学的推論の主要インフラになるアーキテクチャ転換を意味する

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / ツール呼び出し** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した

## 原文リンク

[Google I/Oが示したAI科学研究の方向転換：特化ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
