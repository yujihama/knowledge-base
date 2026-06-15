---
title: "Harness Starter Kit が Codex と Claude Code に対応しました"
url: "https://zenn.dev/yuuaan/articles/3c2f2a8211b610"
date: 2026-06-15
tags: [Harness Starter Kit, Claude Code, Codex, AI coding agent, prompt-first, Agent Skills, リポジトリ管理, ワークフロー自動化]
category: "agent-arch"
related: [4520, 2978, 2930, 3117, 3065]
memo: "[Zenn LLM] Harness Starter Kit が Codex と Claude Code に対応しました"
processed_at: "2026-06-15T09:06:48.858229"
---

## 要約

Harness Starter Kit は、AI コーディングエージェントがプロジェクト内で繰り返し引き起こしがちな問題を、長期的に維持可能なリポジトリのルール・チェック・失敗記録・意思決定記録・評価フローとして蓄積していくための prompt-first なオープンソースツールキットである。今回のアップデートにより、OpenAI Codex および Claude Code（Anthropic）のサポートが追加され、Agent Skills / plugin を通じて関連ワークフローを直接呼び出せるようになった。具体的には `/harness doctor` および `/harness review` というスラッシュコマンドが使用可能になり、エージェント向けの指示・プロジェクト上の制約・フィードバックループ・記憶として残すべき記録・ルールの drift リスクなどを確認できる。このツールキットの設計思想は「1回のプロンプトを改善する」のではなく「リポジトリ自体を AI コーディングエージェントが安定して作業しやすい環境にする」という点にある。つまり、エージェントが失敗した際の教訓や意思決定の背景をリポジトリに蓄積し、次回以降のエージェント実行時に参照できる構造を作ることで、プロジェクト全体の品質と一貫性を維持する仕組みである。対応技術スタックは Python・TypeScript・Node.js・React・Next.js・Vue・Django・Flask・FastAPI・Spring Boot・Android・Go・Rust と幅広く、各スタック向けの参考プロファイルも含まれている。監査エージェント開発への示唆としては、エージェントの失敗記録や意思決定ログをリポジトリ自体に構造化して蓄積するアプローチは、監査トレイル・ガバナンス記録の自動化と親和性が高い。LangGraph ベースの監査エージェントにおいても、各ノードの判断根拠や失敗パターンをリポジトリ管理の形で残す設計に応用できる可能性がある。

## アイデア

- プロンプト単体ではなくリポジトリ構造そのものをエージェント対応化するという設計思想は、エージェントの長期的な品質維持において有効なアプローチである
- /harness doctor や /harness review のようなスラッシュコマンドによるワークフロー呼び出しは、Claude Code の Skills 機構と組み合わせることで、エージェント自身が自己診断・自己改善できる仕組みを実現している
- 失敗記録・意思決定記録をリポジトリに蓄積するパターンは、監査エージェントにおける証跡管理・ガバナンス記録の自動化に直接応用できる

## 前提知識

- **Claude Code Agent Skills** (TODO: 読むべき)
- **OpenAI Codex** → /deep_3427 エージェントオーケストレーション：AIにとって今重要な10のこと（MIT Technology Review）
- **prompt-first 設計** (TODO: 読むべき)
- **Agent ワークフロー** (TODO: 読むべき)
- **リポジトリ規約管理** (TODO: 読むべき)

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_2978 中国のテック労働者がAIドッペルゲンガー訓練を迫られ反発——「同僚スキル」と「反蒸留」ツールの攻防
- /deep_2930 中国のテックワーカーたちが「AIの分身」を訓練し始め、反発も起きている
- /deep_3117 中国のテックワーカーたちがAIドッペルゲンガーのトレーニングを命じられ、反発を始めている
- /deep_3065 中国のテックワーカーがAIドッペルゲンガーの訓練を求められ、反発を始めた

## 原文リンク

[Harness Starter Kit が Codex と Claude Code に対応しました](https://zenn.dev/yuuaan/articles/3c2f2a8211b610)
