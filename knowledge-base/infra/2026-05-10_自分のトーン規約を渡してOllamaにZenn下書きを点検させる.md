---
title: "自分のトーン規約を渡してOllamaにZenn下書きを点検させる"
url: "https://zenn.dev/giteki/articles/002-ollama-draft-proofread"
date: 2026-05-10
tags: [Ollama, gemma3, LLM, Python, textlint, プロンプトエンジニアリング, ローカルLLM, 文章校正]
category: "infra"
related: [4332, 2872, 397, 4911, 3642]
memo: "[Zenn LLM] 自分のトーン規約を渡して、Ollama に Zenn 下書きを点検させる"
processed_at: "2026-05-10T12:50:36.234670"
---

## 要約

ローカルLLM（Ollama）を使ってZenn記事の下書きをトーン規約に基づいて自動校正するPythonスクリプトの実装記録。外部APIを使わない理由はプライバシー保護で、未公開の下書きを外部サーバに送りたくないという消去法的選択。設計の要件は3つ：①Ollamaでローカル完結、②自分のトーン規約をそのままシステムプロンプトに流す、③段落単位で出力して記事内の問題箇所を特定しやすくする。

スクリプトはPython標準ライブラリのみで実装（requestsなし）。処理フローは：Markdownのフロントマター除去→空行区切りの段落分割（コードブロック内の空行は段落境界として扱わない）→HTMLコメント・画像markdown除去（clean_for_llm）→10文字未満や見出し・コードブロックはスキップ→Ollama APIに段落単位で投げてJSON形式で指摘を受け取る。

Ollama API呼び出しでは`format: "json"`を指定してJSON出力を強制し、`temperature: 0`で決定的な出力を優先。指摘は`sentence`（原文引用）・`rule`（違反規約名）・`rewrite`（書き換え案）の3フィールド。

トーン規約の内容：感嘆符禁止、「〜してみた」等の高温度表現を避ける、過度な煽り語（すごい・革命的・ぜひ等）を使わない、結論の出し急ぎを避ける、断定の連発を避ける。

使用モデルはgemma3:4b（約3.3GB、パラメータ約40億）。本記事自身を点検した実走では32件の指摘が出た（推敲の進捗によって変動し、第四走では15件）。

実装上の気づきとして、HTMLコメントやプロンプト内のフィールド説明文を本文と混同して誤指摘するケースが小型モデルで発生した。clean_for_llmによる前処理とis_skippableによるフィルタリングで対処。また`format: "json"`を付けても完全にJSON以外の出力を排除できないためjson.DecodeErrorのハンドリングが必要。temperature=0でも出力は完全には安定せず、同一入力で異なる指摘が返ることがある。

textlintとの役割分担として、感嘆符や定型句の検出はtextlintに任せ、「煽り感」「押し付けがましさ」「結論の出し急ぎ」のような言語化しにくいルール違反をLLMが担うという補完関係を想定している。監査エージェント開発への示唆として、構造化出力（JSON強制）と段落単位の局所化処理の組み合わせは、レポート点検や規程チェックのエージェント設計にも応用可能。

## アイデア

- トーン規約をプロンプトとして言語化する作業が、曖昧なまま運用していた自分の文体規約を成果物として固める副産物になるという点
- segment-level（段落単位）でLLMに投げる設計により、長文の漠然とした指摘を避けつつ記事内の問題箇所を1対1で特定できる構造
- textlintとLLMの役割分担：規則化可能なパターンはtextlint、言語化しきれない曖昧な品質問題はLLMという補完関係

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **gemma3** → /deep_299 MedGemma: 医療AI開発向けGoogleの最高性能オープンモデル群
- **urllib.request** (TODO: 読むべき)
- **JSON structured output** (TODO: 読むべき)
- **temperature parameter** (TODO: 読むべき)

## 関連記事

- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_2872 file-splitter：ローカルLLM時代のファイル分割ツール
- /deep_397 C言語・Docker・Gemini APIで構築する「平安雅翻訳機」— 技術の無駄遣いの先に見たAI時代の生存戦略
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁

## 原文リンク

[自分のトーン規約を渡してOllamaにZenn下書きを点検させる](https://zenn.dev/giteki/articles/002-ollama-draft-proofread)
