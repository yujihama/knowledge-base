---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-13
tags: [Mamba, SSM, State Space Model, Transformer, Selective SSM, 長文脈, 線形スケーリング, ZOH離散化, Parallel Scan, シーケンスモデル]
category: "ai-ml"
related: [199, 222, 833, 255, 1494]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-13T12:48:04.459762"
---

## 要約

MambaはAlbert GuとTri Daoが開発した、Transformerに代わるシーケンスモデルのアーキテクチャで、State Space Model（SSM）をベースとしている。Transformerの最大の弱点はAttention機構のO(n²)計算量と、KVキャッシュによるO(n)メモリ消費であり、100万トークン規模の長文脈処理では実用上の限界がある。Mambaはこの二次的ボトルネックを取り除き、シーケンス長に対してリニアなスケーリングを実現する。

Mambaの理論的基盤は制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) にある。状態hは過去の全情報を圧縮した「要約」であり、新しい入力xと組み合わせることで次の出力yを予測する。この連続時間方程式をZero-Order Hold（ZOH）離散化によりh_t = Ā·h_{t-1} + B̄·x_t という差分方程式へ変換し、実際の離散的な系列データに適用できるようにしている。

SSMは学習時にConvolutionとして並列計算でき（訓練効率）、推論時にはRecurrent Neural Networkとして逐次処理できる（推論効率）という二重の性質を持つ。ただし従来のSSM（S4等）はA・B・Cが入力に依存しない線形時不変（LTI）システムであるため、内容に応じた選択的な情報保持が困難だった。

Mambaの核心的な革新は「Selective SSM」である。入力x_tに基づいてB、C、Δ（ステップサイズ）をダイナミックに変化させることで、選択的な記憶と忘却を可能にする。Δが大きいほど現在の入力を重視し、小さいほど過去の状態を維持する。これはTransformerのAttentionが各トークン間の関連度を動的に計算するのと概念的に対応する。

ただし選択性を持たせると「カーネルトリック」（Convolutionとしての並列計算）が使えなくなるため、MambaはHardware-Aware Parallel Scanというアルゴリズムを採用。CUDA SRAMを活用したFlashAttentionと同様の発想でGPU上の効率的な並列処理を実現している。

Mamba-3Bは同サイズのTransformerを上回り、2倍のサイズのTransformerと同等の性能をThe Pileベンチマークで達成。推論速度はTransformerより最大5倍高速。一方、現時点の限界として、in-context learningが苦手（圧縮された状態表現では類似事例を検索しにくい）、Mambaのベースモデルは少数事例での適応においてTransformerより劣ることが示されている。解釈可能性の観点からも、隠れ状態の意味的解析はAttentionパターンの分析より難しい。監査エージェント開発への示唆として、長文書・監査証跡の長大シーケンス処理においてMambaの線形スケーリングは実用的な優位性を持つが、文書内の特定情報を正確に参照するin-context retrieval用途ではTransformerが依然有利である。

## アイデア

- SSMは訓練時はConvolution（並列計算）、推論時はRNN（逐次処理）という二重の計算モードを持ち、どちらの局面でも効率的に動作できる数学的構造が巧妙
- SelectivitiyをΔ（ステップサイズ）でコントロールするアイデアは、RNNのゲート機構（LSTMのforget gate等）とAttentionの中間的な概念として解釈可能であり、三者の統一的理解につながる
- 監査ログ・長大な契約文書など100万トークン超の処理が必要な領域でMambaのリニアスケーリングは実用価値があるが、「どのトークンを参照したか」の追跡可能性（解釈可能性）ではAttentionマップに劣り、監査用途での透明性確保に課題が残る

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model (S4)** (TODO: 読むべき)
- **畳み込み (Convolution)** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
