---
title: "高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較"
url: "https://huggingface.co/blog/habana-gaudi-2-benchmark"
date: 2026-04-10
tags: [Habana Gaudi2, Nvidia A100, GPU benchmark, HuggingFace Optimum, SynapseAI, BERT, Stable Diffusion, T5, bfloat16, 分散学習]
category: "infra"
memo: "[HF Blog] Faster Training and Inference: Habana Gaudi®2 vs Nvidia A100 80GB"
processed_at: "2026-04-10T21:10:37.773622"
---

## 要約

HuggingFaceとHabana Labsによる2022年12月公開のベンチマーク記事。第2世代AIアクセラレータ「Habana Gaudi2」の性能をNvidia A100 80GBおよび第1世代Gaudiと比較した結果を報告している。

Gaudi2の主な仕様は、1サーバーに8デバイス、各デバイス96GBメモリ（第1世代Gaudiの3倍、A100の約1.2倍）。SDKはSynapseAIで第1世代Gaudiと共通のため、既存のワークフローをコード変更なしにそのまま移行可能。HuggingFaceの🤗 Optimum Habanaライブラリを通じてTransformersおよびDiffusersと連携できる。

【BERT事前学習】バッチサイズ32でGaudi2のスループットは1580.2 samples/s、A100は981.6 samples/s（約1.61倍）。バッチサイズ64ではGaudi2が1835.8 samples/s、A100が1082.6 samples/s（約1.70倍）。第1世代Gaudi比ではスループットx3.53、学習時間は8時間53分→1時間33分と5.75倍短縮。

【Stable Diffusion推論】バッチサイズ8でGaudi2のレイテンシは0.925秒/枚、A100（バッチサイズ1）は2.63秒/枚でGaudi2がx2.84高速。第1世代Gaudi比ではx3.51の高速化。

【T5-3Bファインチューニング】96GBメモリにより3Bパラメータモデルを勾配チェックポイントのみでファインチューニング可能（第1世代Gaudiでは不可）。スループットはGaudi2が19.7 samples/s、A100が8.07 samples/sでx2.44の差。

精度面では、Gaudiはbfloat16/fp32混合精度、A100はfp16で実行しており、単純な条件比較ではない点に注意が必要。Intel Developer Cloud経由でGaudi2インスタンスにSSHアクセスして利用可能。

## アイデア

- SDKレベルで第1世代・第2世代ハードウェアの互換性を保つ設計により、コード変更なしのハードウェア移行が可能になるという設計思想は、エージェントシステムのバックエンド抽象化にも応用できる
- 96GBという大容量メモリが3Bパラメータモデルのファインチューニングを可能にした事例は、モデルサイズとメモリ制約の関係を具体的に示しており、ローカルLLMインフラ選定の基準として参考になる
- バッチサイズを32→64に倍増させることで収束に必要なステップ数が65k→20kに大幅減少した事実は、大バッチ学習による収束効率の実証例として興味深い

## Yujiの取り組みへの示唆

Yujiが構築中のローカルLLMインフラ（RTX 3090予定）の比較対象として、Gaudi2の96GBメモリ・A100比x2倍以上のスループットは代替ハードウェア選択肢の参考になる。監査エージェントでLangGraph+Pydanticを用いたReActシステムを開発する際、LLMのファインチューニングや大規模推論が必要になった場合のクラウドGPU選定基準として活用できる。ただし、本記事は2022年末時点の情報であり、現在はより新しい世代のGPU（H100等）が主流のため、最新の選択肢と合わせて参照すべき。

## 原文リンク

[高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較](https://huggingface.co/blog/habana-gaudi-2-benchmark)
