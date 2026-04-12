---
title: "LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較"
url: "https://huggingface.co/blog/Lora-for-sequence-classification-with-Roberta-Llama-Mistral"
date: 2026-04-09
tags: [LoRA, PEFT, RoBERTa, Llama2, Mistral7B, テキスト分類, HuggingFace, fine-tuning, Transformers]
category: "ai-ml"
memo: "[HF Blog] Comparing the Performance of LLMs: A Deep Dive into Roberta, Llama 2, and Mistral for Disaster Tweets Analysis with Lora"
processed_at: "2026-04-09T21:21:59.272222"
---

## 要約

本記事は、HuggingFace PEFTライブラリのLoRA（Low-Rank Adaptation）を用いて、3つの事前学習済みモデル（RoBERTa-large 355M、Llama 2-7B、Mistral 7B v0.1）を災害ツイート二値分類タスクでファインチューニングし、性能を比較した実験レポートである。

データセットはHuggingFace上の「twitter_disaster」（訓練6,090件、検証1,523件、テスト3,263件）を使用し、クラス不均衡（負例4,342件 vs 正例3,271件）への対策として重み付き損失関数をカスタムTrainerで実装している。全モデルの最大シーケンス長はRoBERTaの制約に合わせて512トークンに統一した。

LoRAの設定では、各モデルのアテンション層（q_proj、v_proj等）に対してランク（r）や alpha などのハイパーパラメータを調整し、元の重みを凍結したまま低ランク行列のみを学習する。これにより、7Bパラメータモデルでも数百万規模の学習パラメータに削減できる。ハイパーパラメータ探索にはWeights & Biasesを使用した。

アーキテクチャ面では、Mistral 7BはSliding Window Attention（各トークンが最大4,096トークンを参照、計算量が線形）とGrouped-Query Attention（KVキャッシュの効率化）を採用している点が特徴的。Llama 2も同様にGQAとRotary Positional Embeddingを採用し、コンテキスト長を4,096トークンに拡張している。RoBERTaはエンコーダ専用モデルであり、系列分類タスクへの適合性が高い。

実験結果として、RoBERTa-largeは355Mという小規模ながら7Bモデルと競争力のある分類精度を示した（具体的な数値はwandbレポートに記載）。Mistral 7BとLlama 2はデコーダ専用の大規模モデルであるため、系列分類への適用にはクラストークンの処理など追加の工夫が必要となる。LoRAにより全パラメータのファインチューニングなしに実用的な精度を達成できることが確認された。

## アイデア

- デコーダ専用LLM（Llama 2・Mistral）を系列分類タスクに適用する際、エンコーダ専用モデル（RoBERTa）と同等以上の精度をLoRAだけで達成できるかを検証している点。アーキテクチャの本来の用途外への転用可能性を示す
- クラス不均衡への対処としてカスタムTrainerで重み付きクロスエントロピー損失を実装している点。実務データでは不均衡が一般的であり、この実装パターンは再利用価値が高い
- LoRAのランク・alpha・対象モジュールをモデルごとに最適化し、Weights & Biasesで実験追跡している構成は、再現性の高いPEFTパイプラインの雛形として機能する

## Yujiの取り組みへの示唆

監査エージェント開発において、監査調書・リスク評価レポート・取引記録などのテキストを分類・ラベリングするサブコンポーネントが必要になる場面でLoRAによるPEFTは直接活用できる。特に、RoBERTa-largeが7Bモデルと競合する性能を示した点は、推論コスト・レイテンシを重視するエージェント内の分類器としてエンコーダ専用小規模モデルを選択する根拠になる。またWeights & Biasesによる実験管理パターンは、GRPO/RLAIFの学習実験追跡にも転用可能。

## 原文リンク

[LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較](https://huggingface.co/blog/Lora-for-sequence-classification-with-Roberta-Llama-Mistral)
