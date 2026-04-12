---
title: "🤗 Transformersでネイティブサポートされる量子化スキームの概要"
url: "https://huggingface.co/blog/overview-quantization-transformers"
date: 2026-04-09
tags: [quantization, bitsandbytes, GPTQ, QLoRA, LLM, transformers, exllama, 4-bit, inference]
category: "infra"
memo: "[HF Blog] Overview of natively supported quantization schemes in 🤗 Transformers"
processed_at: "2026-04-09T21:51:05.532640"
---

## 要約

本記事はHugging Face TransformersにネイティブサポートされているLLM量子化手法、bitsandbytes（BnB）とauto-GPTQの比較分析を行ったブログ投稿（2023年9月公開）。量子化の主な用途は「小型デバイスでの大規模モデル推論」と「量子化モデル上へのアダプタファインチューニング（QLoRA等）」の2つ。

Bitsandbytesの特徴：キャリブレーションデータ不要のゼロショット量子化で、torch.nn.Linearを含む任意モデルに適用可能。Whisper、ViT、Blip2等マルチモーダルモデルにも対応。アダプタ（LoRA等）をマージしても推論速度劣化なし。ただし4-bitモデルのシリアライズ非対応（当時）、GPTQより生成速度が遅い点が課題。

auto-GPTQの特徴：exllamaカーネル使用で生成速度が速く、2〜4bitまでの柔軟なビット数設定が可能。TheBloke名前空間のGPTQモデルをそのまま利用可能、AMDも対応。ただしキャリブレーションデータが必要（175Bモデルで約4GPU時間）、テキスト以外のモダリティへの対応が限定的。

ベンチマーク（Llama-2-13b、A100-80GB、512トークンプロンプト）：バッチサイズ1での推論では、fp16が36.9ms/token、GPTQ（exllama）が33.7ms/token、BnBが52.0ms/token。バッチサイズ16では、fp16が228.76 tok/s、GPTQ 167.68 tok/s、BnB 140.38 tok/s。メモリ使用量はfp16の約29GBに対し、GPTQとBnBはいずれも約10〜11GBに削減。生成速度（decode）ではGPTQがBnBより高速。ファインチューニング（QLoRA）ではBnBが若干高速な場合あり。結論として、使いやすさ重視ならBnB、推論速度・シリアライズ重視ならGPTQ、という使い分けが推奨される。

## アイデア

- BnBはゼロショット量子化でキャリブレーション不要のため、新規モデルへの即時適用コストが極めて低い点はプロトタイピングで有用
- GPTQのexllamaカーネルによりバッチサイズ16でfp16比約26%のスループット維持を実現しており、本番推論への実用水準
- 量子化+LoRAアダプタのマージ戦略（QLoRA→デクォンタイズマージ）はモデル配備時のレイテンシゼロ化に直結する実践的テクニック

## Yujiの取り組みへの示唆

監査エージェント開発においてLlama系ローカルLLMをRTX 3090（24GB VRAM）上で動作させる際、BnBの4-bit量子化によりLlama-2-13B相当のモデルを約11GBで展開可能。QLoRAを使えばPydanticスキーマ準拠の出力や監査特化ファインチューニングをローカルで完結できる。推論速度が重要なReActループやLangGraphのマルチステップエージェントではGPTQ+exllamaが有利なため、用途に応じた選択が重要。

## 原文リンク

[🤗 Transformersでネイティブサポートされる量子化スキームの概要](https://huggingface.co/blog/overview-quantization-transformers)
