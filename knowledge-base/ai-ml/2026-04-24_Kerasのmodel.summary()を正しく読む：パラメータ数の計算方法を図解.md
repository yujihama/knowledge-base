---
title: "Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解"
url: "https://zenn.dev/wasurenamemo/articles/caa1ce29e960da"
date: 2026-04-24
tags: [Keras, TensorFlow, Conv2D, Dense, GlobalAveragePooling2D, model.summary, パラメータ数, ディープラーニング]
category: "ai-ml"
related: [2656, 1578, 1616, 1574, 1710]
memo: "[Zenn 機械学習] Kerasのmodel.summary()、ちゃんと読めてますか？パラメータ数の計算方法を図解"
processed_at: "2026-04-24T12:08:10.195299"
---

## 要約

KerasでCNNやDenseモデルを構築した際に出力される`model.summary()`の3列（Layer type、Output Shape、Param #）の意味と、各層のパラメータ数の計算ロジックを解説した入門記事。

Output ShapeのNoneはバッチサイズが実行時まで未確定であることを示す。Param #はPoolingやFlattenでは常に0であり、学習対象の重みを持つ層にのみ値が入る。

Conv2Dのパラメータ数は「(カーネルH × カーネルW × 入力チャネル数 + 1) × フィルター数」で求まる。例えばConv2D(32, (3,3), input_shape=(28,28,1))の場合は(3×3×1+1)×32=320となる。+1はバイアス項に相当する。

Denseのパラメータ数は「(入力ユニット数 + 1) × 出力ユニット数」で計算される。Flatten後にDense層を置くとパラメータが爆発する典型例として、Flattenの出力が8,192次元になるケースでDense(128)を適用すると約105万パラメータが必要になることが示されている。

この問題への対処として、GlobalAveragePooling2D（GAP）をFlattenの代わりに使う手法が紹介されており、同等の精度を維持しつつパラメータ数を大幅削減できる。GAPは各特徴マップをチャネルごとに空間方向で平均化し、出力テンソルをチャネル数次元のベクトルに圧縮するため、Flattenと比較して後続Dense層への入力次元を劇的に小さく抑えられる。

監査エージェント開発への直接的な示唆は薄いが、軽量なオンデバイス推論モデルやエッジAIを検討する際にモデルサイズの見積もりと削減手法を理解する基礎となる。

## アイデア

- Conv2Dのパラメータ数にバイアス項(+1)が含まれる点を明示しており、フィルター数ごとに1バイアスが存在することが数式から直感的に理解できる
- GlobalAveragePooling2D(GAP)はFlattenの代替として空間次元を平均化するため、後続Dense層の入力次元を入力解像度に依存させず定数（チャネル数）に固定できる点が設計上強力
- model.summary()を読み解けるとモデル設計ミス（意図しないパラメータ膨張）をコード実行前に発見できるデバッグ手法として活用可能

## 前提知識

- **Conv2D** (TODO: 読むべき)
- **Dense層** (TODO: 読むべき)
- **Flatten** → /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- **GlobalAveragePooling2D** → /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- **バックプロパゲーション** (TODO: 読むべき)

## 関連記事

- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針
- /deep_1616 TensorFlowとXLAによる高速テキスト生成
- /deep_1574 HuggingFace ViTモデルをVertex AIにデプロイする
- /deep_1710 Habana GaudiでTransformersを使い始める：AWS EC2 DL1インスタンスでのBERTファインチューニング

## 原文リンク

[Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解](https://zenn.dev/wasurenamemo/articles/caa1ce29e960da)
