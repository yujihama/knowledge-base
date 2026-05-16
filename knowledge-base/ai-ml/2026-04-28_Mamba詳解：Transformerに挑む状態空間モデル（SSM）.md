---
title: "Mamba詳解：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-28
tags: [Mamba, SSM, 状態空間モデル, Transformer, 選択的状態空間, 長文脈, 線形計算量, CUDA最適化, S4, Zero-Order Hold]
category: "ai-ml"
related: [2510, 3105, 2480, 1975, 1837]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-28T12:31:23.446994"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを解消することを目的としている。Transformerはトークン間の全対全通信（O(n²)の訓練計算量、O(n)の自己回帰推論計算量）とKVキャッシュによるO(n)のメモリ消費が問題となるが、Mambaはこれを連続時間微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) で表現される状態空間表現に置き換える。この連続時間モデルをZero-Order Hold（ZOH）法で離散化し、実際のシーケンス処理に適用する。離散化後のパラメータĀ、B̄はΔ（タイムステップサイズ）を介して制御され、このΔ自体を入力依存（selective）にすることがMambaの核心的革新である。従来のS4等のSSMでは行列A、B、Cが入力に依存しない固定パラメータだったが、MambaではB、C、Δを入力xの関数として動的に変化させる「Selective State Space Model」を採用する。これにより、モデルがどの情報を状態に保持し、どの情報を忘却するかを入力に応じて選択できるようになる。Selective SSMは並列畳み込みによる訓練高速化と、逐次的な再帰処理による推論効率の両立をHardware-Aware Parallel Algorithm（CUDA カーネルの融合・IO最適化）で実現する。Mamba-3Bモデルは同規模Transformerを上回り、2倍規模Transformerに匹敵する性能を事前訓練・下流評価の双方で達成。推論速度はTransformerの最大5倍、コンテキスト長は100万トークンまでリニアにスケール。また、言語・音声・ゲノミクスなど複数モダリティでSOTA性能を示す。解釈可能性の観点では、Mambaの圧縮された隠れ状態は情報の選択的保持という点でTransformerのアテンションパターンとは異なる解析アプローチが必要となり、AIセーフティ研究における新たな課題を提示している。監査エージェント開発への示唆としては、長文書・長期ログの一括処理において、Transformerの文脈長制限（4K〜128K程度）を超える100万トークン規模の処理が現実的になる点が注目される。ただし、MambaはIn-Context Learning性能でTransformerに劣るとの指摘もあり、Few-shot推論を多用する監査タスクでは慎重な評価が必要。

## アイデア

- SelectiveメカニズムによりΔ・B・Cを入力依存にすることで、SSMが固定フィルタから動的フィルタに変わる点：これはRNNの「ゲート機構」（LSTMのforget gate等）と概念的に同一であり、SSMとRNNの統一的理解が可能になる
- 訓練時は並列畳み込み（O(n log n)）、推論時は再帰（O(1)/ステップ）という二重の計算グラフをCUDAカーネル融合で実現する設計：同一モデルが訓練・推論で異なるアルゴリズムを使う点は今後のハードウェア最適化研究に示唆が大きい
- 圧縮された固定サイズの隠れ状態（有限メモリ）はTransformerのKVキャッシュ（無限に増大）と本質的に異なり、In-Context Learningに必要な「過去の全トークン参照」ができないというトレードオフ：タスク特性によってMamba/Transformerを使い分ける設計判断が今後重要になる

## 前提知識

- **Transformer・アテンション機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **畳み込み定理・FFT** (TODO: 読むべき)
- **離散化・Zero-Order Hold** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ

## 原文リンク

[Mamba詳解：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
