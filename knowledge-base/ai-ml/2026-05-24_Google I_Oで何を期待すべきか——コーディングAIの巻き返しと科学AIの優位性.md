---
title: "Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-24
tags: [Google I/O, Claude Code, Codex, AlphaFold, AI co-scientist, AlphaEvolve, Antigravity, DeepMind, LLM評価, コーディングAI]
category: "ai-ml"
related: [6385, 3125, 3158, 3430, 3086]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-24T09:16:36.193283"
---

## 要約

MIT Technology Reviewによる2026年Google I/O直前の展望分析記事。現状の評価として、GoogleはLLM基盤モデルレースで「明確な3位」に転落しており、特にコーディング能力でAnthropicのClaude CodeとOpenAIのCodexに大きく劣後している。その証左として、DeepMindのエンジニアがGoogleの内部ツールではなくClaude Codeのアクセス権をめぐって争っていたという報道が引用されている。

注目点1：コーディングの巻き返し。DeepMindには新設のAIコーディング専門チームが存在し、AlphaFoldで2024年ノーベル化学賞を受賞したJohn Jumperも参画しているとされる。I/OではAgentic CodingプラットフォームであるAntigravityのアップデートが発表される可能性が高い。ただし、内部の最先端モデルを使えるDeepMinderでさえClaude Codeを求めていた事実を踏まえると、2日間で業界最前線まで追いつくことは期待できないとしている。

注目点2：科学・ヘルスケアAI。Googleはフロンティアモデル企業の中でノーベル賞を獲得した唯一の組織であり、AI-for-scienceでは突出した強みを持つ。2025年には「AI co-scientist」（仮説立案・研究計画生成システム）やAlphaEvolve（数学・計算問題の反復的解法探索システム）を相次いでリリース。I/Oではさらなる科学AIツールの発表が見込まれる。ヘルスケア分野ではAI-powered Health Coachの一般公開が予告されているが、フィットネス・食事アドバイスに特化した内容であり、医療的懸念への対応能力でOpenAI（ChatGPT Health、2026年1月リリース）に後れを取っているとの見方もある。

注目点3：業界ドラマ。I/Oと同時期にオークランドでElon Musk対Sam Altman裁判の最終局面が進行。Googleは600名の従業員（多くがDeepMind所属）がDOD（米国防総省）との契約に抗議するレターをCEO Sundar Pichai宛てに送付したにもかかわらず翌日に契約を締結した事案を抱えており、中立的イメージの維持が課題となっている。

監査エージェント開発への示唆：AI co-scientistの「仮説立案→研究計画生成」というアーキテクチャはReActエージェントの実用的応用例として参照価値が高い。また、コーディングAI市場でClaude Codeが業界内部でも採用されている事実は、LLM-as-judgeや監査レポート生成における同モデルの信頼性を間接的に裏付ける。

## アイデア

- DeepMindのエンジニア自身がClaude Codeを選好していたという事実は、内部評価としての強力なLLM-as-judgeシグナルであり、公開ベンチマークを超えた実用信頼性の指標になりうる
- AlphaEvolveの「反復的解法探索」アーキテクチャは、監査手続きの自動最適化（手続き候補の生成→評価→改善ループ）に応用できる可能性がある
- AI co-scientistの仮説立案機能は、内部統制の弱点仮説を自動生成してリスク評価に組み込むエージェント設計のモデルケースとして参照できる

## 前提知識

- **LLM基盤モデル** (TODO: 読むべき)
- **Agentic Coding** → /deep_191 Generative UI: あらゆるプロンプトに対応するリッチでカスタムなビジュアル・インタラクティブUX
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **AI-for-science** → /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題

## 関連記事

- /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- /deep_3125 AIに対する意見がこれほど分かれる理由：専門家と一般人の50ポイント差
- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_3086 なぜ、Claude CodeもCodexもエージェントではありえないのか？

## 原文リンク

[Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
