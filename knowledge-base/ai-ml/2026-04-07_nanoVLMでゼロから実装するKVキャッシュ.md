---
title: "nanoVLMでゼロから実装するKVキャッシュ"
url: "https://huggingface.co/blog/kv-cache"
date: 2026-04-07
tags: [KV-cache, Transformer, autoregressive-generation, nanoVLM, RoPE, self-attention, inference-optimization, PyTorch, VLM]
category: "ai-ml"
memo: "[HF Blog] KV Cache from scratch in nanoVLM"
processed_at: "2026-04-07T21:01:42.798292"
---

## 要約

本記事は、HuggingFaceが公開するnanoVLM（純粋なPyTorchで書かれたVision Language Modelの小規模実装）にKVキャッシュをゼロから実装した実践レポートである。実装によってトークン生成速度が38%向上した。

自己回帰型言語モデルはトークンを1つずつ生成する。各ステップで全シーケンスに対してQ・K・Vを再計算するため、シーケンス長に対して二乗オーダーの計算量が発生する。KVキャッシュはこの冗長性を排除する最適化手法である。具体的には、プロンプト処理（prefillフェーズ）でK・Vを計算してレイヤーごとにキャッシュし、デコードフェーズでは新規トークン分のK・Vのみを計算してキャッシュに追記する。Qは毎回現在トークンのみから計算し、キャッシュ済みのK・V全体とアテンション演算を行う。

実装上の変更点は3箇所に集中する。①`LanguageModelGroupedAttention`のforwardメソッドに`block_kv_cache`引数を追加し、prefillか否かで処理を分岐。prefill時はキャッシュなしで全トークンを処理し、decode時はキャッシュに新規K・Vをconcatして使用する。②`LanguageModel`クラスでレイヤーごとのキャッシュを管理し、`start_pos`引数でRoPE（Rotary Positional Embedding）の位置IDを正しく計算する。③生成ループをprefillとdecodeに明示的に分離し、decoderフェーズでは`start_pos`をインクリメントしながら単一トークンずつ処理する。

キャッシュの形状は`(batch_size, num_heads, seq_len_cached, head_dim)`であり、各レイヤーに`{'key': tensor, 'value': tensor}`の辞書として保持される。RoPEとの統合が実装上の注意点で、位置エンコーディングは回転演算の性質上Kに適用後にキャッシュする必要がある（Vへの適用は不要）。また、アテンションマスクもキャッシュ長に応じて動的に生成する必要がある。

本記事はnanoVLMという小規模コードベース（数百行程度）を題材にしているため、FlashAttentionや量子化KVキャッシュといった本番実装の複雑さを排除した状態で原理を学べる点が特徴的である。

## アイデア

- KVキャッシュの実装をprefillとdecodeの2フェーズに明示的に分離することで、コードの見通しが良くなりデバッグが容易になる設計パターン
- RoPEはVではなくKに適用した後にキャッシュする必要があるという非自明な実装上の制約——位置エンコーディングがキャッシュ戦略に影響する典型例
- nanoVLMのような小規模・自己完結型コードベースでゼロから実装することで、本番LLMのブラックボックス部分を透明化して学習できるアプローチの有効性

## Yujiの取り組みへの示唆

監査エージェントはLangGraphで複数ステップの推論チェーンを実行するため、長いコンテキストでの推論コストが実用上の制約になりうる。KVキャッシュの仕組みを理解しておくことで、ローカルLLM（RTX 3090環境でのOllama等）を使った監査エージェントの推論レイテンシ最適化や、バッチサイズ・シーケンス長のトレードオフを定量的に判断できるようになる。特にLLM-as-judgeパターンで同一コンテキストに対して複数回クエリを投げる場合、prefillキャッシュの再利用によりコストを大幅削減できる示唆がある。

## 原文リンク

[nanoVLMでゼロから実装するKVキャッシュ](https://huggingface.co/blog/kv-cache)
