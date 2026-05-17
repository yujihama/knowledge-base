---
title: "生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す"
url: "https://zenn.dev/craftgear/articles/982acf1805e9c5"
date: 2026-05-17
tags: [llama.cpp, MTP, Qwen3, 投機的デコーディング, ローカルLLM, GGUF, RTX4090, トークン生成速度]
category: "infra"
related: [2862, 2292, 3653, 3909, 4331]
memo: "[Zenn LLM] 生成速度2倍は本当か？Qwen3.6のMTPを試す"
processed_at: "2026-05-17T21:01:05.831939"
---

## 要約

2026年5月16日にllama.cppへMTP（Multi-Token Prediction）対応PRがマージされた。MTPは投機的デコーディング（Speculative Decoding）の一種で、ドラフトモデルを別途用意せずにメインモデル自体が複数トークンを先読み予測し、一致したトークンをまとめて採用することで生成速度を向上させる手法。本記事ではRTX 4090 + RTX 5080のデュアルGPU環境（CachyOS Linux、i7-14700KF、64GB DDR4）上で、Qwen3-27B-MTPのGGUFモデル（量子化Q6_K_XL）を用いて実測比較を行った。起動フラグは `--spec-type draft-mtp --spec-draft-n-max 3 --spec-draft-p-min 0.75`。結果として、日本語あらすじ生成では32.05→63.42 tok/s（約1.98倍）、日本語要約では31.49→71.56 tok/s（約2.27倍）、JavaScript Tetris生成では31.00→74.39 tok/s（約2.40倍）、forループなし書き換えでは31.16→74.32 tok/s（約2.38倍）と、いずれのタスクでも約2〜2.4倍の生成速度向上を確認。ドラフト受理率（draft acceptance rate）は日本語で約0.72、コード生成では約0.90〜0.93と高く、特にコードタスクで投機予測の精度が高い。一方でprompt processingのスループットはMTP有効時に約0.55倍（例：2238→1228 tok/s）へ低下する副作用がある。長文入力を多用するRAGパイプラインやメモリ帯域の狭いGPU環境ではprompt processingの遅延が全体のボトルネックになる可能性があり、生成フェーズが支配的な対話・ストリーミング用途で効果が大きい。ローカルLLMの実用速度向上という観点で、監査エージェントのように逐次的に長い出力を生成するワークフローにも適用検討の余地がある。

## アイデア

- MTPはドラフトモデル不要でメインモデル単体で投機生成を実現するため、モデル管理コストを下げつつSpeculative Decodingの恩恵を得られる点が実用的
- コード生成（acceptance rate 0.90以上）と日本語生成（0.72）でドラフト受理率に差があり、タスクの予測可能性・パターン性がMTP効果に直結することが数値で示されている
- prompt processingが約0.55倍に低下するトレードオフは、RAGのようにコンテキストが長く生成が短いユースケースでは逆効果になり得るため、用途別にMTPのオン/オフを切り替える設計が必要

## 前提知識

- **Speculative Decoding** → /deep_1379 アライメントフィードバックを用いたマルチドラフター投機的デコーディング
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **GGUF量子化** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **Qwen3** → /deep_2565 Ecom-RLVE: Eコマース会話エージェント向け適応型検証可能環境

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_2292 8Bモデルが1GBに収まる1ビットLLM「Bonsai」を動かしてみた
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る

## 原文リンク

[生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す](https://zenn.dev/craftgear/articles/982acf1805e9c5)
