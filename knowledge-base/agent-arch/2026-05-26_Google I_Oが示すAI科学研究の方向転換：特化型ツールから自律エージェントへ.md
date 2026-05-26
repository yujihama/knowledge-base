---
title: "Google I/Oが示すAI科学研究の方向転換：特化型ツールから自律エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-26
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, LLMエージェント, Google DeepMind]
category: "agent-arch"
related: [6461, 6370, 6585, 3430, 6435]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-26T21:25:29.245499"
---

## 要約

Google I/O 2026においてDeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と発言し、AI科学研究の将来像を示した。現在のAI科学研究には2つのアプローチが存在する。第一は、WeatherNextやAlphaFoldのような特定科学問題を解くために設計・訓練された専門特化型ツール。第二は、人間の介入を最小化して研究プロジェクトを自律実行できるLLMベースのエージェントシステムである。GoogleはGemini for Scienceパッケージを発表し、仮説生成AI「Co-Scientist」やアルゴリズム最適化AI「AlphaEvolve」を統合した。これらはまだ一般公開されていないが、研究者向けアクセス申請を受け付け始めた。スタンフォードの遺伝学者Gary Peltzは早期テストにおいてAI Co-Scientistを「デルフォイの神託への相談」と評した。一方でGoogleは特化型ツールを放棄していない。AlphaFoldはノーベル賞受賞後も世界300万人以上の研究者が利用し、AlphaFoldの関連技術を活用する創薬子会社Isomorphic Labsは20億ドルのシリーズB調達を完了した。しかしAlphaFoldのノーベル賞受賞者John JumperがAIコーディング部門に異動したことは、リソース配分の優先順位変化を示唆する。業界全体でもOpenAIの汎用推論モデルが数学の重要な予想を反証し、GPT-5.5系の汎用モデルが専門特化なしに研究貢献できることを示した。コーディング能力がエージェント科学システムの成功に不可欠であることから、GoogleがAnthropicやOpenAIに遅れをとるコーディングツールの強化とエージェント科学の推進が連動している。Hassabisは「今後10年はAIを科学者を支援するツールとして捉えるべき」としつつも、その先はコラボレーターになり得ると述べている。監査エージェント開発への示唆として、科学研究と同様に監査領域でも特化型ツールからLLMベースの汎用エージェントへの移行が進む可能性があり、仮説生成・証拠検証・報告書作成を一貫して担うエージェントアーキテクチャの設計が今後の競争優位になりうる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専門特化なしに数学の予想を反証できたことは、特化型ツール vs 汎用エージェントの議論において後者の優位性を示す具体的な証拠であり、エージェントアーキテクチャ設計の方向性に影響する
- AI Co-ScientistとAlphaEvolveをGemini for Scienceとして統合したアーキテクチャは、LLMエージェントが専門ツール（AlphaFold等）をサブモジュールとして呼び出す設計であり、監査エージェントにおけるツール統合パターンと同型である
- ノーベル賞受賞者JumperがAIコーディング部門へ異動した事実は、コーディング能力がエージェント科学（および汎用エージェント全般）の中核能力であるというGoogleの戦略的判断を示す

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / reasoning model** (TODO: 読むべき)
- **tool-use / function calling** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性

## 原文リンク

[Google I/Oが示すAI科学研究の方向転換：特化型ツールから自律エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
