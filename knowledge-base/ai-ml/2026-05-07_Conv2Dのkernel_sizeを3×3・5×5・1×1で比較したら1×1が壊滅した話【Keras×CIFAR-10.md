---
title: "Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】"
url: "https://zenn.dev/wasurenamemo/articles/e7b8331cf77e8a"
date: 2026-05-07
tags: [Conv2D, kernel_size, Keras, CIFAR-10, CNN, TensorFlow, 1x1畳み込み, ResNet, Bottleneck]
category: "ai-ml"
related: [3911, 2783, 2656, 2965, 3652]
memo: "[Zenn 機械学習] Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】"
processed_at: "2026-05-07T09:50:47.497550"
---

## 要約

KerasのConv2Dレイヤーにおけるkernel_sizeの選択が分類精度・パラメータ数・学習時間に与える影響を、CIFAR-10データセットを用いて実験的に比較した記事。対象とするkernel_sizeは(3,3)・(5,5)・(1,1)の3パターン。

結果として、(5,5)がtest accuracy 69.70%で最高精度を記録した一方、パラメータ数は227,594と(3,3)の93,450に比べ約2.4倍、学習時間も179.7秒と約1.3倍に増加した。精度向上幅（約3.6ポイント）に対してコスト増加が大きく、効率面では(3,3)が優位とされる。

最も注目すべき結果は(1,1)の壊滅的な性能で、test accuracy 41.57%にとどまった。原因は構造的に明確で、1×1カーネルは空間方向（縦・横）の情報を一切参照しないため、エッジ・テクスチャ・形状といった画像の局所的特徴を抽出できない。1×1畳み込みの本来の役割はチャンネル数の圧縮・拡張であり、ResNetのBottleneck構造やGoogleNetのInceptionモジュールのように、3×3カーネルの前後に配置して計算コストを削減しつつ表現力を保つ用途が正しい。単独の画像分類タスクに1×1を使うのは設計上の誤用となる。

kernel_sizeの実践的な選び方として、プロトタイプや迷った場合は(3,3)、精度優先でコストを許容できる場合は(5,5)、チャンネル数調整が目的の場合は(1,1)を他のカーネルサイズと組み合わせることが推奨されている。

監査エージェント開発への直接的な示唆は薄いが、モデル設計において各コンポーネントの「本来の役割」を理解せずに流用することがいかに性能劣化につながるかという教訓は、LangGraphベースのエージェント設計においても構成要素の意味論的な正しい使用という観点で通じるものがある。

## アイデア

- 1×1畳み込みが画像分類で壊滅する理由は『空間情報の不参照』という構造的な制約にあり、精度が低い原因を実験で可視化している点が教育的
- 5×5はパラメータ数が約2.4倍増えるにもかかわらず精度向上は約3.6ポイントにとどまり、スケーリング効率の悪さをシンプルな比較で示している
- ResNetのBottleneckやInceptionにおける1×1の正しい用途（チャンネル圧縮）を対比することで、アーキテクチャ設計パターンの意図が明確になる

## 前提知識

- **Conv2D** → /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **ResNet Bottleneck** (TODO: 読むべき)
- **Inception Module** (TODO: 読むべき)
- **チャンネル圧縮** (TODO: 読むべき)

## 関連記事

- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_3652 CNNのDense層をReLUからELUに変えたら精度が上がった話【Keras×CIFAR-10】

## 原文リンク

[Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】](https://zenn.dev/wasurenamemo/articles/e7b8331cf77e8a)
