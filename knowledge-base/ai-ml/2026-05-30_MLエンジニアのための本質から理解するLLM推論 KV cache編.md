---
title: "MLエンジニアのための本質から理解するLLM推論 KV cache編"
url: "https://zenn.dev/kaz20/articles/c77f8a41cf2bf5"
date: 2026-05-30
tags: [KV cache, Self Attention, LLM推論, Transformer, GQA, MHA, MQA, PyTorch]
category: "ai-ml"
related: [6277, 113, 5761, 1264, 4044]
memo: "[Zenn LLM] MLエンジニアのための本質から理解するLLM推論 KV cache編"
processed_at: "2026-05-30T09:05:07.353137"
---

## 要約

本記事は東京科学大学博士課程の藤井氏による「MLエンジニアのための本質から理解するLLM推論」シリーズの一篇で、「なぜKey/ValueをcacheしてQueryをcacheしないのか」という問いに数式と図を用いて厳密に答える。

Self Attentionの出力OはO = softmax(QK^T / √d_k) * Vで表され、Q/K/VはそれぞれX（入力）にW_Q/W_K/W_Vを掛けて得られる。MHA・GQA・MQAの違いはQuery head数n_aとKV head数n_kvの関係（MHA: n_a=n_kv、GQA: 1<n_kv<n_a、MQA: n_kv=1）として整理できる。

Decoding時に位置m+1のトークンを処理する場合、Attention Score行列S全体ではなくS_{m+1,:} = q_{m+1} * K_{1:m+1}^T という1行だけが必要になる。この計算においてq_{m+1}（現在トークンのQuery）のみを使用し、過去のq_1,...,q_mは一切不要である。したがってQueryをcacheする意味がない。

一方でKey側はK_{1:m}（過去トークンのKey全体）が必要であり、cacheなしでは毎ステップ再計算が必要となる。ValueについてもAttention Output o_{m+1} = Σ_{j=1}^{m+1} P_{m+1,j} * v_j の計算においてv_1,...,v_m（過去トークンのValue全体）が必要であるため、cacheの効果がある。

役割を整理すると、Keyは「現在のQueryがどの過去トークンを参照すべきか（attention weightの決定）」に使われ、Valueは「attention weightに基づいて実際に情報を取り出す（weighted sum）」ために使われる。Queryは現在トークンがメモリを読むための一時的なprobeであり、使い終わったら再利用されることがない。

なおRoPEやQK Normを導入するモデルでも、この「Queryをcacheしない理由」の本質は変わらない点も明記されており、応用範囲の広い説明となっている。監査エージェント開発への直接的な示唆は薄いが、LLMの推論効率（メモリ使用量・レイテンシ）を理解することはRAGや長文コンテキスト処理を設計する上で基礎知識として重要。

## アイデア

- QueryをcacheしないのはDecoding時に「現在位置のQueryのみ」で全計算が完結するから、という数式レベルの根拠を明示している点が秀逸
- MHA/GQA/MQAの違いをn_aとn_kvの比率関係として一元的に整理しており、KV cacheサイズとのトレードオフを理解する足がかりになる
- RoPE・QK Normの存在がKV cacheの論理に影響しないと明記しており、実装モデル（LLaMA, Gemma等）への適用範囲を誤解なく把握できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Self Attention** (TODO: 読むべき)
- **Autoregressive Decoding** (TODO: 読むべき)
- **GQA/MQA** (TODO: 読むべき)
- **RoPE** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは

## 関連記事

- /deep_6277 LLM解説シリーズ：Self-Attentionを数式と実装から理解する
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_1264 本番環境でのLLM最適化：低精度・Flash Attention・アーキテクチャ革新
- /deep_4044 多肉植物LMを育てる (1) — データセットの作成とモデル訓練まで

## 原文リンク

[MLエンジニアのための本質から理解するLLM推論 KV cache編](https://zenn.dev/kaz20/articles/c77f8a41cf2bf5)
