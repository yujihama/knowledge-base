---
title: "Google I/Oが示したAI駆動科学の方向性シフト——専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-28
tags: [Google I/O, Claude Code, Codex, AlphaFold, AlphaEvolve, AI co-scientist, Antigravity, LLM-for-science, DeepMind, コーディングエージェント]
category: "agent-arch"
related: [6385, 6646, 6579, 3158, 3430]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-28T21:16:04.436139"
---

## 要約

2026年5月のGoogle I/Oを前にMIT Technology Reviewが分析した記事。現時点でGoogleは基盤モデル競争で「明確な3位」と位置づけられている。コーディング能力においてAnthropicのClaude CodeとOpenAIのCodexに大きく後れを取っており、DeepMindの一部エンジニアが社内ツールではなくClaude Codeを使用することを許可されたとThe Informationが報じた。この状況を受け、DeepMindに新設されたAIコーディングチームが対策に当たっており、2024年ノーベル化学賞受賞者（AlphaFold開発）のJohn Jumperもその取り組みに参加している。I/OではAntigravityというエージェント型コーディングプラットフォームの更新が発表される可能性があるとされるが、記者は「コーディングのフロンティアに2日間で追いつくことはないだろう」と予測している。一方でGoogleの強みは科学・医療AI分野にある。2025年にはAI co-scientist（仮説立案・研究計画生成システム）とAlphaEvolve（数学・計算問題の反復的解法探索システム）を公開しており、Stanford大学の科学者から「oracle（神託）」と評されるほどの評価を得ている。健康AI分野ではAI-powered Health Coachの一般公開が発表されたが、医療的懸念への対応よりフィットネス・食事アドバイスに特化した設計との指摘がある。同時期にオークランドではElon Musk対Sam Altman裁判が進行中で、AI業界の政治的緊張も高まっている。DeepMind内の約600名の従業員が米国防総省との契約に反対する書簡を送ったが、Googleは翌日署名した。記事全体を通じ、GoogleはコーディングAIでは劣勢にある一方、科学・医療領域では依然としてフロンティアを形成しており、I/Oでの発表もその二極構造を反映するとみられる。監査エージェント開発の観点では、AI co-scientistのような「仮説生成→検証計画→結果評価」のループ構造はReActベースの監査エージェントに応用可能であり、LLM-as-judgeとの組み合わせで内部統制評価の自動化に寄与しうる。

## アイデア

- GoogleがDeepMindエンジニアにClaude Code使用を許可したという事実は、内部評価でも競合製品が自社製品を上回っていることを示す——自社AIの品質管理指標としてLLM-as-judgeが機能していない可能性を示唆する
- AI co-scientistの「仮説→研究計画→評価」ループはReActエージェントの思考サイクルと構造的に同一であり、監査エージェントにおける「リスク仮説→証拠収集→判断」フローに直接転用できる
- AlphaEvolveの「反復的解法探索」アプローチは、GRPO/RLAIFにおける報酬最大化ループと近接しており、数学的証明の自動探索から監査手続の最適化へと応用範囲が広がる

## 前提知識

- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **GRPO/RLAIF** (TODO: 読むべき)
- **エージェント型コーディング** → /deep_6510 Google I/Oが示したAI駆動科学の転換：特化型ツールから汎用エージェントへ

## 関連記事

- /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- /deep_6646 Google I/Oが示すAI科学研究の方向転換：特化型ツールから自律エージェントへ
- /deep_6579 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oが示したAI駆動科学の方向性シフト——専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
