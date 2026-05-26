---
title: "MCPとSkillsに続く第3の革命：Claude Code WorkflowがultraworkでAgentをコードに焼き付ける"
url: "https://zenn.dev/lumichy/articles/claude-code-workflow-ultrawork-2026"
date: 2026-05-26
tags: [Claude Code, Workflow, マルチエージェント, ultrawork, MCP, Skills, Evaluator-Optimizer, Pipeline, Orchestrator-Workers]
category: "agent-arch"
related: [4520, 6126, 2538, 4899, 6354]
memo: "[Zenn LLM] MCPとSkillsに続く第3の革命：Claude Code WorkflowがultraworkでAgentをコードに焼き付ける"
processed_at: "2026-05-26T09:04:08.455032"
---

## 要約

Claude Code v2.1.47のChangeLogに一時掲載後に削除されたが、コード本体には残存している未公式機能「Workflow」の詳細解説。環境変数`CLAUDE_CODE_WORKFLOWS=1`を設定し、プロンプトで`ultrawork`キーワードを入力することで有効化できる。Workflowの本質は「マルチエージェントのチームワークをJavaScriptコードとして固定・再現可能にすること」であり、MCP（AIに手足を与える）・Skills（AIに作業手順書を与える）に続く第3の機能として位置付けられる。

既存機能との差異は明確で、Subagentは自然言語で即時起動できるが再現性がなく使い捨て。Skillsはモデルが文脈を見て自動発火するプロンプト固定だが、Workflowは`ultrawork`による明示的トリガーとJSスクリプトによる構造固定を持ち、`/workflows`コマンドでリアルタイム追跡が可能。

Workflowスクリプトの必須要素は3つ：①`name`と`description`のメタデータ、②`ctx.runAgent()`によるAgent呼び出し、③`output`による結果返却。300行超のJavaScriptが自動生成され、`Ctrl+O`でリアルタイム確認できる。

対応する6パターンは、①Pipeline（前段出力を次段入力とする直列処理）、②Parallel（複数Workerへの同時分散と集約）、③Evaluator-Optimizer（品質基準を満たすまでループする対抗検証、GAN的発想）、④Routing（Input種別に応じた専門Agentへの振り分け）、⑤Orchestrator-Workers（動的Workerアサインによる累積処理）、⑥Nested（WorkflowがWorkflowを呼び出す再帰構造、3層以内推奨）。

スクリプトはデフォルト3日で自動削除されるが、ユーザーレベルパスへ移動することで永続化でき、Gitで管理・チーム共有・オープンソース化が可能になる。

監査エージェント開発への示唆としては、Evaluator-Optimizerパターンが「監査判断の品質ループ」に直接応用できる。例えば「証拠収集Agent → 監査判断Agent → Evaluator Agent（基準適合性チェック）」という構造で、人手を介さず監査品質を自動引き上げるワークフローが構築可能。また、Routing パターンは「バグ報告・機能追加・ドキュメント」の振り分けと同様に、「リスク種別（財務・IT・コンプライアンス）→ 専門Agentへの自動ルーティング」として応用できる。

## アイデア

- Evaluator-Optimizerパターンは、監査品質ループ（証拠収集→判断→適合性評価→再判断）として監査エージェントに直接転用できる構造を持つ
- Workflowスクリプトを自動生成しGitHub上で共有・OSS化することで「Workflowのエコシステム」が形成されるという予測は、Skills/MCPのエコシステムと同様の普及パスを示唆している
- ChangeLogから削除されたが本体コードは残存するという状態は、Anthropicが機能を「熟成中」として実験的に提供していることを示しており、正式リリース前の機能トレンドを先取りできるという意味でエンジニアにとって優位性がある

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Subagent** → /deep_43 AI社員8人で取締役会を開いたら、完全に人間の組織論だった件
- **LLM Orchestration** (TODO: 読むべき)

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_2538 【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね
- /deep_4899 OpenHarness：1.1万行のPythonでAI Agentの「黒箱」を丸裸にする
- /deep_6354 Claude Code拡張を47個試して5個に絞った話 ── 残した理由と捨てた基準

## 原文リンク

[MCPとSkillsに続く第3の革命：Claude Code WorkflowがultraworkでAgentをコードに焼き付ける](https://zenn.dev/lumichy/articles/claude-code-workflow-ultrawork-2026)
