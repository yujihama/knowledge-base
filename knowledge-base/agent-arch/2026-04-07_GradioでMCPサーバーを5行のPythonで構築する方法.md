---
title: "GradioでMCPサーバーを5行のPythonで構築する方法"
url: "https://huggingface.co/blog/gradio-mcp"
date: 2026-04-07
tags: [MCP, Gradio, LLM-tool-calling, HuggingFace, SSE, Python, MCP-server]
category: "agent-arch"
memo: "[HF Blog] How to Build an MCP Server with Gradio"
related: [528, 88, 13, 1354, 708]
processed_at: "2026-04-07T21:38:28.735917"
---

## 要約

GradioはPythonでMLモデルのUIを構築するライブラリで、月間100万人以上の開発者が利用している。2025年4月のアップデートにより、`demo.launch(mcp_server=True)` の1パラメータ追加だけでGradioアプリをMCP（Model Context Protocol）サーバーとして公開できるようになった。MCPサーバーとして起動すると、通常のWeb UIと並行してSSEエンドポイント（`http://your-server:port/gradio_api/mcp/sse`）が立ち上がり、Claude Desktop、Cursor、ClineなどのMCPクライアントからLLMのツールとして呼び出せる。

技術的な仕組みとして、GradioはAPIエンドポイントごとにMCPツールへの自動変換を行う。関数のdocstringがツールの説明とパラメータスキーマに変換され、`http://your-server:port/gradio_api/mcp/schema` でスキーマを確認できる。Claude DesktopはSSE方式に未対応のため、Node.jsの`mcp-remote`経由での接続が必要。

2025年9月のアップデートではMCP仕様のResources・Promptsにも対応した。`@gr.mcp.resource("greeting://{name}")`デコレータでデータ公開用リソース、`@gr.mcp.prompt()`デコレータで再利用可能なプロンプトテンプレートを定義できる。また`gr.api()`を使うことでUI上には表示せずMCPのみに公開するMCP専用関数も作成可能。

ファイル処理は自動化されており、base64エンコード文字列のファイルデータへの変換、画像ファイルの適切なフォーマット処理、一時ファイルストレージ管理が透過的に行われる。パフォーマンス分析機能として、成功率・レイテンシパーセンタイル・リクエスト数の自動計測と可視化も提供される（成功率100%は緑、0%は赤、中間はオレンジでカラーコーディング）。

Hugging Face Spacesへ無料でデプロイでき、ホスト型MCPサーバーとして公開可能。認証強化機能として、Hugging Face Spacesの既存OAuth認証とシームレスに統合できる。さらにOpenAPI仕様からMCPサーバーへの変換機能もサポートし、既存のREST APIをMCPツールとして再公開する用途にも対応している。

## アイデア

- docstringをそのままMCPツールのスキーマ定義として活用する設計は、既存のPython関数を最小変更でMCPツール化できる実用的なアプローチ
- gr.api()によるMCP専用関数の仕組みは、LLM向けのバックエンドAPIとユーザー向けUIを同一コードベースで分離管理できる点が興味深い
- OpenAPI仕様からMCPサーバーへの自動変換機能は、既存の内部REST APIをLLMエージェントのツールとして低コストで公開できる可能性を示している
## 関連記事

- /deep_528 Gradio MCPサーバーの5つの大きな改善点（v5.38.0）
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装
- /deep_1354 Hugging Face Hub：美術館・図書館・文書館・博物館（GLAM）向け活用ガイド
- /deep_708 Gradioの新しいDataframeコンポーネント：70件以上の改善を含む大型アップデート

## 原文リンク

[GradioでMCPサーバーを5行のPythonで構築する方法](https://huggingface.co/blog/gradio-mcp)
