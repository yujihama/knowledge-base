---
title: "【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う"
url: "https://zenn.dev/michy/articles/db76efae494691"
date: 2026-04-08
tags: [MarkItDown, RAG, 前処理, PDF変換, Markdown, LLM, uv, Office文書]
category: "infra"
memo: "[Zenn LLM] 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う"
processed_at: "2026-04-08T09:01:17.405396"
---

## 要約

MicrosoftのOSSライブラリ「MarkItDown」（v0.1.5以降）を使い、PDF・Excel・PowerPoint・WordファイルをMarkdown形式に一括変換する手順をまとめた記事。uvによるパッケージ管理で`markitdown[all]`を導入し、最小3行のコードで単一ファイル変換が可能。複数ファイルの一括変換スクリプトでは、変換失敗時も処理継続するエラーハンドリングを実装している。

検証は公開資料4種（原子力白書概要版PDF、退職手当支給状況Excel、オープンデータ基本指針PPTX・DOCX）で実施。全4件の変換が成立。形式別の特徴として、PDFは章構成・見出しテキストの抽出は可能だが画像は欠落する。Excelはシート内容がMarkdownテーブルに変換されるが列数が多いと可読性が低下する。PPTXはスライド単位でMarkdown化されるため検索による該当ページ特定に有用だが、テキストボックスの位置関係は失われる。DOCXは本文テキストの抽出精度が最も高いが図版・装飾の再現は不可。マクロ付きxlsmファイルではマクロ情報は出力されず、シート上の値のみテキスト化される。

著者の総括は「ドキュメントの完全再現・置き換え」ではなく「文字データを取り出して検索や下流処理に渡す」用途に適しているというもの。RAGパイプラインのインジェスト前処理や全文検索インデックス構築の補助ツールとして有効であり、元ファイルの廃棄は不可。MissingDependencyExceptionが発生した場合は`markitdown[all]`か必要なextrasの追加で対処できる。

## アイデア

- PPTXをページ単位でMarkdown化することでスライド番号をメタデータとして検索できる点は、大量スライドのRAG検索で参照箇所を特定しやすくする実用的な設計
- 変換失敗時も処理継続するエラーハンドリングパターンは、大量ファイルのバッチ処理パイプラインで品質を落とさずスループットを維持するための基本実装として参考になる
- MarkItDownは構造抽出に特化しており完全再現を目的としないという明確な位置づけが、ツール選定時のRAG前処理パイプライン設計の指針になる

## Yujiの取り組みへの示唆

監査エージェント開発において、監査調書・規程・基準書（PDF/Word/Excel形式）をRAGのコンテキストとして取り込む際、MarkItDownによるMarkdown前処理はインジェストパイプラインの標準コンポーネントになりうる。LangGraphのワークフロー内でドキュメント取得ノードとしてMarkItDownを組み込み、Pydanticモデルで変換結果の構造を定義してチャンクサイズや抽出品質を管理するアーキテクチャが想定できる。ただし、監査証拠として原本保全が必要な場面では「Markdown化＝原本代替不可」という本記事の結論を前提に、元ファイルとの参照関係を設計に含める必要がある。

## 原文リンク

[【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う](https://zenn.dev/michy/articles/db76efae494691)
