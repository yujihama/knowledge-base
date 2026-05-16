---
title: "LM StudioでLLM-jp4を使う：国産OSS LLMのローカル実行手順と注意点"
url: "https://zenn.dev/hi/articles/64f106cd145fa8"
date: 2026-05-07
tags: [LLM-jp-4, LM Studio, ローカルLLM, GGUF, NII, Reasoning Parsing, Jinja template, 日本語LLM]
category: "infra"
related: [2403, 1423, 1961, 2067, 1333]
memo: "[Zenn LLM] LM StudioでLLM-jp4を使う"
processed_at: "2026-05-07T09:47:32.165058"
---

## 要約

国立情報学研究所（NII）が2026年4月3日に公開した国産OSS LLM「LLM-jp-4」を、ローカルLLM実行環境のLM Studio（v0.4.12）で動作させた実践レポート。LLM-jp-4はアーキテクチャにllama2とQwen3 MoEを採用しつつ、学習自体はフルスクラッチで行われており、日本語性能でGPT-4oを上回ると報告されている。モデルサイズは8Bと32Bの2種が公開され、ライセンスはApache 2.0で商用利用可能。実行環境はWindows 11 Pro、RTX 3060 12GB VRAM、RAM 64GBで検証。HuggingFaceに公開されているGGUF変換済みモデルをLM Studio上からダウンロードし使用する（32Bは約21GB、8Bは約5GB）。起動直後にJinja templateのエラーが発生する既知問題があり、原因はLLM-jp-4のreasoningトークン「<|channel|>final<|message|>」をLM Studioが処理できないこと。回避策として、LM Studio の「My Models > モデル > Inference > Reasoning Parsing」設定で、開始文字列を「<|channel>」（末尾の「|」なし表記）、終了文字列を「final<|message|>」に設定することで動作確認済み。8Bモデルは名刺交換メール作成タスク（200文字以内・条件付き）を約20秒で完了し、指示への準拠度も高い。32Bモデルは同タスクで約2分かかり、思考過程が迂回する挙動が見られたが最終出力は概ね良好。Reasoning Parsingの設定が不完全な場合、32Bでは推論ループが終了しない問題が起きる可能性がある。監査エージェント開発の観点では、日本語特化のローカルLLMが実用レベルで動作することで、社内文書処理や個人情報を含む監査タスクへのオフライン活用が現実的になる。またOpenAIが提供開始した「privacy filter model」と組み合わせた日本語プライバシー処理用途も今後の検討余地がある。

## アイデア

- Jinja templateのreasoningトークン処理問題は、LM StudioのReasoning Parsing設定で開始・終了文字列を手動指定することで回避可能という実用的なトラブルシュート手順
- LLM-jp-4はllama2/Qwen3 MoEアーキテクチャを採用しつつ学習はフルスクラッチという設計で、既存アーキテクチャの知見を活用しながら日本語特化性能を実現している点
- RTX 3060 12GBで32B（21GB）モデルを動作させている点から、量子化（GGUF）によりVRAM容量を大幅に圧縮できることが示されており、ローカルLLM運用のハードウェア要件の現実的な目安になる

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **Jinja template** (TODO: 読むべき)
- **LM Studio** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- **Reasoning tokens** (TODO: 読むべき)
- **ローカルLLM推論** (TODO: 読むべき)

## 関連記事

- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）
- /deep_1961 国産LLMは公開されている。なぜ誰も知らないのか！
- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）

## 原文リンク

[LM StudioでLLM-jp4を使う：国産OSS LLMのローカル実行手順と注意点](https://zenn.dev/hi/articles/64f106cd145fa8)
