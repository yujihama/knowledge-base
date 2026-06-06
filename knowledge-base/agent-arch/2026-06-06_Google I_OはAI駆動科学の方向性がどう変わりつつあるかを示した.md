---
title: "Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-06
tags: [Google DeepMind, エージェント型AI, AI科学, AlphaFold, WeatherNext, Gemini for Science, recursive self-improvement, LLMエージェント, AlphaEvolve, AI Co-Scientist]
category: "agent-arch"
related: [6733, 6461, 6370, 6435, 6825]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-06T21:29:07.889057"
---

## 要約

2026年5月のGoogle I/OにてDeepMind CEOのDemis Hassabisは「特異点の麓に立っている」と発言した。その文脈はAI科学ツールの紹介セクションであり、具体的にはWeatherNextという気象予測ソフトウェアがハリケーン「メリッサ」のジャマイカ上陸を事前に警告し、人命救助に貢献した事例が示された。この発言はAI科学の2つのアプローチの緊張関係を象徴している。第1は特定科学問題向けに設計・訓練された専用ツール（WeatherNext、AlphaFold等）、第2はLLMベースの汎用エージェントシステムで、人間の関与なしに最先端研究を実行できる可能性を持つもの。後者のアプローチは再帰的自己改善（recursive self-improvement）への期待とも結びついており、AIがAI進歩の主要な推進力になるという構想を支えている。Googleは専用ツールを完全に捨てたわけではない。AlphaGenomeやAlphaEarth Foundationsは2025年夏にリリースされ、AlphaFoldはノーベル賞を受賞しており、現在も世界300万人超の研究者に利用されている。関連会社Isomorphic Labsは20億ドルのシリーズB調達を完了した。しかし資源配分と関心の移行を示す兆候もある。AlphaFoldでノーベル賞を共同受賞したGoogleフェローのJohn JumperがAIコーディングの研究に移行したと報じられており、これはGoogleが汎用エージェント型科学を優先する方向性と一致する（コーディング能力はエージェント型研究システムの鍵となるため）。今回発表された「Gemini for Science」パッケージはAI Co-Scientist（仮説生成）やAlphaEvolve（アルゴリズム最適化）などLLMベースの科学システムを統合するもので、研究者向けアクセス申請が開始された。一方OpenAIは同週に、数学的予想の反証という成果を発表しており、使用されたのはGPT-5.5系の汎用推論モデルである点が注目される。専用モデルなしに数学研究へ独立した貢献ができるなら、科学全般への応用も近いかもしれない（ただし科学では実験的検証が必要なためAIにはより困難な領域）。Googleは現在、これらのエージェントを「AI科学者」ではなく「AI共同研究者（AI Co-Scientist）」と位置づけており、人間中心の枠組みを維持しつつも、長期的にはAIが科学的進歩を独自に推進する未来を見据えていることがHassabisの発言から読み取れる。監査エージェント開発への示唆として、汎用推論能力を持つLLMエージェントが専門ドメイン（数学・科学）において独立した貢献を示し始めていることは、監査や内部統制領域においても特定タスク特化型モデルから汎用エージェントへの移行を検討すべき段階に来ていることを示唆する。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専門特化モデルなしに数学的予想の反証という独立した研究貢献を達成した事実は、専用ツール vs 汎用エージェントの議論において後者の優位性を示す具体的根拠となっている
- AlphaFoldノーベル賞受賞者がAIコーディング研究に転向したという人材配置の変化は、組織の戦略的優先度を公式発表以上に明確に示すシグナルとして読める
- 「AI Scientist」ではなく「AI Co-Scientist」という命名の選択は、現時点での能力の限界を認識しつつ将来の自律化を見据えた戦略的ブランディングであり、社会的受容とリスク管理を同時に考慮した設計思想を反映している

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 関連記事

- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6825 Google I/Oが示したAI駆動科学の方向性シフト——専用ツールから汎用エージェントへ

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
