---
title: "FutureBench: 未来のイベント予測によるAIエージェント評価フレームワーク"
url: "https://huggingface.co/blog/futurebench"
date: 2026-04-07
tags: [FutureBench, benchmark, prediction-market, Polymarket, smolagents, DeepSeek-V3, Firecrawl, Tavily, agent-evaluation, forecasting]
category: "agent-arch"
memo: "[HF Blog] Back to The Future: Evaluating AI Agents on Predicting Future Events"
processed_at: "2026-04-07T12:20:52.569491"
---

## 要約

FutureBenchは、AIエージェントが未来のイベントを予測する能力を評価するベンチマークフレームワークである。従来のベンチマーク（HLE、GPQA、GAIAなど）が過去の知識や既知の解答を対象とするのに対し、FutureBenchは実世界の予測市場（Polymarket）とニュース記事から生成した未来の問いを評価対象とする。

質問生成は2つのアプローチで行われる。1つ目は、smolagentsベースのエージェントが主要ニュースサイトをスクレイピングし、DeepSeek-V3を用いて記事から予測問題を生成する方式（週5問程度、予測期間は1週間）。2つ目はPolymarketからの取り込みで、週約8問を収集し、気温・株式・暗号通貨関連の汎用質問はフィルタリングして除外する。技術スタックはDeepSeek-V3（推論・質問生成）、Firecrawl（スクレイピング）、Tavily（検索補完）。

評価は3つの階層で構成される。Level 1はフレームワーク比較（LangChain vs CrewAI等、LLMとツールを固定してフレームワークの影響を測定）、Level 2はツール性能比較（Tavily/Google/Bing等の検索ツールをLLMとフレームワーク固定で比較）、Level 3はモデル比較（フレームワークとツールを固定してLLM本体の予測能力を測定）。

設計上の最大の利点はデータ汚染（contamination）の原理的排除である。存在しないデータで学習することは不可能なため、モデルが訓練データを暗記して高スコアを得る問題が構造的に起きない。また予測結果は時間経過で客観的に検証可能であり、スコアの信頼性が高い。

実験結果として、エージェントが予測市場の確率（例: 60%）より有意に高い正答率を達成できるかを検証しており、単純な「Yes/No」の均等確率（50%）を超えることは確認されているが、予測市場の専門的確率を大きく上回ることの難しさも示している。評価指標にはBrier ScoreやCalibration Errorが使用される。

## アイデア

- データ汚染を原理的に回避する評価手法として、未来のイベント予測をベンチマーク化する設計思想は、他のエージェント評価にも応用可能な重要なパラダイム
- 予測市場（Polymarket）の確率値を基準値（baseline）として使うことで、エージェントの予測精度を相対的に定量化できる点が実用的
- フレームワーク・ツール・モデルを独立変数として分離する3層評価設計により、エージェントシステムのどのコンポーネントがボトルネックかを特定できる
## 関連記事

- /deep_29 OpenEnv実践：実世界環境でのツール使用エージェント評価フレームワーク
- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_212 波形から知恵へ：聴覚知能の新ベンチマーク MSEB（Massive Sound Embedding Benchmark）
- /deep_902 日本語LLMオープンリーダーボードの公開
- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）

## 原文リンク

[FutureBench: 未来のイベント予測によるAIエージェント評価フレームワーク](https://huggingface.co/blog/futurebench)
