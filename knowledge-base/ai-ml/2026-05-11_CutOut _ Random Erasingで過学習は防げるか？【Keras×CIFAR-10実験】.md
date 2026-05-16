---
title: "CutOut / Random Erasingで過学習は防げるか？【Keras×CIFAR-10実験】"
url: "https://zenn.dev/wasurenamemo/articles/5122c014f21c19"
date: 2026-05-11
tags: [CutOut, RandomErasing, データ拡張, 過学習, CIFAR-10, Keras, underfitting, 汎化性能]
category: "ai-ml"
related: [2656, 2965, 4192, 5039, 3911]
memo: "[Zenn 機械学習] CutOut / Random Erasingで過学習は防げるか？【Keras×CIFAR-10実験】"
processed_at: "2026-05-11T21:34:58.119624"
---

## 要約

CutOutとRandom Erasingは、画像の矩形領域をマスクすることで局所特徴への過依存を防ぐデータ拡張手法。CutOut（2017年提案）は固定サイズの正方形領域を黒（値0）で埋め、Random Erasing（2020年提案）は面積比・アスペクト比をランダムサンプリングして乱数値で埋める点が異なる。本記事では、Keras + CIFAR-10（32×32px）+ Google Colab T4環境で30エポックの学習を行い、「なし」「CutOut(size=10)」「Random Erasing(sh=0.40)」の3パターンを比較した。結果は予想に反し、test_accuracyでなし67.11% > CutOut66.03% > RE65.18%となり、デフォルトパラメータのマスク手法が最下位となった。原因はCIFAR-10の画像サイズの小ささ（32×32px）にある。元々情報量が少ない画像に対して大きなマスクを適用すると、正解を学習するための手がかり自体が失われunderfittingが発生する。追加実験としてマスクサイズを縮小したところ、CutOut(size=8)はtest_accuracy 66.47%（差−0.64%）、RE(sh=0.15)はtest_accuracy 67.45%（差+0.34%）と唯一なしを上回る結果を達成した。RE(sh=0.15)はval_accuracyではなしに劣るにもかかわらずtest_accuracyが上回っており、これはvalidationセットへの特化が抑えられ真の汎化性能が向上したと解釈される。論文デフォルトパラメータは大画像（ImageNetの224×224px等）を想定して設定されており、CIFAR-10のような小画像に転用する際はshを0.15前後に縮小する調整が必要。モデルのパラメータ数・学習時間への影響はほぼゼロであり、試すコストは低い。汎化性能の評価はval_accuracyではなくtest_accuracyで行うべきという点も実験から確認された。

## アイデア

- 論文デフォルトパラメータは大画像向けに設定されており、小画像（32×32px）へそのまま転用するとunderfittingを引き起こすという「スケール依存性」の実証
- val_accuracyとtest_accuracyが逆転するケース（RE sh=0.15）の存在——validationセットへの過特化を正則化が抑制し、真の汎化性能が向上するメカニズム
- マスク手法はモデル構造・学習時間に影響を与えず追加コストがほぼゼロであるため、ハイパーパラメータ探索コストと精度改善のトレードオフが非常に有利

## 前提知識

- **データ拡張** → /deep_118 Groundsource: Geminiを使ってニュース記事を構造化データに変換するフレームワーク
- **過学習・underfitting** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **Dropout** → /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- **val/test accuracy分割** (TODO: 読むべき)

## 関連記事

- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- /deep_5039 Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】

## 原文リンク

[CutOut / Random Erasingで過学習は防げるか？【Keras×CIFAR-10実験】](https://zenn.dev/wasurenamemo/articles/5122c014f21c19)
