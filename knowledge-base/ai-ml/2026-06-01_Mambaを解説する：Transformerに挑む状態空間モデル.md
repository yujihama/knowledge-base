---
title: "Mambaを解説する：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-01
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, 選択的SSM, 並列スキャン, 線形計算量]
category: "ai-ml"
related: [2510, 3105, 2480, 1975, 1837]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-01T09:23:20.135685"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを解消することを目的としている。Transformerではトークン間の通信にAttentionを使うため、学習時はO(n²)の時間計算量、KVキャッシュによるO(n)の空間計算量が必要となり、長いコンテキスト（例：100万トークン）では実用的でない。MambaはAttentionの代わりに制御理論由来のSSMを採用し、連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で状態遷移を表現する。連続時間をゼロ次ホールド（ZOH）法で離散化し、実際のシーケンスデータに適用可能にしている。従来のSSM（S4等）との最大の違いは「選択的状態空間（Selective SSM）」であり、行列B・C・ステップサイズΔを入力xに応じて動的に変化させる。これによりモデルは関連する情報を選択的にフィルタリングし、不要な情報を忘却できる。計算上の課題として、選択機構の導入によりSSMのカーネルが時変となり、畳み込みによる高速並列計算が使えなくなる問題が生じる。これをHardware-Aware Parallel Scan（並列スキャン）で解決し、中間状態をHBMに保存せずSRAMで処理するFlashAttention的な最適化を行っている。結果として推論時はO(n)の線形スケーリングを実現し、Transformerより最大5倍高速。Mamba-3Bモデルは同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能をThe Pileベンチマークで示した。言語・音声・ゲノミクスなど複数モダリティでSoTAを達成。一方でAttentionのような完全な過去参照ができないため、in-context learningやファインチューニングの挙動が異なる可能性があり、解釈可能性研究での既存手法（Activation Patching等）の適用が困難になるという課題もある。監査エージェント開発への示唆としては、長大なログや証跡データを線形計算量で処理できる点が重要で、RAGなしに長期的な監査証跡を状態として保持するエージェントバックボーンとして有望な候補となりうる。

## アイデア

- 「状態は過去の圧縮」という概念が核心：MambaのSSMは全過去トークンをO(1)サイズの隠れ状態に圧縮することで線形スケーリングを実現しており、この設計思想はメモリ制約のあるエッジ推論やリアルタイム処理に直結する
- 選択機構（Selective SSM）がRNNとSSMの質的な違いを生む：B・C・Δを入力依存にすることで、従来の固定カーネルSSMでは不可能だった「どの情報を記憶するか」の動的制御が可能になり、実質的にアテンションの「何に注目するか」と類似した機能を実現
- Hardware-Aware設計がアルゴリズムとシステムを不可分にした：SRAMを積極活用する並列スキャンはGPUアーキテクチャの物理的制約に合わせたアルゴリズム設計であり、FlashAttentionと同様に「ハードウェアを意識したML研究」の新しい方向性を示している

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **離散化（ゼロ次ホールド）** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ

## 原文リンク

[Mambaを解説する：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
