---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-12
tags: [Mamba, SSM, State Space Model, Transformer, 長コンテキスト, 選択的SSM, 線形スケーリング, HiPPO, 離散化, ZOH]
category: "ai-ml"
related: [3105, 222, 2480, 2510, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-12T21:18:37.187217"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、Transformerの二次計算量ボトルネックを解消することを目的としている。Transformerはアテンション機構によりトークン間通信をO(n²)の時間・O(n)の空間で行うため、コンテキスト長が増加するにつれて推論速度が低下し、KVキャッシュのメモリ消費も増大する。これに対しMambaは線形スケーリングを実現し、最大100万トークンの長コンテキストを扱える。

基本的な数式はControl Theory由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の圧縮表現として機能する。実装では離散化（Zero-Order Hold法）により差分方程式 h_t = Ā h_{t-1} + B̄ x_t、y_t = C h_t に変換される。

Mambaの最大の革新はSelective State Spaces（選択的SSM）にある。従来のSSMはA・B・Cが入力に依存しない線形時不変（LTI）システムだったため、どの情報を状態に保持するかを動的に制御できなかった。MambaではB・C・∆（ステップサイズ）を入力x_tの関数とすることで、トークンごとに「何を記憶し何を忘れるか」を適応的に決定できる。∆が大きいとき（離散ステップが長い）は入力を重視して状態を大幅更新し、小さいときは入力を無視して状態を維持する動作はLSTMのゲート機構と概念的に対応する。

ただしこの選択性によってA・Bが時変となり、並列プレフィックスサンドを用いた並列スキャンで計算できるものの、畳み込みとして効率的に計算できなくなる。この問題をHardware-Aware Parallel Algorithmで解決し、GPUのHBMとSRAM間のデータ転送を最小化することで、同サイズのTransformerより最大5倍の推論高速化を達成している。Mamba-3Bは同パラメータのTransformerと同等以上の性能を示し、2倍サイズのTransformerにも匹敵するとされる。

解釈性の観点では、Mambaの隠れ状態はTransformerのKVキャッシュより情報量が少なく固定サイズであり、In-Context Learning能力はあるものの、隠れ状態に何が格納されているかの解釈は困難とされる。監査エージェント開発への示唆として、長期のログシーケンスや監査証跡を低コストで処理できる可能性があるが、透明性・説明可能性が求められる監査文脈ではブラックボックス性が課題となる。

## アイデア

- 選択的SSMにおける∆パラメータの大小がLSTMのゲート開閉と対応するという直感は、RNN・LSTM・SSMの系譜を統一的に理解する鍵になる
- 隠れ状態は『過去の圧縮』であり固定サイズである点は、無限に伸びるKVキャッシュと対照的で、メモリ制約環境（エッジデバイス・長期対話ボット）での実用性に直結する
- Hardware-Aware Parallel Algorithmによる『カーネルフュージョン＋再計算』戦略は、FlashAttentionと同様に数学的等価性を保ちつつGPUのメモリ階層を意識した最適化で、アーキテクチャ設計とハードウェア設計の共同最適化の重要性を示す

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Self-Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- **RNN/LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **HiPPO行列** → /deep_3633 Mamba解説：Transformerに挑む状態空間モデル

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
