---
title: "LLMs+：今AIで本当に重要な10のこと（MIT Technology Review）"
url: "https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/"
date: 2026-05-07
tags: [LLM, Mixture-of-Experts, Diffusion Models, Recursive LLM, Context Window, DeepSeek, Transformer, MIT CSAIL, エージェント化]
category: "ai-ml"
related: [99, 216, 1335, 3534, 203]
memo: "[MIT Technology Review AI] LLMs+"
processed_at: "2026-05-07T21:53:10.172069"
---

## 要約

MIT Technology Reviewが「LLMs+」という概念でまとめた、現在のAI開発における主要な技術的前進の概観記事。2022年末のChatGPT登場以来、LLMは日常的なツールとなったが、次のフェーズは「LLMをより良くすること」であり、著者はこれをLLMs+と命名している。

主要な技術トレンドは以下の通り：

①**効率化：Mixture-of-Experts（MoE）**。LLMを複数の専門化されたサブモデルに分割し、タスクに応じて一部だけを起動する手法。計算コストを大幅に削減できる。

②**Transformerの代替：拡散モデル（Diffusion Models）**。画像・動画生成で実績のある拡散モデルをテキスト生成に転用するアプローチ。Transformerに依存しない新たなアーキテクチャの模索が進んでいる。

③**テキストの画像エンコード（DeepSeek）**。中国のAI企業DeepSeekが示した、テキストを画像として符号化することで計算コストを削減する実験的手法。

④**コンテキストウィンドウの拡大と信頼性問題**。数年前は数千トークン（数十ページ）だったコンテキスト窓が、現在は最大100万トークン（書籍数冊分）に拡大。しかし窓が大きくなるほどモデルが「脱線」するリスクが増大する。

⑤**再帰的LLM（Recursive LLMs）**。MIT CSAILの研究者が提唱。巨大なコンテキストを一括処理する代わりに、入力をチャンクに分割して自身のコピーに送り、さらに細分化を繰り返す再帰的処理を行う。複数のLLMインスタンスが小さな情報片を並列処理することで、長距離・高難度タスクの信頼性が大幅に向上するとされる。

記事が示す方向性は、LLM単体の能力向上だけでなく、複数モデルの協調・再帰的処理・アーキテクチャ多様化による「エージェント化」への布石である。監査エージェント開発の観点では、再帰的LLMは長文の監査報告書や複雑な規制文書の処理精度向上に直結する可能性があり、MoEによるコスト削減はローカルLLMインフラ上での実用化を後押しする技術として注目に値する。

## アイデア

- 再帰的LLM（Recursive LLM）：入力を再帰的にチャンク分割して自身のコピーに渡す構造は、LangGraphのサブグラフ再帰やReActの多段推論と概念的に近く、監査エージェントの長文処理ループ設計に応用できる可能性がある
- Mixture-of-Expertsによる選択的活性化は、監査タスク（財務分析・リスク分類・文書照合等）をドメイン別専門モジュールに分割するマルチエージェント設計と親和性が高く、推論コストの最適化戦略として参考になる
- Transformerから拡散モデルへのアーキテクチャ転換の模索は、現在主流のRAG+Transformerベースの検索拡張生成パイプラインが将来的に非Transformerアーキテクチャへ移行する際の互換性リスクを示唆しており、システム設計時の抽象化レイヤーの重要性を再認識させる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **Context Window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く

## 関連記事

- /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_3534 中国のオープンソース戦略：AIの未来をどう塗り替えるか
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ

## 原文リンク

[LLMs+：今AIで本当に重要な10のこと（MIT Technology Review）](https://www.technologyreview.com/2026/04/21/1135645/llm-large-language-models-ai/)
