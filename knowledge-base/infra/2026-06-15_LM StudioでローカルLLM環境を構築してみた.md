---
title: "LM StudioでローカルLLM環境を構築してみた"
url: "https://zenn.dev/phinata/articles/lm-studio-local-llm"
date: 2026-06-15
tags: [LM Studio, ローカルLLM, Ollama, Mistral 7B, OpenAI互換API, GUI, macOS]
category: "infra"
related: [7587, 4043, 1333, 5469, 5027]
memo: "[Zenn LLM] LM StudioでローカルLLM環境を構築してみた"
processed_at: "2026-06-15T09:05:42.757418"
---

## 要約

LM StudioはGUIベースのローカルLLM実行環境で、Webブラウザ上で動作するダッシュボードからモデルのダウンロード・管理・チャット操作をクリック中心で行える。Ollamaがターミナルコマンドを主体とした軽量設計であるのに対し、LM Studioは「使いやすさ」を優先した設計となっている。動作環境はmacOS（Apple Silicon）、Windows、Linuxに対応し、最低8GB・推奨16GB以上のRAMとモデル保存用に50GB以上のストレージが必要。GPUはオプションだが速度向上に寄与する。インストールは公式サイトから.dmgファイルをダウンロードしてApplicationsフォルダへドラッグするだけで完了し、初回起動時にセットアップウィザードが表示される。モデルは画面左のModel SearchからMistral 7B、Llama 2 7B、Gemma 7B、Neural Chat 7Bなどを検索・ダウンロード可能で、Mistral 7B Instructは約4GBのファイルサイズで10〜30分程度でダウンロード完了する。サーバー起動はDeveloperメニューのLocal Serverから行い、モデルをロードしてチャット画面から質問を投げると応答が返る。会話履歴は自動保持され、文脈を踏まえた連続対話が可能。OllamaとのメモリをMistral 7Bで比較すると、Ollamaが約6GBなのに対しLM Studioは7〜8GB程度消費する。OpenAI互換APIを提供しているため、既存のOpenAI SDK対応ツールをそのままローカルLLMに向けることができる。プリセット機能でシステムプロンプト・トークン数・Temperature（創造性）を事前設定でき、Temperatureは0.1〜0.3が事実確認向き、0.7〜1.0が創作向きとされる。一方でOllamaと比べて起動時間が長く、スクリプトによる自動化がしにくいという制約もある。監査エージェント開発の文脈では、OpenAI互換APIを活用してLangChainやLangGraphからローカルLLMを呼び出す構成が可能であり、コスト・プライバシー面でのメリットが大きい。ただし自動化・バッチ処理が主体の用途にはOllamaの方が適している。

## アイデア

- OpenAI互換APIを提供することで、既存のOpenAI SDK対応コードをほぼ変更なしにローカルLLMへ切り替えられる点は、API費用削減や機密データのオンプレミス処理に直結する実用的なアーキテクチャ
- OllamaとLM Studioの同一モデル（Mistral 7B）でのメモリ使用量差（6GB vs 7〜8GB）は、Webアプリ常駐分のオーバーヘッドを定量的に示しており、リソース制約下でのツール選定基準として参考になる
- Temperature・System Prompt・Context Lengthをプリセットとして保存できるUI設計は、実験の再現性管理の観点から、LLM評価やプロンプトエンジニアリングのワークフロー効率化に寄与する

## 前提知識

- **ローカルLLM** → /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **量子化モデル（GGUF）** (TODO: 読むべき)
- **Temperature（LLMパラメータ）** (TODO: 読むべき)

## 関連記事

- /deep_7587 OllamaのメンタルモデルでLM Studio導入 on AlmaLinux
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド
- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】

## 原文リンク

[LM StudioでローカルLLM環境を構築してみた](https://zenn.dev/phinata/articles/lm-studio-local-llm)
