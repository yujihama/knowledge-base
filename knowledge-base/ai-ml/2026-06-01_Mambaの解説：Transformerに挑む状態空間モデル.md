---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-01
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 選択的SSM, 線形スケーリング, 長コンテキスト, Hardware-Aware]
category: "ai-ml"
related: [2510, 222, 2480, 1837, 3105]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-01T21:34:22.262832"
---

## 要約

MambaはAlbert GuとTri Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを解消する。Transformerではすべてのトークンが過去の全トークンを参照するKVキャッシュが必要で、訓練時O(n²)・推論時O(n)の計算量と大量メモリを要する。Mambaはこれをコントロール理論由来のSSMで置き換え、線形スケーリングを実現する。

SSMの数学的基盤は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去情報の圧縮として機能する。離散化にはZero-Order Hold（ZOH）法を採用し、実際のトークン列に適用可能な差分方程式に変換する。

Mambaが従来のSSM（S4等）と異なる最大の特徴は「選択的状態空間（Selective SSM）」の導入で、行列A・B・CをΔ（タイムステップ）を介して入力依存にする点である。これにより「何を記憶し何を忘れるか」を動的に制御できる。タイムステップΔが大きいと入力を強く取り込み、小さいと無視する挙動は、LSTMのゲートに類似する。

ハードウェア効率のためにHardware-Aware Parallel Scanアルゴリズムを採用。並列プレフィックススキャンを使い、GPU SRAMのみで計算することでHBMへのデータ転送を最小化する。推論はリカレント計算（O(1)メモリ）、訓練は畳み込み表現を利用した並列計算の両方が可能。

Mamba-3Bは同サイズのTransformerを凌駕し、2倍サイズのTransformerと同等性能を達成。推論速度はTransformerの最大5倍高速で、100万トークンまでのコンテキストでも性能が向上し続ける。言語・音声・ゲノミクスなど複数モダリティでSoTAを達成。

解釈可能性の観点では、SSMの隠れ状態はTransformerのアテンションヘッドほど直接解釈しにくい課題がある。また選択機構の導入により厳密な畳み込み表現が成立しないため、訓練時も特殊な並列化手法が必要。監査エージェント開発への示唆として、長大な監査ログや取引履歴のシーケンス処理に対し、Mambaの線形スケーリングはTransformerより大幅にコスト効率が高い可能性がある。

## アイデア

- 選択的SSM（Selective SSM）により行列B・C・ΔをトークンごとにLearningすることで、LSTMのゲートに相当する動的な記憶・忘却制御を実現している点が核心的なイノベーション
- 訓練時は畳み込み（並列）・推論時はリカレント（定数メモリ）という二重表現の切り替えが、同一パラメータで両立できる構造的な美しさ
- 隠れ状態の次元数（通常16程度）が情報ボトルネックとなるため、状態サイズの設計がモデル容量とメモリトレードオフの主要パラメータになるという設計上の制約

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **ZOH離散化** → /deep_170 Mambaの解説：Transformerに挑む状態空間モデル
- **並列プレフィックススキャン** → /deep_881 Hawkesプロセスの大規模並列厳密推論

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
