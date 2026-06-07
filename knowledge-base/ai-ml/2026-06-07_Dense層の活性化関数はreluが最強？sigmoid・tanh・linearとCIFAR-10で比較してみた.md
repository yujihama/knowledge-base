---
title: "Dense層の活性化関数はreluが最強？sigmoid・tanh・linearとCIFAR-10で比較してみた"
url: "https://zenn.dev/wasurenamemo/articles/f99d7543a85cf1"
date: 2026-06-07
tags: [活性化関数, BatchNorm, CIFAR-10, Keras, TensorFlow, Dense層, 過学習, CNN]
category: "ai-ml"
related: [3652, 6640, 2656, 5652, 2965]
memo: "[Zenn 機械学習] Dense層の活性化関数はreluが最強？sigmoid・tanh・linearとCIFAR-10で比較してみた"
processed_at: "2026-06-07T09:11:10.804213"
---

## 要約

CIFAR-10データセットを用いて、Conv2D×3層＋BatchNorm＋GAP＋Dense(128)＋Dropout(0.3)という構成のモデルにおいて、Dense隠れ層の活性化関数をrelu・sigmoid・tanh・linearの4種で比較した実験報告。エポック数30、バッチサイズ128、seed=42で固定して実施。

結果として、テスト精度はsigmoid（0.7551）＞linear（0.7343）＞relu（0.7331）＞tanh（0.7017）の順。Val最高値ではlinear（0.7644）がトップとなったが、sigmoidは過学習ギャップ0.2225と最小で安定性が際立った。

sigmoidが上位になった主因は、Dense層が1層のみという構成にある。多層では勾配消失が問題になるsigmoidも、1層では飽和の影響が限定的で、val精度が最終エポックまで崩れない安定した収束を示した。reluとlinearがほぼ同水準（約0.733）だった理由は、BatchNorm後の特徴量が既に正規化されており、活性化なしのlinearでも前段の非線形性（Conv2D）で十分機能するため。tanhは過学習ギャップ0.2757と最大で、後半でval_accが低下する傾向が顕著だった。

実務的な使い分けとして、EarlyStoppingあり（restore_best_weights）の場合はどれでも大差なくreluが無難、EarlyStoppingなしで安定重視の場合はsigmoidまたはrelu、BatchNormなしでDenseが多層の場合はrelu、出力層は多クラス分類にsoftmax・二値分類にsigmoid・回帰にlinearが推奨とまとめられている。

注意点として、GPU演算の非決定性により実行ごとに順位が変わり得るため、1回の結果のみで判断しないよう言及されている。監査AIやエージェント開発への直接的示唆は薄いが、特徴抽出後の分類ヘッド設計（BatchNorm＋1層Dense構成）における活性化関数選択の知見として参照価値がある。

## アイデア

- BatchNorm後の1層Dense構成では、sigmoid特有の勾配消失問題が実質的に無効化され、安定性で優位に立つという反直感的な結果
- linearがrelu同水準の精度を出せる理由が「前段Conv2Dの非線形性で十分」という点で、アーキテクチャの文脈依存性を示す好例
- EarlyStoppingの有無によって推奨活性化関数が変わるという実用的フレームワークは、ハイパーパラメータ選択の指針として整理しやすい

## 前提知識

- **BatchNormalization** (TODO: 読むべき)
- **CNN / Conv2D** (TODO: 読むべき)
- **活性化関数（relu・sigmoid・tanh）** (TODO: 読むべき)
- **Dropout** → /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク

## 関連記事

- /deep_3652 CNNのDense層をReLUからELUに変えたら精度が上がった話【Keras×CIFAR-10】
- /deep_6640 MaxPooling vs AveragePooling（中間層）：CIFAR-10で比較したらMNISTと逆の結果になった【Keras実験】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】

## 原文リンク

[Dense層の活性化関数はreluが最強？sigmoid・tanh・linearとCIFAR-10で比較してみた](https://zenn.dev/wasurenamemo/articles/f99d7543a85cf1)
