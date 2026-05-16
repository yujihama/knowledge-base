---
title: "Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験"
url: "https://zenn.dev/wasurenamemo/articles/35b0e4754e2a44"
date: 2026-05-10
tags: [Data Augmentation, CIFAR-10, Keras, 画像分類, CNN, 過学習, RandomRotation, 実験比較]
category: "ai-ml"
related: [2656, 2965, 4192, 3911, 4049]
memo: "[Zenn 機械学習] Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験"
processed_at: "2026-05-10T12:51:37.898318"
---

## 要約

Data Augmentation（データ拡張）はCNN等の画像分類モデルの過学習を抑える定番手法だが、「強くかけるほど良い」とは限らない。本記事はGoogle Colab上でCIFAR-10（32×32px）とKerasを用い、拡張なし・flip・flip+rotation・flip+rotation+zoom・flip+rotation+zoom+cropの5パターンを同一条件で比較実験した結果を報告する。

実験結果は予想外の傾向を示した。最高精度はflipのみのパターンB（69.35%）であり、ベースライン（68.09%）をわずかに上回った。しかしrotationを加えたパターンCは58.71%と約10%急落し、zoom・cropをさらに重ねるにつれて57.82%、53.60%と単調に低下した。学習時間は拡張が増えるほど延びており（134秒→227秒）、精度と計算コストがトレードオフではなく共に悪化するという結果になった。

精度急落の主因はKerasにおけるRandomRotationの仕様にある。引数0.15は最大±54度（0.15×360°）の回転を意味する。32×32という低解像度では±54度の回転でコーナーに黒い余白が発生し、被写体が大きく歪む。モデルは「本物の犬」ではなく「斜めに歪んだ犬」という人工的なアーティファクトを学習することになり、汎化性能が低下する。同様の設定値でも224×224以上の高解像度画像（ImageNet等）では相対的な歪みが小さく問題になりにくいため、「flip+rotationは定番」という通念が形成されているが、これは解像度依存の前提条件がある。

実験の教訓として、低解像度（32×32程度）ではflipのみを推奨し、rotationを使う場合はRandomRotation(0.05)（±18度）以下から試すべきとしている。高解像度（224×224以上）では従来通りflip+rotation+zoomの組み合わせが有効。「定番設定をそのままコピーしない」ことが最大の学びであり、適用するデータの解像度・ドメイン特性に合わせてAugmentationの種類と強度を慎重に調整する必要がある。監査AI開発への直接的な示唆は薄いが、小規模・低解像度データに対してモデルを学習させる場面（文書スキャン画像の分類等）では同様の落とし穴が生じうるため、Augmentation設定の検証プロセスとして参考になる。

## アイデア

- KerasのRandomRotation引数は0〜1のfraction（全回転角360°に対する割合）であるため、0.15が±54度を意味するという仕様の罠が実験で可視化された点
- 高解像度前提で設計された定番AugmentationレシピをCIFAR-10のような低解像度データに無批判に転用すると、精度・計算コスト両面で損をするという実証的なカウンター事例
- 拡張を増やすほど学習時間が延びるにもかかわらず精度が単調低下するという、コストと性能が同方向に悪化するケースを示した点（通常の過学習抑制とは異なるメカニズム）

## 前提知識

- **Data Augmentation** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **CNN** → /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- **過学習 (Overfitting)** (TODO: 読むべき)
- **Keras ImageDataGenerator** (TODO: 読むべき)

## 関連記事

- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】

## 原文リンク

[Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験](https://zenn.dev/wasurenamemo/articles/35b0e4754e2a44)
