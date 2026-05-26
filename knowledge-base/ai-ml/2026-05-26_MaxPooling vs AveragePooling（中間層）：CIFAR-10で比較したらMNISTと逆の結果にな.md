---
title: "MaxPooling vs AveragePooling（中間層）：CIFAR-10で比較したらMNISTと逆の結果になった【Keras実験】"
url: "https://zenn.dev/wasurenamemo/articles/4948980f649030"
date: 2026-05-26
tags: [CNN, MaxPooling, AveragePooling, CIFAR-10, Keras, TensorFlow, 画像分類, ダウンサンプリング]
category: "ai-ml"
related: [5652, 5039, 3911, 4049, 5914]
memo: "[Zenn 機械学習] MaxPooling vs AveragePooling（中間層）CIFAR-10で比較したらMNISTと逆の結果になった【Keras実験】"
processed_at: "2026-05-26T21:22:23.942242"
---

## 要約

CNNの中間層におけるMaxPoolingとAveragePoolingの性能差を、CIFAR-10データセットを用いてKeras/TensorFlowで実験的に比較した記事。比較したのは3パターン：A（Max+Max）、B（Avg+Avg）、C（Max→Avg混合）。結果はA: 67.47%、B: 63.30%、C: 64.36%で、MaxPooling同士の組み合わせが最高精度を達成し、AvgAvgを約4.2ポイント上回った。学習時間はAvgAvgが約100秒と最速で、MaxMaxの124.7秒より約25秒速い。パラメータ数は3パターンとも93,450で完全に同一であり、精度差は学習パラメータではなく「どの特徴情報を次層に渡すか」という情報の取捨選択のみに起因する。CIFAR-10は飛行機・犬・自動車などの自然画像であり、物体の輪郭・テクスチャ・エッジといった局所的に強い反応が分類の決め手となる。MaxPoolingはこれら局所最大値を保持するため後段Conv層に豊かな特徴を渡せる一方、AveragePoolingは空間全体を平均化するためエッジ情報が薄まる。以前の著者によるMNIST実験ではAvgPoolingがわずかに上回っており、今回CIFAR-10で逆転した。その理由はデータの性質の違いで説明される：MNISTは白背景に黒の線画という単純構造で全体形状把握が重要なため平均化によるノイズ抑制が効くが、CIFAR-10は複雑な自然画像でテクスチャ識別が重要なため最大値保持が有効。「線画・単純形状→Avg、自然画像・テクスチャ重要→Max」という実用的な判断基準を提示している。MixパターンはEfficientNetなどで採用される設計だが、今回の2層シンプル構成では後段AveragePoolingによる平滑化で強い特徴が失われ、MaxMaxには届かなかった。監査AIへの直接的な示唆は薄いが、CNNベースの文書画像認識や証跡スキャン処理において、画像の性質に応じたPooling選択が精度に数ポイント影響する点は実装判断の参考になる。

## アイデア

- パラメータ数が完全に同一（93,450）なのに精度が最大4.2ポイント異なる点：違いは重みの数ではなく「情報の選別方式」のみであり、アーキテクチャ設計における非学習操作の影響力を示す好例
- データセットの画像特性（線画vs自然画像）がPooling選択の最適解を逆転させる点：汎用的な「MaxPoolingが強い」という通念がデータ依存であることを実験で明示
- AvgAvgがMaxMaxより約25秒（約20%）速い点：精度vs推論・学習速度のトレードオフとして、エッジデバイスやリアルタイム処理用途でのPooling選択基準になりうる

## 前提知識

- **CNN（畳み込みニューラルネットワーク）** (TODO: 読むべき)
- **MaxPooling / AveragePooling** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **Keras / TensorFlow** (TODO: 読むべき)
- **GAP（Global Average Pooling）** (TODO: 読むべき)

## 関連記事

- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_5039 Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】
- /deep_5914 Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】

## 原文リンク

[MaxPooling vs AveragePooling（中間層）：CIFAR-10で比較したらMNISTと逆の結果になった【Keras実験】](https://zenn.dev/wasurenamemo/articles/4948980f649030)
