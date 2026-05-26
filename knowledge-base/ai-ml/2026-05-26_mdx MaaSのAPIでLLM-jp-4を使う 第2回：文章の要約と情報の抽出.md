---
title: "mdx MaaSのAPIでLLM-jp-4を使う 第2回：文章の要約と情報の抽出"
url: "https://zenn.dev/suzumura_lab/articles/535473662dd6d4"
date: 2026-05-26
tags: [LLM-jp-4, mdx-MaaS, MarkItDown, 文書要約, 情報抽出, 日本語LLM, OpenAI互換API, PDF処理]
category: "ai-ml"
related: [2067, 4042, 4324, 2794, 5642]
memo: "[Zenn LLM] mdx MaaSのAPIでLLM-jp-4を使う 第2回：文章の要約と情報の抽出"
processed_at: "2026-05-26T09:02:12.811468"
---

## 要約

本記事は、東京大学鈴村研究室が運用するmdx MaaSプラットフォームのAPIを通じて、国立情報学研究所（NII）主導のLLM-jpチームが開発した日本語特化LLM「LLM-jp-4 32B」を活用し、PDFドキュメントの要約と情報抽出を行う実装方法を解説するチュートリアルシリーズの第2回。

mdx MaaSが提供するのはllm-jp/llm-jp-4-32b-a3b-thinkingの量子化版で、エンドポイントはhttps://api.maas.mdx1.jp/v1。最大コンテキスト長は65,536トークンだが、同時4リクエスト処理のため1リクエストは最大16,384トークンに制限されている。応答までに5〜10分かかる場合がある点が実用上の注意点。

PDF→テキスト変換にはMicrosoftの「MarkItDown」ライブラリ（uv add 'markitdown[all]'でインストール）を使用。同ライブラリはPDF・Word・PowerPoint等の多様な形式をMarkdownテキストに変換する。ただしPDFは文書階層構造を保持しないため、変換後のMarkdownは階層のないフラットなテキストになる点に注意が必要。

API呼び出しにはOpenAIクライアントライブラリをそのまま流用し、base_urlをmdx MaaSのエンドポイントに差し替える形を取る。要約タスクではシステムプロンプトに「優秀な編集者」ロールを設定し、ユーザープロンプトに「次の内容を要約してください。\n\n」＋テキスト本文を付加。temperature=0で再現性を確保する。実験ではLLM-jpプロジェクト紹介論文（21,247文字）を入力として構造化された箇条書きの要約が出力された。

情報抽出タスクでは同じ論文から著者名・所属機関を抽出。function callingは使わずプロンプトのみで実現し、河原大輔（早稲田大）、空閑洋平（東大）、黒橋禎夫（NII/京大）、鈴木潤（東北大/理研）、宮尾祐介（東大）の5名を正確に抽出できた。

監査エージェント開発への示唆として、MarkItDown＋LLM-jp-4の組み合わせは監査報告書や内部統制文書（PDF形式が多い）からの構造化情報抽出パイプラインに直接応用可能。日本語特化モデルであるLLM-jp-4は日本語の法令・会計基準・監査基準といったドメイン文書の処理に優位性がある可能性がある。次回はトークン長超過文書の要約手法が紹介予定。

## アイデア

- OpenAIクライアントライブラリのbase_urlを差し替えるだけで国産日本語LLMをOpenAI互換APIとして利用できる設計は、既存のLLMアプリケーションを国産モデルに移行する際の摩擦を大幅に低減する
- function callingを使わずプロンプトエンジニアリングのみで著者・所属の構造化抽出を実現している点は、ツール非対応モデルでの情報抽出パターンとして汎用性が高い
- mdx（国立情報学研究所・大学共同運営GPUクラスタ）という公共計算インフラ上でLLMをMaaSとして提供するモデルは、商用クラウドに依存しない学術・公共セクター向けAI基盤の一形態として注目に値する

## 前提知識

- **LLM推論API** → /deep_768 Fireworks.aiがHugging Face Hubの推論プロバイダーとして統合
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **MarkItDown** → /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- **モデル量子化** (TODO: 読むべき)

## 関連記事

- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- /deep_4042 LM StudioでLLM-jp4を使う：国産OSS LLMのローカル実行手順と注意点
- /deep_4324 LLM-jp-4をM4 MacBook AirのOllamaで動かしてみた
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針
- /deep_5642 論文メモ：SentencePieceからTokenizationを整理する

## 原文リンク

[mdx MaaSのAPIでLLM-jp-4を使う 第2回：文章の要約と情報の抽出](https://zenn.dev/suzumura_lab/articles/535473662dd6d4)
