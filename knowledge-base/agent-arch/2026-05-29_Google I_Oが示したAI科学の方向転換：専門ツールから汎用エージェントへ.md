---
title: "Google I/Oが示したAI科学の方向転換：専門ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-29
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, agentic-science, 汎用推論モデル, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6733, 6435, 6391]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-29T09:16:45.336573"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と発言した。この文脈で注目されたのは、科学AIの二つのアプローチ間の転換点である。第一は特定問題に特化したツール型AI（WeatherNextによる台風Melissa上陸予測、AlphaFoldによるタンパク質構造予測など）、第二はLLMベースの汎用エージェントが自律的に研究を実行するアプローチだ。

GoogleはWeatherNext（気象予測）、AlphaGenome（遺伝学）、AlphaEarth Foundations（地球科学）といった特化型ツールを依然として開発・維持しているが、重心のシフトが複数の指標から読み取れる。AlphaFoldでノーベル賞を受賞したJohn Jumperがスペシャライズド科学AIからAIコーディング分野へ異動した事実は、リソース配分の変化を示唆する。

Googleが新たに発表した「Gemini for Science」パッケージは、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」をLLMベースの統合ブランドとして束ねるもの。Stanford遺伝学者Gary PeltzはNature Medicine誌でCo-Scientistを「デルフォイの神託に相談するようだ」と評した。現在は研究者への限定アクセス申請段階だが、広範な採用が見込まれる。

業界全体でも汎用エージェントの科学的貢献が現実化しつつある。OpenAIは今週、汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表。これは数学者の間でも「生成AIが数学に対してなした最も意義ある貢献」との評価を受けている。モデルは数学専用でも研究専用でもなく汎用である点が重要で、科学領域への一般化可能性を示唆する（ただし科学は実験的検証が必要な点でAIには難しい側面もある）。

Google Cloud主任科学者Pushmeet Kohliは学術誌Daedalusに「AIは科学を促進するだけでなく、科学を『行う』方向に向かっている」と寄稿。Hassabisも同誌インタビューで「今後10年はAIを科学者の支援ツールとして、その先はコラボレーターとなりうる」と述べており、「AI Scientist」ではなく「AI Co-Scientist」という命名も人間中心フレームを維持する意図を示す。

監査エージェント開発への示唆：AlphaFoldのような高精度特化モデルと汎用推論エージェントの役割分担という設計思想は、監査AIにも直接応用できる。財務データ分析や証拠評価のような反復的タスクには特化ツールを、仮説生成・異常検知の説明生成には汎用LLMエージェントを使う二層アーキテクチャが有効と考えられる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専用訓練なしに数学的予想を反証した事実は、特化型ツール vs 汎用エージェントの優位性議論に実証的根拠を与える
- AlphaFoldのような特化ツールは汎用エージェントに置き換わるのではなく、エージェントが呼び出す「ツール」として再定義される可能性がある（Gemini for ScienceがAlphaFoldを内包する構造）
- Nobel賞受賞者Jumperのコーディング分野への異動は、LLMのコーディング能力が汎用エージェント科学の中核スキルであることを示唆しており、コード生成能力の強化が科学AIの競争力に直結する

## 前提知識

- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / reasoning model** (TODO: 読むべき)
- **ツール呼び出し（Function Calling）** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した

## 原文リンク

[Google I/Oが示したAI科学の方向転換：専門ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
