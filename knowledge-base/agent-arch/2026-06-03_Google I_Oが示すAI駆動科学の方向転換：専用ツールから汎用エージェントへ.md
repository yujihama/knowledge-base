---
title: "Google I/Oが示すAI駆動科学の方向転換：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-03
tags: [AgenticAI, 科学AI, AlphaFold, WeatherNext, GeminiForScience, AlphaEvolve, Co-Scientist, LLM, 自律エージェント, recursive self-improvement]
category: "agent-arch"
related: [6251, 6461, 6370, 6299, 6710]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-03T21:14:41.170141"
---

## 要約

2026年のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「特異点の山麓に立っている」と宣言した。この発言の文脈は科学AIのセッションであり、同社の気象予測ソフト「WeatherNext」がハリケーン・メリッサのジャマイカ上陸を事前警告し、人命救助に貢献した実績が紹介された。この場面は、科学AIにおける2つのアプローチの対立を象徴している。一方は特定の科学課題を解くために設計・訓練された専用ツール（AlphaFold、WeatherNext、AlphaGenome、AlphaEarth Foundationsなど）、もう一方はLLMベースの汎用エージェントシステムで、自律的に最前線の研究を遂行することを目指す。

Googleは現在、後者の方向へ軸足を移しつつある。その象徴がGoogle I/Oで発表された「Gemini for Science」パッケージで、仮説生成AIの「Co-Scientist」と、アルゴリズム最適化を行う「AlphaEvolve」を統合している。両者はまだ一般公開されていないが、すべての研究者がアクセス申請できる体制が整えられた。スタンフォードの遺伝学者Gary Peltzは、AI Co-Scientistの使用を「デルフォイの神託に相談するようなもの」と評している。

リソース配分の変化も具体的に表れている。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn Jumperが、現在はAIコーディング分野に移っているとLAタイムズが報道。コーディング能力はAnthropicやOpenAIと比較して評価が低いというGoogleの課題への対応でもあるが、同時にエージェント型科学AIの推進を意味する可能性が高い（コーディング能力はエージェントシステムの中核機能だからだ）。

OpenAIの動向も同方向を示しており、同週に一般目的推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表された。数学者の間ではこれが生成AIの数学への最も意義深い貢献と評価されており、実験的検証が必要な科学領域への波及も議論されている。

Googleは「AI科学者」ではなく「AI Co-Scientist」という命名を意図的に選び、人間の科学者を支援する位置づけを強調している。Hassabisも「今後10年は科学者を助ける驚異的なツール」と述べ、長期的には「コラボレーター」へと進化すると示唆した。ただし、AlphaFoldが世界300万人以上の研究者に利用されている実績や、AlphaFoldを核にしたIsomorphic Labsが20億ドルのシリーズB調達をした事実が示すように、専用ツールの需要は依然として巨大であり、完全な移行ではなく「重心の移動」と見るのが適切だ。監査エージェント開発への示唆としては、汎用推論モデルが専用ツールを呼び出す設計（Gemini for ScienceがAlphaFoldを利用する構造）は、監査エージェントが会計基準検索・異常検知モデル・法令DBなど専用ツールをオーケストレーションするアーキテクチャに直接応用できる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専用訓練なしで数学的予想を反証できたことは、ドメイン特化ファインチューニングなしでも専門的推論が達成される臨界点が近づいていることを示す
- Gemini for ScienceがAlphaFoldなど専用ツールをエージェントから呼び出す設計は、監査エージェントが会計基準DB・異常検知モデル・法令APIを動的に呼び出すオーケストレーション設計のロールモデルになりうる
- AlphaFoldのノーベル賞受賞者が科学AIから汎用コーディングAIへ異動という人材再配置は、技術トレンドの転換点を組織構造の変化で読む指標として使える

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **tool calling / function calling** (TODO: 読むべき)
- **ReAct / Chain-of-Thought** (TODO: 読むべき)

## 関連記事

- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6299 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI強化
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向

## 原文リンク

[Google I/Oが示すAI駆動科学の方向転換：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
