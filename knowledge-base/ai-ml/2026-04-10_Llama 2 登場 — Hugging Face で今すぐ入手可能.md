---
title: "Llama 2 登場 — Hugging Face で今すぐ入手可能"
url: "https://huggingface.co/blog/llama2"
date: 2026-04-10
tags: [Llama2, RLHF, QLoRA, PEFT, transformers, TGI, GQA, オープンLLM, Meta]
category: "ai-ml"
memo: "[HF Blog] Llama 2 is here - get it on Hugging Face"
related: [1305, 1214, 991, 1266, 1216]
processed_at: "2026-04-10T09:15:14.412889"
---

## 要約

MetaがLlama 2ファミリーのLLMを2023年7月18日にリリースした。7B・13B・70Bの3サイズのベースモデルと、RLHFで対話最適化されたLlama 2-Chatモデルが含まれる。商用利用可能なLlama 2ライセンスで提供され、Hugging Face Hub上に12モデル（オリジナルMetaチェックポイント＋transformers対応版）が公開された。

主な技術的改善点：Llama 1比で40%多いトークン（2兆トークン）で学習、コンテキスト長が4,096トークンに拡大、70BモデルはGrouped Query Attention（GQA）を採用して推論速度を向上。ベンチマークスコアはLlama-2-70Bが67.87、13Bが55.69、7Bが50.97で、同規模のFalcon-40B（58.07）やMPT-7B（47.24）を上回る。

Llama 2-Chatは人間評価でChatGPT相当の性能を達成。helpfulnessとsafetyの両面で大半のオープンモデルを超える。

Hugging Face側の統合として、transformers 4.31以降でそのまま利用可能。bitsandbytes（4bit量子化）、PEFT/QLoRA（パラメータ効率的ファインチューニング）、Text Generation Inference（TGI: 連続バッチ処理・テンソル並列対応の本番用推論コンテナ）、Inference Endpointsとの連携が即日提供された。

ファインチューニングはQLoRA＋SFTTrainer（trlライブラリ）でNVIDIA T4（16GB）1枚上でLlama 2 7Bが実行可能。timdettmers/openassistant-guanacoデータセットを用いたInstruction Tuningスクリプトが公開され、LoRAウェイトをsafetensor形式でマージ・保存してTGIでデプロイできる。

プロンプト形式はLlama 2-Chat専用のシステムプロンプト＋マルチターン形式が定められており、[INST]タグを用いた構造化フォーマットが必要。

デプロイ推奨構成：7BはA10G×1、13BはA100×1、70BはA100×2（bitsandbytes量子化）またはA100×4。

## アイデア

- RLHFで対話最適化されたLlama 2-ChatがChatGPT相当の性能を達成しており、クローズドモデルに依存しない本番エージェント構築の現実的な選択肢となった
- QLoRA＋SFTTrainerによりT4 1枚でファインチューニング可能な点は、ドメイン特化（監査・GRC）のカスタムモデル構築コストを大幅に削減する
- Grouped Query Attentionにより70Bモデルの推論速度が向上しており、大規模モデルを実用的なレイテンシで動かすアーキテクチャ上の工夫として注目
## 関連記事

- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1214 LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較
- /deep_991 Llama 3.1 リリース — 405B・70B・8Bの多言語対応・128Kコンテキスト版
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法

## 原文リンク

[Llama 2 登場 — Hugging Face で今すぐ入手可能](https://huggingface.co/blog/llama2)
