---
title: "Mambaとは何か：State Space ModelがTransformerに挑む仕組みの解説"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-19
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, 線形スケーリング, 選択的メカニズム, 離散化, ZOH, FlashAttention]
category: "ai-ml"
related: [3105, 7117, 7961, 2480, 7597]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-19T09:24:39.103716"
---

## 要約

Mambaは、Gu・Daoが2023年に発表したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量の問題を解消しながら、同等以上の性能を実現する。Transformerでは全トークン間のペアワイズ通信（KVキャッシュ）が必要で、訓練時O(n²)・推論時O(n)の計算コストと大きなメモリ消費が長文脈処理の障壁となる。Mambaはこれをアテンション機構の代替として制御理論由来のSSMを採用することで、シーケンス長に対して線形スケーリングを達成し、最大100万トークンの長文脈処理を可能にした。Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をpretraining・下流タスクの両方で示している。推論速度はTransformerの最大5倍とされる。

SSMの基本は連続時間の状態方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、「状態」が過去情報の圧縮として機能する。実用化にあたってはZero-Order Hold（ZOH）法で離散化し、差分方程式 h_{t+1} = Āh_t + B̄x_t に変換する。この再帰的表現はRNNと同型であり、逐次推論には有利だが訓練時の並列化が困難という問題が生じる。

Mambaの核心的革新は「選択的SSM」（Selective State Spaces / S6）にある。古典的SSMのパラメータA・B・C・Δは入力非依存の固定値だったが、MambaではΔ・B・Cを入力x_tに依存する動的パラメータとすることで、どの情報を状態に保持・破棄するかをトークンごとに選択できる。これはTransformerのソフトアテンション的な選択性に相当する。

実装上の課題として、選択性を持たせるとカーネル融合（畳み込みによる並列訓練）が使えなくなる問題があり、これをHardware-Aware Parallel Algorithmで解決している。具体的にはGPUのSRAM（L1キャッシュ）上で再帰計算を完結させるFlash化で、HBM（メインGPUメモリ）へのアクセスを最小化する。

解釈可能性・安全性の観点では、Mambaの隠れ状態は固定次元のベクトルであり、Transformerのアテンション重みのような可視化が困難で、モデルが何を「記憶」しているかの解析が難しい。一方でBアルゴリズムの入力選択メカニズムはある程度の解釈性を持つ可能性がある。監査AIエージェント開発への示唆として、長文脈の契約書・監査ログを低コストで処理するバックボーンとしての適性があり、RNNライクな逐次推論は状態管理が明示的なエージェントループとの相性も期待できる。

## アイデア

- 選択的SSM（S6）は入力ごとにΔ・B・Cを動的に決定することでTransformerのアテンションに相当する「何を覚えるか選ぶ」能力を再帰モデルに与えており、固定係数RNNとの本質的差別化点になっている
- 訓練時は畳み込みとして並列化、推論時は再帰として逐次処理という二重表現の切り替えは、同一モデルが学習効率と推論効率を両立するアーキテクチャ設計のトレードオフ解決策として参考になる
- 隠れ状態が固定サイズベクトルに圧縮されるため解釈可能性が低下するという制約は、監査・コンプライアンス用途でモデルの判断根拠を追跡しなければならないユースケースにおいて重要な検討事項となる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・再帰モデル** (TODO: 読むべき)
- **畳み込みニューラルネット** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **状態空間モデル（制御理論）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_7961 LLMに「睡眠」が必要な理由 ― 論文「Language Models Need Sleep」解説
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_7597 深層学習・生成AIの全体像を「3つの問い」で整理する｜CNNから拡散モデル・Mambaまで

## 原文リンク

[Mambaとは何か：State Space ModelがTransformerに挑む仕組みの解説](https://thegradient.pub/mamba-explained/)
