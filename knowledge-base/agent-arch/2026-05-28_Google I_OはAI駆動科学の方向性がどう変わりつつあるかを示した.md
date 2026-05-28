---
title: "Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-28
tags: [agentic-AI, AI-for-science, AlphaFold, Gemini-for-Science, AlphaEvolve, Co-Scientist, WeatherNext, recursive-self-improvement, 汎用推論モデル]
category: "agent-arch"
related: [6733, 6510, 3220, 6461, 6370]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-28T09:18:11.270837"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEO Demis Hassabisは「シンギュラリティの山麓に立っている」と宣言した。しかしその文脈は、汎用AGIではなく気象予測AIのWeatherNextによるハリケーン・メリッサのジャマイカ上陸事前警告という具体的な成果の紹介だった。この対比は、科学AIの2つのアプローチ間の緊張を象徴している。第1のアプローチは、AlphaFold（タンパク質折り畳み）、WeatherNext（気象予測）、AlphaGenome（遺伝学）、AlphaEarth Foundations（地球科学）のような特定問題に特化した専用AIツール。第2は、LLMベースのエージェントシステムが人間の関与を最小化して研究を自律的に推進するアプローチである。Googleは後者への移行を示唆するシグナルを複数出している。AlphaFoldでノーベル賞を受賞したJohn JumperがAIコーディング分野に異動したこと、Google I/OでGemini for Scienceという統合ブランドを発表し仮説生成AIのCo-Scientistとアルゴリズム最適化AIのAlphaEvolveを束ねたこと、そして一般研究者向けアクセス申請を開放したことがその証拠だ。一方で、AlphaFoldのタンパク質構造予測は世界300万人以上の研究者が使用しており、子会社Isomorphic Labsは20億ドルのシリーズB資金調達を完了するなど、専用ツールの需要は依然高い。OpenAIも今週、汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表しており、専用チューニングなしの汎用エージェントが研究に貢献できることを示した。Googleは「AI Co-Scientist」という命名を意図的に選び、AIを科学者の代替ではなく協調者として位置づけている。しかし実質的には、特化型ツール開発から自律型エージェント研究への重心移動が進んでおり、長期的には人間と対等あるいはそれ以上の能力を持つAI科学者の実現を目指す方向性が読み取れる。監査エージェント開発の観点では、汎用推論モデルが専用ツールなしに高度な論理推論・仮説検証を行える段階に近づいていることは、監査ドメイン特化モデルより汎用LLM＋エージェント設計を優先すべき根拠となりうる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証した事例は、ドメイン特化チューニングなしでも研究貢献が可能であることを示しており、専用AIツール開発の費用対効果を根本から問い直す
- Gemini for Scienceはエージェントと特化ツール（AlphaFold等）の統合アーキテクチャを採用しており、エージェントが必要に応じてツールをcallするオーケストレーション設計は監査エージェントのツール統合設計に直接応用可能
- AlphaFoldで実績のあるJohn JumperをAIコーディング分野に移動させたことは、コーディング能力がエージェント型科学研究の基盤として戦略的に重要視されていることを示す

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / Tool-use** (TODO: 読むべき)
- **汎用推論モデル（o3系）** (TODO: 読むべき)

## 関連記事

- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6510 Google I/Oが示したAI駆動科学の転換：特化型ツールから汎用エージェントへ
- /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
