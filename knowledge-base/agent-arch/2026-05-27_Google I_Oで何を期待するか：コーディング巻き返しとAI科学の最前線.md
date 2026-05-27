---
title: "Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線"
url: "https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/"
date: 2026-05-27
tags: [Google I/O, Claude Code, Codex, Antigravity, AI-for-science, AlphaEvolve, AI co-scientist, DeepMind, AlphaFold, LLMエージェント]
category: "agent-arch"
related: [6646, 6385, 6455, 6365, 6430]
memo: "[MIT Technology Review AI] What to expect from Google this week"
processed_at: "2026-05-27T21:11:50.928172"
---

## 要約

MIT Technology Reviewの記者がGoogle I/O 2026（マウンテンビュー）を前に、注目すべき3つのテーマを分析した記事。

**1. コーディング分野での巻き返し**
Googleは現在、基盤モデルレースで「明確な3位」と評される。コーディング能力でAnthropicのClaude CodeとOpenAIのCodexに大きく水をあけられており、DeepMindのエンジニアがClaude Codeの利用権をめぐって争っていたと報じられた。対策として、DeepMind内に専門のAIコーディングチームが新設され、AlphaFoldでノーベル化学賞（2024年）を受賞したJohn Jumperも参加している。I/Oではエージェント型コーディングプラットフォーム「Antigravity」のアップデートが発表される可能性があるが、内部モデルへのアクセスがあるGooglerでさえClaude Codeを求めていた状況から、劇的な逆転は困難と見られている。

**2. AIサイエンス分野**
Googleの強みはサイエンス応用にあり、フロンティアAI企業唯一のノーベル賞保持者。2025年には「AI co-scientist」（仮説生成・研究計画立案）や「AlphaEvolve」（数学・計算問題の反復的解法発見）をリリース済み。LLMがAI-for-scienceの主流となった現在、Googleの優位は維持されている。

**3. ヘルスケアとドラマ**
OpenAIがChatGPT Health（2026年1月）でヘルスAIの話題を独占する中、GoogleはAI搭載「Health Coach」を一般公開予定だが、フィットネス・食事アドバイスが中心でクリニカルユースには踏み込まない慎重な姿勢。また、I/O開催期間中はオークランドでElon Musk対Sam Altman裁判が進行し、DoD契約に反対するDeepMind社員600人による抗議書簡（Pichai宛）の翌日にGoogleが契約署名した件もくすぶっており、Hassabisが業界ドラマから距離を置くポジショニングを維持できるかが注目される。

**監査エージェント開発への示唆**
GoogleのAI co-scientistのアーキテクチャ（仮説生成→計画立案のループ）は、監査エージェントにおける「リスク仮説→調査計画→証拠収集」フローと構造的に類似しており、AI-for-scienceの設計パターンは監査エージェント設計の参考になり得る。

## アイデア

- コーディングエージェントの性能差がエンジニア生産性に直結し、競合他社のツールを社内利用せざるを得ない状況がGoogleで発生した点は、エージェントツールの評価軸として『内部採用率』が有効であることを示唆する
- GoogleのAI co-scientist（仮説→研究計画→検証のループ）とAlphaEvolve（反復的解法発見）は、ReActやLangGraphのエージェントループと本質的に同じ構造であり、科学的推論をエージェントアーキテクチャに組み込む設計として参照価値が高い
- ヘルスAIで医療判断を避け、フィットネス・栄養アドバイスに留めるGoogleの戦略は、高リスクドメイン（医療・監査）でのAIエージェント展開における責任境界設計の実例として捉えられる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **ReActフレームワーク** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **エージェント型コーディング** → /deep_6510 Google I/Oが示したAI駆動科学の転換：特化型ツールから汎用エージェントへ
- **AI-for-science** → /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題

## 関連記事

- /deep_6646 Google I/Oが示すAI科学研究の方向転換：特化型ツールから自律エージェントへ
- /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- /deep_6455 Google I/OはAI駆動科学の方向性がいかに変化しているかを示した
- /deep_6365 Google I/Oが示したAI駆動科学の方向転換：専門ツールから自律エージェントへ
- /deep_6430 Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ

## 原文リンク

[Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線](https://www.technologyreview.com/2026/05/18/1137439/what-to-expect-from-google-this-week/)
