---
title: "KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】"
url: "https://zenn.dev/wasurenamemo/articles/1ef4690bec409d"
date: 2026-04-22
tags: [Keras, CNN, MaxPooling2D, GlobalAveragePooling2D, Flatten, 正則化, CIFAR-10, 過学習, パラメータ削減]
category: "ai-ml"
related: [109, 159, 1564, 1606, 242]
memo: "[Zenn 機械学習] KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】"
processed_at: "2026-04-22T12:43:57.283973"
---

## 要約

KerasのCNN設計において、MaxPooling2Dのpool_sizeを変えたときの挙動がGlobalAveragePooling2D（GAP）とFlattenで正反対になるという実験結果を報告した記事。CIFAR-10を使い、pool_size=(2,2)/(3,3)/(4,4)の3パターンを比較した。

GAPモデルでは、pool_size=(4,4)が最高精度72.30%・学習時間91.7秒と最も優れた結果を出した。(2,2)は67.80%・128.4秒、(3,3)は69.52%・103.8秒。この逆転の理由はGAPの仕組みにある。GAPはPooling後の特徴マップをチャンネルごとに平均して1スカラーに集約するため、pool_sizeが何であっても出力は常に「チャンネル数（128）次元のベクトル」となる。つまりpool_sizeの違いはGAPで完全に吸収される。その一方で、pool_sizeが大きいほど特徴マップが小さくなりGAPへ入力される前の段階でより強い空間圧縮が行われ、これが正則化として機能し汎化性能が向上したと考えられる。

Flattenモデルでは逆に(2,2)が最下位（68.74%）となった。Flattenはpool_size後の特徴マップをそのまま1次元に展開するため、(2,2)では Dense層への入力が8,192次元・パラメータ数約111万に膨らむ。これにより5エポック時点でval_lossが底を打ち深刻な過学習に陥った。(3,3)は71.33%・約21万パラメータ、(4,4)は71.18%・約13万パラメータと大幅に少ないパラメータで高精度を達成。さらに(4,4)は30エポック時点でtrain_lossが0.24とまだ収束途中であり、エポックを増やせばさらに伸びる余地がある。

設計上の示唆として、pool_sizeの最適値はGAP/Flattenどちらの集約方式を使うかに依存するため、pool_sizeを決める前にまず集約方式を決定すべきという結論が導かれる。GAPを使う場合は大きめのpool_sizeが正則化として有効に機能し、Flattenを使う場合は小さいpool_sizeがパラメータ爆発と過学習を招くリスクがある。この知見は特にリソース制約のある環境や過学習しやすい小規模データセットでのCNN設計に実践的な指針を提供する。

## アイデア

- GAPはpool_sizeの空間的差異を吸収するため、大きなpool_sizeによる強い圧縮が暗黙の正則化として機能するという非直感的なメカニズム
- Flattenではpool_sizeが小さいほどパラメータ数が指数的に増加（(2,2)で111万 vs (4,4)で13万）し、モデル選択よりもpool_size選択が過学習リスクに直結する
- 「集約方式（GAP vs Flatten）を先に決め、その後pool_sizeを最適化する」という設計の優先順位の明示化が実用的な設計指針となる

## 前提知識

- **CNN（畳み込みニューラルネットワーク）** (TODO: 読むべき)
- **MaxPooling2D** (TODO: 読むべき)
- **GlobalAveragePooling2D (GAP)** (TODO: 読むべき)
- **過学習・正則化** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク

## 関連記事

- /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- /deep_159 野生動物をどこでも識別：SpeciesNetによる野生生物モニタリング
- /deep_1564 自己教師あり単眼深度推定のための適応的深度変換スケール畳み込み（DcSConv）
- /deep_1606 実用的なフォールトトレラント量子計算のためのスケーラブルなニューラルデコーダ
- /deep_242 単純性バイアスの圧縮理論的解釈

## 原文リンク

[KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】](https://zenn.dev/wasurenamemo/articles/1ef4690bec409d)
