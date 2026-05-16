---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-16
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, 線形スケーリング, Selective SSM, 離散化, ZOH, Hardware-aware]
category: "ai-ml"
related: [1975, 1837, 199, 222, 833]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-16T12:37:25.252315"
---

## 要約

MambaはAlbert GuとTri Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量のボトルネックを解消することを目的としている。Transformerはトークン間の全対全通信（KVキャッシュ）によりO(n²)の時間計算量とO(n)の空間計算量を必要とするが、Mambaは連続時間微分方程式 h'(t) = Ah(t) + Bx(t) に基づく隠れ状態の圧縮表現を用いることで、系列長に対して線形スケーリングを実現する。Temple Runの例えで直感的に示されているように、状態hは過去の観測を圧縮した表現であり、新しい観測x(t)と組み合わせて次の出力y(t) = Ch(t) + Dx(t)を予測する。連続時間の微分方程式を離散化（Zero-Order Hold法）することでトークン列への適用が可能になる。SSMはCNN（並列畳み込み）としてもRNN（逐次的状態更新）としても計算でき、訓練時は並列計算、推論時は逐次計算を使い分けることで高効率を達成する。重要な革新はSelective SSM（S6）と呼ばれる入力依存的なパラメータB・C・Δの動的変化で、これにより従来のSSMが苦手とした「入力の選択的記憶と忘却」が可能になった。ハードウェア面ではFlashAttentionに類似したHardware-aware Parallel Scanを採用し、HBMとSRAM間のメモリ転送を最適化することでGPU上での高速計算を実現している。Mamba-3Bは同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能を示し、推論速度はTransformerの最大5倍。100万トークン超の長文脈処理も実用的な速度で対応できる。ただし、アテンション機構を持たないため「正確な文字列コピー」「文脈内学習（in-context learning）」はTransformerより苦手であることも示されており、Mambaが過去の圧縮（lossy compression）に依存する設計上の限界として指摘されている。解釈可能性や安全性の観点からは、残留ストリームなどのTransformerの特性が失われるため、既存の解釈ツールが適用しにくいという課題も残る。

## アイデア

- 選択的状態空間モデル（S6）のB・C・Δを入力依存にすることで、RNNの固定遷移行列という弱点を克服しつつ、線形計算量を維持するという設計の巧みさ
- 同一モデルを訓練時はCNN（並列畳み込み）、推論時はRNN（逐次更新）として動作させるデュアルモード設計は、監査エージェントのように長い会話履歴を逐次処理しながら高速推論が必要なユースケースに直接応用できる
- 状態hを「過去の圧縮」と定義する設計思想はRAGや外部メモリ設計と対比的で、何をコンテキストに保持し何を捨てるかというエージェント設計の根本問題に新しい視点を与える

## 前提知識

- **Transformer・アテンション機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **離散化・Zero-Order Hold** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
