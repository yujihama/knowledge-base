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
## 関連記事

- /deep_827 smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_125 SliderQuant: LLM向け高精度ポストトレーニング量子化フレームワーク
- /deep_584 ScreenSuite - GUIエージェント向け最も包括的な評価スイート
- /deep_29 OpenEnv実践：実世界環境でのツール使用エージェント評価フレームワーク

## 原文リンク

[オープンソースDeepResearch – 検索エージェントの解放](https://huggingface.co/blog/open-deep-research)
