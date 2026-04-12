---
title: "smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ"
url: "https://huggingface.co/blog/smolagents"
date: 2026-04-08
tags: [smolagents, CodeAgent, HuggingFace, LiteLLM, E2B, ToolCalling, multi-step-agent, LLM-agent]
category: "agent-arch"
memo: "[HF Blog] Introducing smolagents: simple agents that write actions in code."
processed_at: "2026-04-08T12:26:14.081553"
---

## 要約

HuggingFaceが2024年12月31日にリリースしたsmolagentsは、LLMにエージェント機能を付与するための軽量Pythonライブラリ。コアロジックは数千行程度に抑えられており、シンプルさを最大の設計原則としている。

最大の特徴は「Code Agent」アーキテクチャで、従来のJSON形式のツール呼び出し（OpenAI/Anthropicが採用する形式）ではなく、Pythonコードそのものでアクションを記述させる点。この手法の優位性は研究論文（Executable Code Actions Elicit Better LLM Agents等）によっても示されており、コードの方がJSON比で合成性・オブジェクト管理・汎用性・LLM学習データとの整合性に優れる。たとえば generate_image の出力をJSONで保持するのは困難だが、コードなら変数に代入するだけで済む。

エージェントのループ構造は「memory = [task] → while llm_should_continue(memory): action = llm_get_next_action(memory) → execute_action(action) → memory += [action, observations]」というシンプルな形で実装される。

ライブラリが提供するコンポーネントは主に2つ：(1) CodeAgent（Pythonコードでアクションを記述、E2Bサンドボックス実行に対応）、(2) ToolCallingAgent（従来型JSON/テキスト形式）。モデルはHugging Face Inference API（HfApiModel）のほか、LiteLLM経由でOpenAI・Anthropicなど任意のLLMに対応。ツールはHugging Face Hubで共有・ロード可能。

smolagentsはtransformers.agentsの後継であり、将来的にtransformers.agentsは廃止予定。エージェントの使用判断基準として「ワークフローが事前に決定できない場合にのみ使用する」という原則が明示されており、複雑性のためだけにエージェントを採用しないよう警告している。オープンモデルのエージェント性能評価も含まれており、Qwen2.5-Coder-32B-InstructがGPT-4oと同等のベンチマーク結果を示した。

## アイデア

- JSONではなくPythonコードでアクションを記述させることで、ツール出力の変数保持・ループ・条件分岐をLLMが自然に扱える。これはJSON形式のツール呼び出しに比べて表現力が根本的に異なる
- エージェントの「agency」を0/1ではなく連続スペクトラムとして定義しており、Router（★☆☆）→Tool call（★★☆）→Multi-step Agent（★★★）→Multi-Agent（★★★）という段階的な分類が実用的な設計判断の指針になる
- Qwen2.5-Coder-32B-InstructがGPT-4oと同等のエージェントベンチマーク性能を示しており、オープンモデルでもCode Agent形式であれば商用モデルに匹敵できることを示す

## Yujiの取り組みへの示唆

smolagentsのCodeAgentアーキテクチャは、LangGraphで構築中の監査エージェントにおけるツール呼び出し設計の参考になる。特にE2Bサンドボックス上でPythonコードを実行する仕組みは、監査ロジック（仕訳検証・異常検知スクリプト）をエージェントに動的生成・実行させる際の安全な実装パターンとして直接応用可能。またHugging Face Hub経由でツールを共有できる設計は、監査特化ツール（勘定科目分類器、リスク評価関数等）をチーム内でモジュール化・再利用する際のインフラとして活用できる。transformers.agentsの後継であるためHugging Faceエコシステムとの統合も容易で、ローカルLLM（RTX 3090環境）との組み合わせでオフライン監査エージェントを構築する際の選択肢になる。

## 原文リンク

[smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ](https://huggingface.co/blog/smolagents)
