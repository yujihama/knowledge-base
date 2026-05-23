---
title: "Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-23
tags: [Google I/O, Claude Code, Codex, Antigravity, AlphaFold, AlphaEvolve, AI co-scientist, DeepMind, コーディングエージェント, 科学AI]
category: "ai-ml"
related: [3430, 3158, 3297, 3086, 2541]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-23T09:14:04.983658"
---

## 要約

MIT Technology Reviewの記者がGoogle I/O 2026開幕前夜に書いた展望記事。現時点でGoogleは基盤モデル競争において「明確な3位」と評されており、その主因はコーディング能力の劣後にある。Anthropic の Claude Code と OpenAI の Codex に大幅に水をあけられており、DeepMind 社内のエンジニアでさえ自社ツールを使わず Claude Code の利用権を奪い合っていたという報道（The Information）が出るほど深刻な状況だ。

対策としてDeepMindにAIコーディング専門チームが新設され、AlphaFoldでノーベル化学賞（2024年）を受賞したJohn Jumperもその開発に関与していると報じられている（Los Angeles Times）。I/Oでは同社のエージェント型コーディングプラットフォーム「Antigravity」のアップデートが発表される可能性がある。ただし、社内では公開版より大幅に先行したモデルにアクセスできるエンジニアたちも Claude Code を好んだという事実を考えると、2日間のカンファレンスで業界最前線に返り咲くことは困難と著者は見ている。

科学・医療分野はGoogleの強みで、唯一ノーベル賞を持つフロンティアAI企業として、AI co-scientist（仮説立案・研究計画支援）やAlphaEvolve（数学・計算問題の反復的解法探索）など複数の科学AIツールを2025年に公開済み。I/Oでの新たな科学AIの発表が期待される。ヘルスAIについては、AI-powered Health Coachの一般公開がアナウンスされているが、フィットネス・ダイエットなどのアドバイス用途に限定されており、OpenAIが1月に打ち出したChatGPT Healthのような医療寄りの用途とは一線を画す。

また社内では、600名超の従業員（多数がDeepMind所属）がDoD（米国防総省）との契約に抗議する書簡をSundar Pichai CEOに送ったが、翌日にGoogleはそのまま契約を締結したという経緯もある。監査AIや政府契約にまつわるガバナンス上の緊張も高まっている。

監査エージェント開発への示唆：エージェント型コーディングツール（Claude Code、Codex、Antigravity）のアーキテクチャ競争は、自律的なコード生成・検証ループの設計力が差別化要因になっていることを示しており、監査エージェントにおける自律的なテスト生成・根拠検証の仕組みを設計する際の参考になる。

## アイデア

- 社内エンジニアが自社モデルより競合（Claude Code）を好んだという事実は、ベンチマーク数値と実務利用満足度の乖離を示す実例であり、エージェント評価指標設計の難しさを浮き彫りにする
- AlphaFoldのノーベル賞受賞者John JumperをコーディングAI開発に投入するという人材戦略は、科学的推論能力をコード生成に転用しようとする仮説を示唆しており、推論重視のコーディングモデルへのトレンドと整合する
- Google Health Coachがフィットネス・ダイエット止まりで医療用途を避けているのは技術的限界ではなくリスク管理の判断である可能性が高く、高リスクドメインでのLLM展開における責任範囲の設計思想として参考になる

## 前提知識

- **LLM基盤モデル** (TODO: 読むべき)
- **エージェント型コーディング** → /deep_2660 CodeComp：エージェント型コーディング向け構造的KVキャッシュ圧縮
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **Reinforcement Learning from Human Feedback** (TODO: 読むべき)
- **DoD AI契約** (TODO: 読むべき)

## 関連記事

- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_3297 人工科学者：AIが自律的な研究者になる日
- /deep_3086 なぜ、Claude CodeもCodexもエージェントではありえないのか？
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？

## 原文リンク

[Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
