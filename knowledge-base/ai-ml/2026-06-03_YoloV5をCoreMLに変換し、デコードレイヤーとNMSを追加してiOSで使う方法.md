---
title: "YoloV5をCoreMLに変換し、デコードレイヤーとNMSを追加してiOSで使う方法"
url: "https://zenn.dev/mlboydaisuke/articles/d9e878330465e83cd79d"
date: 2026-06-03
tags: [YoloV5, CoreML, 物体検出, iOS, Non-Max Suppression, モデル変換, coremltools]
category: "ai-ml"
related: [889, 2875, 2208, 129, 2408]
memo: "[Zenn 機械学習] YoloV5をCoreMLに変換。デコードレイヤーも追加する。"
processed_at: "2026-06-03T09:09:31.796842"
---

## 要約

YoloV5（物体検出モデル）をiOS/iPadOSで動作させるため、CoreML形式に変換し、推論結果を実用可能な形に後処理するレイヤーを追加する手順を解説した記事。

CoreMLToolsで単純変換したYoloV5モデルの出力は「クラスごとの大量のバウンディングボックス候補」であり、そのままではiOSのVisionフレームワークで扱えない。具体的には3スケール（stride 8/16/32）×3アンカー×特徴マップグリッド数分の生出力テンソルが得られるため、以下2段階の後処理レイヤーをCoreMLモデルに直接組み込む必要がある。

**1. デコードレイヤーの追加（PyTorch/CoreMLTools Builder API）**
YoloV5の出力はSigmoid後に座標・信頼度の計算式（公式Issues #471準拠）で変換が必要。x,yはSigmoid出力に`*2 - 0.5 + grid_offset`を適用しstrideで乗算、w,hは`(sigmoid*2)^2 * anchor`で実ピクセルサイズに変換する。これらをinput 640px基準で正規化（1/640）し、25,200ボックス（3アンカー×(80²+40²+20²)）分にflattenしてconcat。出力は`raw_confidence (25200, num_classes)`と`raw_coordinates (25200, 4)`の2テンソル。

**2. Non Max Suppression (NMS) レイヤーの追加**
CoreMLのprotoを直接操作し`NonMaximumSuppression`レイヤーを定義。iouThreshold/confidenceThresholdを設定し、最終出力を`confidence`と`coordinates`という名称にする。これによりiOSのVisionフレームワーク（`VNCoreMLRequest`）が物体検出モデルとして認識し、ファイルプレビュー機能（Quick Look）にもそのまま対応できるようになる。

変換スクリプトはGoogle Colabで公開されており、独自データセットでトレーニングしたyolov5モデルにも適用可能。変換済みのCOCO 80クラスモデル（yolov5s）もGitHub（john-rocky/CoreML-Models）で配布。`reverseModel`フラグはモデルによって出力順序が逆転するケースへの対処で、ymlファイルのアンカー設定と合わせて確認が必要。監査AI観点での直接適用は限定的だが、エッジデバイス上でのオフライン推論パターン（モデル変換→後処理のレイヤー埋め込み）は、監査証跡のリアルタイム分析をオンデバイスで行うアーキテクチャ設計の参考になる。

## アイデア

- 後処理（デコード・NMS）をモデルファイル自体に埋め込むことで、推論側コードをシンプルに保てる設計パターン：アプリ側でSigmoidや座標変換を実装せず、モデル出力をそのままVisionフレームワークに渡せる
- CoreMLのBuilder APIを使えばPyTorchやONNX由来のモデルに任意のレイヤーをグラフレベルで後付けできる：これはエッジデプロイ時の前処理・後処理の標準化に応用可能
- stride 8/16/32の3スケールアンカーから25,200ボックスが生成される仕組みの明示：(640/8)²+(640/16)²+(640/32)²=6400+1600+400=8400グリッド×3アンカー=25,200という数値の根拠が理解できる

## 前提知識

- **YoloV5アーキテクチャ** (TODO: 読むべき)
- **CoreML / coremltools** (TODO: 読むべき)
- **Non-Max Suppression** (TODO: 読むべき)
- **アンカーベース物体検出** (TODO: 読むべき)
- **iOS Vision Framework** (TODO: 読むべき)

## 関連記事

- /deep_889 自律走行のための深層ニューラルネットワークを用いた道路工事検知システム
- /deep_2875 第4回海事コンピュータビジョンワークショップ（MaCVi 2026）：チャレンジ概要
- /deep_2208 スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る
- /deep_129 【超入門】YOLOとは何か？物体検出モデルの仕組みから実践まで解説
- /deep_2408 【YOLO】バーコードデータセットでカスタム物体検知モデルを構築する手順

## 原文リンク

[YoloV5をCoreMLに変換し、デコードレイヤーとNMSを追加してiOSで使う方法](https://zenn.dev/mlboydaisuke/articles/d9e878330465e83cd79d)
