---
title: "Google I/O が示す、AIによる科学研究のパラダイムシフト：専門ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-09
tags: [Gemini for Science, AlphaFold, Co-Scientist, AlphaEvolve, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, 汎用推論モデル]
category: "agent-arch"
related: [6461, 6370, 6251, 6299, 6710]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-09T09:17:22.282730"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMindのCEOであるDemis Hassabisは「シンギュラリティの山麓に立っている」と宣言した。その文脈は科学AIセッションであり、同社の気象予測ソフトウェア「WeatherNext」がハリケーン「Melissa」のジャマイカ上陸を事前に警告し、人命救助に貢献したという事例が紹介された。しかしこの発言が象徴するのは、AI科学研究における二つのアプローチの分岐点である。第一のアプローチは、AlphaFold（タンパク質構造予測、ノーベル賞受賞）やWeatherNextのような、特定の科学的問題を解くために設計・学習された専門ツール。第二は、LLMベースの自律エージェントが人間の介入なしに最先端研究を実行するというビジョンだ。GoogleはAlphaGenome（遺伝学）・AlphaEarth Foundations（地球科学）といった専門ツールの開発を継続しているが、重点の移行を示す具体的なシグナルもある。AlphaFoldでノーベル賞を共同受賞したJohn JumperがAIコーディング部門に異動したことが報じられ、これはAnthropicやOpenAIに対するコーディングツールの競争力強化と同時に、エージェント型科学研究へのリソース再配分を示唆している。今回の主要発表は「Gemini for Science」パッケージで、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」を統合。研究者からのアクセス申請を受け付け開始した。スタンフォードの遺伝学者Gary Peltzは、Co-Scientistの使用体験を「デルフォイの神託に相談するようだ」とNature Medicine誌に記している。エージェント型研究の実力を示す事例として、OpenAIの汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したことも挙げられる。これは数学専用モデルではなく汎用モデルによる成果であり、汎用エージェントが科学研究へ独立した貢献を果たし始める可能性を示す。ただし科学では実験的検証が必須なため、数学よりも難易度は高い。Hassabisは「今後10年程度はAIを科学者を支援する強力なツールとして捉えるべき。その先はコラボレーターになりえる」と述べており、'AI Co-Scientist'という命名（'AI Scientist'ではない）も人間中心のフレーミングを意識している。監査エージェント開発への示唆としては、AlphaEvolveのようにアルゴリズムを自律的に最適化するエージェントの設計思想は、監査手続きの自動生成・改善ループに直接応用できる。また、Co-Scientistの仮説生成機能は、リスク仮説の自動立案・検証フレームワークとして内部監査エージェントへの組み込みが構想できる。専門ツールと汎用エージェントを組み合わせたハイブリッドアーキテクチャ（エージェントがAlphaFoldを呼び出す設計）は、監査AI設計の参考モデルになりうる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学の予想を反証した事実は、科学研究における専門特化モデルvs汎用エージェントの優位性議論に新たな証拠を加える。監査AIにおいても、専用ルールエンジンより汎用LLMエージェントが特定タスクで逆転する可能性を示唆
- AlphaEvolveのようなアルゴリズム自己最適化エージェントは、監査手続きの反復改善（どの手続きが不正検出に有効かを学習しながら更新するループ）に応用できる設計パターンを提供する
- 専門ツール（AlphaFold等）をエージェントのツールとして呼び出すハイブリッドアーキテクチャは、監査エージェントがDCF計算エンジンや統計的サンプリングモジュールを動的に呼び出す設計の先行事例として参照価値が高い

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / Tool Use** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6299 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI強化
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向

## 原文リンク

[Google I/O が示す、AIによる科学研究のパラダイムシフト：専門ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
