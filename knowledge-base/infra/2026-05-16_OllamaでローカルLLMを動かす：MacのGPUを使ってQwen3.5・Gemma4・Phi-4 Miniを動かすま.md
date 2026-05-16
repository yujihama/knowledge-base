---
title: "OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順"
url: "https://zenn.dev/libercraft/articles/20260511-ollama-mac-local-llm-setup"
date: 2026-05-16
tags: [Ollama, ローカルLLM, Apple Silicon, Metal GPU, Qwen3.5, Gemma4, Phi-4 Mini, LangChain, OpenAI互換API, RAG]
category: "infra"
related: [4176, 5027, 2257, 2691, 4043]
memo: "[Zenn LLM] OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順"
processed_at: "2026-05-16T09:05:50.146262"
---

## 要約

OllamaはmacOS上でローカルLLMを最小限の手順で動かすためのランタイムツール。HomebrewでCLIをインストール（`brew install ollama`）し、`ollama serve`でサーバを起動、`ollama pull <model>`でモデルをダウンロードするだけで動作する。Apple Silicon（M1〜M4）ではMetal GPU加速が自動で有効になり、CUDA環境の構築やGGUF変換は不要。

対応モデルとして本記事ではQwen3.5:4b（約3.4GB、256Kコンテキスト、Thinking Mode対応）、Gemma4:e4b（約3.0GB、128Kコンテキスト、Google製マルチモーダル）、Phi-4 Mini:3.8b（約2.5GB、Microsoft製、英語・コーディング特化）の3モデルを取り上げる。Apple SiliconではCPUとGPUが統合メモリを共有するため、8GB RAM搭載Macなら3〜4GBのモデルが実用速度で動作し、16GBなら9Bクラス、32GB以上なら27B（MoE含む）まで扱える。

GPU使用状況の確認方法は3種類。`ollama ps`コマンドでPROCESSOR列を確認する方法が最も直接的で、`100% GPU`であればMetal推論が正常に動いている。Activity Monitorの「GPU使用率」ウィンドウ、または`OLLAMA_DEBUG=1 ollama serve`のログで`METAL GPU detected`行を確認する方法もある。

API連携面では、Ollamaは`http://localhost:11434/v1`でOpenAI互換のRESTエンドポイントを提供する。OpenAI SDKでは`base_url`と`api_key`（任意文字列）を差し替えるだけで既存コードをローカルに切り替え可能。Ollama公式Pythonパッケージ（`pip install ollama`）も利用でき、`ollama.chat()`でシンプルな呼び出しができる。

LangChain連携では`langchain-ollama`パッケージの`ChatOllama`と`OllamaEmbeddings`を使う。`ChatOpenAI`と`OpenAIEmbeddings`をそれぞれ置き換えるだけで、LCEL・RAGパイプライン・エージェントをローカル完結構成に移行できる。RAGではChromaDB等のベクトルストアとOllamaを組み合わせ、埋め込みモデルに`nomic-embed-text`を使う構成例が示されている。

Qwen3.5のThinking Modeは`ChatOllama(thinking=True/False)`で切り替え可能。精度優先タスクでは`True`、速度優先では`False`を選択する。監査エージェント開発への示唆として、クラウドAPIへのデータ送信なしにローカル完結でRAGパイプラインを構成できる点は、機密文書を扱う内部監査ユースケースで直接活用可能。LangGraph・Pydanticとの組み合わせで、OllamaをLLMバックエンドとしたエージェントシステムをゼロAPIコストで試作できる。

## アイデア

- Apple SiliconのUnified Memory（統合メモリ）アーキテクチャにより、CPU・GPU間のメモリコピーなしにモデルを推論できる構造が、Ollamaの設定レス高速化の技術的背景になっている
- OpenAI互換エンドポイント（localhost:11434/v1）を提供することで、既存のOpenAI SDKコードを`base_url`と`api_key`の2行変更だけでローカルに差し替えられる設計は、ベンダーロックイン回避とコスト制御の実用的な手法
- Qwen3.5のThinking Mode（/think、/no_think）をLangChainのChatOllamaパラメータで切り替えられる仕組みは、推論精度とレイテンシのトレードオフを動的に制御する設計パターンとして監査エージェントの判断ステップ設計に応用できる

## 前提知識

- **Apple Silicon Metal GPU** (TODO: 読むべき)
- **GGUF形式** (TODO: 読むべき)
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **LangChain LCEL** (TODO: 読むべき)
- **RAGパイプライン** → /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針

## 関連記事

- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入

## 原文リンク

[OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順](https://zenn.dev/libercraft/articles/20260511-ollama-mac-local-llm-setup)
