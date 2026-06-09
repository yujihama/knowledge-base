---
title: "Google I/Oが示すAI駆動科学の転換点：特化型ツールからエージェント型研究者へ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-09
tags: [エージェント型AI, AlphaFold, Gemini for Science, WeatherNext, AI Co-Scientist, AlphaEvolve, 再帰的自己改善, 科学AI]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-09T12:08:15.231839"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEO Demis Hassabisが「シンギュラリティの麓に立っている」と発言した。この発言の文脈は科学AIセッションであり、具体的にはハリケーン「Melissa」のジャマイカ上陸を事前警告した気象予測ソフトウェア「WeatherNext」の紹介だった。この対比が、AI科学における2つのアプローチの緊張関係を浮き彫りにした。第1のアプローチは、WeatherNextやAlphaFoldのような特定科学問題に特化したツール開発。第2は、LLMベースのエージェントシステムが人間の関与を最小化しながら最先端研究を実行する方向性である。後者の文脈では「再帰的自己改善（recursive self-improvement）」の概念も注目されており、AIがAI進歩の主要ドライバーになり得るという議論が活発化している。Googleは特化型ツールを完全に放棄したわけではない。AlphaFoldのタンパク質構造予測は世界300万人以上の研究者が利用しており、AlphaFoldを基盤とした創薬企業Isomorphic Labsは直近で20億ドルのシリーズB調達を完了した。AlphaGenome（遺伝学）やAlphaEarth Foundations（地球科学）も2025年夏にリリース済みである。しかし資源・人材のリアライン兆候も顕在化している。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング分野に異動したとLAタイムズが報道。GoogleはAnthropicやOpenAIにコーディングツールで後れを取っており、コーディング能力はエージェント型科学システムの根幹でもある。Google I/Oの主要発表は「Gemini for Science」パッケージで、仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を統合。現在は申請制での研究者アクセスを開始した。一方OpenAIは汎用推論モデル（GPT-5.5相当）が重要な数学的予想を反証したと発表し、特化型でない汎用エージェントが数学・科学研究に貢献できることを示した。Hassabis自身は「今後10年はAIを科学者支援ツールとして位置付けるべき」としつつ、その先では「コラボレーター」になり得ると述べており、「AI Co-Scientist」という命名も人間中心のフレーミングを意図したものとみられる。監査エージェント開発への示唆として、汎用エージェントが専門領域で成果を出しつつある流れは、監査AIにおいても特化型ルールエンジンよりも汎用LLMエージェント＋専門ツール呼び出しのアーキテクチャが有望であることを示唆する。

## アイデア

- 汎用推論モデル（OpenAI GPT-5.5相当）が特化型訓練なしに数学的予想を反証した事実は、エージェント＋汎用推論の組み合わせが専門特化型モデルを代替し始めるティッピングポイントを示している
- AlphaFold Nobel賞受賞者のJumperがコーディングAIに異動した人事は、Googleの内部優先度の変化を示す具体的シグナルであり、特化ツール開発から汎用エージェント基盤構築へのリソースシフトを表す
- 「AI Co-Scientist」vs「AI Scientist」の命名差は単なるマーケティングではなく、規制・倫理・研究コミュニティとの摩擦を最小化するための戦略的フレーミングであり、監査AIの導入設計（人間の判断を要件とする構造）にも応用可能

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善** → /deep_6455 Google I/OはAI駆動科学の方向性がいかに変化しているかを示した
- **Tool-calling / Function calling** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oが示すAI駆動科学の転換点：特化型ツールからエージェント型研究者へ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
