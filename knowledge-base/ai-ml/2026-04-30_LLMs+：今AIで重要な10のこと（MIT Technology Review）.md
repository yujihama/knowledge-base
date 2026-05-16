---
title: "LLMs+：今AIで重要な10のこと（MIT Technology Review）"
url: "https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/"
date: 2026-04-30
tags: [LLM, Mixture-of-Experts, Diffusion Model, Recursive LLM, Context Window, MIT CSAIL, DeepSeek, Transformer代替]
category: "ai-ml"
related: [1335, 203, 150, 196, 99]
memo: "[MIT Technology Review AI] LLMs+"
processed_at: "2026-04-30T12:43:22.279030"
---

## 要約

MIT Technology Reviewが「LLMs+」という概念で、現在のLLM進化の主要トレンドを整理した記事。2022年末のChatGPT登場以降、LLMはあらゆる産業に浸透したが、次フェーズは「より良いLLM」であるとし、その実現に必要な技術的進歩を複数の軸で解説している。

第一の軸は効率化・低コスト化。Mixture-of-Experts（MoE）アーキテクチャでは、モデルを専門性の異なる小モジュールに分割し、タスクに応じて必要な部分だけを起動することで計算コストを削減する。またTransformerに代わるアーキテクチャとして、画像・動画生成で実績のあるDiffusion Modelをテキスト生成に適用する試みも進んでいる。DeepSeekは2025年にテキストを画像としてエンコードする手法を発表し、計算コスト削減の別アプローチを示した。

第二の軸はコンテキストウィンドウの拡大と信頼性向上。数年前は数千トークン（数十ページ）程度だったが、最新モデルでは100万トークン（書籍数冊分）に達している。しかし、コンテキストが長くなるほどモデルが「脱線」したり指示を忘れる問題が顕在化する。これに対しMIT CSAILの研究者が提案した「Recursive LLM」は、巨大なコンテキストを一括処理するのではなく、入力をチャンクに分割して自身のコピーに順次渡す再帰的構造を採用。複数のLLMが小さな情報断片を並列・階層的に処理することで、長時間・複雑タスクでの信頼性が大幅に向上するという。

全体のゴールは「人間が数日〜数週間かける複雑・多段階タスクをLLMが自律的に処理できること」であり、主要AI研究機関の共通目標となっている。OpenAIは完全自動化された研究者システム構築を推進中（同誌の別記事で詳報）。また、Stanford 2026 AI Indexによれば、AI進化速度は人間の適応速度を上回っているとされる。

監査エージェント開発への示唆：Recursive LLMのアーキテクチャは、長大な監査証跡・ドキュメントを階層的に分析するエージェント設計に直接応用可能。また、MoEによる専門モジュール分割は、監査ルール・会計基準・リスク評価など領域ごとに専門化したサブエージェントを組み合わせるマルチエージェント設計と概念的に親和性が高い。

## アイデア

- Recursive LLMは入力を再帰的にチャンク分割して自己コピーに委譲する構造で、長文タスクの信頼性問題を階層処理で解決する点が新しい——LangGraphの再帰的サブグラフ設計と概念的に対応する
- TransformerではなくDiffusion Modelでテキスト生成を行う試みは、確率的サンプリングプロセスを生成に利用するという根本的なパラダイム転換であり、推論速度・品質トレードオフへの影響が注目される
- DeepSeekのテキスト→画像エンコード手法は、既存の画像圧縮・処理パイプラインを計算コスト削減に転用するというハードウェア制約への創意ある対応であり、エッジデプロイ文脈で応用可能性がある

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **Context Window** → /deep_3151 LLMs+：現在のAIで重要な10のこと（MIT Technology Review）
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **LLM推論コスト** (TODO: 読むべき)

## 関連記事

- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_150 TransformersライブラリにおけるMixture of Experts (MoE)の実装と最適化
- /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する

## 原文リンク

[LLMs+：今AIで重要な10のこと（MIT Technology Review）](https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/)
