---
title: "Claude Code「Dynamic Workflows」完全ガイド：6つのパターンと14ステップ"
url: "https://zenn.dev/aria3/articles/claude-code-dynamic-workflows-6-patterns"
date: 2026-06-04
tags: [Claude Code, Dynamic Workflows, マルチエージェント, オーケストレーション, parallel, pipeline, Adversarial verification, サブエージェント, LLM-as-judge]
category: "agent-arch"
related: [3490, 3532, 6917, 4753, 3906]
memo: "[Zenn LLM] Claude Code「Dynamic Workflows」完全ガイド：6つのパターンと14ステップ"
processed_at: "2026-06-04T21:16:15.795610"
---

## 要約

Claude CodeのDynamic Workflowsは2026年5月28日にリリースされた機能で、Claudeがタスク専用のオーケストレーションハーネスをその場で生成し、複数のサブエージェントを協調させる仕組みである。通常の単一コンテキストウィンドウアプローチが抱える3つの失敗パターン——Agentic laziness（タスク未完了での「完了」宣言）、Self-preferential bias（自己出力への優先評価）、Goal drift（長期実行時の目標逸脱）——を構造的に解決する。コアAPIはagent()・parallel()・pipeline()の3関数で構成される。parallel()はバリア型で全結果を待ってから次へ進み、pipeline()はストリーミング型で各アイテムが独立してステージを流れる。コスト・スループット面ではpipeline()が有利。6つのパターンは以下の通り。①Classify-and-act：分類エージェントがタスク種別を判定し、複雑さに応じてHaikuからOpusへ振り分ける。②Fan-out-and-synthesize：50ファイル・200エンドポイントなど列挙可能な作業を並列展開し、最後にOpusが統合する。③Adversarial verification：生成エージェントとは別コンテキストの検証エージェントがルーブリックのみを参照して敵対的レビューを実施し、Self-preferential biasを排除する。④Generate-and-filter：アイデアを大量生成してルーブリックでフィルタリングし、遅いコミットで品質を担保する。⑤Tournament：N個のエージェントが同一タスクに異なるアプローチで取り組み、ペアワイズ比較で勝者を決定する（1,000件以上のソートに有効）。⑥Loop until done：停止条件（「新しい発見がない」「ゼロエラー」等）が満たされるまでエージェントスポーンをループする。実運用では/goal（ハードな完了要件設定）・/loop（定期実行）・明示的トークン予算（例：「5kトークン使って」）の3設定が重要で、予算なしでは期待値の5〜10倍に膨れ上がる。信頼できない外部コンテンツを扱う場合はQuarantineパターンを適用し、読み取りエージェントと実行エージェントを分離してプロンプトインジェクションリスクを排除する。機能したワークフローは~/.claude/workflowsに保存し、Skillとしてバンドル配布も可能。監査エージェント開発への示唆として、Adversarial verificationパターンはLLM-as-judgeの自己優先バイアスを構造的に解消する手法として直接応用可能であり、Loopパターンと/goalの組み合わせは監査手続きの「全件確認完了まで継続」という要件とも親和性が高い。

## アイデア

- Self-preferential biasを「構造」で解決するAdversarial verificationパターン——検証エージェントに生成者情報を渡さないというペアリングルールが、LLM-as-judge設計の核心的な知見になる
- parallel()とpipeline()の使い分け基準（「次の処理の前に全結果が必要か？」）が、分散処理設計の思考フレームワークとして汎用的に使える
- Tournamentパターンによるペアワイズ比較——絶対スコアより比較判断の方が信頼性が高いという発想は、大規模ランキング問題（1,000件超）の解法として注目に値する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **サブエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_3490 エージェントオーケストレーション：今AIで重要な10のこと｜MIT Technology Review
- /deep_3532 エージェントオーケストレーション：今AIで重要な10のこと
- /deep_6917 Claude Opus 4.8 の新機能・4.7との違いを整理｜Fast mode/Dynamic Workflows
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_3906 検証付きマルチエージェント協調：「計画・実行・検証・再計画」フレームワーク VMAO

## 原文リンク

[Claude Code「Dynamic Workflows」完全ガイド：6つのパターンと14ステップ](https://zenn.dev/aria3/articles/claude-code-dynamic-workflows-6-patterns)
