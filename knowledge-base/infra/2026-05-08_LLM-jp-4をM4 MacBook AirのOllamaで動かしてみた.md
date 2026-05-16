---
title: "LLM-jp-4をM4 MacBook AirのOllamaで動かしてみた"
url: "https://zenn.dev/black_lotus/articles/393aecc980ed20"
date: 2026-05-08
tags: [LLM-jp-4, Ollama, GGUF, Q4_K_M量子化, ローカルLLM, M4 MacBook Air, huggingface-cli, Modelfile, 日本語LLM, Qwen3]
category: "infra"
related: [2862, 4042, 3642, 1961, 2403]
memo: "[Zenn LLM] LLM-jp-4をM4 MacBook AirのOllamaで動かしてみた"
processed_at: "2026-05-08T09:37:14.760895"
---

## 要約

国立情報学研究所（NII）を中心とした国内コンソーシアムが開発した日本語特化LLM「LLM-jp-4」の8Bモデルを、M4 MacBook Air（メモリ16GB）上でOllamaを使いローカル推論した実験レポート。OllamaのライブラリにないモデルはGGUF形式で手動取得する必要があるため、Hugging FaceからQ4_K_M量子化済みGGUFファイル（5.30GB）をhuggingface-cli（hfコマンド）でダウンロードし、Modelfileを作成してOllamaに登録する手順を詳説している。Modelfileではstopトークンに`<|endoftext|>`、temperature=0.7、num_ctx=8192を設定。`ollama create`でモデルを登録し、`ollama run`で対話起動する。比較対象として同環境で動かしたQwen3（8B）と「最新の量子力学の技術動向」という同一質問を投げて回答品質を比較した。LLM-jp-4はNVセンターの磁場感度（10⁻¹⁸ T/√Hz）や光格子時計の不確かさ（5×10⁻¹⁹）など具体的な数値を含む技術的詳細な回答を返した一方、Qwen3は構造が整理されているが情報が2023年頃で止まっており、IBMの量子ビット数など事実と異なる記述が見られた。応答速度は両者ほぼ同等。M4のMetal GPUで100%GPU処理（ollama ps確認）、コンテキスト8192トークンで動作し、アイドル5分後に自動メモリ解放される挙動も確認。ローカルLLMインフラ構築の観点では、GGUF+Ollamaの組み合わせによりM-seriesチップで8Bモデルを実用的な速度で動かせることが実証されており、Qwen3との差別化点として日本語タスクでの技術的具体性の高さが示された。ただし両モデルとも情報の正確性は別途検証が必要と筆者は注記している。

## アイデア

- 日本語特化モデルLLM-jp-4は多言語モデルQwen3より技術質問への具体的数値を含む回答を返す傾向があり、専門的な日本語タスクでの差別化が確認できる
- GGUF+Modelfile方式によりOllamaライブラリ外のモデルも登録可能で、HuggingFace上の任意のGGUFモデルをローカル推論環境に取り込めるパターンが汎用的に使える
- M4 MacBook Air 16GBで8B Q4_K_Mモデルを100% GPU処理できることが実証されており、Apple Siliconの統合メモリアーキテクチャがエッジLLM推論に有効であることを示している

## 前提知識

- **GGUF** → /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- **量子化（Q4_K_M）** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **LLM-jp** → /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- **Apple Silicon推論** (TODO: 読むべき)

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_4042 LM StudioでLLM-jp4を使う：国産OSS LLMのローカル実行手順と注意点
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_1961 国産LLMは公開されている。なぜ誰も知らないのか！
- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した

## 原文リンク

[LLM-jp-4をM4 MacBook AirのOllamaで動かしてみた](https://zenn.dev/black_lotus/articles/393aecc980ed20)
