---
title: "MCP・A2A・Function Calling：3つを混同していませんか？【Google Cloud ADK視点で整理】"
url: "https://zenn.dev/seachickenkatsu/articles/fa13fb7b2b5f68"
date: 2026-05-12
tags: [MCP, A2A, Function Calling, Google ADK, マルチエージェント, Gemini, エージェントアーキテクチャ]
category: "agent-arch"
related: [41, 3638, 4337, 2627, 2]
memo: "[Zenn LLM] MCP・A2A・Function Calling：3つを混同していませんか？【Google Cloud ADK視点で整理】"
processed_at: "2026-05-12T09:16:37.654737"
---

## 要約

LLMが外部と連携するための3つの仕組み（Function Calling・MCP・A2A）は、それぞれ異なるレイヤーの問題を解く補完関係にある。Function Callingは、LLMが「どの関数をどの引数で呼ぶか」をJSON形式で出力し、実際の実行はアプリ側が担う仕組み。OpenAIが2023年6月に導入し、LLMに「手」を持たせる最もシンプルな方法だが、ツール定義をアプリごとに書き直す再利用性の問題がある。MCPはこの問題を解決するためAnthropicが2024年11月に提唱したオープンプロトコルで、ツール定義をMCPサーバーとして外部に切り出すことで、どのLLM・どのアプリからも接続可能にする。USB-Cの比喩が示す通り、一度作ったMCPサーバーはGemini・Claude等複数のLLMから共用できる。Googleは2026年時点でBigQuery・Google Maps・Google Analytics・LookerなどのフルマネージドMCPサーバーを提供している。MCPサーバーはTools（LLMが呼べる関数）・Resources（参照データ）・Prompts（再利用可能テンプレート）の3要素を外部公開する。A2AはGoogleが2025年4月に提唱したプロトコルで、ADK・LangChain・Amazon Bedrock・Azure AI Foundryなど異なるフレームワーク間のエージェント通信を標準化する。2026年時点で150以上の組織が参加しデファクトスタンダードとなっている。ADKでは`sub_agents=[]`にサブエージェントを登録することでA2A連携を実現する。3者の方向性を整理すると、Function CallingとMCPはLLM↔外部ツールを繋ぐ「縦方向（垂直）」の問題を解き、A2Aはエージェント↔エージェントを繋ぐ「横方向（水平）」の問題を解く。実際のプロダクトでは、エージェント内のツール呼び出しにFunction Calling/MCPを使い、エージェント間連携にA2Aを使うという形で3つを組み合わせる。監査エージェント開発への示唆として、調査・分析・レポート・通知を担う専門エージェントをA2Aで連携させ、各エージェントがMCP経由でBigQuery等の内部データソースにアクセスする構成が有効。Function CallingはプロトタイプやAudit固有の小規模ツール（2〜5個程度）に適し、社内DB接続やGRC標準データソースへの接続はMCPサーバー化することでエージェント間の再利用性を高められる。

## アイデア

- 「縦方向（LLM↔ツール）」と「横方向（エージェント↔エージェント）」という2軸でFunction Calling・MCP・A2Aを整理するフレームは、エージェントシステム設計時の判断軸として実用的
- MCPサーバーをUSB-Cに例える比喩が明快：ツール定義をアプリ外に切り出すことで、LLMやフレームワークが変わっても接続ロジックを使い回せる設計思想
- Google ADKの`sub_agents=[]`がA2Aの実装抽象化を担っており、フレームワーク間通信の複雑さを隠蔽しつつマルチエージェント構成を宣言的に記述できる点

## 前提知識

- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Google ADK** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_3638 NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン
- /deep_4337 Harness Engineering Meetup に参加して、AIエージェントの「ハーネス」について考えた
- /deep_2627 Autogenesis：自己進化型エージェントプロトコル
- /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 原文リンク

[MCP・A2A・Function Calling：3つを混同していませんか？【Google Cloud ADK視点で整理】](https://zenn.dev/seachickenkatsu/articles/fa13fb7b2b5f68)
