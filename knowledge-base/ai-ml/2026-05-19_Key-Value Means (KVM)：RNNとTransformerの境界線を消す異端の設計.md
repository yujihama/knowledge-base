---
title: "Key-Value Means (KVM)：RNNとTransformerの境界線を消す異端の設計"
url: "https://zenn.dev/openmose/articles/93ee355984ca11"
date: 2026-05-19
tags: [KVM, Linear RNN, Transformer, RWKV-7, K-means, attention mechanism, sublinear state, JIT normalization, RoPE, attention sink]
category: "ai-ml"
related: [4121, 3788, 585, 3917, 753]
memo: "[Zenn LLM] Key-Value Means (KVM)：RNNとTransformerの境界線を消す異端の設計"
processed_at: "2026-05-19T09:05:48.202587"
---

## 要約

2026年5月、Recursal AI / Eleuther AIのDaniel氏とEugene氏が発表したKey-Value Means (KVM)は、Linear RNNとFull Attentionの計算量トレードオフを連続的なスペクトラムとして扱う新アーキテクチャ。論文はarXiv:2605.09877で公開。

従来の問題意識は明確で、Linear RNN（RWKV-7等）はO(1)デコードを実現するが長文リコールに弱く、Full AttentionはO(N²)のPrefillコストとO(N)のKVキャッシュが避けられない。KVMはこの二択に「目盛り」を引き直す。

計算量プロファイルは3段階で選択可能。KVM (fixed)はO(1)状態サイズ・O(N)Prefillで実質chunked RNN。KVM (√N)はO(√N)の状態サイズ・O(N^1.5)Prefillでリコール性能を大幅強化。Full Attentionはそのまま。同一アーキテクチャ内で推論時に切り替えられる点が最大の特徴。

中核技術はオンラインK-meansによるState更新。Overflowトークンに対してState内の最近傍スロットをargmax（winner-take-all）で選び、そのスロットにのみ加算する。これは温度ゼロ極限のAttentionであり、Stateキーの分離性（separability）を保つ設計。OVQとの差分として、単一のsoftmax passでState+BSWAを統合・JIT正規化でcentroidカウント追跡不要・RoPE次元のゼロ化・無制限State拡張・Sinkトークン保護・領域別learnable temperatureが挙げられる。

4つの主要技術：(1)JIT正規化——Stateキーを累積加算のまま保持し、Attention投入直前にLayerNormを適用することでノルム減衰を回避。Value側はスロット固有の初期ノルムをそのスロット専用のJIT正規化半径として恒久利用。(2)Partial RoPEのゼロ化——複数の絶対位置からマージされたStateキーは単一RoPE角度を持てないため、RoPE適用次元の先頭r次元をゼロにして意味空間のみで動作。(3)State拡張——Overflowブロック到来時に既存Stateとの類似度が最低のトークン（最もnovelなトークン）をappendし、残りはwinner-take-allでマージ。power-law等の複数スケジュールバリアントを提案。(4)Sinkトークン保護と learnable temperature——先頭sink_len個のスロットをマージ対象から除外し、StateとBSWAに別々の温度パラメータを学習。

RWKV-7との比較では、RWKV-7がdiag(w)·S + k⊗vによる全スロット連続更新（custom CUDA kernel必須）なのに対し、KVMはargmax選択による局所更新（標準PyTorch操作のみ）。追加パラメータもW_merge_gate・LayerNorm γβ・温度スカラー・s_vlen・初期Stateのみで、論文はこれを「insignificant number of new parameters」と強調。全レイヤー置換可能でカスタムカーネル不要なため、AMD MI300等でも動作しTransformer-to-X蒸留パイプラインへの組み込みに適する。

## アイデア

- winner-take-all（argmax）をState更新に使うことで、Softmax attentionの表現力とRNNの固定状態サイズの利点を両立しつつ、Stateキーの分離性を数学的に保証する設計思想が独創的
- State拡張を「最も意外なトークン（現Stateとの類似度最小）をappend」という単純規則で実現し、O(√N)のsublinear growthに帰着させる点は、情報理論的な「surprise」概念を工学的に実装した例として興味深い
- カスタムCUDAカーネル不要・追加パラメータ最小という設計は、Transformer蒸留やアダプター的活用を容易にし、既存の大規模モデルへのpost-training適用パスとして監査エージェントの長文コンテキスト処理改善にも応用可能

## 前提知識

- **Linear RNN / RWKV-7** (TODO: 読むべき)
- **Softmax Attention** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **RoPE** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Online K-means** (TODO: 読むべき)

## 関連記事

- /deep_4121 学習可能な回転空間：逐次モデリングのための時間的・意味的回転エンコーディング（SIREN-RoPE）
- /deep_3788 収束進化：異なる言語モデルが類似した数値表現を学習する仕組み
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_3917 URoPE: 幾何学的空間を横断するユニバーサル相対位置埋め込み
- /deep_753 QUEST: クエリ変調球面アテンションを用いたロバストなアテンション定式化

## 原文リンク

[Key-Value Means (KVM)：RNNとTransformerの境界線を消す異端の設計](https://zenn.dev/openmose/articles/93ee355984ca11)
