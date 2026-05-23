---
title: "Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-23
tags: [Claude Code, Google I/O, Antigravity, AlphaFold, AlphaEvolve, AI co-scientist, DeepMind, コーディングエージェント, AI-for-science]
category: "agent-arch"
related: [6365, 3158, 3220, 3430, 2964]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-23T21:04:10.611057"
---

## 要約

MIT Technology Reviewの記者がGoogle I/O 2026（マウンテンビュー）に向けた事前分析記事。2025年のGoogle I/O時点ではGemini 2.5 Proが強力なポジションにあったが、2026年時点ではAnthropicのClaude CodeおよびOpenAIのCodexに対してコーディング能力で明確な劣位に立たされている。この差は深刻で、DeepMindの一部エンジニアが社内ツールではなくClaude Codeを業務利用することをGoogleが許可するまでに至ったとThe Informationが報道している。

対策としてDeepMindにはAIコーディング専任チームが新設され、2024年ノーベル化学賞を（Hassabisとともに）受賞したJohn Jumper（AlphaFold開発者）がその取り組みに加わっているとLos Angeles Timesが報道。アジェンティックコーディングプラットフォーム「Antigravity」のアップデートが発表される可能性が高いが、記者はClaude Codeに対抗できるレベルに到達するとは考えていない。

一方で科学・ヘルス分野ではGoogleが強みを持つ。2025年には仮説生成・研究計画立案AI「AI co-scientist」、数学・計算問題の解法を反復的に発見する「AlphaEvolve」をリリース。スタンフォードの研究者からは「oracle（神託）」と評されるほど。I/O 2026でも新たな科学AIツールの発表が期待される。ヘルス分野ではChatGPT Health（2026年1月）にOpenAIに先行を許しているが、「AI-powered Health Coach」をI/Oで公開予定。ただしフィットネス・食事アドバイス中心で医療診断には踏み込まない慎重な設計とされている。

また背景として、Elon Musk対Sam Altman裁判（オークランド）がI/Oと同時期に進行しており、AI業界のガバナンス・CEO間の政治的緊張が高まっている。Google内でも600名の従業員がDoD（国防総省）との契約に抗議する書簡をSundar Pichai宛に送ったが、Googleは翌日そのまま契約を締結した。HasssabisはCEO間の公開的な対立から距離を置くスタンスを維持している。

監査エージェント開発への示唆：コーディングエージェント能力の差がエンタープライズ採用に直結することがGoogleの事例で実証された。エージェントシステムの能力評価において「コーディングベンチマーク」が現在の業界標準となっており、LangGraphやReActを用いた監査エージェント評価にも同様の定量指標設計が重要になる。

## アイデア

- コーディング能力が基盤モデルの評価基準として事実上の業界標準となり、GoogleのエンジニアがClaude Codeを選択したという事実がエージェント能力の実用評価の指標になっている
- AlphaFold・AlphaEvolveのような科学特化型AIとLLMベースの汎用コーディングエージェントは異なる開発トラックで進化しており、GoogleはScience側で独自優位を維持している
- AI Health CoachがフィットネスアドバイスにとどまりOpenAIのHealth機能に対抗できていない点は、医療ドメインにおけるリスク管理とAgentの責任範囲設計のトレードオフを示す

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Gemini 2.5 Pro** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **アジェンティックコーディング** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_6365 Google I/Oが示したAI駆動科学の方向転換：専門ツールから自律エージェントへ
- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_2964 LLMコーディングエージェントの振る舞いを制約する設計思想

## 原文リンク

[Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
