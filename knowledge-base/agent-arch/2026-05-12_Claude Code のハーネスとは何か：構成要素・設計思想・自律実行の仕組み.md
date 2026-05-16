---
title: "Claude Code のハーネスとは何か：構成要素・設計思想・自律実行の仕組み"
url: "https://zenn.dev/kent_salt2/articles/571bd944d0cb0d"
date: 2026-05-12
tags: [Claude Code, ハーネス, Subagent, Skill, Agent Memory, コンテキスト管理, マルチエージェント, Generator-Evaluator, Hooks, 自律実行]
category: "agent-arch"
related: [2824, 2961, 2055, 2957, 4753]
memo: "[Zenn LLM] Claude Code のハーネスとは何か"
processed_at: "2026-05-12T09:20:02.203496"
---

## 要約

Claude Code を長期プロジェクトで使い続けると、同種のミスの反復・前提の再説明・コンテキスト逼迫という3つの構造的問題が生じる。この課題に対処する仕組みが「ハーネス」である。

Anthropicの広義定義では「Claudeを呼び出しツール呼び出しを関連インフラにルーティングするループ」だが、本記事は狭義として「.claude/配下のファイル群を組み合わせてClaude Codeをプロジェクト固有作業環境として整備する設計」と定義する。構成要素は7種：CLAUDE.md（常時注入・200行以下推奨）、Rules（ファイルパス別条件付き注入）、Skills（オンデマンド注入）、Subagents（別コンテキストウィンドウで実行・要約のみ返却）、Settings（実行権限制御）、Hooks（イベント駆動シェル実行）、Agent Memory（セッション横断の永続記憶）。

SkillとSubagentの最大の差異は「動作する場所」にある。Skillは同一コンテキスト内で実行され手順を定型化するのに対し、Subagentは独立ウィンドウで動作しメイン会話に要約のみを返す。Subagentはコンテキスト汚染の防止・ドメイン特化・ツール権限の構造的絞り込み・Haikuへのコストオフロードに適する。

ハーネスが単なるショートカット集合を超えて機能するには2条件が必要だ。①連動：Skill起動→Explore Subagent調査→backend-expert実装委譲→rules自動注入→並列レビューという一連のチェーン。②フィードバックループ：検出された問題がRulesやAgent Memoryに書き戻され次回以降の動作に自動反映される仕組み。

自律実行がもたらす効果は3点。(1)記憶の引き継ぎ：CLAUDE.md・Rules・Agent Memoryがセッション横断知識を保持。(2)役割の分離：Generator-Evaluatorパターンにより実装エージェントとレビューエージェントを構造分離し、レビュー系にEdit/Write権限を付与しない。(3)品質の蓄積：Rulesへの教訓追記が以降の全作業に自動適用される。

実装例として示された「ソリューション設計自動化ハーネス」は、案件ごとに数日〜数週間かかっていた提案資料・アーキテクチャ・デモの作成を自動化する。/build-solution <案件名> --phase=B1 の一コマンドで、5層構造12エージェント（solution-orchestrator, solution-validator, traceability-manager, gate-validator, hearing-designer, screen-designer, mockup-builder, demo-builder, production-builder, package-reviewer×3, red-team）が分担して処理を進め、人間の介入は「実装着手合意」の1ステップのみとなる。設計書自体もCodexによるレビューをv1〜v5と反復し、Critical 2件・Major 5件の指摘をすべて解消してconditionally-validated判定を得た。ファイル衝突は原子的mkdir lock方式で制御し、deadlock・race conditionも設計書改訂で対処済み。

## アイデア

- コンテキスト注入タイミングの設計（常時/条件付き/オンデマンド/別ウィンドウ）という軸でハーネス構成要素を整理する視点は、監査エージェントのプロンプト設計にも直接応用できる
- 設計書自身をCodexでv1→v5と反証・改訂し、Critical 0になるまでフィードバックループを回した実例は「ハーネスで品質が蓄積される」の具体的証明になっている
- レビュー系エージェントにEdit/Write権限を与えないRead-only固定という構造的制約が、自己評価バイアスを設計で排除する手法として参考になる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_2824 プロンプトの再現性をAIに自動チューニングさせる方法 〜 暗黙知を排除する
- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_2055 Claude Codeのトークン消費を半分にする——800時間の運用データから見つけた実践テクニック
- /deep_2957 Claude Codeで80Kトークンを2,100に削減する方法：廃棄設計による97%削減アーキテクチャ
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[Claude Code のハーネスとは何か：構成要素・設計思想・自律実行の仕組み](https://zenn.dev/kent_salt2/articles/571bd944d0cb0d)
