---
title: "【AdamWとは】Adamとの違いをコードと実験グラフで徹底解説"
url: "https://zenn.dev/wasurenamemo/articles/4b0e9937a301b2"
date: 2026-05-08
tags: [AdamW, Adam, Weight Decay, オプティマイザ, Keras, TensorFlow, 正則化, Decoupled Weight Decay]
category: "ai-ml"
related: [4192, 2783, 2656, 1578, 2965]
memo: "[Zenn 機械学習] 【AdamWとは】Adamとの違いをコードと実験グラフで徹底解説"
processed_at: "2026-05-08T12:27:18.104110"
---

## 要約

AdamWは、2017年の論文「Decoupled Weight Decay Regularization」で提案されたオプティマイザで、標準的なAdamオプティマイザにWeight Decay（重み減衰）を正しく組み込んだ改良版である。

Adamの問題点は、L2正則化を勾配に直接加算する形で実装されている点にある。Adamはパラメータごとに学習率を自動スケーリングする機構（二次モーメント推定）を持つが、L2正則化項を勾配に混入させると、このスケーリングと干渉し、実質的なWeight Decayの強度がパラメータごとに不均一になる。結果として、正則化が意図通りに機能せず、過学習への対策効果が弱まる。

AdamWはこの問題を「Decoupled（分離）」方式で解決する。具体的には、パラメータ更新を2ステップに分離し、①勾配に基づく通常のAdam更新と、②重みに対して直接スケールする独立したWeight Decayステップを行う。これにより、Weight Decayが学習率スケーリングの影響を受けず、全パラメータに対して均一かつ設計通りの正則化強度で適用される。

実用上の推奨は明確で、Weight Decayを0に設定すればAdamWはAdamと同一の挙動を示すため、AdamWはAdamの上位互換として機能する。TransformerやBERTなど大規模モデルの学習では現在AdamWが標準的に採用されている。

使い分けの基準として、小規模データセットでの素早いプロトタイピングや、Dropoutのみで正則化が十分な場合はAdamで構わないが、汎化性能を重視する本格的な学習ではAdamWが推奨される。MNISTを用いたAdam vs AdamWの比較実験では学習曲線グラフで差異が確認されており、実装はKeras/TensorFlowで行われている。監査エージェント開発においても、LangGraphベースのモデルファインチューニング時にAdamWを採用することで過学習リスクを低減できる。

## アイデア

- Weight DecayをL2正則化として勾配に混入する実装と、パラメータ更新と独立して適用する実装は数式上は似て見えるが、Adamの適応的学習率スケーリングと組み合わさると挙動が根本的に異なる点は、実装の細部が性能に直結する典型例
- AdamWのWeight Decay=0でAdamと等価になる設計は、後方互換性を保ちながら上位互換を実現するAPIデザインの好例であり、ハイパーパラメータのデフォルト値設計の重要性を示す
- MNISTのような小規模・単純なデータセットではAdamとAdamWの差が軽微でも、Transformerや大規模モデルでは差が顕著になる点は、正則化手法の効果がモデル複雑度・データ規模に依存することを示す

## 前提知識

- **Adamオプティマイザ** (TODO: 読むべき)
- **Weight Decay / L2正則化** (TODO: 読むべき)
- **勾配降下法** → /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- **過学習・汎化** (TODO: 読むべき)
- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは

## 関連記事

- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】

## 原文リンク

[【AdamWとは】Adamとの違いをコードと実験グラフで徹底解説](https://zenn.dev/wasurenamemo/articles/4b0e9937a301b2)
