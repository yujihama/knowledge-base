---
title: "1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった"
url: "https://zenn.dev/tktomaru/articles/bonsai_demo_20260406"
date: 2026-04-09
tags: [Bonsai-8B, 1-bit量子化, llama.cpp, PrismML, GGUF, ローカルLLM, CUDA, Docker, RTX-4060, Windows]
category: "infra"
memo: "[Zenn LLM] 1-bit Bonsai 8Bを触ってみた。爆速だったが、普段のllama.cpp運用にはそのまま載らなかった"
processed_at: "2026-04-09T12:38:50.820089"
---

## 要約

PrismML製の1-bit量子化モデル「Bonsai 8B」をWindows + RTX 4060環境でローカル実行した検証記録。まず動作確認には公式のBonsai-demoリポジトリを使用し、setup.ps1でバイナリとモデル（GGUF形式）をまとめてセットアップ。llama-cli.exeに-ngl 99を渡してGPUオフロードを有効化することで、「軽快」と表現される高速推論を確認した。

最大のハマりポイントは、既存のghcr.io/ggml-org/llama.cpp:server-cudaベースのDocker構成にモデルファイルを差し替えるだけでは動作しなかった点。Bonsaiは通常のGGUFとしてllama.cppが扱えるフォーマットではなく、PrismML側の1-bit前提実装に依存しているため、既存の汎用llama.cppコンテナでは起動できなかった。これは「GGUFなら何でも同じ」という前提が崩れる典型例。

日本語処理については、-pフラグで日本語を直接渡すとPowerShell環境で文字化け（UTF-8エンコーディング問題）が発生。回避策として、(1) UTF-8 BOMなしでprompt.txtを書き出してから-fで渡す、(2) 引数なしで起動して対話入力する、の2方法が有効。応答内容は「こんにちは！私はBonsaiと呼ばれています」のような基本的な日本語は問題なし。

ただし「作業エージェント」としての能力は限定的。「MCPでファイルを読めますか」と質問するとModel Context Protocolではなく別の意味に解釈する誤りが発生。ローカルファイル操作についても「自分では直接読めない、PowerShellやPythonを使う必要がある」という返答にとどまり、ツール連携の文脈理解は弱い。

著者の結論は「速い前段モデル」としての活用。軽量チャット応答・一次要約・一次分類・下書き生成を担わせ、難しい判断は別モデル、実作業はMCP/ツールに委ねるハイブリッド構成が適切とのこと。GPU 8GB級で動作可能なため、リソース制約がある環境での一次処理ステージに有用。

## アイデア

- 1-bit量子化モデルはGGUFフォーマットであっても汎用llama.cppランタイムとの互換性が保証されず、専用ランタイム（Bonsai-demo）が必要な点は、モデル配布・運用設計の標準化問題として注目に値する
- PowerShell環境での-pフラグ日本語文字化けは、Windows向けLLMツールのUTF-8ハンドリング問題を示しており、-fオプション（ファイル経由入力）が回避策になるというパターンは他のllama.cpp系ツールにも応用できる
- 「速い前段モデル + 強いモデルで判断 + MCPで実作業」というハイブリッド構成は、コスト・レイテンシ最適化のマルチモデルオーケストレーションパターンとして実践的な設計指針になる
## 関連記事

- /deep_1143 AIがスマホで動く時代が来た — エッジAIとは何か、何が変わるのか、Bonsai 8Bを動かしてみた
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）

## 原文リンク

[1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった](https://zenn.dev/tktomaru/articles/bonsai_demo_20260406)
