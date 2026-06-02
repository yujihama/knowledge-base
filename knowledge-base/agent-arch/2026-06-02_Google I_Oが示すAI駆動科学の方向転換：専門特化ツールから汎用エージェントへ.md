---
title: "Google I/Oが示すAI駆動科学の方向転換：専門特化ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-02
tags: [AI-for-science, LLMエージェント, AlphaFold, Gemini-for-Science, AI-Co-Scientist, AlphaEvolve, WeatherNext, 汎用推論モデル, recursive-self-improvement]
category: "agent-arch"
related: [6733, 6391, 3220, 6461, 6783]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-02T21:28:07.170866"
---

## 要約

Google I/O 2026のキーノートでDeepMind CEO Demis Hassabisは「シンギュラリティの山麓に立っている」と発言した。その文脈はAI科学ツールの紹介であり、具体的にはWeatherNextという気象予測ソフトウェアがハリケーン「Melissa」のジャマイカ上陸を事前予測し、人命救助に貢献した事例が示された。この発言が象徴するのは、AI科学における二つのアプローチの緊張関係である。一方は特定科学問題を解くために設計・訓練された専用ツール（AlphaFold、WeatherNext、AlphaGenome、AlphaEarth Foundationsなど）、もう一方はLLMベースの汎用エージェントシステムによる自律的な科学研究の実行だ。

Googleは後者への重心移動を見せている。AlphaFoldでノーベル賞を受賞したJohn Jumperが現在AIコーディング領域に配置転換されていることが、Los Angeles Timesの報道で明らかになった。同社はGemini for Scienceブランドのもと、仮説生成AIであるCo-ScientistとアルゴリズムオプtimizerであるAlphaEvolveを統合し、研究者向けのアクセス申請受付を開始した。Stanford大学のGary Peltz氏はAI Co-Scientistを「デルポイの神託に相談するようだ」と評した（Nature Medicine掲載）。

一方、OpenAIは今週、一般推論モデル（GPT-5.5系統）が重要な数学的予想を反証したと発表。数学者によればこれは生成AIが数学に対して行った最も重要な貢献とされる。これが科学に及ぶ可能性も示唆されるが、科学的知見は実験的検証が必要であり、数学より難易度が高い。

GoogleはAI Co-Scientist（AI Scientistではない）という命名に示されるように、現時点では人間科学者の補完という位置付けを維持している。AlphaFoldはタンパク質構造予測において依然として代替不可であり、Isomorphic LabsはAlphaFold技術を用いた創薬で20億ドルのシリーズB資金調達を完了した。しかしHassabisは「今後10年はAIを科学者を支援するツールとして考えるべきだが、その先はAIがより協働者に近くなるかもしれない」と述べており、中長期的な方向性はエージェント化・自律化にある。監査エージェント開発観点では、専門特化ツールとLLMエージェントの組み合わせアーキテクチャ（AlphaFoldをツールとして呼び出すエージェント）が、監査AI設計における特化型モジュールとオーケストレーターLLMの構成と直接対応する示唆を持つ。

## アイデア

- 専門特化ツール（AlphaFold等）をサブツールとして呼び出す汎用エージェントというアーキテクチャは、監査AIにおける特化型検証モジュール＋オーケストレーターLLMの構成と同型であり、設計参考になる
- GPT-5.5系の汎用推論モデルが数学的予想を反証した事例は、ドメイン特化ファインチューニングなしでも専門的推論タスクに寄与できることを示しており、監査エージェントにおけるベースモデル選定の前提を問い直す
- Hassabisが1970年代以降の物理学の停滞とAIの限界突破可能性を起点にDeepMindを着想したという文脈は、AI科学エージェントが「人間の認知的天井を突破する」という方向性が単なるマーケティングでなく研究戦略に根ざしていることを示す

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ツール呼び出し型エージェント** (TODO: 読むべき)

## 関連記事

- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した
- /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6783 Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか

## 原文リンク

[Google I/Oが示すAI駆動科学の方向転換：専門特化ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
