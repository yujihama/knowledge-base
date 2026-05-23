---
title: "Google I/Oが示したAI駆動科学の方向転換：専門ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-23
tags: [agentic-AI, AI-for-science, Gemini-for-Science, AlphaFold, Co-Scientist, AlphaEvolve, WeatherNext, recursive-self-improvement, LLM-agent, Google-DeepMind]
category: "agent-arch"
related: [3220, 6333, 6251, 6140, 6170]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-23T09:10:49.583463"
---

## 要約

Google I/O 2026でDeepMind CEOのDemis Hassabisは「特異点の山麓に立っている」と宣言し、科学AIの文脈でその発言をした。具体的な成果として挙げたのは気象予測システム「WeatherNext」で、ジャマイカに壊滅的な上陸をしたハリケーン・メリッサの事前警報を発し、人命救助に貢献した可能性がある。しかしこの発表は、AIによる科学の2つのアプローチ間の緊張を浮き彫りにした。第一のアプローチは、AlphaFoldやWeatherNextのような特定問題に特化した専門ツール。第二は、最終的に人間の関与なしに最先端研究を遂行できる可能性を持つ、LLMベースの自律エージェントシステムである。Googleはこの第二のアプローチへのリソースシフトを示唆している。AlphaFoldでノーベル賞を受賞したJohn JumperをAIコーディング部門に異動させたことがその証左だ（AnthropicやOpenAIのコーディングツールに競争優位を奪われている背景もある）。今回発表された「Gemini for Science」パッケージは、仮説生成AI「Co-Scientist」と、アルゴリズム最適化「AlphaEvolve」を統合したLLMベースの科学支援システム群であり、研究者申請制で公開予定。スタンフォード大学の遺伝学者Gary Peltzは初期テストでCo-Scientistを「デルフォイの神託に相談するようだ」とNature Medicine誌で評価した。一方、OpenAIは汎用推論モデル（GPT-5.5系統）を使って重要な数学的予想を反証することに成功し、AIが専門特化なしに独立した研究貢献を行えることを示した。業界全体としてrecursive self-improvementへの期待が高まっており、AIシステムがAI進歩そのものの主要ドライバーになる可能性が議論されている。Googleは公式には「AI Co-Scientist（AIサイエンティストではなく）」という命名にも表れるように、人間科学者の加速ツールとして位置づけているが、Hassabisは10年超のスパンでは「コラボレーター」へ進化する可能性を示唆。AlphaFoldは依然として世界300万人以上の研究者に利用され、Isomorphic Labsが20億ドルのシリーズB資金調達を実施するなど専門ツールへの需要は旺盛だが、Googleの重心は明確にエージェント科学へ移りつつある。監査エージェント開発への示唆として、汎用推論モデルが専門訓練なしに数学的証明を行えたという事実は、LangGraph等で構築する監査エージェントも特定ドメインへの過剰な専門化よりも、強力な汎用推論基盤の上に軽量なドメイン知識を乗せるアーキテクチャが有効である可能性を示している。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証できたという事実は、専門特化vs汎用エージェントの設計判断において、汎用基盤＋軽量ドメイン知識という構成の優位性を示す実証例になりうる
- Co-Scientistの命名が「AI Scientist」でなく「AI Co-Scientist」である点は、規制・倫理面での受容性を高める戦略的フレーミングであり、監査AIでも「AIによる自律判断」ではなく「AIによる監査支援」として設計・命名する際に参考になる
- AlphaFold開発者をコーディングAI部門へ異動させるというGoogleの人材配置は、科学特化ツールよりもコーディング能力がエージェント科学の基盤として重要視されていることを示しており、エージェント構築においてコード生成・実行能力が中核能力であることを裏付ける

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** (TODO: 読むべき)
- **Gemini** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **agentic reasoning** (TODO: 読むべき)

## 関連記事

- /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_6333 Google I/O 2026：コーディングAIでの挽回、科学AI、そして業界ドラマ
- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6140 Google I/O 2026のAI発表を読むエンジニア・研究視点
- /deep_6170 Google I/O 2026に向けた期待：コーディングAIの挽回、科学AI、業界ドラマ

## 原文リンク

[Google I/Oが示したAI駆動科学の方向転換：専門ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
