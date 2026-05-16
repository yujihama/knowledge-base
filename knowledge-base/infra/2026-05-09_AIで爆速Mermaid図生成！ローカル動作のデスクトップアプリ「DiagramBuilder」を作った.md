---
title: "AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った"
url: "https://zenn.dev/nuldev0/articles/717010cc00f7da"
date: 2026-05-09
tags: [Electron, Mermaid.js, Next.js, Ollama, ローカルLLM, TypeScript, DOMPurify, keytar, 図自動生成]
category: "infra"
related: [3903, 3642, 2209, 4176, 4029]
memo: "[Zenn LLM] AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリを作った"
processed_at: "2026-05-09T09:34:57.476842"
---

## 要約

DiagramBuilderは、Electron + Next.js 16 + TypeScript + Mermaid.js v10 を組み合わせたローカル動作のデスクトップアプリ。要件を日本語で入力するだけでMermaid図を自動生成・編集・管理できる。フローチャート・シーケンス・ER・クラス・ガント・マインドマップ・状態遷移・ネットワーク構成図など11種類の図に対応。LLMはClaude / OpenAI / Gemini / Ollama / Azure OpenAI / カスタム（OpenRouter等）から選択可能で、OllamaによるフルローカルLLM運用も対応。

技術スタックはフロントエンドにNext.js 16 + React 19 + Tailwind CSS v4、バックエンドにNode.js + Express、デスクトップ層にElectronを採用。APIキーはOS標準のキーチェーン（keytar）に暗号化保存することでGitリポジトリへの流出を防ぐ設計。Mermaid生成SVGはDOMPurifyでサニタイズしてXSSを対策。Electron + Next.js standalone ビルドの組み合わせでは、パッケージング後にsystem PATHが制限されるためHomebrew配下（/opt/homebrew/bin/node等）を明示探索するロジックを実装しており、静的ファイルのCSSコピー漏れという落とし穴も解説している。

既存ツール（Mermaid Live Editor・ChatGPT・draw.io・Eraser.io）の欠点──AI生成の欠如・管理機能なし・クラウド前提──を一括解消するために開発。図のフォルダ管理・タグ検索・ソート機能のほか、複数図をまとめて表紙付きPDF出力する機能も備える。macOS (Apple Silicon/Intel) とWindows向けにGitHub Releasesで配布中（v1.2.0）。

監査エージェント開発への示唆としては、機密情報を含む仕様書や業務フローをローカルLLM（Ollama）で処理しながらMermaid形式のシステム構成図・シーケンス図を自動生成するパイプラインに直接転用できる。LangGraphの状態遷移やReActループの可視化ドキュメント生成にも応用可能。

## アイデア

- APIキーをOSキーチェーン（keytar）に暗号化保存することで、Gitリポジトリへの秘密情報流出を構造的に防ぐ設計パターン
- Electron + Next.js standalone ビルドの組み合わせにおけるsystem PATH制限の回避策（Homebrew明示探索ロジック）
- OllamaによるフルローカルLLM運用でAPI不要・機密情報漏洩ゼロの図生成パイプラインを実現する構成

## 前提知識

- **Electron** (TODO: 読むべき)
- **Mermaid.js** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Next.js standalone** (TODO: 読むべき)
- **DOMPurify** (TODO: 読むべき)

## 関連記事

- /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4029 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤

## 原文リンク

[AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った](https://zenn.dev/nuldev0/articles/717010cc00f7da)
