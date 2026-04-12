---
title: "Mambaとは何か：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-04
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈処理, 線形スケーリング, 選択的状態空間, ZOH離散化, FlashAttention, RNN]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [201, 199, 222, 833, 221]
processed_at: "2026-04-04T21:07:51.510280"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのquadratic bottleneckを解消することを目的としている。Transformerは全トークン間のAttentionによりトレーニング時O(n²)・推論時O(n)の計算量およびO(n)のKVキャッシュメモリを要するが、Mambaは線形スケーリング（O(n)）で動作し、最大100万トークンの長文脈を実用的に扱える。推論速度はTransformerの最大5倍。

Mambaの核心はSSMの離散化と選択的状態更新（Selective State Space Model）にある。連続時間の状態方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) をZero-Order Hold（ZOH）法で離散化し、h_t = Ā·h_{t-1} + B̄·x_t という差分方程式として実装する。従来のSSM（S4など）はA・B・Cを入力に依存しない定数としていたため「入力選択性」がなかったが、MambaはこれらをInputに依存するパラメータとし、モデルが「どの過去情報を記憶・忘却するか」を動的に制御できる。

この選択機構はRNNの逐次処理（推論は高速だが並列学習不可）とTransformerの並列学習（学習は高速だが推論がO(n)）の両立を目指している。Mambaはトレーニング時はconvolution形式（並列計算可能）、推論時はrecurrence形式（定数メモリ）に切り替えるhardware-aware algorithmを採用。FlashAttentionに類似したGPUメモリ階層の最適化により、HBM（高帯域メモリ）とSRAM（高速オンチップメモリ）間の転送を最小化する。

性能面ではMamba-3Bが同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する結果を示す（The Pile評価）。言語・音声・ゲノミクスなど複数モダリティでstate-of-the-artを達成。欠点としては、圧縮された隠れ状態に全過去を詰め込む構造上、「特定の過去トークンを正確に想起する」タスク（Transformer得意領域）では劣ることがある。解釈可能性の観点では、Attentionヘッドのような直接的な解釈ツールが未整備であり、Mechanistic Interpretabilityの研究が今後の課題。

## アイデア

- 選択的状態更新（A・B・CをInput依存にする）というアイデアは、エージェントの「記憶管理」設計に応用できる。関連情報だけを動的に状態に保持し、無関係な情報を忘却するメカニズムをLangGraphのノード設計に組み込む発想と対応する
- トレーニング時はconvolution（並列）・推論時はrecurrence（定数メモリ）に切り替えるdual-mode実装は、バッチ学習と逐次推論の要件が異なるシステム設計の参考になる
- Mambaの「状態は過去の圧縮」という概念は、RAGシステムにおける検索粒度の設計に示唆を与える。全コンテキストを保持するRAGとMambaの圧縮状態の組み合わせで、長期記憶と正確な検索を相補的に実現できる可能性がある
## 関連記事

- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 原文リンク

[Mambaとは何か：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
