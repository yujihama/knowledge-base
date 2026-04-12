---
title: "Text Generation Inference（TGI）ベンチマークツールの使い方と活用指針"
url: "https://huggingface.co/blog/tgi-benchmarking"
date: 2026-04-09
tags: [TGI, LLM推論, ベンチマーク, スループット, レイテンシ, TTFT, HuggingFace, Flash Attention, Continuous Batching, RAG]
category: "infra"
memo: "[HF Blog] Benchmarking Text Generation Inference"
processed_at: "2026-04-09T09:24:33.376222"
---

## 要約

Hugging FaceのText Generation Inference（TGI）に付属するベンチマークツールの概要と使い方を解説したブログ記事（2024年5月公開）。LLMサービングの最適化において、スループットだけでなくレイテンシとの両立が不可欠であることを出発点に、TGIベンチマークツールを使ったプロファイリング手法を実践的に説明している。

背景として、LLMの推論はデコーダ構造上、トークン生成ごとに1回のフォワードパスが必要であり本質的に非効率。Flash Attention・Paged Attention・Continuous Batching・投機的デコード・量子化など多数の最適化手法が登場しているが、ユースケースによって最適な構成が異なる。たとえばRAGシステムでは複数ドキュメント（500〜1000トークン×N件）をコンテキストウィンドウに詰め込む大入力が主流であるのに対し、チャットシステムでは1ターンあたり50〜200トークン程度の短い入力が多く、要求特性が大きく異なる。

主要な指標として、Token Latency（1トークン処理時間）、Request Latency（リクエスト全体の応答時間）、Time to First Token（TTFT：最初のトークンが返るまでの時間）、Throughput（単位時間あたりのトークン数）の4つを定義。スループットとレイテンシは直交する指標であり、トレードオフ関係にある。ユーザー数最大化を目指すならスループット重視、離脱防止にはTTFT最小化、モデレートな同時ユーザー数での体験重視にはレイテンシ最小化が有効とされる。

ツールの使い方は、HuggingFace Space「derek-thomas/tgi-benchmark-space」を複製し、JupyterLab上のターミナルからCLIで実行する形式。`text-generation-benchmark`コマンドに対し、`--tokenizer-name`（モデル指定）、`--sequence-length`（入力トークン数）、`--decode-length`（生成トークン数）、`--runs`（繰り返し回数）などを指定して計測を行う。結果はJSONで出力されるほか、付属ノートブックで可視化も可能。実験例として、Meta-Llama-3-8B-Instructを用い、入力長・出力長・同時リクエスト数（concurrency）を変えた複数条件でレイテンシとスループットのPareto曲線を描き、デプロイ構成の意思決定に活用する方法を示している。concurrencyを上げるとスループットが向上する一方でレイテンシが増加するトレードオフが数値として確認できる点が特徴。最終的にはInference Endpoints等の本番環境と同一ハードウェア上でベンチマークを取ることで、実運用に即した構成選択が可能になる。

## アイデア

- スループットとレイテンシは直交する指標であり、ユースケース（RAG vs チャット）に応じて最適化すべき指標が異なるという設計思想は、システム要件定義の段階で明示的にトレードオフを議論するフレームワークとして有用
- Prefilling（1回のフォワードパスで完結）とDecoding（トークン数分のフォワードパスが必要）の非対称性が、入力長・出力長によってレイテンシ特性が大きく変わる根本原因であり、ベンチマーク条件設計の際に両者を独立に変化させることが重要
- 同一ハードウェア上でconcurrencyを変化させたPareto曲線を描くことで、レイテンシ上限を固定した上でスループットを最大化するという実用的な構成選択が可能になる

## Yujiの取り組みへの示唆

監査エージェントシステムでLangGraphを用いたマルチステップ処理を行う場合、RAGパターンによる大量ドキュメント参照が頻発するため、TGIのベンチマークツールでRAG相当の入力長（1000〜5000トークン）と出力長を設定した条件でプロファイリングを行うことで、適切なconcurrencyとスループット/レイテンシのバランスを事前に把握できる。ローカルLLMインフラ（RTX 3090）の構築時に、OllamaやvLLMと並んでTGIをバックエンドとして評価する際にも、このベンチマーク手法で定量的な比較が可能。

## 原文リンク

[Text Generation Inference（TGI）ベンチマークツールの使い方と活用指針](https://huggingface.co/blog/tgi-benchmarking)
