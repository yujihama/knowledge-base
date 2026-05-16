---
title: "Transformerの数式を完全整理：埋め込みからAttentionまで一気に俯瞰"
url: "https://zenn.dev/hitama/articles/c05ff27a852983"
date: 2026-05-08
tags: [Transformer, Attention, Multi-Head Attention, LayerNorm, Positional Encoding, FFN, Encoder, 数式整理]
category: "ai-ml"
related: [2975, 201, 2654, 2381, 4001]
memo: "[Zenn 機械学習] Transformerの数式を完全整理：埋め込みからAttentionまで一気に俯瞰"
processed_at: "2026-05-08T21:16:05.283336"
---

## 要約

本記事はTransformer（Encoder）の全処理を「テンソルのデータフロー」という観点から数式で体系的に整理したものである。4つのレベル（入出力・ブロック構造・サブブロック・演算）に分解して解説する構成をとっている。

最上位レベルの統合式として、1層のEncoderブロックの出力は X^(ℓ) = LN(LN(X^(ℓ-1) + MHA(X^(ℓ-1))) + FFN(LN(X^(ℓ-1) + MHA(X^(ℓ-1))))) で表される。これをL層繰り返すことで最終出力 X^(L) が得られる。

入力処理ブロックでは、トークン列 x = [x1, ..., xT]（各トークンは語彙インデックス）を埋め込み行列 E ∈ R^(V×d_model) で連続ベクトルに変換し、正弦・余弦関数による位置符号化 P を加算して X^(0) = E[x] + P を得る。

AttentionブロックはMHA（Multi-Head Attention）と残差接続・LayerNormで構成される。MHAでは各ヘッドiについて Q_i = X W_i^Q、K_i = X W_i^K、V_i = X W_i^V と線形射影し、head_i = softmax(Q_i K_i^T / √d_k) V_i を計算。h個のヘッドをConcatして出力行列 W^O で変換する。LayerNormは各トークンtの d_model 次元ベクトルに対してトークン内の平均μtと分散σt²を計算し、学習パラメータγ（スケール）とβ（シフト）を用いて正規化する。

FFNブロックはトークンごとに独立に適用される2層MLPで、FFN(x) = max(0, xW1 + b1)W2 + b2 と表される。W1 ∈ R^(d_model×d_ff)、W2 ∈ R^(d_ff×d_model) であり、中間次元d_ffに一旦拡張してReLUで非線形変換した後に元の次元に戻す。

監査エージェント開発への示唆としては、LangGraphで構築するRAGパイプラインや文書理解モジュールの内部動作を正確に把握する上でこの数式的理解が直接役立つ。特にAttentionのQ/K/V射影とLayerNormの挙動を理解することで、RAGの埋め込み検索精度の問題や、LLM-as-judgeにおけるコンテキスト依存性の解析において、モデルの内部表現を論理的に追跡できるようになる。

## アイデア

- Encoder全体を1本の統合数式 X^(ℓ) = LN(LN(X^(ℓ-1)+MHA(...))+FFN(...)) で表現することで、LayerNormが2箇所（Attention後・FFN後）に存在するPost-LN構造が視覚的に明確になる点
- LayerNormがBatchNormと異なり「各トークン内（行方向）でd_model次元にわたって」正規化される点——バッチサイズや系列長に依存しないためTransformerに適合する設計上の理由が数式から直接読み取れる
- FFNが位置ごとに独立に適用される（トークン間の情報混合なし）2層MLPである点——Attentionが「トークン間の関係集約」を担い、FFNが「各トークンの表現再構成」を担うという明確な役割分担が数式で確認できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Self-Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- **LayerNormalization** (TODO: 読むべき)
- **残差接続（Residual Connection）** (TODO: 読むべき)
- **Softmax** → /deep_3691 GSQ：Gumbel-Softmaxサンプリングによる高精度低ビット幅スカラー量子化

## 関連記事

- /deep_2975 正規化フリーTransformerの初期化時における劣臨界信号伝播
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_2654 Multi-Head Attentionはなぜ効くのか？（現代編）— 論文から理解の変遷を整理する
- /deep_2381 Multi-Head Attentionはなぜ効くのか？ — 論文から辿る理解の変遷
- /deep_4001 DepthKV: 層依存KVキャッシュ枝刈りによる長文脈LLM推論の効率化

## 原文リンク

[Transformerの数式を完全整理：埋め込みからAttentionまで一気に俯瞰](https://zenn.dev/hitama/articles/c05ff27a852983)
