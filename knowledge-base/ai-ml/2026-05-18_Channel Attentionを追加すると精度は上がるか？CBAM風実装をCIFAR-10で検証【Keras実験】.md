---
title: "Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】"
url: "https://zenn.dev/wasurenamemo/articles/5691b7a6f7bcd5"
date: 2026-05-18
tags: [Channel Attention, CBAM, SENet, Keras, CIFAR-10, CNN, アテンション機構, TensorFlow]
category: "ai-ml"
related: [5652, 3911, 4049, 2656, 2965]
memo: "[Zenn 機械学習] Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】"
processed_at: "2026-05-18T09:09:07.426864"
---

## 要約

SENetやCBAMで使われるChannel Attention機構をKerasでカスタムレイヤーとして自前実装し、CIFAR-10データセットで「なし vs あり」の精度・学習時間を比較した実験報告。Channel Attentionは①Squeeze（Global Average Poolingでチャンネルごとのスカラー値を取得）②Excitation（Dense(C/r)→ReLU→Dense(C)→Sigmoidでチャンネル重要度スコアを算出し元の特徴マップに乗算）の2ステップで構成される。実装はKeras Layer継承クラスとして作成し、Conv2D直後に1行追加するだけで差し込める設計になっている。実験条件は30エポック・バッチサイズ64。結果は「Attentionなし」がval_accuracy 67.54%・test_accuracy 66.82%（パラメータ数93,450・学習時間139.1秒）に対し、「Attentionあり」はval_accuracy 66.54%・test_accuracy 66.31%（パラメータ数98,570・学習時間128.6秒）と、Channel Attentionを追加した方が約1%低い精度となった。パラメータ増加は+5,120（約5.5%）のみで学習時間はむしろ10秒短縮されている。効果が出なかった原因として3点が挙げられている：①モデルが浅い（Conv2D 2層のみ）——Channel AttentionはResNetのような深いネットワーク向けに設計されており、浅いモデルではチャンネルの役割分担が未熟；②チャンネル数が少ない（64ch・128ch）——SENet原論文では256ch以上で効果が大きいとされている；③Sigmoidスケーリング追加による勾配の流れの変化で30エポックでは収束不足の可能性。一方、深いネットワーク（ResNet等）・チャンネル数256ch以上・転移学習モデル（EfficientNet等）では効果が高いとまとめている。監査エージェント開発への直接的な示唆は薄いが、「手法の有効性はネットワーク深さ・チャンネル数・タスクに依存する」という知見は、LLMへのアテンション改良手法を適用する際にも同様の文脈依存性を意識する必要があることを示唆している。

## アイデア

- Channel Attentionを浅いCNNに適用すると精度が下がる実験結果——「追加すれば必ず改善」という思い込みを定量的に否定した点が価値ある
- Squeeze-and-Excitation構造をKeras Layerとして継承実装することで、Functional APIの任意箇所に1行で差し込めるモジュール化パターン
- 学習時間が短縮（139秒→128秒）しているのに精度が下がる現象——Sigmoidによる勾配変化が収束速度を変えている可能性の考察

## 前提知識

- **SENet** (TODO: 読むべき)
- **CBAM** → /deep_5573 ChladniSonify: クラドニ図形のリアルタイム視聴覚マッピング手法
- **Global Average Pooling** → /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- **Keras Functional API** (TODO: 読むべき)
- **CNN特徴マップ** (TODO: 読むべき)

## 関連記事

- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】
- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】

## 原文リンク

[Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】](https://zenn.dev/wasurenamemo/articles/5691b7a6f7bcd5)
