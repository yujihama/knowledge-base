---
title: "AIは失敗していない、我々の作り方が間違っている — Web Summit Vancouver 2026 セッションレポート"
url: "https://zenn.dev/genzou9201/articles/eb1d063c105f4b"
date: 2026-05-28
tags: [Agent Identity, Intent monitoring, IAM, Local Maxing, Token Maxing, context layer, controls layer, last mile problem, model routing, AI-native]
category: "agent-arch"
related: [1320, 4903, 2108, 5028, 5055]
memo: "[Zenn LLM] AIは失敗していない、我々の作り方が間違っている — Web Summit Vancouver 2026 セッションレポート"
processed_at: "2026-05-28T21:05:15.488454"
---

## 要約

Web Summit Vancouver 2026（2026年5月13日）で行われたセッション「AI isn't failing we're building it wrong」のレポート。登壇者はScribe CEO Jennifer Smith、1Password CTO Nancy Wang、Webflow CEO Linda Tongの3名。

【何を作り間違えているか】3者はそれぞれ異なるレイヤーの欠如を指摘した。①データ層：組織固有の業務フロー・例外処理・依存関係が担当者の頭の中にしか存在せずデータ化されていない「last mile problem」。②ガバナンス層：従来のIAM（role-based access）はエージェントの非決定的な挙動を扱えず、Agent Identity＋Intent monitoringの仕組みが必要。③インフラ層：「AI-native」を標榜しながら実態はAI-assistedの後付けにすぎず、architecture・systems of record・data schema・modelingをAI前提で作り直す必要がある。

【ベンチマークと現実のギャップ】原因はモデル性能ではなく組織側の準備不足。技術の進歩は指数関数的、組織変革は線形という2曲線の乖離がギャップの正体。2024年は「全社員にAIを配布」、2025年は「トークンコスト肥大化への気づき」、現在は「ROIで語る」段階へ移行中。目標は「少ない人手でより多く」ではなく「新人営業のramp timeを縮める」レベルまで具体化することが必要。

【Token MaxingからLocal Maxingへ】Token Maxing（トークン利用量をノルマ化）は組織適応の初期手段としては有効だったが、「投入量≠価値創出量」という手段と目的の混同を招く。小型モデルの性能向上とコスト最適化の潮流を受け、タスク・適切なモデル選定・チューニング・ビジネス価値の4点で判断する「Local Maxing」が主流化。モデル切り替えだけで1ワークフローのコストが$20〜40/日から$3〜4/日（約10分の1）になった実例あり。

【AIシステムに欠けているもの】①運用コスト統制：サブエージェントの自己増殖により1エンジニアあたり週$50K〜$100Kのトークン費用が発生する事例あり。対策はモデルルーティング・差分処理アーキテクチャ・スペンドキャップ・支出可視化・credentials再教育。②コンテキスト管理：コンテキストは多いほど良いわけでなく過剰投入は逆効果。組織レベルのコンテキストは権限・セキュリティリスクを内包し、有効な対処策は未確立。

【職種の収束とbuilder化】PM・デザイナー・エンジニアの受け渡し（break point）がAIによって消滅し、全員が「builder」へ収束。人間に求められる価値は実行から戦略・判断へ移行。カスタマーサクセス担当者が業務用SaaS相当ツールを自作する事例も発生。一方、可能性が見えるほど仕事量が際限なく膨らむ副作用と、全員を新しい働き方へ移行させる未解決課題が残る。

監査エージェント開発への示唆：Agent Identity＋Intent monitoringの概念は監査エージェントの権限管理・操作ログ設計に直結する。組織の業務フローをlegibleにする「文脈層」の構築は、監査エージェントが組織固有の内部統制手続きを理解するためのコンテキスト設計と同義であり、最優先課題として位置づけられる。

## アイデア

- Agent Identity＋Intent monitoringという概念：role-based accessではなくエージェント固有の身元と意図を紐づけて継続監視する設計は、監査エージェントの操作ログ・承認フロー設計に直接応用可能
- 技術の指数関数的成長vs組織変革の線形成長という非対称性：この2曲線の乖離がベンチマークと本番環境のギャップの構造的原因という分析は、AIプロジェクトのROI評価フレームとして使える
- コンテキストの逓減収益と過剰投入の逆効果：「会議録をすべて投入する」アプローチが逆効果になるという知見は、RAGのチャンク戦略やコンテキスト設計の原則として重要

## 前提知識

- **IAM（Identity and Access Management）** (TODO: 読むべき)
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **モデルルーティング** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年

## 関連記事

- /deep_1320 エージェント型コマースは「真実」と「コンテキスト」で動く
- /deep_4903 【エンジニアの類推思考】呪詛・デスノート・LLMエージェントに見る「指示の設計」
- /deep_2108 SageMaker Training Jobを使う理由を整理しつつ、Terraformで試してみた
- /deep_5028 LLMアプリにOAuthでモデル利用権限を委譲するのは現実的なのか
- /deep_5055 AIエラにおけるサイバー不安全：攻撃面の拡大と次世代セキュリティの必要性

## 原文リンク

[AIは失敗していない、我々の作り方が間違っている — Web Summit Vancouver 2026 セッションレポート](https://zenn.dev/genzou9201/articles/eb1d063c105f4b)
