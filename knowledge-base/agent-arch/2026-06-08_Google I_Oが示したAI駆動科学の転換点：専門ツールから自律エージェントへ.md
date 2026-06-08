---
title: "Google I/Oが示したAI駆動科学の転換点：専門ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-08
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, LLMエージェント]
category: "agent-arch"
related: [6461, 6370, 6733, 6710, 6585]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-08T21:12:38.474222"
---

## 要約

Google I/Oにて、DeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と宣言した。その文脈は科学AIに関するセグメントであり、具体的にはハリケーン「Melissa」のジャマイカ上陸を事前警告した気象予測ソフト「WeatherNext」の成果が紹介された。この発言は、現在の科学AI開発における2つのアプローチの緊張関係を象徴している。

第1のアプローチは、AlphaFold（タンパク質構造予測、ノーベル賞受賞）やWeatherNextのような特定科学問題に特化した専門ツールの開発である。AlphaFoldは世界300万人以上の研究者に利用され、関連技術を持つIsomorphic Labsは20億ドルのシリーズB資金調達を完了した。

第2のアプローチは、LLMベースの自律エージェントが人間の介入なしに研究を遂行するというビジョンである。Googleはこの方向性を示す「Gemini for Science」パッケージを発表。これは仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」を統合したものであり、研究者が申請すればアクセス可能になる。スタンフォードの遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」とCo-Scientistを評した（Nature Medicine掲載）。

リソース配分にも変化の兆候がある。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn JumperがAIコーディング分野に異動したことをLos Angeles Timesが報じた。コーディング能力はエージェント型科学AIの成功に不可欠であり、AnthropicやOpenAIに対してコーディングツールで劣後しているGoogleにとっての戦略的再配置とも読める。

同週にはOpenAIが、汎用推論モデル（GPT-5.5相当）が重要な数学的予想を反証したと発表。これは数学者の間でも生成AIの数学研究への最も重要な貢献と評価されており、汎用エージェントが科学分野でも独立した貢献を果たせる可能性を示している。

Googleは「AI Co-Scientist」という命名（AI Scientistではなく）に示されるように、現時点では人間科学者の加速装置として位置づけている。Hassabisは「今後10年はAIを科学者を助く道具として捉えるべき」としつつ、それ以降は「コラボレーター」になり得ると述べた。監査エージェント開発への示唆としては、専門タスク特化型ツールと汎用推論エージェントの役割分担設計、エージェントから専門ツールへの呼び出し（tool-use）アーキテクチャの重要性が参考になる。

## アイデア

- 汎用推論モデル（GPT-5.5相当）が専門訓練なしに数学的予想を反証したことは、特化型ツールの存在意義を問い直す転換点になる可能性がある
- エージェント型科学AIが専門ツール（AlphaFold等）をtool-callとして呼び出す設計により、専門ツールとエージェントの対立ではなく階層的統合が実現できる
- 人材配置（Jumper氏のコーディングAIへの異動）がロードマップを語る：コーディング能力の強化がエージェント型科学AIの基盤整備と連動している

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **tool-use / function calling** (TODO: 読むべき)
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / reasoning model** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱

## 原文リンク

[Google I/Oが示したAI駆動科学の転換点：専門ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
