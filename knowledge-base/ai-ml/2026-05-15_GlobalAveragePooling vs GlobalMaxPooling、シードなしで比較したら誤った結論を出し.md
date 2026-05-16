---
title: "GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】"
url: "https://zenn.dev/wasurenamemo/articles/968f97b272b90d"
date: 2026-05-15
tags: [Keras, GlobalAveragePooling, GlobalMaxPooling, CNN, CIFAR-10, 再現性, 乱数シード固定, TensorFlow]
category: "ai-ml"
related: [3911, 4049, 2656, 2965, 4192]
memo: "[Zenn 機械学習] GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras"
processed_at: "2026-05-15T09:07:57.496827"
---

## 要約

KerasのCNNにおいて畳み込み後の特徴集約レイヤーとして使われるGlobalAveragePooling2D（GAP）とGlobalMaxPooling2D（GMP）を、CIFAR-10データセットで比較実験した結果と、その過程で発見した「シード固定なし比較の罠」を報告する記事。GAPは空間方向の平均値を、GMPは最大値を取ることで(H, W, C)→(C,)に圧縮し、Flattenと異なりパラメータ爆発を防ぐという共通の利点を持つ。実験は3パターン（A：GAP単体128次元、B：GMP単体128次元、C：GAP+GMP連結256次元）で実施し、Pooling層以外の条件（Conv構成・Dense・Dropout・エポック数）はすべて同一に設定した。乱数シード42固定での結果は、A（GAP）が66.48%、B（GMP）が66.25%、C（GAP+GMP連結）が68.44%となり、GAPとGMP単体の差は0.23ポイントとほぼ同等だった一方、GAP+GMP連結はパラメータ数を93,450から109,834（+17.5%）に増やす代わりに約2ポイントの安定した精度向上を達成した。最大の発見は再現性に関するもので、シード固定前の1回目実験ではGAPが66.19%、GMPが68.60%と2.41ポイントのGMP優位という結果が出た。この差は「初期重みの運」によるものであり、シード42を固定した2回目実験では差がほぼ消滅した。シード固定には`os.environ['PYTHONHASHSEED']`、`random.seed()`、`np.random.seed()`、`tf.random.set_seed()`の4行セットが必要とされている。実践的な選択指針として、「迷ったらGAP、精度向上を狙うならGAP+GMP連結」が推奨されており、単一実行の結果を信じずシードを固定した上で複数回実験することの重要性が強調されている。監査AIや評価実験の文脈においても、再現性の担保は評価の信頼性に直結するため、同様の教訓が適用できる。

## アイデア

- 単一実験の結果（GMP優位2.41pt）が初期重みの運に過ぎず、シード固定により差が0.23ptまで縮小した事例は、ML実験設計における再現性担保の具体的な失敗例として教育的価値が高い
- GAP+GMP連結がパラメータ+17.5%でテスト精度+2ptを達成した点は、情報の補完性（平均的反応と最強反応の両立）という直感と実験結果が一致しており、特徴集約の設計指針として参考になる
- シード固定に4種類の設定（PYTHONHASHSEED, random, numpy, tensorflow）が必要という点は、Python/TensorFlow環境の非決定性の多層構造を示しており、再現可能な実験環境構築の実践知として汎用性がある

## 前提知識

- **CNN** → /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- **GlobalAveragePooling2D** → /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- **Keras/TensorFlow** (TODO: 読むべき)
- **乱数シード固定** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク

## 関連記事

- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】

## 原文リンク

[GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】](https://zenn.dev/wasurenamemo/articles/968f97b272b90d)
