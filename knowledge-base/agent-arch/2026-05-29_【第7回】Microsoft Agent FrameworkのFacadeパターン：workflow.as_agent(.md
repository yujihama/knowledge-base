---
title: "【第7回】Microsoft Agent FrameworkのFacadeパターン：workflow.as_agent()でワークフローをAgentとして公開する"
url: "https://zenn.dev/naruaki/articles/af-design-07-facade"
date: 2026-05-29
tags: [Microsoft Agent Framework, Facadeパターン, マルチエージェント, SequentialBuilder, HandoffBuilder, WorkflowAgent, カプセル化, GoF]
category: "agent-arch"
related: [5793, 6359, 1641, 4753, 16]
memo: "[Zenn LLM] 【第７回】Microsoft Agent Frameworkで学ぶAIエージェント設計原則：ワークフローを Agent として公開する"
processed_at: "2026-05-29T09:06:58.479986"
---

## 要約

本記事はMicrosoft Agent Frameworkを用いたAIエージェント設計原則シリーズの第7回で、GoFデザインパターンの「Facade（ファサード）パターン」をマルチエージェントシステムに適用する手法を解説する。

テーマはコンテンツ制作支援システムを例とした設計改善。改善前のコードでは、coordinatorエージェントがルーティングした後、呼び出し元のmain関数がresearcher→writer→editorの3工程を直接制御していた。この設計の問題点はカプセル化の欠如であり、呼び出し元がcontentチームの内部構造（3工程の存在・順序）を知っている必要があり、工程変更時に呼び出し元のifブロックも修正が必要になる。

改善策としてworkflow.as_agent()を使用する。SequentialBuilder(participants=[researcher, writer, editor]).build()で3工程のシーケンシャルワークフローを構築し、content_workflow.as_agent(name="content", description="...")でWorkflowAgentに変換する。これにより呼び出し元はawait content_agent.run("...")という単一インターフェースのみを知ればよく、内部が何工程かを意識しなくなる。さらにWorkflowAgentは通常のエージェントと同等のインターフェースを持つため、HandoffBuilderのparticipantsにそのまま渡せる。

改善後はHandoffBuilder(participants=[coordinator, content_agent, qa_agent])でハンドオフ型ワークフローを構築し、coordinatorが自動的にルーティングを担う。これによりルーティング制御のifブロックが消え、content_workflowの内部を変更しても呼び出し元コードへの影響がゼロになる。

workflow.as_agent()は「外向きのFacade」（外部への公開インターフェース）、WorkflowExecutorは「内向きの組み込み」（別ワークフロー内のステップとして埋め込む用途）として使い分ける設計指針も示されている。

監査エージェント開発への示唆：監査ワークフロー（証拠収集→リスク評価→レポート生成）を単一のaudit_agentとしてFacade化することで、オーケストレーター層が内部工程を知る必要がなくなり、工程追加・変更時の影響範囲を局所化できる。LangGraphでも同様のパターンはサブグラフのコンパイルとして実現可能だが、Agent Frameworkのworkflow.as_agent()はより明示的なインターフェース設計を促す。

## アイデア

- workflow.as_agent()によりワークフローをAgentと同一インターフェースに変換する発想は、LangGraphのサブグラフやOpenAI Agents SDKのhandoffと概念的に対応しており、マルチエージェント設計の抽象化レベルを統一できる
- WorkflowExecutor（内向き埋め込み）とworkflow.as_agent()（外向きFacade）の使い分けにより、ワークフローの合成粒度を「外部公開用」と「内部再利用用」で明確に分離できる設計思想が興味深い
- HandoffBuilderのparticipantsにWorkflowAgentを通常Agentと混在して渡せる設計は、Composite パターンとFacadeパターンの組み合わせであり、エージェントツリーの深さを任意にネスト可能にする

## 前提知識

- **Facadeパターン（GoF）** (TODO: 読むべき)
- **マルチエージェント orchestration** (TODO: 読むべき)
- **SequentialWorkflow** (TODO: 読むべき)
- **Handoff / ルーティング** (TODO: 読むべき)
- **Pydantic BaseModel** (TODO: 読むべき)

## 関連記事

- /deep_5793 Microsoft Agent FrameworkのHandoffBuilderによるルーティング設計と開放閉鎖原則
- /deep_6359 仕様書に埋もれた「決まっていない意思決定」を、マルチエージェントで炙り出す
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_16 長期実行アプリケーション開発のためのハーネス設計

## 原文リンク

[【第7回】Microsoft Agent FrameworkのFacadeパターン：workflow.as_agent()でワークフローをAgentとして公開する](https://zenn.dev/naruaki/articles/af-design-07-facade)
