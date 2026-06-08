---
title: "Copilot CLI モデル別コスパ比較 (2026年6月版) — SWE-bench × Pareto frontier"
url: "https://zenn.dev/takyone/articles/copilot-cli-cost-2026-06"
date: 2026-06-08
tags: [GitHub Copilot, SWE-bench, Pareto frontier, LLM cost, Claude Opus 4.8, GPT-5.4, usage-based billing, blended cost, agentic loop]
category: "infra"
related: [7337, 2920, 2889, 6194, 395]
memo: "[Zenn LLM] Copilot CLI モデル別コスパ比較 (2026 年 6 月版) — SWE-bench × Pareto frontier"
processed_at: "2026-06-08T21:01:38.000098"
---

## 要約

2026年6月1日からGitHub Copilot CLIがpremium-request制からAIクレジット制（1 credit = $0.01）のusage-based billingに移行した。これにより `--model` の選択がそのまま月末請求額に直結するため、SWE-bench Verified（標準難度、500タスク）とSWE-bench Pro（高難度、multi-file diff）の2軸でモデルの性能を定量評価し、blended costと組み合わせたPareto frontier分析を行った。

コスト計算にはinput:outputトークン比率が異なる3プロファイル（Light 1.5:1 / Standard 4:1 / Heavy 10:1）を設定し、メイン分析はStandard（4:1）で実施。Pareto最適とは「同コストでより高性能、または同性能でより安価な代替が存在しない」モデルのことで、frontier外のモデルには必ず支配的な代替が存在する。

SWE-bench Verified（GA限定frontier）では Haiku 4.5（$1.8/1M, 73.3%）→ GPT-5.4（$5.0/1M, 80.0%）→ Opus 4.8（$9.0/1M, 88.6%）の3段。SWE-bench Pro（高難度frontier）では GPT-5.4 mini（$1.5/1M, 54.4%）→ Gemini 3.5 Flash（$2.7/1M, 55.1%）→ GPT-5.4（$5.0/1M, 57.7%）→ Opus 4.8（$9.0/1M, 69.2%）の4段が最もrobustな選択肢。

主要な発見として：(1) GPT-5.5（$10.0/1M, SWE-Pro 58.6%）はOpus 4.7（$9.0/1M, 64.3%）にdominateされ圏外；(2) Gemini 3.1 Pro Preview（SWE-Pro 54.2%, $4.0）はGemini 3.5 Flash GA（55.1%, $2.7）に劣るためPreviewの優位はVerifiedのみ；(3) Opus 4.7→4.8の世代差はVerified 1ptに対しPro 5ptと大きく、Pro軸の方が弁別力が高い。GPT-5.4からOpus 4.8への限界費用はSWE-Pro 1ptあたり$0.35/1Mと最も安く、escalate先として合理的。

監査エージェント開発への示唆：agentic loopのような多ファイル・長時間タスク（Heavy 10:1相当）ではinputトークンが膨らむため、input単価の低いモデル（GPT-5.4 mini $0.75/1M、Gemini 3.5 Flash $1.50/1M）のコスト優位が拡大する。タスク複雑度に応じてこの4段階を使い分けるルーティング戦略が費用対効果を最大化する。

## アイデア

- SWE-bench VerifiedとProの2軸を同時にプロットすることで、memorization懸念のあるVerified単独評価の盲点を補う方法論：ProはPublic ground-truthの汚染を防ぐ設計で、Verified 80%超の飽和帯でも差が出る
- input:output比率（Light 1.5:1 / Standard 4:1 / Heavy 10:1）でfrontierの形状が変わるという洞察：Heavy寄りのagentic workloadではinput単価の軽いモデルの優位が拡大し、最適なescalation閾値が変動する
- GPT-5.5がOpus 4.7にdominateされるという反直感的結果：高性能＝高コストが常に成立しないことをPareto分析で定量的に示した点。frontier外モデルを一律除外せず「specific用途（long-context等）での正当化条件」も整理している点も実践的

## 前提知識

- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Pareto frontier** (TODO: 読むべき)
- **usage-based billing** → /deep_7337 GitHub CopilotでユーザーごとにAICreditの上限を設定しダッシュボードで可視化する方法
- **blended cost** (TODO: 読むべき)
- **agentic loop** (TODO: 読むべき)

## 関連記事

- /deep_7337 GitHub CopilotでユーザーごとにAICreditの上限を設定しダッシュボードで可視化する方法
- /deep_2920 見て・指して・磨く：視覚フィードバックを用いたGUI接地のマルチターンアプローチ
- /deep_2889 現在のAIの状況を理解するためのチャート集：Stanford AI Index 2026レポート解説
- /deep_6194 急変するAIコードレビューツール市場：2026年版比較と選び方
- /deep_395 図形入りの PowerPoint を Markdown に変換する方法（GitHub Copilot + OpenXML SDK）

## 原文リンク

[Copilot CLI モデル別コスパ比較 (2026年6月版) — SWE-bench × Pareto frontier](https://zenn.dev/takyone/articles/copilot-cli-cost-2026-06)
