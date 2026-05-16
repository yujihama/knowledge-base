---
title: "技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ"
url: "https://zenn.dev/suwash/articles/markitdown_20260410"
date: 2026-04-13
tags: [MarkItDown, RAG, MCP, LLM前処理, ドキュメント変換, AutoGen, Azure Document Intelligence, Python]
category: "infra"
related: [1247, 682, 858, 1475, 856]
memo: "[Zenn LLM] 技術調査 - markitdown"
processed_at: "2026-04-13T12:50:04.032623"
---

## 要約

MarkItDownはMicrosoftのAutoGenチームが開発したオープンソースのPythonユーティリティで、2024年末に公開後2026年4月時点でGitHubスター数91,000超を誇る。設計思想の核心は「LLMとテキスト分析パイプラインへの入力最適化」であり、人間向けの美しい出力ではなく機械が効率よく読み取れる構造化テキストの生成を優先する。対応フォーマットはDOCX/XLSX/PPTX等のOffice文書、PDF（pdfminer.six + pdfplumber）、画像（EXIF + OCR + LLMキャプション）、音声（WAV/MP3の文字起こし）、HTML/RSS/YouTube URL/Wikipedia、CSV/JSON/XML、ZIP/EPUB/Outlook .msg/Jupyter Notebookと15種以上に及ぶ。アーキテクチャはMarkItDownクラスがオーケストレーターとして機能し、優先度付きConverterRegistrationリストを管理する。各ConverterはDOCXConverter・PdfConverter・ImageConverter等に分割されており、accepts()がTrueを返した最高優先度のConverterが変換を担当する仕組み。PRIORITY_SPECIFIC_FILE_FORMAT=0.0が最高優先度、PRIORITY_GENERIC_FILE_FORMAT=10.0が汎用優先度として定義される。magika（機械学習ベース）によるファイル判定、エントリポイント機構によるプラグイン拡張にも対応。MCPサーバー実装（markitdown-mcp）はSTDIO/Streamable HTTP/SSEの3トランスポートをサポートし、Claude Desktop等のMCP対応AIアシスタントと直接統合可能。Azure Document Intelligenceとの連携により複雑レイアウトPDFの高精度OCRも実現する。Pandoc（60種以上対応だがGPL-2.0かつHaskellランタイム依存）やDocling（IBM製、HFモデル1GB超で重量級）、Unstructured（64種以上対応だがクラウドAPI依存）と比較して、MarkItDownはMITライセンス・軽量Python実装・LLM最適化の三点で優位性を持つ。RAGパイプラインの前処理層としての活用が主なユースケースであり、`pip install 'markitdown[all]'`または用途別extras個別指定でのインストールが可能。監査エージェント開発においては、PDF監査報告書・Excel管理台帳・PowerPointプレゼンテーション等の多様な監査ドキュメントをLLM入力用Markdownに一括変換するデータ前処理層として直接活用できる。MCPサーバーとして起動すればLangGraphエージェントからのドキュメント変換ツール呼び出しも容易になる。

## アイデア

- magika（機械学習ベースのファイル判定）を用いることで拡張子に依存しない堅牢なフォーマット検出が可能になっている点
- MCPサーバーとして起動することでClaude Desktop等のAIアシスタントから直接ファイル変換ツールを呼び出せる設計は、エージェントのツール統合パターンの実例として参考になる
- Converterの優先度レジストリ（PRIORITY_SPECIFIC=0.0, PRIORITY_GENERIC=10.0）とエントリポイント機構によるプラグイン拡張は、監査エージェントの独自フォーマット対応を外部プラグインとして追加できる拡張性を提供する

## 前提知識

- **RAGパイプライン** (TODO: 読むべき)
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **LLMトークン効率** (TODO: 読むべき)
- **pdfminer.six** (TODO: 読むべき)
- **AutoGen** → /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】

## 関連記事

- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- /deep_856 Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで

## 原文リンク

[技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ](https://zenn.dev/suwash/articles/markitdown_20260410)
