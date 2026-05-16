---
title: "YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ"
url: "https://zenn.dev/ka_kan/articles/c1529ebad88cff"
date: 2026-04-14
tags: [YOLOv8, RT-DETR, 物体検出, COCO, Transformer, CNN, mAP, 推論速度]
category: "ai-ml"
related: [129, 258, 291, 1494, 113]
memo: "[Zenn 機械学習] YOLOとRT-DETRを眺める"
processed_at: "2026-04-14T12:01:58.171308"
---

## 要約

本記事は、物体検出モデルであるYOLOv8（Ultralytics, 2023）とRT-DETR（Baidu, Zhao et al. 2023）をCOCO val 2017データセット（5000枚）上で比較実験した報告である。YOLOv8はCNNベースのアーキテクチャを採用し、論文なしで公開されたモデル。RT-DETRはFacebook AI ResearchのDETR（Carion et al., 2020）を後継するTransformerベースの検出器である。評価指標はmAP@50、mAP@50-95、推論時間（ウォームアップ10枚後の100枚平均）、モデルサイズ（.ptファイル）。実験環境はRTX 3060（12GB）、ultralyticsの事前学習済み重みを追加学習なしで使用した。結果は以下の通り：YOLOv8n（3.15M params, 6.25MB）はmAP@50=0.519、推論時間19.4ms。YOLOv8s（11.16M, 21.54MB）はmAP@50=0.611、推論時間9.7ms（最速）。YOLOv8m（25.89M, 49.72MB）はmAP@50=0.665、推論時間26.0ms。RT-DETR-l（32.15M, 63.43MB）はmAP@50=0.701、推論時間64.3ms。RT-DETR-x（65.63M, 129.47MB）はmAP@50=0.715、推論時間55.8ms。精度面ではRT-DETRがYOLOv8を上回り（mAP@50で最大+0.104）、速度面ではYOLOv8sが9.7msと最速でRT-DETRの約1/6の推論時間を達成。YOLOv8mとRT-DETR-lはパラメータ数が近い（25.89M vs 32.15M）にもかかわらず推論時間に大きな差（26.0ms vs 64.3ms）があり、TransformerアテンションのCNNに対する計算コストの高さが顕在化している。リアルタイム性が求められる用途ではYOLOv8、精度優先の用途ではRT-DETRという使い分けが示唆される。監査AIへの直接的な示唆は薄いが、証跡画像や帳票スキャンの物体検出タスクにおいて、精度・速度・モデルサイズのトレードオフを定量的に把握する際の参考になる。

## アイデア

- YOLOv8sが推論時間9.7msと最速であるにもかかわらず、より大きいYOLOv8m（26.0ms）より速いという逆転現象は、バッチ処理最適化やアーキテクチャ設計の影響を示唆している
- TransformerベースのRT-DETRはCNNベースのYOLOv8に対してmAP@50で最大+0.104の精度向上を達成しているが、推論時間は2〜6倍かかる点で、精度・速度トレードオフの定量的な把握が実用選定に直結する
- 同程度のパラメータ数（YOLOv8m: 25.89M vs RT-DETR-l: 32.15M）でも推論時間が26.0ms対64.3msと2.5倍異なる事実は、パラメータ数だけでは推論効率を評価できないことを示しており、アーキテクチャ選定基準の再考を促す

## 前提知識

- **COCO dataset** (TODO: 読むべき)
- **mAP** → /deep_131 トークン効率的な画像生成のためのセマンティック認識プレフィックス学習（SMAP）
- **DETR** (TODO: 読むべき)
- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **CNNベース検出器** (TODO: 読むべき)

## 関連記事

- /deep_129 【超入門】YOLOとは何か？物体検出モデルの仕組みから実践まで解説
- /deep_258 EEGベース生存予測におけるデータリーケージ防止：2段階埋め込みとTransformerフレームワーク
- /deep_291 EEGによる生存予測におけるデータリークの防止：二段階埋め込みとTransformerフレームワーク
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた

## 原文リンク

[YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ](https://zenn.dev/ka_kan/articles/c1529ebad88cff)
