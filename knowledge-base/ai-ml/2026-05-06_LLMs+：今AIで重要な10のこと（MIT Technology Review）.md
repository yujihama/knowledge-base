---
title: "LLMs+：今AIで重要な10のこと（MIT Technology Review）"
url: "https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/"
date: 2026-05-06
tags: [LLM, Mixture-of-Experts, Recursive LLM, context window, Diffusion Model, Transformer, DeepSeek, MIT CSAIL, 長文処理, 効率化]
category: "ai-ml"
related: [99, 216, 1335, 3534, 203]
memo: "[MIT Technology Review AI] LLMs+"
processed_at: "2026-05-06T12:08:22.354021"
---

## 要約

MIT Technology Reviewによる2026年時点のLLM技術動向の概観記事。2022年末のChatGPT登場以降、LLMは「次の大きなもの」として産業全体を席巻してきたが、本記事はその先にある「LLMs+」という概念を提示する。LLMs+とは、人間が数日〜数週間かけて取り組むような複雑・多段階の問題を自律的に解決できるよう改良されたLLMの総称であり、以下の技術領域での進展が鍵となる。

**効率化：Mixture-of-Experts（MoE）と代替アーキテクチャ**
MoEはLLMを専門性の異なる複数の小モデル（エキスパート）に分割し、タスクに応じて必要な部分のみを活性化することで計算コストを削減する手法。また、ほぼ全てのLLMの基盤であるTransformerに代わり、画像・動画生成で実績のある拡散モデル（Diffusion Model）を採用する試みも進行中。DeepSeekが示したテキストを画像としてエンコードして計算コストを削減するアプローチも紹介される。

**コンテキストウィンドウの拡張と信頼性問題**
数年前は数千トークン（数十ページ相当）だったコンテキストウィンドウは、最新モデルで最大100万トークン（書籍数冊分）にまで拡大した。しかし、ウィンドウが長くなるほど、モデルが指示を忘れたり脱線したりするリスクも増大する。

**Recursive LLMs（MIT CSAIL）**
この問題への有望な解法として、MIT CSAILの研究者が提案した「Recursive LLM」がある。巨大なコンテキストを一括処理する代わりに、入力をチャンクに分割し、各チャンクを自身のコピーに渡す再帰的構造を持つ。さらにそのコピーが再分割して別のコピーに渡すことも可能。小さな情報単位を並列処理する複数のLLMにより、長くて難しいタスクの信頼性が大幅に向上するとされる。

**監査エージェント開発への示唆**
Recursive LLMの構造は、長大な監査文書や複数の内部統制項目を段階的・再帰的に処理するエージェント設計に直接応用可能。MoEによるコスト削減は、推論頻度の高い監査エージェントのランニングコスト管理にも有効。また、長文コンテキストの信頼性問題はLangGraphのような多段階エージェントフレームワークで設計上考慮すべき重要課題である。

## アイデア

- Recursive LLMは入力を再帰的にチャンク分割して自身のコピーに渡す構造であり、これはMapReduceやツリー型マルチエージェント設計と概念的に近く、LangGraphのサブグラフ分割設計に応用できる可能性がある
- TransformerからDiffusion Modelへのアーキテクチャ転換は、テキスト生成の確率的サンプリングプロセスを根本的に変えるものであり、将来的なLLMの推論コスト・速度特性を大きく変える可能性がある
- DeepSeekのテキスト→画像エンコーディングによるコスト削減は、モダリティ変換を計算効率化の手段として使うという逆転の発想であり、マルチモーダルモデルの設計思想を刷新するかもしれない

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **context window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Recursive LLM** → /deep_3151 LLMs+：現在のAIで重要な10のこと（MIT Technology Review）

## 関連記事

- /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_3534 中国のオープンソース戦略：AIの未来をどう塗り替えるか
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ

## 原文リンク

[LLMs+：今AIで重要な10のこと（MIT Technology Review）](https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/)
