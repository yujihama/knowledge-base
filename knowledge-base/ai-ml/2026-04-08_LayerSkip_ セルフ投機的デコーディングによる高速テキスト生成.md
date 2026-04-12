---
title: "LayerSkip: セルフ投機的デコーディングによる高速テキスト生成"
url: "https://huggingface.co/blog/layerskip"
date: 2026-04-08
tags: [LayerSkip, speculative-decoding, early-exit, LLM推論高速化, transformers, Llama, inference-optimization]
category: "ai-ml"
memo: "[HF Blog] Faster Text Generation with Self-Speculative Decoding"
processed_at: "2026-04-08T21:11:22.952933"
---

## 要約

LayerSkipは、単一モデルの早期レイヤーをドラフト生成に、深層レイヤーを検証に使う「セルフ投機的デコーディング」手法。従来の投機的デコーディングは小型モデル（ドラフト）と大型モデル（検証）の2モデル構成が必要だったが、LayerSkipは同一モデル内でその役割を分担するため、追加メモリが不要。

技術的な核心は3点：①早期出口（Early Exit）：中間レイヤーの出力をドラフトトークンとして使用、②アンエンベディング（Unembedding）：中間レイヤーの隠れ状態をLM Headで語彙空間に変換、③専用訓練レシピ：早期出口損失（Early Exit Loss）の適用と段階的なレイヤードロップアウト率の増加により、早期レイヤーの予測精度を向上。この訓練を施したモデルのみでスピードアップが得られる。

ベンチマーク結果（A100 80GB、要約タスク）では、Llama3 8Bで効率1.83倍（通常の投機的デコーディング Llama3 8B + Llama3.2 1Bの1.53倍を上回る）、Llama3.2 1Bで1.80倍、Llama2 70Bで2.06倍を記録。特に13Bモデルはレイヤー8での早期出口で1.746倍となり、レイヤー4（0.995倍）より大幅に効率的で、最適な出口レイヤー選択が重要であることが示された。

実装はHugging Face transformersライブラリに統合済み。`model.generate()`の`assistant_early_exit`引数に出口レイヤー番号を指定するだけで利用可能。対応チェックポイントはfacebook/layerskip-llama2-7B、13B、70B、llama3-8B、llama3.2-1B等。メモリ節約効果により、より小型のGPUでの大規模モデル推論が実現可能になる。

## アイデア

- 同一モデルの浅い層と深い層を非対称に活用することで、外部ドラフトモデルなしに投機的デコーディングを実現する設計思想は、RAGやエージェントの推論ループにも応用できる可能性がある
- 訓練レシピ（早期出口損失＋段階的ドロップアウト）が推論時の速度を決定するという「訓練と推論の結合設計」は、タスク特化ファインチューニング時にも考慮すべき新しい設計軸になりうる
- 最適な早期出口レイヤーはモデルサイズやタスクによって異なり（13B: layer 8が有効、layer 4は非効率）、出口レイヤーのチューニングが実運用上の重要パラメータになる
## 関連記事

- /deep_907 Universal Assisted Generation：任意のアシスタントモデルによる高速デコード
- /deep_267 Speculative Cascades：LLM推論を高速化・高品質化するハイブリッドアプローチ
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する

## 原文リンク

[LayerSkip: セルフ投機的デコーディングによる高速テキスト生成](https://huggingface.co/blog/layerskip)
