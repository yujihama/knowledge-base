---
title: "CPU上でのBERT推論をスケールアップする（Part 1）：ハードウェア最適化の基礎"
url: "https://huggingface.co/blog/bert-cpu-scaling-part-1"
date: 2026-04-14
tags: [BERT, CPU推論, PyTorch, TensorFlow, ONNX Runtime, NUMA, SMT, Hyper-Threading, Intel oneDNN, スループット最適化, Multiple Inference Stream]
category: "infra"
related: [1710, 1116, 1489, 113, 1611]
memo: "[HF Blog] Scaling-up BERT Inference on CPU (Part 1)"
processed_at: "2026-04-14T12:48:31.751837"
---

## 要約

本記事はHugging FaceのエンジニアMorgan Funtowiczによる、CPU上でのBERTライクモデル推論を最適化するシリーズの第1弾。対象ハードウェアはAWS c5.metalインスタンス（Intel Xeon Platinum 8275CL、48コア/96スレッド）で、Ubuntu 20.04、transformers 4.5.0、PyTorch 1.8.1、TensorFlow 2.4.0を使用。

まずベースライン比較として、PyTorchとTensorFlowのアウト・オブ・ザ・ボックスの推論性能を比較。PyTorchがOpenMPとIntel MKL（oneDNN）を内部利用しているのに対し、TensorFlowはEigenと独自スレッド実装を使うため、全設定においてPyTorchが優位な結果を示した。ただしこれは「最適化なし」の状態での比較であり、双方の最適化後の性能差ではない点に注意が必要。

次に「Multiple Inference Stream」というアプローチを紹介。同一モデルの複数インスタンスを生成し、各インスタンスをCPUコアの非重複サブセットに割り当てることで真の並列推論を実現する手法。これによりレイテンシを維持しつつスループットを向上させることが可能。

SMT（Simultaneous Multi-Threading）／Hyper-Threadingについても詳述。物理コアと論理スレッドの違いを説明し、Deep Learning推論ではメモリアクセス待機が少なく演算密度が高いため、SMTの効果が限定的である点を指摘。実験結果として、SMT有効時より物理コアのみ使用時のほうがBERT推論性能が高いケースが多いことを示している。

NUMA（Non-Unified Memory Architecture）の考慮も重要なポイント。c5.metalは2ソケット構成であり、コアとメモリの配置がNUMAドメイン（Node 0/Node 1）に分かれている。cross-NUMAアクセスは同一NUMAノード内アクセスより低速なため、numactl等を用いてプロセスを特定NUMAノードに固定することが推奨される。

コア数スケーリングの実験では、コア数を増やしても単一推論のレイテンシは単調に改善しないことが判明。物理コア数を超えてスレッドを増やすと性能が劣化する傾向がある。一方、バッチサイズスケーリング（複数の独立したモデルインスタンスを並列実行）では、インスタンス数に応じてスループットが線形に近い形でスケールすることを確認。ONNX RuntimeはPyTorch/TensorFlowと比較してさらに良好な性能を示す場面もあり、今後の最適化候補として言及されている。また量子化（int8等）についても今後のシリーズでカバー予定と述べている。

## アイデア

- SMT（Hyper-Threading）はメモリ待機の多い汎用タスクには有効だが、演算密度の高いDL推論では物理コアのみ使用のほうが性能が高い場合があるという逆説的な知見
- 単一インスタンスのコア数を増やすよりも、複数の独立したモデルインスタンスを各コアグループに割り当てる『Multiple Inference Stream』のほうがスループット向上に効果的
- NUMAトポロジーを無視したコア割り当てはメモリアクセス遅延を引き起こすため、numactl等でNUMAノードへのプロセス固定が本番CPU推論では必須

## 前提知識

- **Transformer / BERT** (TODO: 読むべき)
- **CPU スレッド / SMT** (TODO: 読むべき)
- **NUMA アーキテクチャ** (TODO: 読むべき)
- **ONNX Runtime** → /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応
- **量子化（int8）** (TODO: 読むべき)

## 関連記事

- /deep_1710 Habana GaudiでTransformersを使い始める：AWS EC2 DL1インスタンスでのBERTファインチューニング
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1611 近接方策最適化（PPO）：方策更新を安定させるクリッピング手法

## 原文リンク

[CPU上でのBERT推論をスケールアップする（Part 1）：ハードウェア最適化の基礎](https://huggingface.co/blog/bert-cpu-scaling-part-1)
