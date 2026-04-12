---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-10
tags: [Mamba, SSM, 状態空間モデル, Transformer, 線形RNN, 選択的状態空間, 長文脈, FlashAttention, parallel-scan]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [199, 222, 833, 221, 255]
processed_at: "2026-04-10T21:24:52.443545"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのコアな制約であるAttentionの二次計算量（O(n²)）を線形計算量（O(n)）で代替する。Transformerでは全トークン間のペアワイズ通信が必要なため、KVキャッシュがO(n)空間を占有し、長文脈になるほど推論速度が悪化する。Mambaはこれを制御理論由来のSSMで解決する。

SSMの基本方程式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される。hが隠れ状態（過去の圧縮）、xが新規入力、yが出力。これをZero-Order Hold（ZOH）離散化により差分方程式に変換し、実際のシーケンス処理に適用する。

Mambaの最大の革新は「選択的状態空間」（S6）にある。従来のSSMでは行列A・B・Cが入力に依存しない固定パラメータだったが、MambaではB・C・Δを入力xの関数として動的に変化させる。これによりモデルが「どの情報を記憶し、何を忘れるか」を文脈に応じて選択できる。例えば「Harry Potter本」と「ハリー・ポッター本」の質問に対し、前者は「本」という情報を忘れて「Harry Potter」のみを記憶し、後者は両方を記憶する。

ハードウェア最適化として、FlashAttentionと同様の手法で中間状態をSRAMに保持し、HBM転送を最小化するParallel Associative Scanを採用。これによりTransformerより最大5倍高速な推論を実現する。学習時は並列スキャンで高速化、推論時は再帰的計算でメモリ効率を最大化する二重構造。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等性能を達成（The Pile評価）。文脈長は100万トークンまでスケール可能で、言語・音声・ゲノミクスなど複数モダリティで最高水準の性能を示す。

一方の課題として、固定サイズの隠れ状態は「lossy compression」であり、Transformerのように全過去トークンへの完全アクセスを保証しない。そのためin-context learningやプロンプトエンジニアリング、few-shot学習においてTransformerより劣る可能性がある。またMamba-2ではSSMとAttentionの双対性が示されており、両者の統一理論への道が開かれている。

## アイデア

- 隠れ状態を「過去の非可逆圧縮」と定義することで、Markov性を持つ効率的なシーケンス処理が可能になる点。Transformerが全履歴を保持するのに対し、SSMは必要な情報のみを圧縮・選択的に保持する設計思想は、長期記憶と短期記憶のトレードオフを明示している
- 選択性（Selectivity）の実装：B・C・Δを入力依存にすることで、固定パラメータSSMでは表現できなかったコンテキスト依存の記憶・忘却が可能になる。これはRNNのゲーティング機構（LSTMのセルゲート等）と概念的に近いが、連続時間系から離散化するという理論的枠組みが異なる
- 学習時（並列スキャン）と推論時（逐次再帰）で計算グラフを切り替えるデュアルモード設計。同一モデルが学習効率と推論効率を両立できる点は、ハードウェア制約を数学的構造で解決するエレガントな手法
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
