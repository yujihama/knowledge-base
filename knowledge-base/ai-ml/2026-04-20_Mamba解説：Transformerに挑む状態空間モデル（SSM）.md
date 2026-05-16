---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-20
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, 選択的SSM, HiPPO, 並列スキャン, 長文脈処理, シーケンスモデル]
category: "ai-ml"
related: [1837, 222, 833, 255, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-20T12:52:53.823356"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量（O(n²)）の問題を解決するアーキテクチャである。Transformerはすべてのトークン間の全対全通信をKVキャッシュで実現するが、これにより長いシーケンスでは計算量・メモリ使用量が急増する。MambaはAttentionをSSMに置き換え、線形スケーリングO(n)を実現しながらも同等の性能を達成する。

SSMの中核は制御理論由来の状態方程式で、隠れ状態h(t)の更新を h'(t) = Ah(t) + Bx(t)、出力をy(t) = Ch(t) + Dx(t) で表現する。連続時間の微分方程式をZero-Order Hold（ZOH）離散化によって離散時間の差分方程式に変換し、h_{t+1} = Āh_t + B̄x_t として実装する。

SSMは畳み込み（並列学習）と再帰（逐次推論）の二重性を持つ。学習時は全シーケンスを一度に処理する畳み込み計算で効率化し、推論時は再帰的な更新で一定サイズの隠れ状態のみを保持する。これによりTransformerより最大5倍高速な推論を実現し、100万トークン規模のシーケンスにも対応できる。

HiPPO（High-order Polynomial Projection Operators）理論でA行列を初期化することで、SSMは過去の入力を直交多項式基底に投影して圧縮保持する。これにより長期依存関係を捕捉しやすくなる。

従来のSSM（S4等）が抱えていた問題は「選択性の欠如」で、入力内容に関わらず同一のA, B, C行列を使用していた。Mambaのキーイノベーションは「選択的状態空間モデル（S6）」で、B, C行列と時間ステップΔを入力x_tに依存させる（入力依存パラメータ化）ことで、重要な情報を選択的に保持・忘却できるようにした点にある。ただしこの入力依存性によって畳み込みとしての計算が困難になるため、FlashAttentionに倣ったHardware-Aware Parallel Scanアルゴリズムを採用し、HBMへのアクセスを最小化しつつSRAM上で並列スキャン計算を行う。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する事前学習・下流評価性能をThe Pileで示した。言語・音声・ゲノミクスなど複数モダリティでSOTA性能を達成。一方で既存の解釈可能性（Induction Heads等のCircuit分析）手法がそのまま適用できない課題があり、安全性・解釈性研究での対応が必要とされる。監査エージェント開発においては、長文ドキュメント（監査報告書、法規制文書）の処理やリアルタイムストリーミング推論への適用可能性が注目点となる。

## アイデア

- 選択的状態空間モデル（S6）により入力に依存してB, C, Δを動的に変化させる仕組みは、RNNの固定遷移行列とAttentionの全対全注意の中間的な設計思想であり、「何を記憶し何を忘れるか」を学習で決める点が独自
- 畳み込みと再帰の二重性（学習時は並列畳み込み、推論時は逐次再帰）はSSMの構造的な特性であり、Transformerのような学習・推論の一貫したアーキテクチャとは異なるトレードオフ設計になっている
- HiPPO行列による初期化で過去入力を直交多項式空間に投影するアプローチは、信号処理理論をDLアーキテクチャ設計に応用した例であり、A行列の初期化がSSM性能に与える影響を示す重要な知見

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込みニューラルネットワーク** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
