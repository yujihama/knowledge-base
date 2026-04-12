---
title: "図形入りの PowerPoint を Markdown に変換する方法（GitHub Copilot + OpenXML SDK）"
url: "https://zenn.dev/headwaters/articles/convert-pptx-with-shapes-to-markdown"
date: 2026-03-29
tags: [OpenXML SDK, GitHub Copilot, Mermaid, PowerPoint, DevContainer, C#, dotnet, Markdown変換]
category: "infra"
memo: "図形入りの PowerPoint を Markdown に変換"
processed_at: "2026-03-29T21:54:31.452295"
---

## 要約

日本マイクロソフトのリポジトリを参考に、図形・コネクタ・テーブルを含む複雑な PowerPoint ファイルを Mermaid 図入り Markdown に変換する手順をまとめた記事。環境構築は DevContainer（C#/.NET）または GitHub Codespaces で行い、OpenXML SDK を用いて .pptx の XML を解析する。GitHub Copilot は slash command `/scripting-guide` でスキルを明示的に指定しないと Python で実装しようとするため、dotnet を強制する工夫が必要。変換処理は複数段階のコード生成で構成され、①スライド全体のテキスト・図形数の把握、②各図形の位置・サイズ・接続関係（spTree の sp/cxnSp/graphicFrame）の詳細抽出、③LLM による Mermaid 図への意味推定、という流れで行われる。最終的な Markdown は VSCode 拡張（markdown-mermaid, markdown-pdf）でレンダリング・PDF化が可能。Claude Sonnet 4.6 クラスのモデルであれば変換精度が高いと言及されている。

## 要点

- GitHub Copilot に特定ツール（dotnet）を使わせるには、slash command でスキルを明示指定し、絶対パスでファイルを指定することで成功率が上がる
- OpenXML SDK は .pptx の XML を spTree 単位で解析し、図形（sp）・コネクタ（cxnSp）・グラフィックフレーム（graphicFrame）の位置・サイズ・接続関係を EMU 座標で取得できる
- 複雑な図形の Mermaid 変換は LLM による多段階コード生成で実現され、Claude Sonnet 4.6 クラスのモデルで高精度な変換が可能

## 監査エージェントへの示唆

監査業務では PowerPoint 形式の報告書や内部統制フローチャートを扱うことが多く、OpenXML SDK による図形・接続関係の構造化抽出は、エージェントが非構造化ドキュメントをグラフ構造として取り込む際の前処理パイプラインとして応用できる。また、LLM に slash command でスキルを明示指定して特定ツール使用を強制するプロンプト設計は、エージェントのツール選択制御にも参考になる。

## 原文リンク

[図形入りの PowerPoint を Markdown に変換する方法（GitHub Copilot + OpenXML SDK）](https://zenn.dev/headwaters/articles/convert-pptx-with-shapes-to-markdown)
