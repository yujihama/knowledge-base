---
title: "MCPをContext Boundaryとして使う：AgentのCapability Shapingという設計思想"
url: "https://zenn.dev/mofuteq/articles/be562471f96a68"
date: 2026-05-29
tags: [MCP, Context Boundary, capability shaping, RAG, flattening of reasoning, scope check, output boundary, contract-question-agent, LLM設計]
category: "agent-arch"
related: [4520, 1784, 2404, 1247, 6412]
memo: "[Zenn LLM] MCPでAgentのできることを増やすのをやめたら、Context Boundaryが残った"
processed_at: "2026-05-29T09:03:16.205181"
---

## 要約

本記事は、Model Context Protocol（MCP）を「Agentのできることを増やす仕組み」としてではなく、「Agentに渡す自由の形を決める境界（Context Boundary）」として設計する考え方を論じたものである。

著者が契約書レビューAgent（contract-question-agent）を開発する中で気づいた核心的問題は、LLMが「何でも答えられる」という特性にある。LLMは問いの立て方や観点まで自律的に生成できるため、意図しない推論が混入しやすい。RAGにおいては特に顕著で、複数の論点・矛盾・不足情報が最終回答の中で平均化される「flattening of reasoning」が発生する。契約書のように、どの条項についていかなる確認質問を立てるかの粒度が求められるドメインでは、この平均化そのものがリスクになる。

この問題に対し著者は、MCP を autonomous tool use ではなく system-controlled candidate context として扱う設計を提唱する。具体的には「capability expansion」ではなく「capability shaping」の観点でMCPを使い、Runtimeが使ってよい観点（candidate review lenses）をAgentに提示する。

Agent設計における境界は3層に分離される。①Scope Check：そもそもその入力に答えてよいかを判断する責務境界。②Candidate Review Lenses：どの観点から見てよいかをRuntimeが提示する（MCPはここに置く）。③Output Boundary：最終出力をverdict（判定）ではなくverification questions（確認質問）に留める。この3つをプロンプトではなくRuntime側に実装することで、「どの観点を使ったか」「なぜverdictに進まなかったか」が観測可能になり、Agent修正が容易になる。

プロンプトに境界を押し込む設計と対比した重要な主張は「No disclaimer by design」である。危険な回答をした後に免責文を付加するのではなく、そもそも危険な回答の形に進ませない構造設計こそが責任ある設計だとしている。

監査エージェント開発への示唆は大きい。内部監査領域でも「リスクがあります」という平均化された回答ではなく、どの統制項目について何を検証すべきかを分解して出力させる必要があり、Scope Check・Review Lenses・Output Boundaryの3層設計は直接応用可能である。MCPをツール呼び出しの拡張としてではなく、エージェントの認識範囲を制御するContext Boundaryとして位置づける発想は、LangGraphベースの監査Agentのアーキテクチャ設計にも転用できる。

## アイデア

- MCPを『ツール追加の仕組み』ではなく『candidate review lensesを提示するRuntime境界』として使うという逆転発想：Agentの自由を広げるのではなく、渡す自由の形をRuntime側で決める
- RAGのflattening of reasoning問題：複数の論点・矛盾・例外が最終回答で平均化されることがドメインによってはリスクになるという指摘と、それに対してOutput Boundaryでverdictではなくverification questionsに止めるという設計解
- 境界をプロンプトではなくRuntime側に置くことで観測可能性（observability）を確保する：どの観点を使ったか・なぜverdictに進まなかったかがRuntime側でトレースできるようになる

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Tool Calling** → /deep_946 HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に
- **LLM Agent** → /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果
- **Runtime設計** (TODO: 読むべき)

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_6412 コンテキストエンジニアリングは7要素の組み合わせ ── 構成図で見る全体像

## 原文リンク

[MCPをContext Boundaryとして使う：AgentのCapability Shapingという設計思想](https://zenn.dev/mofuteq/articles/be562471f96a68)
