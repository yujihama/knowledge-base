---
title: "SEブロック（Squeeze-and-Excitation）を追加すると精度は上がるか？CIFAR-10で実験【Keras】"
url: "https://zenn.dev/wasurenamemo/articles/cc2c6088fb3104"
date: 2026-05-22
tags: [SENet, Channel Attention, Keras, CIFAR-10, CNN, Squeeze-and-Excitation, カスタムレイヤー, アブレーション実験]
category: "ai-ml"
related: [5914, 2656, 5652, 5039, 3911]
memo: "[Zenn 機械学習] SEブロック（Squeeze-and-Excitation）を追加すると精度は上がるか？CIFAR-10で実験【Keras】"
processed_at: "2026-05-22T09:10:20.621773"
---

## 要約

SENet（Squeeze-and-Excitation Networks）は2017年のILSVRCで優勝したアーキテクチャに採用されたChannel Attention手法で、本記事ではKerasカスタムレイヤーとして実装し、CIFAR-10データセットで「SEブロックなし」vs「あり」の精度比較実験を行った結果を報告している。

SEブロックの処理は2ステップで構成される。①Squeeze：特徴マップ（H×W×C）をGlobal Average Pooling（GAP）で空間方向に集約し、チャンネルごとのスカラー（1×1×C）を得る。②Excitation：FC→ReLU→FC→Sigmoidでチャンネルごとの重要度スコア（0〜1）を計算し、元の特徴マップにスカラー乗算でスケーリングする。reduction_ratioのデフォルトは16で、削減後のユニット数はmax(C//16, 1)で決定される。実装はSEBlock()(x)の1行で任意の位置に差し込めるカスタムレイヤーとして仕上げており、再利用コストがほぼゼロである点が強調されている。

実験条件はCIFAR-10、30エポック、batch_size=64。結果はAパターン（SEなし）がval_accuracy 67.26%・test_accuracy 66.44%・パラメータ数93,450・学習時間132.1秒、Bパターン（SEあり）がval_accuracy 65.30%・test_accuracy 65.50%・パラメータ数98,570・学習時間132.2秒。SEブロックなしが0.94%上回り、追加パラメータ5,120（+5.5%）・学習時間ほぼ同一にもかかわらず精度が低下した。前回のCBAM実験（なし66.82% vs あり66.31%、差−0.51%）と合わせ、浅いCNNでは2回連続でAttentionなしが勝つという一貫した結果となった。

CBAMとの違いとして、SENetはGAPのみ・空間Attentionなし、CBAMはGAP＋GMP＋空間Attentionありでパラメータと計算コストがやや大きい。

効果が出にくい根本的な理由として、SENetの原論文がResNet・VGG・Inceptionなど深いネットワーク上で検証されている点が挙げられる。浅いCNN（Conv2D 2層・64〜128ch）では各チャンネルの「役割分担」が未熟なため、Attentionの選択機構が有効に機能しない。深いネットワーク（ResNet等）やチャンネル数256以上、EfficientNetなど転移学習ベースモデルでは効果が出やすいとされる。監査エージェントのモデル選定においても、Channel Attention系手法は小規模モデルへの安易な適用では効果が期待できず、ベースアーキテクチャの深さと特徴表現の豊かさを確認してから導入を検討すべきという示唆が得られる。

## アイデア

- 浅いCNN（2層・64〜128ch）ではChannel Attention系手法（SENet・CBAM）が2回連続で逆効果になるという再現性のある実験結果は、「とりあえずAttentionを足せば良くなる」という思い込みを定量的に否定している
- SEBlock()(x)の1行で差し込めるカスタムレイヤー設計はモジュール性の手本であり、大規模モデルでの検証コストをほぼゼロにする実装パターンとして転用価値が高い
- reduction_ratio=16という固定値がCIFAR-10規模（64〜128ch）では過剰な削減をもたらす可能性があり、小規模モデルではratio調整の実験が効果の鍵になり得る

## 前提知識

- **CNN（畳み込みニューラルネットワーク）** (TODO: 読むべき)
- **Global Average Pooling** → /deep_4192 DropoutをCIFAR-10で0.0/0.2/0.5と変えたらtrain_lossが逆転した話【Keras実験】
- **Channel Attention** → /deep_5914 Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】
- **CBAM** → /deep_5573 ChladniSonify: クラドニ図形のリアルタイム視聴覚マッピング手法
- **Kerasカスタムレイヤー** (TODO: 読むべき)

## 関連記事

- /deep_5914 Channel Attentionを追加すると精度は上がるか？CBAM風実装をCIFAR-10で検証【Keras実験】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_5039 Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】

## 原文リンク

[SEブロック（Squeeze-and-Excitation）を追加すると精度は上がるか？CIFAR-10で実験【Keras】](https://zenn.dev/wasurenamemo/articles/cc2c6088fb3104)
