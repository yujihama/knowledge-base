---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-18
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, 選択的状態空間, S4, 並列スキャン, 長文脈]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-18T09:17:41.007347"
---

## 要約

Mambaは、Gu and Dao（2023）が提案した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttention機構が抱える二次計算量（O(n²)）の問題を解消することを目的としている。Transformerでは全トークン間のペアワイズAttentionによりKVキャッシュがO(n)のメモリを要し、長文脈では速度・メモリ双方がボトルネックになる。MambaはこれをSSMで置き換えることでシーケンス長に対して線形スケーリング（O(n)）を実現し、推論速度はTransformer比最大5倍を達成する。

SSMの数学的基盤は制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の情報を圧縮する「状態」として機能する。連続時間式はZero-Order Hold（ZOH）離散化によって離散差分方程式に変換され、実際のシーケンスデータに適用可能になる。

Mambaの最大の革新点は「選択的状態空間モデル（S6）」と呼ばれる入力依存パラメータ化にある。従来のS4等のSSMではA・B・Cが入力に依存しない固定パラメータだったため、全トークンに均等に注意を払う構造だった。MambaはB・C・∆を入力xの関数とすることで、関連情報を選択的に記憶・忘却できる。これはRNNのゲーティング機構（LSTMのforget gate等）と概念的に近いが、SSMの並列計算可能な構造を維持している。

ハードウェア最適化として、Mambaは「並列スキャン」アルゴリズムと「カーネル融合」によりGPUのSRAM（高速）を最大限活用し、低速なHBM（メインGPUメモリ）へのアクセスを最小化する。これによりFlashAttentionと同様のIO-awareな実装を実現している。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を事前学習・下流評価の双方で達成した（The Pile評価）。言語のみならず音声・ゲノミクスでもSOTA級の性能を示す。

一方で課題も存在する。固定サイズの隠れ状態への圧縮はin-context learningや検索タスク（特定トークンの正確な参照）でTransformerに劣る場合がある。また解釈可能性研究はまだ初期段階で、CircuitsやInduction Heads相当の知見は未整備。監査エージェントへの示唆としては、長文書（監査調書・財務報告書）の処理で線形スケーリングの恩恵が大きく、ローカルLLMインフラ（RTX 3090等）での長文脈推論コスト削減に直結する可能性がある。

## アイデア

- 入力依存パラメータ化（選択的SSM）によりRNNの逐次性を保ちながら並列学習を可能にした点：LSTMのゲーティングとSSMの畳み込み表現を統合した設計は、長文書を扱う監査エージェントのバックボーンアーキテクチャ候補として有望
- 隠れ状態が「過去の圧縮」として機能するという概念：Transformerの完全な過去参照とのトレードオフを理解することで、in-context learning依存のRAGアーキテクチャとMamba型ストリーミング処理の使い分け判断基準になる
- ZOH離散化とカーネル融合によるIO-aware実装：FlashAttentionと同じ設計思想（HBMアクセス最小化）をSSMに適用しており、ローカルGPU環境でのメモリ効率最大化の具体的手法として参照価値が高い

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **S4（構造化状態空間モデル）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **離散化（ZOH）** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
