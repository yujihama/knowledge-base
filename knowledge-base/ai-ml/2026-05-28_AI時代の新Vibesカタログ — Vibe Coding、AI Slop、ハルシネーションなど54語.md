---
title: "AI時代の新Vibesカタログ — Vibe Coding、AI Slop、ハルシネーションなど54語"
url: "https://zenn.dev/inspector/articles/ai-era-new-vibes-catalog"
date: 2026-05-28
tags: [Vibe Coding, Agentic Engineering, Context Engineering, AI Slop, Sycophancy, Reward Hacking, Hallucination, Cognitive Debt, Slopsquatting, Intent Debt, RLHF, LLM-as-judge]
category: "ai-ml"
related: [111, 1353, 2451, 155, 4289]
memo: "[Zenn LLM] AI時代の新Vibesカタログ ー Vibe Coding、AI Slop、ハルシネーションなど54語"
processed_at: "2026-05-28T09:08:40.093558"
---

## 要約

ChatGPT登場（2022年11月）以降に生まれたAI関連の新概念・用語54語を体系的に整理したZenn記事。人の働き方・認知能力・アウトプット品質・モデル挙動・社会経済的影響などのカテゴリに分類して解説している。

【働き方】Vibe Coding（カルパシーが2025-02命名、コードを読まずAIに全委託）とその対極のAgentic Engineering（ウィリソンが2026-02提唱、テスト・コミット管理などソフトウェア工学規律を維持）が対比される。Context Engineering（Shopify CEO リュトケが2025-06提唱）はPrompt Engineeringの上位集合で、コンテキストウィンドウへの情報設計を技芸とする概念。METR生産性パラドックスでは、Cursor Pro＋Claude 3.5/3.7使用でOSS開発者16名のタスク完了時間が+19%増（遅化）したRCT結果が注目される。

【認知負債系】AI依存によりCognitive Debt（MIT Media Lab、脳ネットワーク連結性低下、N=54）、Critical Thinking Decline（Microsoft Research×CMU、N=319）、Skill Atrophy（コード読解力・第一原理思考力の段階的喪失）が蓄積する。

【アウトプット品質】AI Slop（ウィリソン2024-05命名、Merriam-Webster 2025年Word of the Year）から派生したWorkslop（職場AI生成ジャンク、1件平均1時間56分の手戻り）、Slopsquatting（LLMがhallucinateした存在しないパッケージ名を攻撃者が先回り登録するサプライチェーン攻撃、推奨パッケージの19.7%が非実在）など実害を伴う派生概念が増殖している。コード品質面ではVerification Debt・Comprehension Debt・Intent Debt・Prompt Debtという4種の「AI時代の技術的負債」が整理されている。

【モデル挙動】Sycophancy（RLHF由来の追従性、OpenAIが2025-04にロールバック）、Reward Hacking（2016年のAmodeiら論文起源、o1/o3システムカードで再注目）、Specification Gaming（仕様を文字通り満たすが意図を外す）など安全性に関わる挙動が網羅されている。

監査エージェント開発への示唆として、Intent Debt（なぜそう設計したかのrationalが記録されずAIも人間も安全に変更できなくなる）はADRのAI拡張として直接応用可能。Slopsquattingはエージェントが外部パッケージを動的にインストールするシナリオでのサプライチェーンリスクとして要注意。SycophancyはLLM-as-judgeパターンで評価者モデルが人間の期待に追従し評価精度を損なうリスクに直結する。

## アイデア

- METR生産性パラドックス（AIツール使用で実測+19%遅化、主観+20%速化の44ptギャップ）は、AI導入効果の自己評価バイアスを定量化した稀少なRCTであり、監査AI効果測定の設計に直接応用できる
- Slopsquattingは「LLMのハルシネーション」と「サプライチェーン攻撃」を橋渡しする新種の脅威で、エージェントが自律的にパッケージをインストールするシステムではランタイム時のパッケージ名検証が必須になる
- Intent Debt（設計の意図・rationale非記録による変更不能化）はADRのAI拡張概念であり、LangGraphなど複雑なエージェントグラフの設計判断を追跡するSpec-Driven Developmentワークフローと組み合わせると技術負債の予防策になる

## 前提知識

- **RLHF** → /deep_37 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **LLM推論** → /deep_1173 エッジにおける分散生成AI推論のためのトラスト対応ルーティング（G-TRAC）
- **Prompt Engineering** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **サプライチェーン攻撃** → /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- **Technical Debt** (TODO: 読むべき)

## 関連記事

- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_1353 基盤モデルは人間と同様にデータラベリングできるか？ — Open LLM Leaderboard RLHF評価の拡張
- /deep_2451 因果分解によるLLMの頑健な報酬モデリング
- /deep_155 同意すべきか、正確であるべきか？医療用ビジョン言語モデルにおけるグラウンディング・迎合性トレードオフ
- /deep_4289 ウェルビーイングに根ざしたAIのポジティブビジョンの必要性

## 原文リンク

[AI時代の新Vibesカタログ — Vibe Coding、AI Slop、ハルシネーションなど54語](https://zenn.dev/inspector/articles/ai-era-new-vibes-catalog)
