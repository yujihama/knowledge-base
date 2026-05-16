---
title: "【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね"
url: "https://zenn.dev/sika7/articles/778304406e60e0"
date: 2026-04-21
tags: [Claude Code, カスタムスラッシュコマンド, Workflow, サブエージェント, CC Workflow Studio, Mermaid, MCP]
category: "agent-arch"
related: [2254, 430, 2404, 2140, 13]
memo: "[Zenn LLM] 【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね"
processed_at: "2026-04-21T12:32:06.319721"
---

## 要約

Claude Codeのカスタムスラッシュコマンド機能を活用したWorkflow構築手法を解説した実践記事。Claude CodeのWorkflowとは、`.claude/commands/`ディレクトリに配置したMarkdownファイルであり、これがそのままスラッシュコマンドとして機能する。Markdownにステップ形式でClaudeへの指示を記述することで、サブエージェントの呼び出し順序、使用するSkillsやMCPツール、エラー時の条件分岐、完了条件などを事前に定義できる。

著者が今回作成したのは2つのカスタムスラッシュコマンドで、`/workflow-design`（要件の壁打ちとMermaidによる設計図出力担当）と`/workflow-generate`（設計図からMarkdown生成と`.claude/commands/`への配置案内担当）に役割を分離している。あえて2コマンドに分割した理由は、設計と実装を分けることで「設計図レビュー→修正→Markdown生成」という手戻りの少ないフローを実現するためである。

`/workflow-design`のポイントは、ファイルパスが渡された場合はそのMarkdownを読み込み、質問は一度に全て行わず会話形式で1〜2個ずつ行い、Markdown生成は行わない点。`/workflow-generate`のポイントは、設計図が渡されない場合は`/workflow-design`へ誘導し、サブエージェントが含まれる場合は`.claude/agents/`用の定義ファイルも併せて生成する点。

CC Workflow StudioはOSSのVSCode拡張機能で、ノードのドラッグ＆ドロップによるビジュアル編集でWorkflowを構築できるツール（GitHubスター1,000以上）。ただし最終的に生成されるのも同じ`.claude/commands/`のMarkdownファイルであるため、Markdownを手書きすれば同等の成果物が得られる。CC Workflow Studioの優位性は既存Workflowのビジュアル管理・編集機能であり、Workflowが増えたりチーム共有が必要な場面では有利。

監査エージェント開発への示唆として、LangGraphで構築するReActエージェントにおいても「設計フロー（グラフ定義）と実装を分離し、Mermaid等で可視化してからコード化する」というアプローチは、複雑なマルチステップ監査ワークフローの品質管理に直接応用できる。特にサブエージェントへのタスク委譲ルールを`.claude/agents/`定義ファイルとして外部化する手法は、Pydantic AIやLangGraphのノード定義と概念的に対応しており、ハーネス設計のパターンとして参考になる。

## アイデア

- Workflowの「設計（/workflow-design）」と「生成（/workflow-generate）」を2コマンドに分離することで、Mermaidによる設計レビューを挟んだ反復可能な開発フローを実現している点
- CC Workflow StudioのようなビジュアルツールもMarkdownファイルに変換されるため、ツールの有無に関係なく最終成果物は同一であり、手書きMarkdownで代替可能という逆説的な構造
- `.claude/agents/`ディレクトリへのサブエージェント定義ファイルの自動生成により、Workflowとエージェント定義を同時に管理する仕組みを、チャット会話のみで構築できる点

## 前提知識

- **Claude Code カスタムスラッシュコマンド** (TODO: 読むべき)
- **サブエージェント / Sub-agent** (TODO: 読むべき)
- **Mermaid フロー図** (TODO: 読むべき)
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **Skills / ハーネス設計** (TODO: 読むべき)

## 関連記事

- /deep_2254 同僚の「細かすぎた」が機能になった──Cladeが育つ仕組み【v1.15.0】
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装

## 原文リンク

[【Claude Code】Workflowを自分で作ってみた！CC Workflow Studioがあるけどね](https://zenn.dev/sika7/articles/778304406e60e0)
