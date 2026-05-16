---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-14
tags: [Mamba, SSM, 状態空間モデル, Selective SSM, Transformer代替, 長文脈処理, 線形スケーリング, Parallel Associative Scan, 離散化, ZOH]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5535]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-14T21:36:53.868789"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttentionメカニズムが持つ二次計算量ボトルネックを解消することを目指している。Transformerでは全トークン間のペアワイズ通信が必要なため、訓練時O(n²)、自己回帰推論時O(n)の時間計算量となり、長文脈処理が困難。またKVキャッシュがO(n)空間を占有し、CUDA OOMエラーの原因になる。Mambaはこの問題を制御理論由来のSSMで解決し、シーケンス長に対して線形スケーリングを実現、最大100万トークンの長文脈処理を可能にしつつTransformerと同等もしくは若干上回る性能を達成する。推論速度はTransformerの最大5倍。

技術的核心はh'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)という連続時間微分方程式で表される状態遷移にある。状態hは過去の観測の圧縮表現であり、新しい入力xと組み合わせることで次の出力yを予測する。連続時間方程式はZero-Order Hold（ZOH）離散化によって差分方程式に変換され、コンピュータ上で扱えるようになる。

古典的なSSMはA・B・C・Dが入力に依存しない（線形時不変：LTI）ため、Mambaの前身であるH3やS4は畳み込みとして効率的に計算できたが、「選択性」を持たず、Which情報を記憶するかを動的に制御できなかった。Mambaの革新はここにあり、B・C・∆を入力xに依存させる「Selective SSM（S6）」を導入した。これにより文脈に応じて重要な情報を選択的に記憶・忘却できる。

ただしこの選択性が離散畳み込みカーネルによる並列計算を不可能にするため、代わりにParallel Associative Scanを用いる。訓練時は全入力を並列処理し、推論時は逐次的に実行することで効率的な推論を実現。さらにFlashAttentionに相当するHardware-Aware Scanアルゴリズムを実装し、HBMとSRAM間のデータ転送を最適化している。

Mamba-3Bは同サイズのTransformerを超え、2倍サイズのTransformerに匹敵する性能をThe Pileで達成。言語・音声・ゲノムなど複数のモダリティで最先端を記録。解釈可能性の観点では、AttentionのAttribution Patternsに相当する分析手法が未確立であり、Mechanistic Interpretabilityの課題が残る。監査エージェント開発への示唆として、長文脈の契約書・規制文書・取引ログをメモリ効率よく処理できる点が注目に値する。

## アイデア

- 選択的状態空間モデル（S6）は入力に応じてB・C・∆を動的に変化させることで、RNNのような逐次記憶とAttentionのような選択的情報取得を両立している点が根本的に新しい
- 訓練時は並列スキャン、推論時は逐次RNNとして動作するデュアルモード設計により、TransformerのO(n²)訓練とRNNのO(1)推論の両利点を組み合わせている
- 状態hを「過去の圧縮」と定義することでマルコフ決定過程に帰着させる思想は、監査エージェントが取引履歴や内部統制の状態を固定サイズベクトルで追跡するアーキテクチャ設計に直接応用できる

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **畳み込みニューラルネット (CNN)** (TODO: 読むべき)
- **状態空間モデル (SSM)** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5535 GEM: 変形可能Mambaによるリダールワールドモデル生成

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
