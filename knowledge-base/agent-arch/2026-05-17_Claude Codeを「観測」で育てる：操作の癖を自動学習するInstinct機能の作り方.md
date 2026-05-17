---
title: "Claude Codeを「観測」で育てる：操作の癖を自動学習するInstinct機能の作り方"
url: "https://zenn.dev/syrsan/articles/claude-code-instinct-self-learning"
date: 2026-05-17
tags: [Claude Code, PostToolUse hook, エージェントメモリ, 自動学習, confidence管理, JSONL, コンテキスト管理]
category: "agent-arch"
related: [430, 5029, 3506, 3004, 2825]
memo: "[Zenn LLM] Claude Code を「観測」で育てる：操作の癖を自動学習する仕組みの作り方"
processed_at: "2026-05-17T09:07:02.243981"
---

## 要約

Claude Code 2.1.33で導入された公式memory機能は、ユーザーが明示的に記述した内容のみを記憶する「教える記憶」である。本記事では、これとは異なる「観測して育つ記憶」としてInstinctという自作機能の最小設計を紹介する。

Instinctは3ステップで構成される。①観測：Claude CodeのPostToolUseフックを使い、全ツール呼び出しをJSONL形式でobservations.jsonlに記録する。ツール名・入力・タイムスタンプを保存し、AWSキーやBearerトークン等の機密情報は正規表現でREDACTEDに置換してから保存する。②分析：観測が20件蓄積された時点でパターン抽出を実行する。「Editの前に必ずGrepを実行」「Terraform操作時にmain.tf・variables.tf・outputs.tfを並列Readする」といったツール順序やワークフローの繰り返しパターンをInstinctファイル（Markdown＋frontmatter形式）として書き出す。③信頼度管理：各Instinctはconfidence値（0〜1）を持ち、生成時は0.3〜0.5の仮説として始まる。同じパターンが再観測されるとreinforceコマンドで+0.1、一定期間観測されない場合はweakenで-0.1される。confidenceが閾値以下かつ30日経過で自動削除（prune）される。セッション開始時はconfidence 0.4以上のInstinctのみをコンテキストに注入し、低信頼度のものを除外することでコンテキスト肥大化を防ぐ。

公式memoryとの主な違いは、①何を覚えるか（人間が書く vs 操作観測による自動抽出）、②強弱（全て同じ重み vs confidenceによる強弱）、③寿命（手動削除まで永続 vs 使われないと自動削除）の3点。両者は排他でなく、「絶対守ってほしい制約」は公式memory、「無意識の操作の癖」はInstinctと役割分担して使うのが最適とされる。confidence 0.7以上のパターンが3つ蓄積されると明示的なSKILLへの昇格通知が出る仕組みも備える。

監査エージェント開発への示唆：LangGraphや監査ワークフローにおいても、エージェントの操作履歴をPostToolUseフック相当の仕組みで収集し、繰り返しパターンをconfidence付きで動的に管理するアーキテクチャは、エージェントの「学習コスト」を下げながら信頼性の低いパターンを自動排除できる設計として応用可能。

## アイデア

- 「教える記憶」と「観測して育つ記憶」の役割分担設計：明示的制約はmemory、暗黙の操作パターンはInstinctと分離することで、エージェントのコンテキスト品質を最適化できる
- confidence値による記憶の自然淘汰メカニズム：強化・弱体化・自動削除（prune）の組み合わせが、不要なパターンの蓄積（記憶の肥大化）を防ぐ弁として機能する
- PostToolUseフックによるゼロ侵襲の観測：エージェントのコード本体を変更せずにフックだけで全ツール呼び出しを記録できるため、既存ワークフローへの後付け適用が容易

## 前提知識

- **Claude Code hooks** → /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- **PostToolUse** → /deep_4519 安全装置を盛りすぎたらAIエージェントが撤退バイアスを発症したので松岡修造で解決した話
- **エージェントメモリ設計** (TODO: 読むべき)
- **JSONL** → /deep_89 Claude CodeとCodexのPlan Modeはどこに何を保存しているのか
- **コンテキストウィンドウ管理** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_3004 LLMに長期記憶を実装して、失敗にいたる
- /deep_2825 Claude Codeハーネスエンジニアリングを最小構成でA/Bテストしてみた

## 原文リンク

[Claude Codeを「観測」で育てる：操作の癖を自動学習するInstinct機能の作り方](https://zenn.dev/syrsan/articles/claude-code-instinct-self-learning)
