---
title: "MacBook Pro M シリーズで始めるローカル LLM ハンズオン"
url: "https://zenn.dev/ppgm/books/mac-local-llm-hands-on"
date: 2026-05-11
tags: [Ollama, Apple Silicon, ローカルLLM, Gemma, Mastra, Next.js, Continue, VS Code, マルチモーダル]
category: "infra"
related: [4176, 4618, 5037, 4911, 3642]
memo: "[Zenn LLM] MacBook Pro M シリーズで始める ローカル LLM ハンズオン"
processed_at: "2026-05-11T21:33:57.347240"
---

## 要約

本書はMacBook Pro Mシリーズ（Apple Silicon）上でローカルLLMを動かすための実践的ハンズオンガイドである。全12章構成で、OllamaのインストールからMastra+Next.jsを使ったチャットアプリ構築まで体系的にカバーする。

中心ツールはOllama（ローカルLLM実行ランタイム）で、モデルのダウンロード・管理・API提供を一括して担う。対応モデルとしてGemmaが主に紹介されており、マルチモーダル対応（画像・UI・帳票読み取り）の活用例も含まれる。Chapter 5〜6ではOllama APIを直接叩いて画像チャットを実装する方法を解説し、REST API経由でのマルチモーダル推論を実証している。

Chapter 7〜8ではVS Code拡張のContinueと組み合わせたコーディング支援環境の構築を扱う。Continueはローカル起動中のOllamaモデルをバックエンドとして利用でき、コード補完・チャット支援をオフライン環境で実現できる。Chapter 9ではモデル比較メモとして複数モデルの特性差が整理されている。

Chapter 10ではMastra（TypeScript製AIエージェントフレームワーク）とNext.jsを組み合わせ、ローカルLLMを推論バックエンドとするWebチャットアプリの実装手順を示す。Mastraはツール呼び出し・ワークフロー・エージェントオーケストレーションを抽象化するフレームワークであり、LangChainのTypeScript版に相当するポジションを持つ。

文章量は約28,724字で無料公開。Apple SiliconのUnified Memoryアーキテクチャにより、RTX 3090等のGPUなしでも7B〜13Bクラスのモデルを実用速度で実行可能な点が前提となっている。監査エージェント開発への示唆として、ローカルLLM環境はデータ外部送信リスクを排除できるため、機密性の高い監査ログや内部統制文書を扱うユースケースに適しており、OllamaのAPIサーバー機能を活用してLangGraphエージェントのバックエンドとして組み込む構成が現実的な選択肢となる。

## アイデア

- OllamaをREST APIサーバーとして起動し、LangGraphやMastraから叩く構成により、クラウドLLM依存なしのエージェントパイプラインを構築できる
- Continueの導入によりVS Code上でローカルLLMをコード補完に使う環境が5分以内に構築でき、機密コードをクラウドに送らない開発フローが実現する
- Mastra+Next.jsの組み合わせはTypeScriptベースのフルスタックAIアプリを最短構成で立ち上げる事例として、Python以外のエージェントフレームワーク選択肢を示している

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Apple Silicon / Unified Memory** (TODO: 読むべき)
- **REST API** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Mastra** → /deep_4175 マルチステップ画像生成AIで、LLMが会話にない場面を描く問題に試した工夫
- **VS Code Continue** (TODO: 読むべき)

## 関連記事

- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4618 AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁

## 原文リンク

[MacBook Pro M シリーズで始めるローカル LLM ハンズオン](https://zenn.dev/ppgm/books/mac-local-llm-hands-on)
