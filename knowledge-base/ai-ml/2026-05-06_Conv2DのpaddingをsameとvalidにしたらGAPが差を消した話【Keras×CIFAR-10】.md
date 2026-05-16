---
title: "Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】"
url: "https://zenn.dev/wasurenamemo/articles/0de8db0ff28d66"
date: 2026-05-06
tags: [Keras, CNN, CIFAR-10, padding, GlobalAveragePooling, TensorFlow, Conv2D]
category: "ai-ml"
related: [2783, 2656, 2965, 3652, 1578]
memo: "[Zenn 機械学習] Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】"
processed_at: "2026-05-06T12:28:39.770095"
---

## 要約

CIFAR-10データセットを用いて、Keras（TensorFlow）のConv2Dレイヤーにおけるpadidng='same'とpadding='valid'の精度・パラメータ数・学習時間を比較した実験記事。

結果はsame: Test Acc 66.91%（145.3秒）、valid: Test Acc 66.26%（124.4秒）で、精度差はわずか0.65%、パラメータ数は93,450で完全一致した。

パラメータ数が一致した理由はGlobalAveragePooling2D（GAP）にある。validパディングでは畳み込みのたびに特徴マップが縮小し（例: Conv2D後32×32→30×30、MaxPooling後16×16→15×15、さらにConv2D×2後16×16→13×13、MaxPooling後8×8→6×6）、最終的にsameが8×8×128、validが6×6×128と異なるサイズになる。しかしGAPは「チャンネルあたり1つの平均値」に集約するため、どちらも128次元ベクトルに変換され、後続のDense層への入力次元が揃い、パラメータ数が一致する。

興味深い点として、val_accuracyではvalid（67.28%）がsame（67.17%）をわずかに上回ったが、test_accuracyではsame（66.91%）がvalid（66.26%）を上回り、評価セットによって勝敗が逆転した。差は最大0.65%と誤差の範囲内であり、統計的有意差はない。

学習時間はvalidがパディング計算不要かつ特徴マップが小さいため約21秒（約14%）短縮された。精度が同等であれば計算コスト面でvalidに利点がある。

一方、Flatten使用モデルの場合はvalidによる特徴マップ縮小がDense層の入力次元を減らしパラメータ数が変化するため、sameが有利になりやすい。実用的な指針として「迷ったらsame、GAP使用モデルなら大きな差は出ない」とまとめられている。監査AIや一般的なCNN設計においても、GAPを挟む構成ではpaddingの選択が精度に与える影響は小さく、推論・学習コスト最適化の観点でvalidを選ぶ余地があると示唆される。

## アイデア

- GAPがsame/validの特徴マップサイズ差を完全に吸収することで、padding選択がパラメータ数に無影響になるという設計上の性質は、モデルのポータビリティ（異なる入力解像度への対応）にも応用できる
- val_accuracyとtest_accuracyで勝敗が逆転した点は、ハイパーパラメータ選択をvalidation setのみで行う危険性を示す小さなケーススタディになっている
- 14%の学習時間削減はpaddingの有無という些細な変更から生まれており、同等精度でコスト削減を狙う際にFlatten→GAP置き換えとvalid padding組み合わせが有効な選択肢になりうる

## 前提知識

- **Conv2D** → /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- **GlobalAveragePooling2D** → /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- **MaxPooling** → /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **Flatten vs GAP** (TODO: 読むべき)

## 関連記事

- /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_3652 CNNのDense層をReLUからELUに変えたら精度が上がった話【Keras×CIFAR-10】
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針

## 原文リンク

[Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】](https://zenn.dev/wasurenamemo/articles/0de8db0ff28d66)
