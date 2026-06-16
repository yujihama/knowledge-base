---
title: "TinyLidarNet解説: 2D LiDARを入力とするEnd-to-End自動運転軽量モデル"
url: "https://zenn.dev/tiger_zenn/articles/af39f65608d910"
date: 2026-06-16
tags: [TinyLidarNet, 1D CNN, End-to-End, LiDAR, 自動運転, Behavior Cloning, PyTorch, エッジ推論, F1TENTH, 模倣学習]
category: "ai-ml"
related: [7968, 716, 5762, 5535, 2860]
memo: "[Zenn 機械学習] TinyLidarNet 解説: 2D LiDAR の End-to-End 自動運転モデル"
processed_at: "2026-06-16T09:10:27.528957"
---

## 要約

TinyLidarNetは2D LiDARのスキャンデータ（距離配列）を入力とし、ステアリング角と速度を直接出力するEnd-to-End自動運転モデル。第12回F1TENTH Autonomous Grand Prix（13チーム中3位）で実績を持つ。

アーキテクチャは5層の1D畳み込み層（Conv1d）と4層の全結合層で構成され、総パラメータ数は約22万と極めて小規模。入力はLモデルで1081点の距離配列、中間特徴は28×64チャンネルに変換され、最終出力はtanh活性化で[-1, 1]に制限されてから実際の制御値にスケーリングされる。従来のMLP256（全結合層のみ）と比較して、1D Convによる空間構造の抽出が汎化性能を大幅に向上させている点が核心的な貢献。シミュレーション4トラックでの完走率100%に対し、MLP256はほぼ完走不可。

計算コストはINT8量子化時、Jetson Xavier NXで1ms未満、ESP32-S3（Xtensa LX7）でLモデル16ms（40Hzリアルタイム制御に対応）、Raspberry Pi Pico（Cortex-M0+）でもSモデル36ms（約20Hz）と、MCU上での動作を実現している。

学習はBehavior Cloning（模倣学習）で、手動運転約5分・約1.2万サンプルで十分な性能が得られる。損失関数はHuber Loss（delta=1.0）、最適化はAdam（lr=5e-5）、バッチサイズ64。教師ラベルはtanhの出力域[-1, 1]に正規化して揃える設計。

本記事ではPyTorch＋自作軽量2Dシミュレータ（robosim2d）による再実装も提供。公式実装（TensorFlow/Keras＋ROS）の環境構築コストを回避し、collect→train→autodrive→evaluateの4サブコマンドでパイプラインを構成。val lossが最小のエポックの重みを保持するearly stopping的な実装も加えている。

動的環境への対応として、静的障害物のみで学習したモデルが動く他車両を追い越す挙動を示した報告があり、移動物体を壁・静止物として扱う暗黙的な汎化が生じた可能性が指摘されている。監査エージェント開発への直接的な示唆は薄いが、小規模データ（1.2万サンプル）でリアルタイム推論可能なEnd-to-Endモデルを構築する設計思想は、センサデータを入力とする軽量意思決定モジュールの参考になる。

## アイデア

- カメラ画像ではなく1081点の1D LiDAR距離配列に1D Convを適用することで、MLP比較で完走率を大幅改善。入力のモダリティに合ったアーキテクチャ選択が汎化性能に直結する具体例
- 約22万パラメータ・手動運転5分のデータでESP32-S3上40Hzリアルタイム推論を実現。エッジデバイス向けモデル設計においてパラメータ数とデータ効率のトレードオフを示す実践的ベンチマーク
- 静的環境のみで学習したモデルが動的障害物（他車両）を回避・追い越す挙動を示した現象は、分布外データへの予期せぬ汎化として興味深く、モデルの内部表現が環境の幾何構造を抽象化している可能性を示唆

## 前提知識

- **Conv1d** (TODO: 読むべき)
- **Behavior Cloning** → /deep_1522 オフライン多エージェント強化学習のためのValue-Guidance MeanFlow
- **Huber Loss** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **INT8量子化** → /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 関連記事

- /deep_7968 知覚ジッターの制御：信頼性の高い動き分類のための不確実性対応LiDAR物体検出
- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_5762 LeRobot — 録画したデータセットでポリシーをトレーニングする
- /deep_5535 GEM: 変形可能Mambaによるリダールワールドモデル生成
- /deep_2860 Car-GPT：LLMは自動運転を実現できるか？

## 原文リンク

[TinyLidarNet解説: 2D LiDARを入力とするEnd-to-End自動運転軽量モデル](https://zenn.dev/tiger_zenn/articles/af39f65608d910)
