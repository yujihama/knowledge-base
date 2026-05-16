---
title: "LLMs+：今AIで重要な10のこと（MIT Technology Review）"
url: "https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/"
date: 2026-05-05
tags: [LLM, Mixture-of-Experts, Recursive LLM, Diffusion Model, Context Window, DeepSeek, MIT CSAIL, 長期エージェント]
category: "ai-ml"
related: [1335, 3534, 203, 150, 196]
memo: "[MIT Technology Review AI] LLMs+"
processed_at: "2026-05-05T12:15:46.369730"
---

## 要約

MIT Technology Reviewが「LLMs+」と名付けた次世代LLMの方向性を概説した記事。2022年末のChatGPT登場以降、LLMは社会インフラ化したが、次の課題は「人間が数日〜数週間かかる複雑・多段階タスクをAIが自律的に解決できるか」である。そのために必要な技術進化として、以下の4領域が挙げられている。

①効率化・低コスト化：Mixture-of-Experts（MoE）アーキテクチャにより、LLMを専門領域ごとのサブモデルに分割し、必要なパーツのみを起動することで計算コストを削減する。②Transformerの代替：画像・動画生成で実績のあるDiffusionモデルをテキスト生成に応用する実験的アプローチが進んでいる。③DeepSeekの手法：テキストを画像としてエンコードすることで計算コストを削減する技術を中国のDeepSeekが発表した。④コンテキストウィンドウの拡張と信頼性向上：数年前は数千トークン（数十ページ）だったコンテキスト窓が最新モデルでは100万トークン（書籍数冊分）に達しているが、長くなるほどモデルが脱線・忘却しやすいという問題がある。これに対しMIT CSAILの研究者が提案した「Recursive LLMs」は、大きな入力を分割してそれぞれのチャンクを自身のコピーに渡す再帰的処理により、長大タスクの信頼性を大幅に向上させる。

あわせて関連トピックとして、OpenAIが全自動研究者構築に注力していること（チーフサイエンティストJakub Pachocki談）、Nianticがポケモンgoの30億枚の都市画像を使い配達ロボット向けワールドモデルを訓練していること、Stanford 2026 AI Indexが示すAI加速の実態なども紹介されている。

監査エージェント開発への示唆：Recursive LLMsの「分割→再帰処理→統合」アーキテクチャは、複数文書にまたがる監査手続き（証憑突合・リスク評価チェーンなど）を長期エージェントタスクとして実行する際の信頼性向上手法として直接応用可能。MoEによる推論コスト削減は、監査システムをオンプレミスGPU環境で運用する際のスループット設計にも関係する。

## アイデア

- Recursive LLMsの再帰的チャンク分割アーキテクチャは、LangGraphの並列サブグラフ実行と組み合わせることで、監査エージェントの長期タスク信頼性を高める設計パターンになり得る
- DiffusionモデルをLLMの代替として使うアプローチは、非自己回帰的生成（並列デコード）による推論高速化という点で、リアルタイム監査判断システムのレイテンシ要件に応える可能性がある
- DeepSeekのテキスト→画像エンコーディングによるコスト削減は、モダリティ境界を意図的にクロスさせることで計算効率を上げるという逆転の発想であり、マルチモーダルエージェント設計の新たな最適化軸として注目できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Context Window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **Recursive LLM** → /deep_3151 LLMs+：現在のAIで重要な10のこと（MIT Technology Review）

## 関連記事

- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_3534 中国のオープンソース戦略：AIの未来をどう塗り替えるか
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_150 TransformersライブラリにおけるMixture of Experts (MoE)の実装と最適化
- /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則

## 原文リンク

[LLMs+：今AIで重要な10のこと（MIT Technology Review）](https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/)
