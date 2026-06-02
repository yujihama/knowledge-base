---
title: "RAGは検索して終わりではない：TiDB Cloudで作る監査可能なAIメモリ基盤"
url: "https://zenn.dev/tomyuk/articles/29956f1aebc719"
date: 2026-06-02
tags: [RAG, TiDB Cloud, AIメモリ, Lineage, ベクトル検索, 全文検索, ハイブリッド検索, Human-in-the-loop, RDE, 監査可能性]
category: "audit-ai"
related: [5132, 5881, 6255, 5694, 2739]
memo: "[Zenn LLM] RAGは検索して終わりではない：TiDB Cloudで作る監査可能なAIメモリ基盤"
processed_at: "2026-06-02T09:04:37.187944"
---

## 要約

本記事は、RAG（Retrieval-Augmented Generation）を「検索してLLMに渡す仕組み」として捉えるのではなく、AIとの共同作業で生まれる文脈を追跡・評価・更新するための「監査可能なAIメモリ基盤」として再設計する提案である。著者はSayaneというシステム構想を軸に、TiDB Cloud（MySQL互換の分散SQL DB）をバックエンドとした参照実装「sayane-tidb-context-store-demo」をApache 2.0で公開している。

通常のRAGの限界として5点を指摘する。①検索結果の選択理由が記録されない、②LLMによる意味変換が追跡されない、③人間の承認プロセスが弱い、④棄却された候補が消える、⑤複数LLMサービスをまたぐと文脈の来歴が断絶される。

これに対し、Auditable Memory（監査可能なAIメモリ）の核心として「LLMの回答はそのままメモリではなくCandidateである」という設計思想を提示する。Candidateは人間が採用・棄却・修正する一段階を経てはじめてMemory Profileへ反映される。

データモデルは7層に分解される：Source（元情報源とハッシュ）、Chunk（意味単位の断片とembedding）、Retrieval Event（検索方式・スコアの記録）、Context Package（LLMに実際に渡された文脈束）、Generation（モデル名・温度・出力本文）、Candidate（更新候補、状態はpending/approved/rejected等）、Memory Profile（採用済み文脈）、Lineage（全体の来歴チェーン）。さらにRDE（Resonant Deviation Evaluator）という意味変化評価層を設け、「元文脈の何が保存・変換・補完・逸脱されたか」を定量化する。

検索戦略は3層を組み合わせる：ベクトル検索（意味的近傍）、全文検索（固有名詞・バージョン番号・ライセンス等）、構造化SQL検索（承認状態・日付・プロジェクト等のメタデータ絞り込み）。TiDB Cloudはこの3層を単一基盤で扱える点が選定理由として挙げられる。

監査エージェント開発への示唆：内部監査でのAI活用では「AIが何を参照し、どう判断し、人間が何を採用したか」の来歴（Lineage）こそが証跡として機能する。Candidate→承認フローとRDE評価は、LangGraphの条件分岐ノードやHuman-in-the-loopパターンと直接対応し、ReActエージェントにおける「ツール呼び出し履歴の監査」にそのまま応用できる設計思想である。

## アイデア

- LLMの回答をそのままメモリに入れず一度Candidateとして保留し、人間の承認を経て初めてMemory Profileへ反映するという設計は、監査証跡の生成と意思決定責任の明確化を両立する実装パターンとして汎用性が高い
- RDE（Resonant Deviation Evaluator）という「元文脈と生成結果の意味的差分を保存・変換・補完・逸脱の4軸で評価する」層は、LLM-as-judgeの評価軸を来歴データとして永続化する仕組みとして、評価フレームワーク設計に転用できる
- ベクトル検索・全文検索・SQL構造化検索の3層を単一DB（TiDB Cloud）上で統合することで、意味検索と監査条件フィルタ（承認状態・機密度・出典）を同一クエリで扱えるアーキテクチャは、エンタープライズRAGの実装パターンとして参考になる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Vector Embedding** (TODO: 読むべき)
- **TiDB / 分散SQL** (TODO: 読むべき)
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_5132 RAGの精度を上げる：チャンキングとハイブリッド検索をGoで実装した記録
- /deep_5881 金融サービスにおけるエージェントAIのためのデータ準備態勢
- /deep_6255 金融サービスにおけるエージェントAIのためのデータ準備態勢
- /deep_5694 金融サービスにおけるエージェントAIのためのデータ対応戦略
- /deep_2739 制約の多い公共部門環境でAIを実用化する：SLMという選択肢

## 原文リンク

[RAGは検索して終わりではない：TiDB Cloudで作る監査可能なAIメモリ基盤](https://zenn.dev/tomyuk/articles/29956f1aebc719)
