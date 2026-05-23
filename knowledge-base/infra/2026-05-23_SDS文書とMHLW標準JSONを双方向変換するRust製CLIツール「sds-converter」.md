---
title: "SDS文書とMHLW標準JSONを双方向変換するRust製CLIツール「sds-converter」"
url: "https://zenn.dev/kent_kamome/articles/8c83babdbb5637"
date: 2026-05-23
tags: [Rust, LLM, SDS, MHLW, JIS Z 7253, Claude, Ollama, 構造化出力, CLI, 化学品管理]
category: "infra"
related: [5037, 4475, 2872, 5721, 6006]
memo: "[Zenn LLM] SDS文書とMHLW標準JSONを双方向変換するRustツールを作ってみた"
processed_at: "2026-05-23T09:01:57.374786"
---

## 要約

安全データシート（SDS）文書を厚生労働省が2025年3月に公開した「SDS情報交換のための標準的フォーマット v1.0」（JSON形式）へ変換し、逆変換（JSON→Word文書）も行うRust製CLIツール「sds-converter」の開発記録。JIS Z 7253に基づく16項目のSDS情報を、約200フィールドを持つMHLWスキーマに正確にマッピングする。ルールベースパーサが非現実的な理由として、メーカーごとのフォーマット差異・第3項（成分・含有量）の構造の多様性・第9項（物理化学的性質）における「N/A」「測定なし」等のテキスト値問題・MHLWスキーマ自体に存在するタイポ（"HumanExposureAndEmergencyMeasuress"等）への対応を挙げ、LLMによる変換を採用。バックエンドはClaude（Haiku/Sonnet）・GPT・Gemini・ローカルLLM（Ollama等）を差し替え可能。変換処理は16項目をGROUP_A（第1〜9項）とGROUP_B（第10〜16項）に分けて2並列でLLMを呼び出し、レイテンシを半減。HTTPレート制限（429/529）には指数バックオフ（2秒→4秒→8秒）で最大3回リトライ。品質プリセット（low/medium/high）でコストと精度のトレードオフを調整でき、highではSonnet-4.6を使用して最大60,000文字のコンテキストを渡す。LLMの課題として幻覚（数値フィールドへの補完）・構造化出力の不安定さ・型変換ミスを挙げ、validateコマンドによる後検証で対応。ライブラリクレート（sds-converter-core）としても提供され、Rustアプリへの組み込みが可能。監査AIへの示唆として、法定文書（SDS等）の電子化・標準化フローにおけるLLM活用パターン——ルールベース不可→LLM抽出→スキーマバリデーション——は、内部統制文書や監査証跡の構造化にも転用できる設計思想を示している。

## アイデア

- MHLWスキーマのタイポ（'Desclaimer'等）をそのまま再現しなければバリデーションが失敗するという「仕様としてのバグ」への対応は、実務的な標準化文書処理の難しさを示している
- 16項目を2グループに並列LLM呼び出しするアーキテクチャは、長文書のコンテキスト制限を回避しつつレイテンシを削減する実践的パターンで、監査エージェントの証跡分析にも応用可能
- 法定文書のルールベースパーサが「メーカー数×フォーマット差異」で指数的に複雑化する問題をLLMで解決するアプローチは、内部統制文書・契約書・規制報告書の自動構造化にも横展開できる

## 前提知識

- **Rust async/tokio** (TODO: 読むべき)
- **構造化出力（JSON Schema）** (TODO: 読むべき)
- **LLM hallucination対策** (TODO: 読むべき)
- **JIS Z 7253 / GHS** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】

## 関連記事

- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_4475 採点基準v2改訂で「直感力9点」が認定された——LLM個人アセスメントプロンプト設計の実践記録
- /deep_2872 file-splitter：ローカルLLM時代のファイル分割ツール
- /deep_5721 RAGナレッジベース作成を簡単にしたくてツールを作った（mrag）
- /deep_6006 Claudeに4カ国の祖父母の話を聞いたら、回答の『生成過程』に大きな差が出た

## 原文リンク

[SDS文書とMHLW標準JSONを双方向変換するRust製CLIツール「sds-converter」](https://zenn.dev/kent_kamome/articles/8c83babdbb5637)
