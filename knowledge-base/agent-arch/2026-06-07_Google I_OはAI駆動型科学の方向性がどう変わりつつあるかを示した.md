---
title: "Google I/OはAI駆動型科学の方向性がどう変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-07
tags: [Gemini for Science, AlphaFold, WeatherNext, Co-Scientist, AlphaEvolve, エージェント型科学, recursive self-improvement, 汎用推論モデル]
category: "agent-arch"
related: [6461, 6783, 6370, 6733, 6435]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-07T21:06:20.982828"
---

## 要約

Google I/OのキーノートでDeepMind CEO Demis Hassabisは「特異点の山麓に立っている」と述べた。この発言は、科学向けAIの2つのアプローチの対比という文脈で語られた。第一は特化型ツール（WeatherNext、AlphaFold等）、第二は汎用LLMベースのエージェントによる自律的な研究実行である。

WeatherNextは2025年にハリケーン・メリッサのジャマイカ上陸を事前警告し、人命救助に貢献した実績を持つ。AlphaFoldはタンパク質構造予測でノーベル賞を受賞し、世界300万人以上の研究者に利用されている。Isomorphic Labs（Googleの子会社）はAlphaFold関連技術で新薬開発を目指し、シリーズBで20億ドルを調達した。これらの専門特化ツールは依然として科学コミュニティで高い人気を誇る。

一方で、リソースと関心の軸足は移動しつつある。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門へ異動したことは、専門特化ツール開発よりもエージェント型科学への優先順位付けを示唆する。コーディング能力はAnthropicやOpenAIに対してGoogleが競争上の課題を抱える領域であると同時に、エージェント型研究システムの基盤でもある。

GoogleはLLMベースの科学システムを統合した「Gemini for Science」パッケージを発表した。これには仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」が含まれるが、いまだ一般公開されておらず、研究者は申請制でアクセスを求める形となっている。StanfordのGary Peltz遺伝学者は「Delphi神託に相談するようだ」とCo-Scientistを評価した。

OpenAIはGPT-5.5系の汎用推論モデルが重要な数学的予想を反証したと発表し、一部の数学者から生成AIの数学分野への最も意味ある貢献と評価された。科学分野では実験的検証が必要なため数学より難度は高いが、汎用エージェントの研究貢献能力の向上が示された。

Hassabisは「今後10年程度はAIを科学者を支援する優れたツールとして考えるべき、その先はコラボレーターになりうる」とし、「AI Co-Scientist」という命名も人間中心性を意図したものと見られる。しかし有能な科学的協力者であるためには科学者としての能力も必要であり、エージェント型AIの進歩は人間の能力を超える可能性を内包する。監査エージェント開発への示唆：汎用推論モデルが複雑な論理的推論（数学的予想の反証等）を実行できるようになったことは、監査エージェントにおいても専用Fine-tuningなしに複雑なリスク評価や矛盾検出を汎用LLMで実装できる可能性を示す。

## アイデア

- 「Co-Scientist」という命名は意図的な人間中心フレーミングであり、AIの役割を『代替』ではなく『協働』として位置づける戦略的コミュニケーションの事例として興味深い
- AlphaFold（専門特化）でノーベル賞を取った人材をコーディングAI（汎用エージェント基盤）に再配置するという人的資源の移動が、Googleの技術戦略の実質的な優先順位を示す
- OpenAIの汎用推論モデルによる数学的予想の反証は、Fine-tuningなしの汎用エージェントが閉じた論理ドメインで専門家レベルの貢献をできる段階に入ったことを示唆し、監査・リスク評価領域への応用可能性がある

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **科学AI（AI for Science）** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6783 Google I/Oは何を示したか——コーディングAIの方向性がどう変わりつつあるか
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性

## 原文リンク

[Google I/OはAI駆動型科学の方向性がどう変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
