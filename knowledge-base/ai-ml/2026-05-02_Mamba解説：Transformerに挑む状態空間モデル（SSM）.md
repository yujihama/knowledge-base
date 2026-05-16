---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-02
tags: [Mamba, SSM, State Space Model, Transformer, 線形スケーリング, 選択的状態空間, 長コンテキスト, S4, Zero-Order Hold, 並列スキャン]
category: "ai-ml"
related: [3105, 222, 2480, 2510, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-02T12:19:05.610964"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時O(n²)の計算量とO(n)のKVキャッシュメモリが必要となるが、MambaはSSMを用いて線形スケーリングを実現する。

Mambaの数理的基盤は制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) にある。これを離散化（Zero-Order Hold法）することでシーケンス処理に適用可能にし、h_t = Ā·h_{t-1} + B̄·x_t、y_t = C·h_t という差分方程式を得る。「状態」は過去の情報の圧縮表現であり、マルコフ的性質を持つ。

従来のSSM（S4等）との最大の差異は「選択的状態空間モデル（Selective SSM / S6）」にある。S4ではパラメータA・B・Cが入力に依存しない固定値であるため、どのトークンも等しく記憶・忘却される。MambaではB・C・Δ（ステップサイズ）を入力x_tの関数として動的に変化させ、関連トークンを選択的に保持・無視できる。これはTransformerのアテンションが入力依存的にトークン間の重みを変えることと機能的に対応する。

ハードウェア実装面では「ハードウェアアウェア並列スキャン」を採用。ConvモードとRecurrentモードを切り替え可能で、トレーニング時はFFT畳み込みで並列化、推論時はRNNのように逐次処理することでバッチサイズ1での低レイテンシ生成を実現する。Mamba-3BモデルはPileデータセットでの事前学習・下流評価で同サイズのTransformerを上回り、自身の2倍サイズのTransformerと同等の性能を示し、推論速度はTransformerの最大5倍とされる。

Mambaブロック構造はSelective SSM・線形投影・SiLU活性化・乗算ゲートで構成され、TransformerのAttentionをSSMで、MLPを保持する形でブロックを積層する。解釈可能性の観点では、固定圧縮状態を持つためCircuit分析がTransformerより困難になる可能性がある一方、状態サイズの制約が情報圧縮の強制により解釈しやすい潜在表現を生む可能性もある。監査エージェントへの応用としては、長大な監査ログ・取引履歴・内部統制文書などの超長コンテキスト処理において、Transformerの二次計算量制約なしに100万トークン規模のシーケンスを扱える点が直接的な優位性となる。

## アイデア

- 選択的状態空間（S6）における入力依存パラメータ（B, C, Δ）の動的変化が、Transformerのソフトアテンションと機能的に等価な「選択的記憶・忘却」を実現している点——アーキテクチャが全く異なりながら同等の表現力を持つことの示唆
- トレーニング時（並列Convモード）と推論時（逐次Recurrentモード）で計算グラフを切り替えるハードウェアアウェア設計——同一の数学的定式化から2つの計算モードを導出する実装戦略
- 状態が「過去の圧縮」であるというSSMの原理が、固定サイズのボトルネックを持つことで情報の選別を強制する——これは無制限に過去を参照できるTransformerとは本質的に異なる帰納バイアスであり、長期依存性の学習特性に影響する

## 前提知識

- **Transformer・Attention機構** (TODO: 読むべき)
- **RNN・隠れ状態** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **離散化・差分方程式** (TODO: 読むべき)
- **並列スキャン** → /deep_672 Mambaの解説：Transformerに挑む状態空間モデル

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
