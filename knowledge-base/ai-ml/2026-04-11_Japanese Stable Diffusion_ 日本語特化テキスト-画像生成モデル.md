---
title: "Japanese Stable Diffusion: 日本語特化テキスト-画像生成モデル"
url: "https://huggingface.co/blog/japanese-stable-diffusion"
date: 2026-04-11
tags: [Stable Diffusion, fine-tuning, Japanese NLP, text-to-image, SentencePiece, CLIP, latent diffusion model, rinna, LAION-5B, 多段階学習]
category: "ai-ml"
memo: "[HF Blog] Japanese Stable Diffusion"
processed_at: "2026-04-11T09:11:13.353893"
---

## 要約

rinna株式会社が開発した「Japanese Stable Diffusion」は、Stability AI等が開発したStable Diffusionを日本語キャプション付き画像でファインチューニングした日本語特化型テキスト-画像生成モデル。Stable Diffusionは主にLAION-5BのEnglishサブセット（LAION2B-en）で学習されており、日本語固有表現（「サラリーマン」「擬音語」等）や日本的な文化・風俗の表現が困難だった。Japanese Stable Diffusionはこの課題を解決するため、約1億枚の日本語キャプション付き画像（LAION-5Bの日本語サブセットを含む）を使用。英語データセット比で1/20のデータ規模という制約に対応するため、スクラッチ学習ではなくファインチューニングを採用し、さらにPITIの手法に倣った2段階学習を実施した。第1段階では潜在拡散モデル（Latent Diffusion Model）を固定した上で、CLIPトークナイザーの代わりに日本語SentePieceトークナイザーを用いた日本語特化テキストエンコーダーを学習。CLIPトークナイザーでは「サラリーマン 油絵」が12トークンに断片化されるのに対し、日本語トークナイザーでは5トークンに正しく分割される。この段階でモデルは日本語プロンプトを理解できるが、潜在拡散モデル自体は変更されていないため、生成画像は依然として西洋風のスタイルに留まる。第2段階では、テキストエンコーダーと潜在拡散モデルを同時にファインチューニングし、日本的なスタイルの画像生成を実現。例として「サラリーマン 油絵」というプロンプトに対し、第2段階後は日本人の顔立ちを持つビジネスマン像が生成されるようになった。前処理として、rinna公開のjapanese-cloob-vit-b-16を使用して低品質サンプルをスコアフィルタリング済み。モデルはHugging Face（rinna/japanese-stable-diffusion）およびGitHubで公開されており、🧨 Diffusersをベースに実装。推論には約10GB VRAMのGPUで動作可能。

## アイデア

- データ量が1/20でも2段階ファインチューニング（エンコーダー固定→全体joint学習）で言語・文化適応を達成できる点は、リソース制約下でのドメイン特化モデル構築の汎用的な設計パターンとして参考になる
- CLIPの汎用トークナイザーを言語固有のSentencePieceに置き換えることで、トークン数を削減しつつ意味的な分割精度を高める手法は、日本語LLMや日本語RAGのトークナイズ設計にも直接応用できる
- 文化・言語固有の概念（「サラリーマン」等の英語由来だが意味が変容した語）を正しく扱うには翻訳では不十分であり、文化コンテキストを持つデータで直接学習する必要があるという知見は、ドメイン特化エージェント設計にも通じる

## 原文リンク

[Japanese Stable Diffusion: 日本語特化テキスト-画像生成モデル](https://huggingface.co/blog/japanese-stable-diffusion)
