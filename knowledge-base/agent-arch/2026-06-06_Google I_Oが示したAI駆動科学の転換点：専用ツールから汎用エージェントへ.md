---
title: "Google I/Oが示したAI駆動科学の転換点：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-06
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 汎用推論モデル, 自律科学AI, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6733, 6435, 6391]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-06T09:14:05.718684"
---

## 要約

2026年5月のGoogle I/Oキーノートにて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と発言した。この発言の文脈は科学AIセクションであり、ハリケーン「メリッサ」のジャマイカ上陸を事前予測した気象予測ソフト「WeatherNext」の成果が紹介された。しかしこの juxtapositionが示すのは、科学AIにおける二つのアプローチの間の緊張関係だ。

第一のアプローチは、AlphaFoldやWeatherNextのような特定問題に特化した専用ツールの開発。AlphaFoldのタンパク質構造予測は世界300万人以上の研究者に利用され、関連技術を持つIsomorphic Labsは20億ドルのシリーズB資金調達を完了している。第二のアプローチは、LLMベースの汎用エージェントが人間の関与を最小化しながら研究を自律実行するモデルであり、現在業界の主流トレンドとなっている。

Googleの姿勢の変化を示す具体的な指標として、AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn Jumperが科学特化AIではなくAIコーディング開発にリソースを移したことが挙げられる。これはAnthropicやOpenAIに対するコーディングツール競争での遅れを取り戻す戦略と同時に、エージェント型科学AIへの資源シフトを意味すると解釈される。

Gemini for Scienceは複数のLLMベース科学システムを統合したパッケージとして発表された。仮説生成AI「Co-Scientist」と、アルゴリズム最適化ツール「AlphaEvolve」が含まれ、現在は研究者がアクセス申請可能。Co-Scientistについてスタンフォードの遺伝学者Gary Peltzは「デルポイの神託に相談するようだ」と評した（Nature Medicine掲載）。

OpenAIは同週、汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表。数学者の一部はこれを生成AIの数学への最も意義ある貢献と評価した。専用数学モデルではなく汎用モデルが独立した数学的貢献を行ったことは、エージェント型科学AIの潜在力を示す重要な証拠となっている。

GoogleはAI Co-Scientistという名称選択（AI Scientistではなく）に見られるように、人間科学者の「補助者」として位置付ける戦略を維持している。HassabisはDaedalus誌のインタビューで「今後10年はAIを科学者支援の道具として考えるべき」と述べつつ、それ以降は「コラボレーターになる可能性がある」と示唆した。

監査エージェント開発への示唆：仮説生成と検証を自律的に繰り返すAI Co-Scientistのアーキテクチャは、監査エージェントにおけるリスク仮説の自動生成→証拠収集→検証ループの設計に直接応用可能。特にAlphaEvolveのアルゴリズム自動最適化機能は、監査サンプリング戦略の動的最適化に転用できる可能性がある。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専用数学ツールなしに重要な数学的予想を反証した事実は、特化モデル vs 汎用エージェントの優位性論争に実証的な一石を投じる
- AI Co-Scientistが「Co-Scientist」と命名されたことは意図的な差別化であり、人間との協調フレーミングがAIガバナンス・倫理的受容の観点でどう機能するかが興味深い
- AlphaFold開発者JumperがコーディングAIへ異動した事実は、特化型科学AIの限界とLLMベースエージェントへのリソース再配分という業界トレンドのシグナルとして読める

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **RAG/ツール呼び出し** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した

## 原文リンク

[Google I/Oが示したAI駆動科学の転換点：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
