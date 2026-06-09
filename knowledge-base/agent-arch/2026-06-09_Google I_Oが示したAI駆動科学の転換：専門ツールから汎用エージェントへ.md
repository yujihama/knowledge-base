---
title: "Google I/Oが示したAI駆動科学の転換：専門ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-09
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 汎用推論モデル, 自律型科学エージェント, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6733, 6435, 6391]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-09T21:11:58.367636"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言の文脈は科学AIセクションであり、具体的にはハリケーン「メリッサ」のジャマイカ上陸を事前に警告した気象予測ソフト「WeatherNext」の事例が紹介された。この対比が、現在のAI科学研究における2つのアプローチの緊張関係を浮き彫りにしている。第一のアプローチは、AlphaFoldやWeatherNextのような特定の科学問題に特化した専門ツールの開発。第二は、LLMベースの汎用エージェントが自律的に最先端研究を実行するモデルである。Googleは後者への傾斜を示しており、その証拠として、AlphaFoldでノーベル賞を受賞したJohn JumperがAIコーディング分野に異動したことが報じられた。科学特化ツールへの注力は維持されており、AlphaGenome（ゲノム）・AlphaEarth Foundations（地球科学）・最新版WeatherNextが引き続きリリースされ、AlphaFoldは世界300万人以上の研究者に利用されている。しかし公式発表の重心は、仮説生成AI「Co-Scientist」と最適化AI「AlphaEvolve」を統合した「Gemini for Science」パッケージに移行しつつある。Gemini for Scienceは研究者向けのアクセス申請を開始しており、Stanford大学の遺伝学者Gary PeltzはAI Co-Scientistを「デルフォイの神託に相談するようだ」とNature Medicine誌で評した。同週、OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表し、専門特化なしに研究貢献が可能なことを示した。Hassabisは今後10年はAIを「科学者を支援するツール」と位置付けつつ、その先では「コラボレーター」になりうると述べる。命名も「AI Scientist」ではなく「AI Co-Scientist」と人間中心の枠組みを維持しているが、方向性は自律型AIサイエンティストへの長期シフトを示唆している。監査エージェント開発への示唆として、仮説生成・検証・反証というサイクルをエージェントに組み込む設計（Co-Scientistが採用するアプローチ）は、監査における異常検出→仮説立案→証拠収集ループに直接応用可能であり、LangGraphベースのReActエージェントとの親和性が高い。

## アイデア

- 専門特化ツール（AlphaFold等）vs 汎用エージェント（Gemini for Science）という二項対立は、監査AIの設計方針にも直結する：特定リスクに特化したルールベースvs汎用LLMエージェントのどちらに投資すべきかという問いと同型
- OpenAIの汎用モデルが数学的予想を反証したという事実は、ファインチューニングなしにドメイン貢献が可能であることを示しており、監査領域でも汎用推論モデルのゼロショット適用を再評価する根拠になりうる
- AI Co-Scientistの命名（Scientistではなく）は、規制・倫理・ガバナンス上の責任帰属を人間に残すための意図的なフレーミングであり、監査AIにおける「AIは補助」「判断は人間」という構造と同じロジックで商業展開・社内承認を得やすくなる設計思想

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した

## 原文リンク

[Google I/Oが示したAI駆動科学の転換：専門ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
