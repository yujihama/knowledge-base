---
title: "「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG"
url: "https://zenn.dev/msmtec/articles/bedrock-kb-rag"
date: 2026-04-16
tags: [Amazon Bedrock, RAG, Knowledge Bases, Streamlit, boto3, Claude Haiku, ベクトルストア, S3, チャンキング, 社内ドキュメント]
category: "infra"
related: [969, 1917, 1785, 1848, 1116]
memo: "[Zenn LLM] 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG"
processed_at: "2026-04-16T12:42:23.879840"
---

## 要約

ミスミグループのエンジニアが、ビジネス部門から「社内ドキュメントをAIに学ばせたい」という要望を受け、Amazon Bedrock Knowledge Basesを用いて1日でRAGのサンプルを構築・デモした取り組みの記録。対象ドキュメントは機械設計に関する設計標準や教育資料など。

実装の流れは「S3へのドキュメント配置 → ナレッジベース作成・同期 → APIからの呼び出し」という3ステップ。Bedrock Knowledge Basesは埋め込み・ベクトルストア・検索パイプラインをコード不要で構築できるマネージドサービスであり、S3の他にウェブクローラやSharePointもデータソースとして選択可能。

埋め込みモデルはAmazon Titan Embeddings V2を採用し、デモ目的で最小の256次元を選択。ベクトルストアにはOpenSearch Serverless、Amazon S3 Vectors、Aurora、Neptune Analytics（グラフRAG向け）が選択肢として提供される。チャンキング戦略は固定トークン数分割や意味類似度分割から選択でき、画像を多く含む文書ではClaudeやNovaシリーズのモデルをパーサーとして使うオプションもある（今回はデフォルトパーサーを使用）。

97ファイルのドキュメント同期は1〜2分で完了。APIはRetrieveAndGenerateを使用し、質問文を渡すだけで検索から回答生成まで一括実行。レスポンスには回答本文に加え参照元ドキュメントのソースチャンク情報が含まれ、根拠のトレーサビリティが確保される。

フロントエンドはStreamlitで実装（コードはClaude生成）。チャット形式のUIに加え、参照元ドキュメントの全文をエキスパンダーで表示する機能を付与。モデルはClaude Haiku 4.5（claude-haiku-4-5-20251001）を使用、boto3経由でbedrock-agent-runtimeクライアントから呼び出す。

「サーボモータの選定基準」「ボールねじの寿命計算方法」などの質問に対し、対象ドキュメントを参照した回答が得られた。ビジネス側の反応も良好で、たたき台としての目的は達成。最終的には社内既存のRAGベースAIアシスタントにドキュメントを追加する形で対応することになり、本サンプルは直接の本番導入には至らなかったが、2週間かかる社内プロセスの前に方針合意を得られた点で有意義だったと評価されている。

監査エージェント開発への示唆として、「精度より先に体験を見せる」プロトタイピング戦略は、内部監査領域でのAI導入においても有効なアプローチであり、Bedrock Knowledge Basesの参照元トレーサビリティはエビデンス管理の観点からも活用可能。

## アイデア

- 「完璧より、まず見せる」戦略：精度作り込みより動くデモを優先することで、2週間かかる社内プロセスの前に方針合意を得られた。承認プロセスの長い組織でのAI導入に有効なパターン
- RetrieveAndGenerate APIのソースチャンク付きレスポンス：回答根拠のトレーサビリティがAPIレベルで保証されており、監査・コンプライアンス用途や根拠確認が必要な業務ドキュメント検索に直接活用できる設計
- Neptune Analytics（グラフRAG向け）がベクトルストアの選択肢に含まれている点：通常のRAGではなくグラフ構造を活かした検索が必要なユースケース（規程間の参照関係など）への応用可能性

## 前提知識

- **RAG（Retrieval-Augmented Generation）** (TODO: 読むべき)
- **ベクトル埋め込み** (TODO: 読むべき)
- **Amazon Bedrock** (TODO: 読むべき)
- **チャンキング戦略** (TODO: 読むべき)
- **boto3** (TODO: 読むべき)

## 関連記事

- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- /deep_1917 GoエンジニアのためのRAG実践入門
- /deep_1785 CloudflareスタックだけでブラウザゲームのNaive RAGシステムを構築する
- /deep_1848 🤗 データ測定ツール紹介：データセット分析のためのインタラクティブツール
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG](https://zenn.dev/msmtec/articles/bedrock-kb-rag)
