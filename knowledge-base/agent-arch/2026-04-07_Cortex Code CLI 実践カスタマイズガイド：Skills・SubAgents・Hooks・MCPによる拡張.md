---
title: "Cortex Code CLI 実践カスタマイズガイド：Skills・SubAgents・Hooks・MCPによる拡張"
url: "https://zenn.dev/snowflakejp/articles/46369359327022"
date: 2026-04-07
tags: [CortexCode, SubAgents, Skills, Hooks, MCP, AGENTS.md, Snowflake, エージェントカスタマイズ, WorktreeIsolation]
category: "agent-arch"
memo: "[Zenn LLM] Cortex Code CLI 実践カスタマイズガイド"
processed_at: "2026-04-07T09:09:11.088325"
---

## 要約

Snowflake が提供するターミナル常駐型AIコーディングエージェント「Cortex Code CLI（CoCo CLI）」の拡張機能を実践的に解説した記事。著者はCursorからCoCo CLIに乗り換え、カスタムスキル7個・カスタムサブエージェント5個を定義し、Hookによる品質チェック・Slack通知・MCP外部連携まで構築した経験をもとに執筆している。

CoCo CLIのカスタマイズは5つの構成要素からなる。①AGENTS.md：プロジェクトルートに置くMarkdownファイルで、コーディング規約・Do/Don'tルール・ディレクトリ構成・カスタムスキル利用ガイドをエージェントに注入する。②Skills：ドメイン固有のワークフローをYAML frontmatter付きMarkdownで定義し、$skill-nameで明示呼び出しするか、descriptionとの照合で自動発動させる。CoCo CLIにはv1.0.45時点で33個のビルトインスキル（dynamic-tables、cortex-agent、cost-intelligenceなど）が搭載済み。③SubAgents：最大50並列実行可能な専門エージェントで、モデルをタスクごとに個別指定できる（例：critic-reviewerにopenai-gpt-5.2を指定）。Git worktreeによる変更の分離（Worktree Isolation）も可能。④Hooks：PreToolUse/PostToolUse/Stop等のライフサイクルイベントをインターセプトし、シェルスクリプトで品質チェックや通知を自動実行。例として、SQLクエリ実行前にDROP/TRUNCATE等の破壊的操作を検知してブロックするHookや、タスク完了時にSlack通知を送るHookが紹介されている。⑤MCP（Model Context Protocol）：JSON設定でGitHub・Slack・Notionなどの外部ツールを追加し、エージェントのツールセットを拡張する。

著者が特に有用と評価する点は「モデルの使い分け」で、SubAgentsごとにSnowflake Arctic・Mistral・GPT系を目的別に割り当てることでコストと精度を最適化できる。また、Hookの活用により破壊的SQL操作のガードレールをエージェントレベルで設けられる点を安全運用の観点から強調している。

## アイデア

- SubAgentsごとにモデルを個別指定できる設計により、タスク特性（コストvs精度）に応じたLLM使い分けが実現できる点は、LangGraphのノード設計でも応用可能な考え方
- HooksでPreToolUseイベントをインターセプトし破壊的操作をブロックする仕組みは、監査エージェントにおける「ガードレール付き自律実行」の実装パターンとして参考になる
- AGENTS.mdのDo/Don't構造とSkillsのdescription自動マッチングを組み合わせることで、エージェントの判断精度を設定ファイルレベルで制御できる点は、Instructionエンジニアリングの実践例として興味深い

## Yujiの取り組みへの示唆

監査エージェント開発において、HooksによるPreToolUse制御（破壊的操作のブロック）はLangGraphのノード前後処理やPydanticによるバリデーションと同様のガードレール設計として直接応用できる。SubAgentsのWorktree Isolationと並列実行（最大50）は、マルチエージェントで並列に監査証跡を検証するアーキテクチャの参考になる。またSkillsのdescription自動マッチングは、LLM-as-judgeでタスクルーティングを行う際のプロンプト設計に示唆を与える。

## 原文リンク

[Cortex Code CLI 実践カスタマイズガイド：Skills・SubAgents・Hooks・MCPによる拡張](https://zenn.dev/snowflakejp/articles/46369359327022)
