---
title: "長い時系列予測における効率的なTransformer：LogTrans・Informer・Reformer・Pyraformerの比較整理"
url: "https://zenn.dev/yuyu1/articles/a7160c5c5f5241"
date: 2026-05-22
tags: [Transformer, 時系列予測, Sparse Attention, LogTrans, Informer, Reformer, Pyraformer, LSH, ProbSparse, 効率化]
category: "ai-ml"
related: [1979, 1494, 113, 5502, 2598]
memo: "[Zenn 機械学習] 長い時系列予測における効率的な Transformer：LogTrans、Informer、Reformer、Pyraformer の比較整"
processed_at: "2026-05-22T09:10:55.583142"
---

## 要約

標準的なTransformerのSelf-AttentionはO(L²)の計算量・メモリを必要とするため、数百〜数千点の長い時系列データへの適用が困難になる。この問題に対して提案された4つの効率化手法を比較する。

**LogTrans**（Enhancing the Locality and Breaking the Memory Bottleneck of Transformer on Time Series Forecasting）は2つの工夫を組み合わせる。Causal Convolutionをquery/key生成に使い局所パターンを捉え、LogSparse Attentionで参照する過去時点を「t-1, t-2, t-4, t-8, ...」と対数間隔に絞ることで計算量を削減する。近い過去は細かく、遠い過去は粗く見るという設計だが、参照位置はルールベースであり全データに最適とは限らない。

**Informer**（Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting）は3要素から構成される。ProbSparse Attentionでは、attention分布が一箇所に集中するqueryを「重要」と判定し、そのqueryだけにfull attentionを計算する。Self-Attention Distillingでencoder内の系列長を96→48→24→12と段階的に圧縮し、Generative Style Decoderで将来系列t+1〜t+Hを一括出力することで誤差蓄積も抑える。ただし「重要queryは少数」という前提がデータによっては成立しない。

**Reformer**（Reformer: The Efficient Transformer）は時系列専用ではなく汎用の効率化Transformerであり、比較対象として参照される。LSH（Locality-Sensitive Hashing）で類似ベクトルを同一bucketに振り分け、bucket内のみでattentionを計算する。加えてReversible Residual Layersにより学習時の中間結果を保存せず後から復元可能にすることでメモリ削減を実現するが、時系列特有の局所性・周期性・多尺度性は明示的に考慮しない。

**Pyraformer**（Pyraformer: Low-Complexity Pyramidal Attention for Long-Range Time Series Modeling and Forecasting）は時系列の多尺度構造を最も強く意識する。Pyramidal Attention Module（PAM）によってデータをピラミッド構造に組織化し、Inter-scale connections（異スケール間の粗粒化）とIntra-scale neighboring connections（同スケール内の近傍接続）を組み合わせる。x1→局所ノード→中間ノード→全体ノード→x1000という経路で遠距離依存を間接的に捉えるため、full attentionなしで長期依存を扱える。実装コストは最も高い。

時系列構造への特化度はPyraformer > LogTrans > Informer > Reformerの順。監査AI開発においては、財務データや取引ログのような長い時系列のアノマリ検知に、これらのスパースattention設計を応用できる可能性がある。

## アイデア

- LogSparseの「近い過去は密に、遠い過去は対数間隔で」という設計は人間の記憶の減衰モデルと類似しており、監査ログのタイムスタンプ重み付けに応用できる
- ProbSparse Attentionの「attention分布のエントロピーで重要queryを選ぶ」という発想は、エージェントが取得した情報の重要度スコアリングに転用できる
- Pyraformerのピラミッド構造は時系列の多粒度（時・日・週・季節）を明示的に扱えるため、財務データの異常検知で短期スパイクと長期トレンドを同時にモデル化するのに適している

## 前提知識

- **Transformer Self-Attention** (TODO: 読むべき)
- **時系列予測** → /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- **Locality-Sensitive Hashing** (TODO: 読むべき)
- **Sparse Attention** → /deep_3789 DeepSeek V4が重要な3つの理由：オープンソース・長コンテキスト・国産チップ対応
- **Encoder-Decoder構造** (TODO: 読むべき)

## 関連記事

- /deep_1979 Reformer：言語モデリングの限界を押し広げる長文処理Transformer
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_5502 データセンターのSLAコンプライアンス監視のためのマルチヘッドアテンション手法
- /deep_2598 ウェアラブルセンサーデータから介入後の生理的反応を予測するパーソナライズ・コンテキスト対応Transformerモデル

## 原文リンク

[長い時系列予測における効率的なTransformer：LogTrans・Informer・Reformer・Pyraformerの比較整理](https://zenn.dev/yuyu1/articles/a7160c5c5f5241)
