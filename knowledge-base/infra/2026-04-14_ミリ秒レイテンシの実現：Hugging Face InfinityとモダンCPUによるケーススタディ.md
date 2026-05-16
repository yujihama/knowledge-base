---
title: "ミリ秒レイテンシの実現：Hugging Face InfinityとモダンCPUによるケーススタディ"
url: "https://huggingface.co/blog/infinity-cpu-performance"
date: 2026-04-14
tags: [Hugging Face Infinity, CPU推論最適化, Intel Ice Lake, DistilBERT, ONNX Runtime, Optimum Intel, AVX-512, INT8量子化, EC2 C6i, 推論パイプライン]
category: "infra"
related: [1449, 1116, 1536, 411, 705]
memo: "[HF Blog] Case Study: Millisecond Latency using Hugging Face Infinity and modern CPUs"
processed_at: "2026-04-14T12:08:35.503496"
---

## 要約

Hugging Face Infinityは、Transformerモデルをエンドツーエンドで最適化してデプロイするコンテナ化ソリューション。2022年1月時点の発表（同年12月に商用提供終了）。本記事では、第3世代Intel Xeon Scalable（Ice Lake）を搭載したAmazon EC2 C6iインスタンス上でのベンチマーク結果を詳述している。

システム構成は2層：①Infinity Container（ハードウェア最適化済み推論エンジン、Dockerイメージ）と②Infinity Multiverse（ターゲットハードウェア向けモデル最適化サービス）。推論パイプラインは前処理・推論・後処理をすべて含むエンドツーエンド計測であり、モデル単体の計測ではない点が特徴。

ベンチマーク対象はDistilBERTの感情分類タスク。192通りの構成（物理コア数：1/2/4/8、シーケンス長：8〜512、バッチサイズ：1〜32）で実施。主な結果は以下のとおり：

【スループット（2コア、バッチサイズ1）】
- シーケンス長8：Infinity 248 req/sec vs vanilla Transformers 49 req/sec（+506%）
- シーケンス長128：55 req/sec vs 18 req/sec（+305%）
- シーケンス長512：12 req/sec vs 4 req/sec（+300%）
全シーケンス長で300〜500%以上のスループット向上を達成。

【レイテンシ】バッチサイズ1・2コアの構成で、p95・p99・p100（最大レイテンシ）の偏差が極めて小さく安定した予測応答時間を実現。これは本番環境でのSLA保証に直結する特性。

Ice LakeベースのC6iインスタンスは、旧世代Cascade LakeベースのインスタンスとのInfinity比較でも最大34%のレイテンシ・スループット改善を示した。また、vanilla TransformersをIce Lake上で動作させた場合と比較して、最大800%のレイテンシ・スループット改善。

最適化技術の根幹はIntel AVX-512命令セット、Intel Deep Learning Boost（INT8演算加速）、Intel Turbo Boostの活用。モデルをINT8に量子化し、AVX-512のベクトル演算でバッチ推論を高速化する構造。

監査エージェントへの示唆：大量ドキュメントの同時処理（テキスト分類、エンティティ抽出）においてGPUなしでもCPU最適化推論で実用的スループットが得られる。特にコスト制約のある社内デプロイ環境では、GPU不要のCPU最適化推論コンテナは有効な選択肢となる。現在はInfinity自体は終了しているが、後継として🤗 Optimum Intel・Optimum ONNX Runtimeが同等の最適化を提供しており、実務的には後継ツールの活用が推奨される。

## アイデア

- エンドツーエンド（前処理+推論+後処理）で計測することで、モデル単体ベンチマークでは見えなかった実運用レイテンシのボトルネックを可視化できる設計思想
- GPU不使用のCPU最適化だけでvanilla Transformers比最大800%のスループット向上を実現しており、ハードウェアアーキテクチャへの最適化（AVX-512, INT8）の効果が極めて大きいことを定量的に示している
- p99・p100レイテンシの安定性（低偏差）は本番SLA保証に直結する品質指標であり、平均レイテンシだけでなく尾部分布の安定性をベンチマーク指標に含める重要性を示している

## 前提知識

- **BERT / DistilBERT** (TODO: 読むべき)
- **ONNX / INT8量子化** (TODO: 読むべき)
- **Transformers推論パイプライン** (TODO: 読むべき)
- **Intel AVX-512** (TODO: 読むべき)
- **Docker コンテナデプロイ** (TODO: 読むべき)

## 関連記事

- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1536 最適化の記録: BLOOM推論サーバーの高速化
- /deep_411 faster-whisperで手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度
- /deep_705 Transformerベースのソースコード表現を用いた並列化可能ループの自動識別

## 原文リンク

[ミリ秒レイテンシの実現：Hugging Face InfinityとモダンCPUによるケーススタディ](https://huggingface.co/blog/infinity-cpu-performance)
