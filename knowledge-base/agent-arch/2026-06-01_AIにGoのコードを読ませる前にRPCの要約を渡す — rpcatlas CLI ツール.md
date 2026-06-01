---
title: "AIにGoのコードを読ませる前にRPCの要約を渡す — rpcatlas CLI ツール"
url: "https://zenn.dev/usuginu/articles/2e601d3c01196c"
date: 2026-06-01
tags: [rpcatlas, gRPC, Go, 静的解析, AST, LLMコンテキスト最適化, AIコードレビュー, Clean Architecture, call graph, CI]
category: "agent-arch"
related: [3340, 1917, 764, 6194, 4384]
memo: "[Zenn LLM] AI に Go のコードを読ませる前に RPC の要約を渡す"
processed_at: "2026-06-01T09:05:26.506525"
---

## 要約

Go の gRPC コードベースを AI にレビューさせる際、AI が毎回 grep を繰り返してトークンを無駄遣いする問題を解決するために作られた CLI ツール「rpcatlas」の紹介記事。`go install github.com/usuginus/go-rpcatlas/cmd/rpcatlas@latest` でインストールでき、DB・ビルド・サーバ不要でソースコードのみから動作する。

主な機能は「RPC ごとの処理フローを Markdown または JSON で出力する」こと。`--list` で検出可能な RPC を一覧表示し、`--rpc CreateFoo --depth 5 --format markdown` のように指定すると4種類の情報を出力する：(1) execution summary（handler、request/response 型、各 layer の呼び出し件数）、(2) call tree（handler → usecase → repository → external_client の層別ツリー）、(3) function index（layer ごとの関数一覧）、(4) decision points（interface calls・function values・conditional paths・keyed dispatches）。

設計方針は「完全な解析器を目指さない」こと。runtime 経路の証明ではなくレビュー・調査の入口として「読む順番が分かれば十分」という割り切りのもと、AST ベースの静的解析のみで実装されている。gopls・SSA・LSP を使わず go/ast のみに依存するため、多くのケースで 1 秒以内に結果を返す。

CodeGraph 系ツール（index 構築・graph DB・MCP 経由）と比較すると、rpcatlas はステートレス・ビルド不要・前準備なしの点で「CI 上の AI レビュー」や「Slack bot からの呼び出し」に向いている。.rpcatlas.yaml でハンドラ検出ルールや layer 分類ルールをカスタマイズでき、チームのアーキテクチャ用語（application・persistence・gateway など）に合わせられる。

監査エージェント開発への示唆：監査エージェントが大規模コードベースを調査する際、rpcatlas のように「事前に構造化されたコンテキスト」を LLM に渡す設計パターンは有効。特に Clean Architecture・DI・interface 解決の情報を事前整形することで、LLM の探索コスト（トークン・レイテンシ）を削減できる。エージェントに grep を自律的にさせるより、専用の静的解析ツールでコンテキストを前処理してから渡す「コンテキスト前処理パターン」として応用できる。

## アイデア

- LLM に自律的な grep をさせるより、専用 CLI で構造化コンテキストを事前生成して渡す「コンテキスト前処理パターン」はエージェント設計の一般原則として応用できる
- interface calls・keyed dispatches・conditional paths を decision points として独立出力する設計により、DI や map dispatch による実装切り替えを grep では見落としやすい箇所を明示できる
- AST ベースのみでステートレス・ビルド不要を実現する設計は、CI パイプラインや Slack bot のように「その場で即時実行」が求められる場面での静的解析ツール設計の参考になる

## 前提知識

- **gRPC** → /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- **Go AST** (TODO: 読むべき)
- **Clean Architecture** → /deep_1917 GoエンジニアのためのRAG実践入門
- **Static Analysis** (TODO: 読むべき)
- **LLM Context Window** (TODO: 読むべき)

## 関連記事

- /deep_3340 Stena Expenseの検知アーキテクチャ ── Go × Python × gRPCで不正検知を実現する仕組み
- /deep_1917 GoエンジニアのためのRAG実践入門
- /deep_764 生成しながら実行する：LLMコード生成における実行レイテンシの隠蔽
- /deep_6194 急変するAIコードレビューツール市場：2026年版比較と選び方
- /deep_4384 命令型プログラムのグラフ構築とマッチング：ニューラル手法と構造的手法の統合

## 原文リンク

[AIにGoのコードを読ませる前にRPCの要約を渡す — rpcatlas CLI ツール](https://zenn.dev/usuginu/articles/2e601d3c01196c)
