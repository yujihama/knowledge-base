---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-01
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, 選択的スキャン, 長文脈処理, Hardware-Aware Algorithm]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-01T12:39:43.252122"
---

## 要約

Mambaは、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消するために設計された状態空間モデル（SSM）ベースのアーキテクチャ。著者はAlbert GuとTri Dao。Transformerではトークン間のAttentionがO(n²)の時間計算量を要し、KVキャッシュもO(n)のメモリを消費するため、長文脈（例：100万トークン）では速度・メモリの両面でスケールが困難になる。Mambaはこの問題をコントロール理論由来のSSMで代替することで、系列長に対して線形スケーリングを実現し、Transformerと同等以上の性能を達成する。

SSMの基本は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、隠れ状態hが過去の情報を圧縮・保持する。実装上は連続時間をZero-Order Hold（ZOH）離散化で差分方程式に変換し、h_{t+1} = Āh_t + B̄x_tとして扱う。これはRNNに構造的に似ており、推論時はO(1)の状態更新で自己回帰生成が可能。訓練時は畳み込み（コンボリューション）として並列計算可能な二重表現を持つ点が重要な特徴。

従来のSSM（S4等）との最大の違いは「選択的状態空間」の導入。S4ではA, B, Cが入力に依存しない固定パラメータだったが、Mambaでは入力x_tに応じてB, C, Δを動的に変化させるSelection Mechanismを採用。これにより「何を記憶し何を忘れるか」を入力に応じて制御できるようになる。ただし、この選択性によって訓練時の畳み込み的並列計算が使えなくなるため、Hardware-Aware Algorithmとして選択的スキャン（selective scan）と、SRAM/HBM間のデータ転送を最小化するカーネル融合を組み合わせた実装で高速化を実現している。

Mamba-3BモデルはThe Pileベンチマークで同パラメータ数のTransformerを上回り、2倍サイズのTransformerとも同等の性能を発揮。推論速度はTransformerと比較して最大5倍高速。スケーリング則もTransformerと同様に成立することが示されている。一方で弱点もあり、固定サイズの隠れ状態による情報圧縮の制約（Transformerのような厳密な過去参照が不可）や、回顧的な情報検索タスクへの対応が課題として挙げられる。解釈可能性の観点では、Transformerの注意重みのような直接的な可視化ツールが未整備であり、AIセーフティ研究上の課題として残る。監査エージェント開発への示唆としては、長大なログや監査証跡を低コストで処理できる可能性があり、100万トークンスケールの文書処理への応用が期待される。

## アイデア

- SSMの隠れ状態は「過去の圧縮」として機能するが、固定サイズのため情報損失が生じる——これはRNNの消えた勾配問題と本質的に同じトレードオフであり、何を圧縮し何を捨てるかの選択がモデルの表現力を決定する
- Selection Mechanism（B, C, Δを入力依存にする）により畳み込み的並列計算が失われるという矛盾を、SRAMへのカーネル融合でハードウェアレベルで解決している点——アルゴリズムの数学的性質とハードウェア特性を同時に設計する思想はFlashAttentionと共通
- 訓練時は畳み込み、推論時はRNNとして振る舞う二重表現——同一モデルが計算グラフの形を変えて動作するこの構造は、長期記憶が必要な監査エージェントの推論ループ設計（ステートフルvs並列バッチ処理）に示唆を与える

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **畳み込みニューラルネット** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **状態空間モデル（S4）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
