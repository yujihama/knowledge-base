---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-16
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, Selective SSM, S4, ZOH離散化, HardwareAwareParallelScan, 長文脈処理]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5535]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-16T09:25:46.538407"
---

## 要約

Mambaは、Transformerの二次計算量ボトルネックを克服する代替アーキテクチャとして、Gu・Dao両氏が開発した状態空間モデル（SSM）ベースのシーケンスモデルである。Transformerのアテンション機構は全トークン間のペアワイズ通信を行うため、訓練時にO(n²)の時間計算量、推論時にO(n)の時間計算量、KVキャッシュにO(n)の空間計算量を要する。これにより、コンテキスト長が伸びるほど速度・メモリ両面で劣化する。Mambaはこの問題を制御理論由来のSSMで代替することで、シーケンス長に対して線形スケーリングを実現し、Transformerと比較して最大5倍の推論速度を達成する。数学的基盤として、連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表されるSSMを、Zero-Order Hold（ZOH）離散化により差分方程式へ変換する。これにより、過去の全履歴を記録する代わりに、固定サイズの隠れ状態hへ過去を圧縮する。Mambaの最大の革新はSelective State Space（S6）機構にある。古典的なS4ではA/B/C/Dが入力に依存しない固定パラメータであるため、「選択的な記憶」ができなかった。MambaではB・C・Δを入力xに依存させることで、どの情報を隠れ状態に残すかを動的に制御する。ただし、この入力依存性により並列スキャンによる高速畳み込みが使えなくなる問題が生じる。これをHardware-Aware Parallel Scanアルゴリズムで解決し、GPUのSRAM（高速）とHBM（低速）の階層を意識した再計算戦略で効率化している。アーキテクチャとしては、ExpandしたxをSSMと乗算ゲートの二経路に分岐し、最終的にProjectionで出力するMambaブロックを積み重ねる。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵するスコアをThe Pile評価で示した。解釈可能性の観点では、固定隠れ状態への圧縮により記憶容量に上限があるため、Transformerのアテンションパターンのような直接的な分析手法が適用できず、Mechanistic Interpretabilityの研究は発展途上である。監査エージェント開発への示唆として、百万トークン超の長文書（監査報告書、内部統制文書の全文）を単一コンテキストで処理できる可能性があり、KVキャッシュ起因のOOMエラーなしにLangGraphエージェントのメモリ効率を改善できる点が注目に値する。

## アイデア

- 隠れ状態への圧縮が『過去の情報を選択的に忘れる』能力を持つため、Transformerの全トークン参照より計算効率が高いが、その代償として固定サイズの記憶容量制限という根本的なトレードオフが存在する
- B・C・Δを入力依存にするSelective機構が、RNNの並列化不可という弱点を持ち込む問題を、GPUのSRAM/HBM階層を意識した再計算アルゴリズムで回避している点は、ハードウェア制約を逆手に取るアーキテクチャ設計の好例
- 百万トークン規模の長文コンテキストが現実的になることで、監査証跡全体や大規模契約書群をRAGなしに単一パスで処理するエージェント設計が可能になり、チャンキングや検索誤りによる情報損失リスクを排除できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **アテンション機構** → /deep_241 任意地点における時空間地下水位予測のための純粋および物理ガイド深層学習手法
- **RNN/LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5535 GEM: 変形可能Mambaによるリダールワールドモデル生成

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
