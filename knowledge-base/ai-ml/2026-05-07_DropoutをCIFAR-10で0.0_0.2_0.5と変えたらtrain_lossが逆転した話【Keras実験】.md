---
title: "DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】"
url: "https://zenn.dev/wasurenamemo/articles/8a862cefc3f28e"
date: 2026-05-07
tags: [Dropout, CIFAR-10, Keras, Global Average Pooling, 正則化, 過学習, TensorFlow]
category: "ai-ml"
related: [2656, 2965, 3911, 4049, 2783]
memo: "[Zenn 機械学習] DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】"
processed_at: "2026-05-07T21:20:57.054937"
---

## 要約

CIFAR-10データセットを用いてKerasでDropout率（0.0/0.2/0.5）を変化させた際の挙動を実験的に検証した記事。モデル構成はGlobal Average Pooling（GAP）＋Dropoutの組み合わせ。

【実験結果】Dropout=0.0ではTest Acc 65.64%、Ep30時点のtrain_loss=0.852/val_loss=0.953。Dropout=0.2ではTest Acc 67.35%（最高）、train_loss=0.881/val_loss=0.894で乖離幅0.013と最小。Dropout=0.5ではTest Acc 66.53%、train_loss=0.967/val_loss=0.929となり、訓練lossが検証lossを上回る「逆転現象」が発生した。学習時間はDropout=0.5が124.4秒と最短だった。

【逆転現象のメカニズム】Dropout=0.5でtrain_loss＞val_lossとなる現象は異常ではなく、Dropoutの動作仕様に起因する。Dropoutは訓練時のみランダムにノードを無効化し、推論時（val/test）は全ノードを使用する。率が高いほど訓練時のネットワーク容量が制限され、訓練lossが見かけ上大きくなる。この非対称性により、高いDropout率では訓練時lossが検証時lossを超えることがある。

【GAPの正則化効果】Global Average Pooling自体が空間情報を平均化する操作であり、パラメータ数を削減して過学習を抑制する正則化効果を持つ。そのため、Dropout=0.0でも深刻な過学習（train/valの大きな乖離）は発生していない。GAPを使用したモデルではDropoutの過剰適用は逆効果となりやすく、0.1〜0.3程度の控えめな率が適切という実用的知見が得られている。

【結論】GAPを含むモデルではDropout=0.2が精度・安定性ともに最適。train_loss＞val_lossの逆転はDropoutの訓練/推論非対称性から生じる正常な挙動であり、過学習の指標として誤解しないことが重要。

## アイデア

- Dropoutの訓練/推論非対称性（訓練時はノード無効化、推論時は全ノード使用）がtrain_loss＞val_lossという直感に反する逆転現象を引き起こす点は、lossの解釈において見落とされがちな重要な概念
- GAPとDropoutを併用する場合、GAPが既に正則化効果を持つためDropoutの追加効果が逓減し、高すぎるDropout率が精度低下を招くというアーキテクチャ間の相互作用
- Dropout率の選択は「過学習の有無」だけでなく、使用するアーキテクチャの固有の正則化特性を考慮した上で決定すべきであり、GAP使用時は0.1〜0.3が実用的な出発点となる

## 前提知識

- **Dropout** (TODO: 読むべき)
- **Global Average Pooling** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **過学習・正則化** (TODO: 読むべき)
- **Keras/TensorFlow** (TODO: 読むべき)

## 関連記事

- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】
- /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解

## 原文リンク

[DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】](https://zenn.dev/wasurenamemo/articles/8a862cefc3f28e)
