---
title: "Stochastic Depth（DropPath）を実装したらパラメータ増やさずに精度が約9ポイント上がった【Keras実験】"
url: "https://zenn.dev/wasurenamemo/articles/342e3c0fc1786e"
date: 2026-05-28
tags: [StochasticDepth, DropPath, Keras, 正則化, ResidualBlock, CIFAR-10, TensorFlow, InvertedDropout]
category: "ai-ml"
related: [4192, 4405, 6419, 6640, 2656]
memo: "[Zenn 機械学習] Stochastic Depth（DropPath）を実装したらパラメータ増やさずに精度が約9ポイント上がった【Keras実験】"
processed_at: "2026-05-28T09:09:06.244138"
---

## 要約

Stochastic Depth（確率的深度、別名DropPath）は、ResNeXt・EfficientNet・DeiTなど近年の高精度モデルで広く採用されている正則化手法である。Dropoutがニューロン単位でランダムにOFFにするのに対し、Stochastic DepthはConv層のグループ（残差ブロック）単位ごとまるごとランダムにスキップする「Dropoutのブロック版」として機能する。本記事では、KerasでStochastic Depthカスタムレイヤーを自前実装し、CIFAR-10データセットを用いてdrop_rateを変えた3パターン（なし・0.1・0.2）の精度・学習時間・パラメータ数を比較実験した。結果として、ベースライン（SDなし）のtest accuracy 72.80%に対し、drop_rate=0.1では81.62%と約8.8ポイント向上した。特筆すべきはパラメータ数が3パターンとも695,114で完全に同一であり、純粋に正則化効果のみで精度改善が得られた点である。drop_rate=0.2ではBより約2.4ポイント低下し79.23%となり、正則化が強すぎるとモデルの学習能力が損なわれることを示している。実装上の核心はResidual接続（スキップ接続）が必須という点で、ブロックをスキップした際に入力がショートカット経由で次の層に渡されなければ情報が完全にロストし学習が崩壊する。また学習時に `x / keep_prob * random_tensor` でInverted Dropoutと同様のスケーリングを行うことで、推論時に特別なスケーリング補正が不要になる。drop_rateの目安として0.1が汎用的なスタート地点であり、より深いネットワーク（8層以上）ではdrop_rateを高めるLinear Decayスケジュールが実務標準とされる。監査エージェント開発への直接的な示唆として、パラメータを増やさずに過学習を抑制するこの手法はリソース制約が厳しい環境でのモデル改善に有効であり、LangGraphなどで構成するエージェントの内部モデルの品質向上に応用できる可能性がある。

## アイデア

- パラメータ数ゼロ増でtest accuracy +8.8ポイントという結果は、正則化手法の選択がアーキテクチャ設計と同等以上にインパクトを持つことを示す好例
- ブロック単位のスキップはアンサンブル学習的な効果をもたらし、深いネットワークほど多様な深さのサブネットワークを暗黙的に学習させるという理論的根拠がある
- Linear Decayスケジュール（浅い層は低drop_rate、深い層は高drop_rate）という実務標準は、層の重要性・情報の流れの観点から理論的に妥当であり、固定drop_rateより有望な拡張方向

## 前提知識

- **Residual Network** (TODO: 読むべき)
- **Dropout / 正則化** (TODO: 読むべき)
- **Inverted Dropout** (TODO: 読むべき)
- **畳み込みニューラルネットワーク** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **Keras / TensorFlow** (TODO: 読むべき)

## 関連記事

- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- /deep_4405 【AdamWとは】Adamとの違いをコードと実験グラフで徹底解説
- /deep_6419 SEブロックとResidual接続を組み合わせたら予想外の結果に【Keras×CIFAR-10実験】
- /deep_6640 MaxPooling vs AveragePooling（中間層）：CIFAR-10で比較したらMNISTと逆の結果になった【Keras実験】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】

## 原文リンク

[Stochastic Depth（DropPath）を実装したらパラメータ増やさずに精度が約9ポイント上がった【Keras実験】](https://zenn.dev/wasurenamemo/articles/342e3c0fc1786e)
