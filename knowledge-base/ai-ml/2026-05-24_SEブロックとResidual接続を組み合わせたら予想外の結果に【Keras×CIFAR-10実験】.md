---
title: "SEブロックとResidual接続を組み合わせたら予想外の結果に【Keras×CIFAR-10実験】"
url: "https://zenn.dev/wasurenamemo/articles/a056a3141bd575"
date: 2026-05-24
tags: [SEブロック, Residual接続, Keras, CIFAR-10, チャネルAttention, TensorFlow, アブレーションスタディ]
category: "ai-ml"
related: [5652, 2965, 4192, 3911, 4049]
memo: "[Zenn 機械学習] SEブロックとResidual接続を組み合わせたら予想外の結果に【Keras×CIFAR-10実験】"
processed_at: "2026-05-24T09:07:56.490650"
---

## 要約

CIFAR-10データセットを用いて、SEブロック（Squeeze-and-Excitation Block）とResidual接続（スキップ接続）の4パターン比較実験を行った結果、組み合わせが単体より劣るという予想外の結果が得られた。実験パターンはA：ベースライン（75.17%）、B：Residualのみ（76.35%）、C：SEのみ（80.57%）、D：SE+Residual（76.00%）の4種類。最高精度はCのSE単体で80.57%、組み合わせのDはSE単体に対して約4.6ポイント下回った。SEブロックはGlobal Average Poolingでチャネルごとの重要度スコアを算出し、Sigmoid出力でチャネルAttentionを動的に調整する仕組み。Kerasでは`se_block(x)`として5行程度で実装可能で、Conv2Dの後に1行追加するだけで利用できる。組み合わせが失敗した原因として、Residual接続のAdd()が勾配の流れを変え、SEブロックのチャネルAttention重みの最適化と干渉した可能性が指摘されている。実際にDパターンではエポック10・23・27でval_lossが2.3〜2.5まで急上昇する不安定な学習が観測され、エポック30時点でもval_loss=1.20とSE単体の0.91より大幅に高かった。パラメータ効率の観点では、SEのみがパラメータ増加+20,480（+1.8%）で精度+5.40ポイントと最高コスト効率を達成。一方でSE+Residualはパラメータ+62,976と最も多いにもかかわらず精度向上は+0.83ポイントにとどまった。SE-ResNetの組み合わせが有効なのはResNet-50以上の深いネットワークや大規模データセットの場面であり、浅い2ブロック構成ではResidualによる勾配安定の恩恵が小さく、SEの効果を打ち消す方向に働くと結論付けられている。監査エージェント開発への示唆として、モジュールの組み合わせが常に相乗効果をもたらすとは限らず、浅い構成・小規模データでは単一の効果的手法を優先する方が合理的という設計指針が得られる。

## アイデア

- モジュールの組み合わせが相乗効果ではなく干渉を引き起こすケースがあり、浅いネットワークではSEブロック単体がResidual+SEを上回るという実験的証拠
- SEブロックはパラメータ増加+1.8%で精度+5.40ptと高コスト効率を示し、軽量モデル設計において有力な選択肢となる
- val_lossの急騰（2.3〜2.5）というログ分析から、勾配フローの干渉という仮説を立てるアプローチ——ブラックボックスではなく訓練ダイナミクスから原因を推定する方法論

## 前提知識

- **SEブロック（Squeeze-and-Excitation）** → /deep_6283 SEブロック（Squeeze-and-Excitation）を追加すると精度は上がるか？CIFAR-10で実験【Keras】
- **Residual接続** (TODO: 読むべき)
- **チャネルAttention** (TODO: 読むべき)
- **Global Average Pooling** → /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク

## 関連記事

- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】

## 原文リンク

[SEブロックとResidual接続を組み合わせたら予想外の結果に【Keras×CIFAR-10実験】](https://zenn.dev/wasurenamemo/articles/a056a3141bd575)
