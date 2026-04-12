---
title: "OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド"
url: "https://huggingface.co/blog/olympic-coder-lmstudio"
date: 2026-04-08
tags: [OlympicCoder, LM-Studio, GGUF, Continue.dev, ローカルLLM, VS-Code, Open-R1, 量子化]
category: "infra"
memo: "[HF Blog] Open R1: How to use OlympicCoder locally for coding"
processed_at: "2026-04-08T09:14:51.096737"
---

## 要約

OlympicCoderは、HuggingFaceのOpen R1プロジェクトが公開したオープンソースのコーディング特化LLMで、7Bと32Bの2バリアントが存在する。LiveCodeBenchの評価では、7Bパラメータ版がClaude 3.7 SonnetおよびGPT-4oを上回るスコアを記録している。本記事はOlympicCoder 7BをローカルのVS Code環境に組み込むための実践的なセットアップ手順を解説する。

技術スタックはOlympicCoder 7B（4bit GGUF量子化版）、LM Studio、VS Code、Continue.devの4つで構成される。LM StudioはHugging Face Hubからモデルを取得・管理し、OpenAI互換のREST APIをlocalhost:1234/v1で公開するツール。GGUF形式のモデルを量子化レベルを選んでダウンロードでき、Q4_K_Mが一般的なデバイスで推奨される。より高スペックのGPUがあればQ8_*も選択肢に入る。CLIからは`lms get lmstudio-community/OlympicCoder-7B-GGUF`、`lms load olympiccoder-7b`、`lms server start`の3コマンドで起動可能。

VS Code側ではContinue.dev拡張をインストールし、JSONコンフィグでモデル名（olympiccoder-7b）とエンドポイント（http://localhost:1234/v1）を指定するだけで接続が完了する。利用可能な機能はコード補完、コード生成、コード説明、リファクタリング、ユニットテスト生成など。

OlympicCoderはCodeForces-CoTsデータセット（競技プログラミングの思考過程を含む）でファインチューニングされており、説明的・対話的な応答よりもアルゴリズム的に難しい問題への対応を得意とする。Claudeのような丁寧な説明スタイルとは異なり、直接的・実装重視のスタイルが特徴。バイナリサーチの最適化など計算効率が重要なタスクに向き、ユーザー向けAPIデザインなどの設計タスクにはClaude 3.7 SonnetやQwen-2.5-Coderの方が適すると記事は述べている。エージェント的な機能が必要な場合はClineなどの他拡張との組み合わせも紹介されている。

## アイデア

- LiveCodeBenchで7BモデルがClaude 3.7 Sonnetを上回るという評価結果は、モデルサイズと性能の関係を再考させる。ドメイン特化（競技プログラミング）のファインチューニングが汎用大型モデルを特定タスクで超える好例
- LM StudioがOpenAI互換APIを公開する設計により、既存のOpenAIクライアントコードをそのままローカルLLMに切り替えられる。これはベンダーロックインを避けつつ開発環境を構築する実用的なアーキテクチャパターン
- 「用途によってモデルを使い分ける」アプローチ（アルゴリズム問題→OlympicCoder、API設計→Claude）は、単一モデルへの依存を避けるマルチモデル戦略として、エージェントシステム設計にも応用できる考え方
## 関連記事

- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_1146 1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド](https://huggingface.co/blog/olympic-coder-lmstudio)
