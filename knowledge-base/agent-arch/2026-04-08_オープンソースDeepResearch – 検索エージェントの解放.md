---
title: "オープンソースDeepResearch – 検索エージェントの解放"
url: "https://huggingface.co/blog/open-deep-research"
date: 2026-04-08
tags: [smolagents, CodeAgent, GAIA, DeepResearch, DeepSeek-R1, Magentic-One, web-search-agent, multi-step-reasoning]
category: "agent-arch"
memo: "[HF Blog] Open-source DeepResearch – Freeing our search agents"
processed_at: "2026-04-08T09:50:22.908319"
---

## 要約

HuggingFaceチームが、OpenAIのDeep Researchシステムを24時間以内にオープンソースで再現した取り組みの報告。OpenAIのDeep ResearchはGAIAベンチマーク（General AI Assistants benchmark）でバリデーションセット67.36%を達成し、ツールなしのGPT-4（7%未満）と比較して一桁以上の性能向上を示した。GAIAは多段階推論・マルチモーダル・ツール使用を要求する高難度ベンチマークであり、例えば「2008年の絵画に描かれた果物のうち、特定の船の1949年10月の朝食メニューに出されたものを時計回りに列挙せよ」といった複合的な問題が含まれる。HuggingFaceの再現実装の核心は「CodeAgent」アーキテクチャの採用。Wang et al.(2024)の知見に基づき、エージェントのアクション表現にJSONではなくコードを用いることで、(1)ステップ数を平均30%削減、(2)LLMコスト約30%削減、(3)並列アクションの簡潔な表現、(4)状態管理の改善（特にマルチモーダルデータ）を実現した。ツールとしては、テキストベースのウェブブラウザとテキストインスペクタをMicrosoft ResearchのMagentic-Oneから転用。今後はビジョンベースのブラウザへの置き換えやファイル形式の拡充が計画されている。使用LLMはDeepSeek R1等のオープンソースモデルを前提としており、OpenAIのクローズドモデルに依存しない構成を目指している。smolagentsライブラリをエージェントフレームワークとして使用し、コミュニティによる追加再現実装も複数報告されている。

## アイデア

- CodeAgentはJSON形式のアクション列より30%少ないステップで同等タスクを実行でき、LLM呼び出しコストを直接削減できる設計原則
- GAIAベンチマークはエージェント評価の事実上の標準となりつつあり、ツールなしLLM（7%）とエージェント化LLM（67%）の性能差が60ポイント以上に達する
- 状態変数としての中間成果物管理（画像・音声等をコード変数に格納して後続ステップで再利用）はマルチモーダル・エージェントの実装パターンとして汎用性が高い

## Yujiの取り組みへの示唆

監査エージェント開発においてLangGraphベースのReActエージェントを構築しているYujiにとって、CodeAgentのアーキテクチャ（JSONツール呼び出しではなくコード生成によるアクション）は監査証跡の収集・照合ステップの記述を簡潔にする可能性がある。GAIAの多段階推論問題は、内部統制評価における複数文書の連鎖的な検証（例：仕訳→証憑→承認フローの突合）と構造的に類似しており、ベンチマーク設計の参考になる。smolagentsのCodeAgentとLangGraphを比較実装することで、監査タスク特有の要件（監査証跡の再現性、ステップの説明可能性）に適したフレームワーク選定の判断材料が得られる。

## 原文リンク

[オープンソースDeepResearch – 検索エージェントの解放](https://huggingface.co/blog/open-deep-research)
