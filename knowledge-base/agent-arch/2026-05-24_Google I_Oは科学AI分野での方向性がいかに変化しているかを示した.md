---
title: "Google I/Oは科学AI分野での方向性がいかに変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-24
tags: [Google I/O, Gemini, Claude Code, AlphaFold, AlphaEvolve, AI co-scientist, Antigravity, コーディングAI, 科学AI]
category: "agent-arch"
related: [3430, 6430, 3158, 3297, 6365]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-24T21:06:03.089018"
---

## 要約

MIT Technology ReviewのAIニュースレター「The Algorithm」による2026年5月のGoogle I/O直前の展望記事。Googleは2026年時点でAI基盤モデルのレースにおいて明確に3位に後退している。2025年3月のGemini 2.5 Pro発表時は首位争いをしていたが、現在はコーディング能力でAnthropicのClaude CodeとOpenAIのCodexに大きく水をあけられており、DeepMindのエンジニアが社内ツールではなくClaude Codeを使わざるを得ない状況が報じられている。

対応策として、DeepMind内部に新たなAIコーディングチームが設立され、2024年ノーベル化学賞受賞者（AlphaFoldのタンパク質構造予測への貢献でDemis HassabisとともにJohn Jumperが受賞）がコーディングAI開発に参加している。I/Oでは同社のエージェント型コーディングプラットフォーム「Antigravity」のアップデートが期待されるが、社内エンジニアでさえClaude Codeを選んでいた状況から、コーディングフロンティアへの即時復帰は難しいと分析されている。

一方、科学AIはGoogleの強みである。同社はAlphaFoldでノーベル賞を獲得した唯一のフロンティアAI企業であり、2025年にはAI co-scientist（仮説立案・研究計画策定）とAlphaEvolve（数学・計算問題の反復的解法探索）をリリースしている。ヘルスケアAIではHealth Coachを正式公開予定だが、医療相談よりも健康・食事アドバイスに特化しており、OpenAIのChatGPT Health（2026年1月リリース）と比較して保守的な位置づけとなっている。

社内ではDoD（米国防総省）との契約に抗議する600人のDeepMind社員署名があり、翌日に契約締結されるという内部摩擦も存在する。CEO Demis Hassabisはノーベル賞科学者としての中立的イメージを維持しているが、競合CEO間の確執（Altman対Amodei、Musk対Altman裁判）とは一線を画している。

監査エージェント開発への示唆：AlphaEvolveのような「反復的解法探索」と「AI co-scientistの仮説立案」のアーキテクチャは、監査シナリオにおける異常仮説の自動生成や検証ループの設計に応用できる可能性がある。

## アイデア

- フロンティアAI企業の自社エンジニアが競合ツール（Claude Code）を使わざるを得ない状況は、モデル能力の差が内部生産性指標に直結していることを示しており、コーディングベンチマーク以上の実証データとなっている
- AlphaEvolveの「反復的解法探索」とAI co-scientistの「仮説立案・研究計画策定」を組み合わせたアーキテクチャは、監査における不正仮説の自動生成→証拠収集→検証ループのエージェント設計に応用できる
- ノーベル賞受賞科学者（John Jumper）をコーディングAIチームに投入するという人材戦略は、科学的厳密さをソフトウェアエンジニアリング品質に転用しようとする実験的なアプローチである

## 前提知識

- **Gemini 2.5 Pro** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **エージェント型コーディング** → /deep_2660 CodeComp：エージェント型コーディング向け構造的KVキャッシュ圧縮
- **LLM-as-scientist** (TODO: 読むべき)

## 関連記事

- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_6430 Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ
- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_3297 人工科学者：AIが自律的な研究者になる日
- /deep_6365 Google I/Oが示したAI駆動科学の方向転換：専門ツールから自律エージェントへ

## 原文リンク

[Google I/Oは科学AI分野での方向性がいかに変化しているかを示した](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
