---
title: "Training Cluster as a Service — Hugging FaceとNVIDIAによる大規模GPU クラスター提供サービスの発表"
url: "https://huggingface.co/blog/nvidia-training-cluster"
date: 2026-04-07
tags: [GPU-cluster, NVIDIA-DGX-Cloud, Hugging-Face, H100, GB200, DGX-Cloud-Lepton, Training-as-a-Service, 大規模モデル訓練]
category: "infra"
memo: "[HF Blog] Introducing Training Cluster as a Service - a new collaboration with NVIDIA"
related: [1263, 1487, 524, 1114, 989]
processed_at: "2026-04-07T12:49:42.858518"
---

## 要約

2025年6月11日、GTC Parisにて、Hugging FaceとNVIDIAはTraining Cluster as a Service（TCaaS）を共同発表した。本サービスは、大規模GPUクラスターへのアクセスを世界中の研究機関・大学・企業に対して、必要な期間だけ利用できる従量課金モデルで提供する。

技術構成は3層からなる。まず、NVIDIA Cloud Partnersが地域データセンターにおいてNVIDIA Hopper（H100等）およびGB200を含む最新アクセラレーテッドコンピューティングキャパシティを提供。これらはNVIDIA DGX Cloudに集約される。次に、GTC Parisで同時発表されたNVIDIA DGX Cloud Leptonが、研究者向けにプロビジョニングされたインフラへの簡易アクセスと、トレーニングランのスケジューリング・モニタリング機能を担う。最後に、Hugging Faceのオープンソースライブラリ群（Transformers、Accelerate等）がトレーニング開始を容易にする。

フロー面では、Hugging Face上の25万以上のOrganizationが、hf.co/training-clusterからGPUクラスターをリクエストでき、リクエスト受理後にHugging FaceとNVIDIAが連携してサイズ・リージョン・期間の要件に合わせた調達・価格設定・プロビジョニング・セットアップを実施する。

実際の活用事例として3組織が紹介されている。TIGEM（Telethon Institute of Genomics and Medicine）は希少遺伝性疾患の病原性バリアント予測と創薬転用向けAIモデルの訓練に活用。Numina（数学推論AI非営利団体、2024 AIMO進歩賞受賞）はDeepMindのAlphaProofに対抗するオープン代替モデルの構築に使用。Mirror Physicsは化学・材料科学向けフロンティアAIシステムの構築にMACEチームと協力して活用している。

GTC Parisでの関連発表として、NVIDIA DGX Cloud LeptonによるEurope向けグローバルNVIDIAコンピュートエコシステム接続、NVIDIA AI顧客向け10万以上のHugging FaceモデルのNIM経由デプロイ対応、NVIDIA Cosmos Predict-2によるPhysical AIモデル構築、Isaac GR00T N1.5（ヒューマノイドロボット向け）のHugging Face公開なども行われた。

背景として、ギガワット規模のGPUスーパークラスター建設が進む中でGPUリッチとGPUプアの格差拡大が懸念される一方、ハイパースケーラーや地域クラウドがキャパシティを急拡大しており、その供給と研究ニーズをつなぐマーケットプレイス機能を本サービスが担う位置づけとなっている。

## アイデア

- 従量課金型GPUクラスター調達モデルにより、研究機関がCapExなしでGB200規模の計算リソースを必要なタイミングだけ確保できる点は、モデル訓練の経済性を根本的に変える
- DGX Cloud Leptonがスケジューリング・モニタリングを担うミドルウェア層として機能することで、研究者がインフラ管理を意識せずHugging Faceのライブラリをそのまま使える抽象化レイヤーの設計が参考になる
- 希少疾患研究・数学推論・材料科学という異なるドメインの非GPUリッチ組織が最初のユーザーとして挙がっており、汎用基盤モデルではなくドメイン特化モデル訓練の民主化が主眼であることが示唆される

## 関連記事

- /deep_1263 物体検出リーダーボード：評価指標とその落とし穴の解説
- /deep_1487 機械学習におけるバイアスについて語ろう！倫理・社会ニュースレター第2号
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_1114 NVIDIA DGX CloudのH100 GPUでモデルを簡単にトレーニングする方法
- /deep_989 Hugging FaceとNVIDIA NIMによるサーバーレス推論（DGX Cloud連携）

## 原文リンク

[Training Cluster as a Service — Hugging FaceとNVIDIAによる大規模GPU クラスター提供サービスの発表](https://huggingface.co/blog/nvidia-training-cluster)
