---
title: "フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装"
url: "https://zenn.dev/dysksh/articles/27617be34cc336"
date: 2026-04-07
tags: [Claude API, Go, ECS Fargate, エージェントループ, ToolChoice, トークン最適化, LLM-as-judge, 2フェーズ設計, サーバーレス, 自己選好バイアス]
category: "agent-arch"
memo: "[Zenn LLM] フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装"
processed_at: "2026-04-07T12:00:38.517858"
---

## 要約

Discord のスラッシュコマンドからGitHub PRを自動生成するエージェント「Nemuri」の設計・実装の解説記事。LangChainやCrewAIを使わず、Claude APIをGoで直接呼び出すアーキテクチャを採用。「常時起動するインフラを持たない」を原則に、1ジョブ = 1 ECS Fargateタスクのワンショット実行で構成し、ジョブがない間のAWSコストをほぼゼロに抑える。リクエストフローはAPI Gateway → Ingress Lambda（Ed25519署名検証・DynamoDB/SQSへの登録）→ Runner Lambda → ECS Fargateの順に非同期処理される。

エージェントループは「Gathering（情報収集）」と「Generating（成果物生成）」の2フェーズに分割。Claude APIがステートレスである特性から、全会話履歴をそのまま引き継ぐと入力トークンが増大するため、Gatheringフェーズではリポジトリファイルをインメモリの fileCache に保存し、Generatingフェーズでは新しいコンテキストに詰め直して単一LLMコールで成果物JSONを生成する設計。ToolChoiceで deliver_result ツールを強制指定することで、LLMは必ず構造化JSONを返す。

品質担保のためにレビューループを実装。実装にはclaude-sonnet-4-6、レビューにはclaude-opus-4-6を分離して使用。自己選好バイアス（Panickssery et al., 2024）への対応として、より高性能なモデルによる4軸（正確性・セキュリティ・保守性・完全性）スコアリングを最大3ラウンド実行し、平均7.0以上で合格とする。収束しない場合はスコア改善停滞・同一指摘繰り返し・minor指摘のみ残存などの5条件で打ち切る。

コスト制御は4層構成：①fileCache による重複ファイル読み取り防止、②入力トークン予算（80,000トークン）による動的制御、③list_repo_files 結果へのLLM事前フィルタリング（MaxTokens: 1024）、④会話履歴トリミング（直近3イテレーション保持・古いツール結果を先頭20行に短縮）。イテレーション数ではなくトークン数を直接制約する設計により、タスク複雑度に適応したコスト管理を実現している。LLMは型付きJSONスキーマの入力側のみ操作でき、GitHub APIの認証・ブランチ命名・S3パスはAgent Engine側が制御する権限分離も特徴的。

## アイデア

- GatheringとGeneratingの2フェーズ分離でコンテキストをリセットする設計は、ステートレスなLLM APIのトークンコスト問題への実践的な解法であり、長時間エージェントのコスト制御パターンとして汎用性が高い
- ToolChoice強制（type: 'tool' + name指定）による構造化JSON出力の保証は、エージェントの出力を型安全に処理するための実装テクニックとして、フレームワーク非依存の設計において有効
- イテレーション数ではなく入力トークン予算（80,000トークン）でループを制御するアプローチは、タスク複雑度に適応しながらコストを直接制約する代理指標排除の設計思想として注目に値する

## Yujiの取り組みへの示唆

監査エージェント開発において、Gatheringフェーズで証拠・ドキュメントを収集しfileCacheに集約し、Generatingフェーズで監査調書や所見レポートを構造化JSON出力するという2フェーズ設計は直接転用できる。ToolChoice強制による型付きJSON出力の保証はPydanticモデルとの親和性が高く、LangGraphのノード間データフローを安定させる実装パターンとして参考になる。また、実装モデルとレビューモデルを分離してLLM-as-judgeを構成する手法は、Yujiが研究中のRLAIF・LLM評価における自己選好バイアス対策の実装例としても具体的な示唆を与える。

## 原文リンク

[フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装](https://zenn.dev/dysksh/articles/27617be34cc336)
