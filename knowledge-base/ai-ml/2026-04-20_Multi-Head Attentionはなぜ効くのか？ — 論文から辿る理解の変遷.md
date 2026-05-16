---
title: "Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷"
url: "https://zenn.dev/hitama/articles/62565e5a749789"
date: 2026-04-20
tags: [Multi-Head Attention, Transformer, Self-Attention, BERT, アーキテクチャ解釈, 過パラメータ化, 論文調査, 自然言語処理]
category: "ai-ml"
related: [201, 585, 518, 1664, 1759]
memo: "[Zenn 機械学習] 【Transformerとは？ - 第七回(番外編)】Multi-Head はなぜ効くのか？ ~論文から理解の変遷を整理する~"
processed_at: "2026-04-20T12:01:03.514102"
---

## 要約

本記事はTransformerのMulti-Head Attention（MHA）に対する理解が、原論文（2017年）から現代（2022年以降）にかけてどのように変遷してきたかを、5つのフェーズに沿って整理したものである。

①誕生期（2017年）：「Attention Is All You Need」では「we found it beneficial」という表現が示す通り、MHAは理論的必然性よりも実験的有効性から導入された。Q・K・Vをh回射影して並列にAttentionを計算し結合するという構造のみが提示された。

②解釈期（2018〜2019前半）：「What Does BERT Look at?」（Clark et al., 2019）はBERTのAttention重みを可視化し、特定のheadが限定詞（det）・目的語（dobj）など特定の構文依存関係に特化する傾向を観察した。ただし「no single head performs well at many relations」とも述べており、知識は複数headに分散していることが示された。

③批判期（2019後半）：「Analyzing Multi-Head Self-Attention」（Voita et al., 2019）はLRP（Layer-wise Relevance Propagation）で重要度を評価し、48head中38headを削除してもBLUEスコアの低下が0.15程度に留まることを示した。「Are Sixteen Heads Really Better than One?」（Michel et al., 2019）も同様に、大多数のheadが冗長であることを確認。役割分担仮説は実証的に崩された。

④再理論化期（2020〜2021）：「On the Expressive Power of Self-Attention」などはカーネル近似や表現力の観点からMHAを再定式化。MHAは「意味の役割分担」ではなく、過パラメータ化（over-parameterization）によって学習を安定させる構造として再解釈された。

⑤現代（2022〜）：スケーリング則（Scaling Laws for Neural Language Models）の文脈では、head数はモデル規模・計算量の最適化パラメータとして扱われ、役割論よりも過パラメータ化・最適化の枠組みが支配的になっている。

結論として、MHAは「意味を分担する仕組み」ではなく、過パラメータ化によって学習を安定させる構造として理解されつつある。監査エージェント開発の観点では、Transformerベースの特徴抽出器においてhead数の設計はアーキテクチャ選択の問題ではなく計算効率の問題として捉えるべきことを示唆する。

## アイデア

- MHAの「役割分担」仮説は可視化研究（②）で広まったが、削除実験（③）で崩された——解釈可能性研究の結論が後続の定量実験で覆される典型例
- 48head中38head削除でBLUE低下0.15という結果は、実運用上headの大幅削減によるモデル軽量化の余地を示唆する
- 過パラメータ化による学習安定化という再理論化は、LLMのスケーリング則と接続しており、head数を「表現力」ではなく「最適化ランドスケープの滑らか化」として捉える視点を提供する

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **Self-Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- **QKV Attention** (TODO: 読むべき)
- **BERT** → /deep_117 DariMis: YouTubeにおけるダリ語偽情報検出のためのハーム認識モデリング
- **スケーリング則** → /deep_164 ATLAS: 多言語モデルのための実用的スケーリング則

## 関連記事

- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_518 TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化
- /deep_1664 GraphcoreとHugging FaceがIPU対応Transformerモデル群を大幅拡充
- /deep_1759 BERT 101：最先端NLPモデルの仕組みを解説

## 原文リンク

[Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷](https://zenn.dev/hitama/articles/62565e5a749789)
