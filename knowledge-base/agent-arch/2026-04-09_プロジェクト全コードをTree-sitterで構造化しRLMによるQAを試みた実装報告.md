---
title: "プロジェクト全コードをTree-sitterで構造化しRLMによるQAを試みた実装報告"
url: "https://zenn.dev/yumefuku/articles/codetwine-rlm"
date: 2026-04-09
tags: [RLM, Tree-sitter, DSPy, AST, コード解析, 依存関係グラフ, RAG, Python REPL, LLM-as-agent]
category: "agent-arch"
memo: "[Zenn LLM] プロジェクト内の全コードをTree-sitterで構造化 → RLMによるQAを試してみた"
processed_at: "2026-04-09T09:39:28.096032"
---

## 要約

本記事は、RLM（Retrieval with Language Models）という手法をソースコードのQAに適用した実験報告である。RLMはLLMにコンテキストを直接渡さず、Python REPL環境の変数にデータを格納した上でLLM自身がPythonコードを生成・実行しながら必要な情報を探索・抽出する手法（arxiv: 2512.24601）。通常のRAGとは異なり、ベクトル検索による上位N件取得ではなく、情報同士の繋がりや複雑な条件検索にも対応できる点が特徴。著者はcodetwineというツールを開発し、プロジェクトのソースコードをTree-sitterで構文解析してAST（実際はCST）ノードから関数・クラス定義を抽出し、ファイル間依存関係グラフ（トポロジカルソート使用）とLLM生成の詳細設計書を単一のproject_knowledge.jsonに統合する。対応言語はPython/JavaScript/TypeScript/Java/Kotlin/C/C++。処理は5ステップ：依存関係グラフ構築→変更ファイル検出（ハッシュ比較）→依存関係情報抽出→LLMによる設計書生成→JSON保存。RLMの実行にはDSPyのRLMモジュールとDenoランタイムを使用。実際にcodetwine自身（約4000行）をClaude Sonnet 4.6で構造化した際のAPI料金は3.5ドル。RLMのQA実行コードはDSPyを使い、メインLLMにClaude Opus 4.6、サブLLMにClaude Sonnet 4.6を想定した実装となっている。キーワード検索・エントリーポイント探索・依存関係調査などのコード例も提示されており、大規模コードベースへの適用可能性を示している。

## アイデア

- LLMにコンテキストを渡さずPython REPLの変数として保持し、LLM生成コードで探索させるRLMアーキテクチャは、超大規模コンテキストのロスト・イン・ザ・ミドル問題を根本から回避する設計
- トポロジカルソートで依存先→依存元の順に設計書を生成し、後続ファイルの処理時に依存先ドキュメントを入力に含める連鎖的ドキュメント生成パイプラインは、コードベース全体の意味理解を段階的に構築する
- ハッシュ比較による差分検出で変更ファイルのみ再処理する設計により、大規模プロジェクトへの増分更新が実用的なコスト（4000行で3.5ドル）に収まっている

## Yujiの取り組みへの示唆

監査エージェント開発において、LangGraphやPydanticで構築した自身のエージェントシステムのコードベースをcodetwineで構造化し、RLMでQAすることで設計書の自動生成や依存関係の可視化に活用できる。特にRLMのアーキテクチャ（コードをPython変数として保持しLLM生成コードで探索）はLangGraphのステートグラフ上でのReActループと相性がよく、監査証跡の大規模JSONデータへの適用も検討に値する。DSPyのRLMモジュールを通じてGRPO/RLAIF的な観点でのコード生成品質評価基盤としても応用できる。

## 原文リンク

[プロジェクト全コードをTree-sitterで構造化しRLMによるQAを試みた実装報告](https://zenn.dev/yumefuku/articles/codetwine-rlm)
