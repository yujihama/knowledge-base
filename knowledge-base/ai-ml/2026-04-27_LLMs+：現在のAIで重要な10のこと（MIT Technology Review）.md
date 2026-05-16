---
title: "LLMs+：現在のAIで重要な10のこと（MIT Technology Review）"
url: "https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/"
date: 2026-04-27
tags: [LLM, Mixture-of-Experts, Diffusion Models, Recursive LLM, Context Window, MIT CSAIL, DeepSeek, Transformer]
category: "ai-ml"
related: [99, 216, 1335, 203, 105]
memo: "[MIT Technology Review AI] LLMs+"
processed_at: "2026-04-27T12:45:07.954743"
---

## 要約

MIT Technology Reviewが「LLMs+」というフレームで、2026年時点のLLM技術の進化方向を整理した記事。ChatGPTが2022年末に登場して以来、LLMは主要技術として定着したが、次の課題は「数日〜数週間かかる複雑な多段階問題を自律的に解かせること」であり、そのためにいくつかの技術的ブレイクスルーが進行中と報告している。

**効率化のアプローチ**として、まず「Mixture-of-Experts（MoE）」が紹介されている。LLMを専門分野ごとの小さなサブモデルに分割し、タスクに応じて必要な部分だけを起動する仕組みで、計算コストを大幅に削減できる。次に、LLMの基盤であるTransformerを「拡散モデル（Diffusion Models）」に置き換えるアプローチが挙げられる。拡散モデルは画像・動画生成で主流の手法だが、テキスト処理への応用が模索されている。さらに実験的手法として、中国のAI企業DeepSeekが2025年に公開した「テキストを画像内にエンコードする手法」も言及されており、これにより計算コストの削減が期待される。

**コンテキストウィンドウの拡大と信頼性**については、数年前は数千トークン（数十ページ相当）だったコンテキスト長が、最新モデルでは最大100万トークン（書籍複数冊相当）に拡大した。しかしウィンドウが大きくなるほど、モデルが「脱線」したり「途中で何をしていたか忘れる」リスクが増す。この問題に対し、MIT CSAILの研究者らが「Recursive LLMs（再帰的LLM）」を提案している。巨大なコンテキストを一度に処理するのではなく、入力をチャンクに分割し、各チャンクを自分自身のコピー（サブモデル）に渡し、さらにそのコピーが再びチャンクを細分化して別のコピーに送るという再帰的構造を採る。複数のLLMが小さな情報片を並列処理することで、長時間・高難度タスクでの信頼性が大幅に向上するとされる。

監査エージェント開発への示唆としては、Recursive LLMsのアーキテクチャが特に重要。監査タスクは長大な契約書・財務データ・規制文書を横断的に参照する多段階推論を要するため、コンテキスト長の限界とハルシネーション問題が直結する。チャンク分割と再帰的サブエージェント呼び出しのパターンは、LangGraphによるサブグラフ設計やReActループの多段化に直接応用できる観点である。

## アイデア

- Recursive LLMsは入力を再帰的にチャンク分割して複数の自己コピーに処理させる構造で、単一の巨大コンテキストよりも長タスクの信頼性が高い——これはLangGraphのサブグラフ多段化やエージェント分業設計と同じ思想
- TransformerからDiffusion Modelへの置き換えという方向性は、テキスト生成の確率モデルを根本から変えうる実験的潮流であり、将来のLLMアーキテクチャ選定に影響しうる
- DeepSeekの「テキストを画像内にエンコード」する手法は、モダリティ境界を意図的に曖昧にすることで計算グラフを最適化するという逆張り的アプローチであり、推論コスト削減の新たな方向を示す

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Context Window** (TODO: 読むべき)
- **Recursive Neural Network** (TODO: 読むべき)

## 関連記事

- /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_105 TransformerでAttention Residualsを観察する

## 原文リンク

[LLMs+：現在のAIで重要な10のこと（MIT Technology Review）](https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/)
