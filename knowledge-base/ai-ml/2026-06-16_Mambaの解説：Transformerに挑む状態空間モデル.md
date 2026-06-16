---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-16
tags: [Mamba, SSM, State Space Model, Transformer, 選択的状態空間, 長文脈処理, 線形スケーリング, 離散化, ZOH]
category: "ai-ml"
related: [3105, 7117, 7961, 2480, 7597]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-16T09:21:54.510968"
---

## 要約

Mambaは、Transformerの代替となる状態空間モデル（SSM: State Space Model）ベースのシーケンスモデルアーキテクチャである。Transformerの核心的問題はAttention機構の計算量がシーケンス長nに対してO(n²)となる「二次ボトルネック」であり、KVキャッシュのメモリ消費もO(n)に達する。これにより、100万トークン規模の長文脈処理は事実上困難であった。

Mambaはこの問題を制御理論由来のSSMで解決する。基本的な連続時間状態方程式はh'(t) = Ah(t) + Bx(t)、出力方程式はy(t) = Ch(t) + Dx(t)で表される。ここでhは隠れ状態（過去の情報の圧縮）、xは現在の入力、A/B/C/Dは学習可能な行列パラメータである。連続時間方程式はZero-Order Hold（ZOH）離散化によって差分方程式へ変換され、実装可能な形式となる。

従来のSSM（S4等）との最大の違いは「選択的状態空間（Selective State Space）」機構にある。S4ではA/B/C行列が入力に依存しない固定パラメータだったが、MambaではB、C、さらに離散化パラメータΔを入力x_tに応じて動的に変化させる。これにより「何を状態に保持し、何を忘れるか」を入力内容に応じてモデル自身が制御できる。たとえば文脈上重要なトークンは長く保持し、不要な情報は積極的に忘却する動作が可能になる。

計算効率の面では、Mambaはシーケンス長に対して線形O(n)スケールを実現しており、Transformerより最大5倍高速な推論速度を達成している。学習時はHardware-Aware Parallel Scanアルゴリズムを用いて並列化するが、推論時は再帰（RNN的）計算で定数メモリで動作する。この二重の動作モードがMambaの実用上の強みである。

性能面では、Mamba-3Bモデルが同サイズのTransformerを上回り、パラメータ数が2倍のTransformerと同等の性能をThe Pile等のベンチマークで達成している。ゲノム解析や音声など長い系列を扱うモダリティでも有効性が示されている。

一方で課題もある。Transformerのキー・バリュー検索のような「特定トークンへの直接参照」はMambaの固定サイズ隠れ状態では原理的に苦手であり、in-context learningの一部タスクでTransformerに劣るケースがある。解釈可能性（Interpretability）の観点でも、Attention Headのような直感的な分析単位が存在しないため、内部動作の理解が難しい。

監査エージェント開発への示唆として、Mambaの「選択的忘却」機構は長大な監査証跡や法令文書を扱う際のメモリ効率化に応用可能である。また線形スケールの推論コストは、ReActループで大量の中間ステップを処理するエージェントシステムのレイテンシ削減に直結する。ただし特定証拠への正確な参照が求められる監査タスクにはAttentionベースのモデルが依然優位な場面もある。

## アイデア

- 選択的状態空間（Selective SSM）：入力に応じてB・C・Δを動的に変化させることで、RNNの固定ゲートを超えた柔軟な情報選択が可能になる点が革新的
- 学習時は並列スキャン、推論時は再帰計算という二重モード動作により、TransformerのKVキャッシュ問題を回避しながらGPU効率も確保するハードウェアco-designの発想
- 隠れ状態hを「過去の圧縮」と定義することで、100万トークン超の文脈を固定サイズのベクトルに圧縮して保持できる点は、超長期の会話履歴や監査ログ処理への応用可能性を示唆する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model (S4)** (TODO: 読むべき)
- **離散化・差分方程式** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_7961 LLMに「睡眠」が必要な理由 ― 論文「Language Models Need Sleep」解説
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_7597 深層学習・生成AIの全体像を「3つの問い」で整理する｜CNNから拡散モデル・Mambaまで

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
