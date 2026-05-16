---
title: "Agentic AIはどう攻撃されるのか：EchoLeakをAAEF v0.2.0で解剖する"
url: "https://zenn.dev/mkz0010/articles/91d7120d5c30b9"
date: 2026-05-05
tags: [prompt-injection, AAEF, EchoLeak, CVE-2025-32711, RAG, 行為統制, M365-Copilot, XPIA, trust-level, authorization]
category: "agent-arch"
related: [1116, 2794, 1334, 2103, 861]
memo: "[Zenn LLM] Agentic AIはどう攻撃されるのか：EchoLeakをAAEF v0.2.0で解剖する"
processed_at: "2026-05-05T12:06:15.207989"
---

## 要約

Microsoft 365 CopilotのゼロクリックPIAI脆弱性EchoLeak（CVE-2025-32711）を題材に、Agentic AIにおける行為統制の設計論を展開した記事。EchoLeakは細工された外部メールをRAG文脈に混入させることで、モデルに内部情報を参照させ外部送信経路に乗せるという攻撃構造を持つ。CVSSではCritical扱いで権限不要・ユーザー操作不要・ネットワーク経由という評価がなされている。筆者はこれを「モデルが騙された」という観点だけで捉えることの限界を指摘する。本質は、未信頼入力がモデル文脈に混入し、内部情報アクセスと外部通信という高影響行為に接続された点にある。この問題を分析するフレームとして著者自身が公開するAAEF（Agentic Authority & Evidence Framework）v0.2.0を用いる。AAEFは「Model output is not authority」を基本原則とし、行為をモデル外部のAction Boundaryで認可・境界づけ・証跡化することを要求する。具体的な対策として、①RAGソースにtrust levelやprovenance metadataを付与（AAEF-MEM-02）、②外部コンテンツをデフォルトで信頼済み命令として扱わない（AAEF-MEM-03）、③外部通信・機密データアクセスをHigh-Impact Action（HIA-DATA/HIA-COMM）として分類（AAEF-TOOL-03）、④高影響行為を実行時点で認可（AAEF-AUZ-01）、⑤未信頼コンテンツ由来のツール呼び出しに意図確認・ポリシーチェックを課す（AAEF-TOOL-04）の5点を提示する。Reference ArchitectureではAuthorization Decision Point、Tool Dispatch Enforcement Point、Evidence WriterをTrusted Control Boundaryに配置し、モデルの出力はあくまで「提案」として扱い、Action Boundaryを通過した場合のみ実行される設計を示す。証跡はWhat（何が起きたか）だけでなくWhy（なぜ許可されたか）まで記録することが求められる。監査エージェント開発においては、LangGraphのツール実行層でprovenance情報を保持し、高影響ツール呼び出しをAAEF的なポリシーチェックで包む設計が直接応用可能である。

## アイデア

- モデル出力を権限（authority）として扱わず、Action BoundaryをモデルとTool実行の間に置くアーキテクチャパターンは、LangGraphのToolノード前にポリシーチェックノードを挿入する形で実装可能
- RAGで取得したドキュメントにsource_type/origin/trust_levelのprovenance metadataを付与し、そのメタデータを後段の認可判断に引き渡す設計は、外部ソース由来の情報が高影響行為を誘発するEchoLeak型攻撃への構造的防御になる
- 「外部ドメインへのリンク生成」「外部画像参照」「query parameterへの内部情報埋め込み」もHIA-COMMとして高影響行為に分類する発想は、従来のAPI呼び出し中心のセキュリティ設計では見落としがちな出力経由の情報漏洩経路を体系化している

## 前提知識

- **prompt injection / XPIA** (TODO: 読むべき)
- **RAG（Retrieval-Augmented Generation）** (TODO: 読むべき)
- **Agentic AI / tool-use** (TODO: 読むべき)
- **CVE / CVSS** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力

## 原文リンク

[Agentic AIはどう攻撃されるのか：EchoLeakをAAEF v0.2.0で解剖する](https://zenn.dev/mkz0010/articles/91d7120d5c30b9)
