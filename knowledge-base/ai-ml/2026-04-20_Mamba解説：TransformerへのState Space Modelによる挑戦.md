---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-20
tags: [Mamba, State Space Model, SSM, Transformer, Selective SSM, 線形スケーリング, Parallel Scan, 長コンテキスト, シーケンスモデル]
category: "ai-ml"
related: [222, 1975, 199, 833, 255]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-20T12:11:22.772480"
---

## 要約

Mambaは、Transformerの二次計算量ボトルネックを解消するState Space Model（SSM）ベースのアーキテクチャ。Gu・Dao両氏が開発し、Transformerの自己注意機構をSSMで置換することで、シーケンス長に対して線形スケーリングを実現した。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。推論速度はTransformerの最大5倍高速。

【Transformerの問題点】Attention機構では全トークンがKVキャッシュを通じて相互参照するため、訓練時のFLOPはO(n²)、自己回帰推論時のメモリはO(n)。100万トークン級のコンテキストは実質的に非現実的だった。

【SSMの仕組み】連続時間の状態方程式 h'(t)=Ah(t)+Bx(t)、y(t)=Ch(t)+Dx(t) を離散化（Zero-Order Hold法）して差分方程式に変換。状態hは過去の圧縮表現として機能し、マルコフ決定過程と同様に現在の状態から次の出力を導出する。畳み込みとしても表現できるため、訓練時は並列処理が可能で、推論時はRNN的に再帰処理できる双方向の効率性を持つ。

【Selective SSMの核心】従来のSSMは時不変（行列A・B・Cが固定）だったため、「selective copying」や「induction heads」などのシーケンス選択的タスクに失敗していた。MambaはΔ（時間ステップ）、B、Cを入力依存（input-selective）にすることで、重要な情報を選択的に状態に保持・破棄できる。Δが大きい入力は状態に強く反映され、Δが小さい入力は無視される仕組み。

【ハードウェア効率化：Parallel Scan】入力依存パラメータにより畳み込みが使えなくなるが、Parallel Scan（プレフィックス和の並列化）により効率的に処理。HBMとSRAMの間のメモリ転送を最小化するkernel fusionも実装し、実効的な高速化を実現。

【限界と課題】Mamba-3BはThe Pile上でTransformerを僅差で上回るが、文脈内学習（in-context learning）ではTransformerに劣る報告もある。また、状態サイズが固定（例：16次元）のため、極めて長い依存関係の保持には理論的限界がある。解釈可能性・AIセーフティ面では、Transformerで発達したCircuit分析や活性化パッチングの手法がそのまま適用できない。

## アイデア

- 入力依存的なΔパラメータによるSelective SSMは「何を記憶し何を忘れるか」をデータドリブンに学習する仕組みで、LSTMのゲート機構をSSMの枠組みで再発明したとも解釈できる
- 訓練時は並列畳み込み、推論時は再帰処理という二重性は、エージェントシステムのバッチ訓練と逐次推論の非対称なコスト構造に対してアーキテクチャレベルで応答しており、長期記憶を持つ監査エージェントの状態管理に応用可能性がある
- Mamba-3Bが2倍サイズのTransformerと同等という結果は、パラメータ効率の観点でKV-cacheの廃止によるメモリ削減と合わせて、エッジ・ローカルLLM推論の実用化に直結する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **畳み込みニューラルネット** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **状態空間モデル（制御理論）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
