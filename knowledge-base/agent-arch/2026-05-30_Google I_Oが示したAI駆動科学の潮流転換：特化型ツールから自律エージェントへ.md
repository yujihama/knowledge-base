---
title: "Google I/Oが示したAI駆動科学の潮流転換：特化型ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-30
tags: [Gemini for Science, AlphaFold, AI Co-Scientist, AlphaEvolve, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, agentic research]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-30T09:13:13.261491"
---

## 要約

2026年5月のGoogle I/Oで、DeepMind CEOのDemis Hassabisは「特異点の麓に立っている」と宣言し、科学AIの方向性が大きく転換していることを示した。従来のアプローチは、AlphaFold（タンパク質構造予測でノーベル賞）やWeatherNext（ハリケーン・メリッサの上陸前警報を発出）のような特定問題に特化した訓練済みモデルの開発だった。新たなアプローチは、LLMベースの自律エージェントが人間の介入なしに研究を実行するというビジョンであり、Googleは「Gemini for Science」として仮説生成AIのCo-Scientistと、アルゴリズム最適化のAlphaEvolveを統合したパッケージを発表した（まだ一般公開前で研究者が申請可能な段階）。転換の具体的なシグナルとして、AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門に異動した事実がある。これはGoogleのコーディングツールがAnthropicやOpenAIに対して競争力を失っているという背景もあるが、エージェント型科学AIではコーディング能力が中核となるため、戦略的な人材配置とも読める。同週にOpenAIも汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したと発表しており、特化型でない汎用エージェントが独立した研究貢献をする事例が現れ始めた。一方、AlphaFoldは世界300万人以上の研究者が利用し、子会社Isomorphic Labsは20億ドルのSeries B調達に成功するなど、特化型ツールの需要は依然として旺盛。Gemini for Scienceは特化型ツールとの併用を前提として設計されており（例：タンパク質構造予測にはAlphaFoldを呼び出す）、完全な置き換えではなく、エージェントが特化ツールをオーケストレーションする構造が志向されている。Hassabisは「今後10年はAIを科学者を支援するツールとして考えるべきだが、それ以降はコラボレーターとなる可能性がある」と述べており、AI Co-ScientistとAI Scientistの命名の違いにも慎重な人間中心フレーミングが反映されている。監査エージェント開発への示唆：自律型科学エージェントと特化型ツールのハイブリッドアーキテクチャは、監査エージェントの設計にも直接応用可能。汎用LLMエージェントが仮説立案・調査計画を担い、特化型モジュール（財務データ解析、異常検知）をツールとして呼び出す構成は、Gemini for Scienceが示すオーケストレーションパターンそのものである。

## アイデア

- 汎用推論モデル（GPT-5.5系）が特化訓練なしで数学的予想を反証した事実は、特化型モデルvs汎用エージェントの優位性議論に実証的なデータポイントを加える
- AlphaFoldノーベル賞受賞者JumperのコーディングAI部門への異動は、エージェント型AIではコーディング能力がコア能力であることを示す人材戦略の読み方ができる
- Gemini for ScienceがAI Co-ScientistとAlphaEvolveを統合した構造は、LLMオーケストレーター＋特化ツール群というハイブリッドアーキテクチャの実装例として参照価値がある

## 前提知識

- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ツール呼び出し（function calling）** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **科学的仮説生成AI** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oが示したAI駆動科学の潮流転換：特化型ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
