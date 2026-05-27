---
title: "Difyで社内問い合わせAIを作ってみた — 情シス・人事・経費の質問に答える5つのKnowledge"
url: "https://zenn.dev/makinestai/articles/dify-vs-claude-ops-rag-20-cases"
date: 2026-05-27
tags: [Dify, RAG, Claude Sonnet 4.5, ノーコード, 社内問い合わせAI, Prompt Caching, LLM-as-judge, 評価ハーネス, Knowledge検索]
category: "agent-arch"
related: [6276, 112, 2563, 75, 5962]
memo: "[Zenn LLM] Dify で社内問い合わせ AI を作ってみた — 情シス・人事・経費の質問に答える 5 つの Knowledge"
processed_at: "2026-05-27T09:03:42.766901"
---

## 要約

中堅企業（従業員100〜500名規模）向けの社内問い合わせAIをDify + Claude Sonnet 4.5で実装し、OSSとして公開した実装ノート。情シスFAQ・人事規則・経費規則・情シスセキュリティ規則・マニュアルの5つのKnowledgeを構築し、Difyのノーコードワークフローで並列検索→Claude応答生成というパイプラインを実現した。

構成の核心はRAG（Retrieval Augmented Generation）で、ユーザーの自然言語質問に対して4つのKnowledgeを同時並列検索し、上位3件をClaude Sonnet 4.5に渡して引用付き回答を生成する。Claudeには繰り返し呼び出しコストを下げるPrompt Cachingを適用している。文章のベクトル化にはOpenAI埋め込みAPIを使用。

品質評価は「評価ハーネス」と呼ぶ5軸採点スクリプトで実施した。20ケース（情シスFAQ 8件・人事規則5件・経費規則5件・マニュアル参照2件）を投入し、別インスタンスのClaude Sonnet 4.5をjudge（採点AI）として使用。accuracy（正確性/50点）・coverage（網羅性/20点）・tone（トーン/10点）・latency（応答時間/10点）・cost（APIコスト/10点）の配点で採点した結果、平均89.10点・中央値90点・最小83点を記録。応答時間の中央値は17.80秒、1件あたりコストは平均3.91円。コンプライアンスpass率100%（個人情報リーク・不適切言及なし）。

比較として素のAnthropic SDK実装（全ファイルをsystemプロンプトに詰める構成）でも同20ケースを評価したところ平均89.45点とほぼ同スコアだったが、Dify版はノーコードで運用担当者がStudio画面から検索件数・類似度閾値・プロンプト・最大応答長をコード変更なしで調整できる点が保守コスト低減において優位。

実装ハマりポイントとして、Dify v1.xのDSL（ワークフロー設定YAML）はバージョン番号をv0.3.0に上げる必要があること、Claudeモデル名は日付サフィックス付き（`claude-haiku-4-5-20251001`形式）でなければ認識されないこと、edgesノードに必須フィールドが存在すること、ワークフローモードは専用APIエンドポイントを使う必要があることが報告されている。公式ドキュメントではカバーされておらずソースコードの型定義を直接読む必要があった。

v0.2ロードマップではPDFマニュアルの図表検索（マルチモーダル対応）と日本語特化リランカー（再順位付け）の評価を予定。監査AI開発への示唆として、本構成の評価ハーネス（5軸ルーブリック＋judge AI）はドメインを変えてもrubricとjudgeプロンプトの差し替えだけで流用可能であり、監査エージェントの応答品質測定基盤として転用できる。

## アイデア

- 評価ハーネス（5軸ルーブリック＋judge AI）をドメイン横断で流用する設計思想：「成果物より測る仕組みを作る」ことで別ドメイン展開のコストを大幅削減できる
- Dify Studio上のノーコード運用が保守引き渡しコストを下げる：エンジニア不在の現場でも担当者が検索パラメータやプロンプトを直接調整でき、SIer的な業務AI案件で実用的
- 素のSDK実装（全文systemプロンプト詰め込み）とRAG構成でスコアがほぼ同等（89.45 vs 89.10）という結果は、小規模ドキュメント（17Kトークン）ではRAGの優位性よりもスケーラビリティや運用性で選択判断すべきことを示唆する

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Dify** → /deep_1908 DifyのテキストノードによるPDF構造崩壊の根本原因特定と、Geminiへの直接渡しによる解決
- **Prompt Caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **ベクトル検索** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装

## 関連記事

- /deep_6276 製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_2563 文字通りの要約を超えて：医療SOAPノート評価におけるハルシネーションの再定義
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成
- /deep_5962 ゼロコードMemGPT：GeminiとNotebookLMの循環ループでAIの長期記憶を実現する二層分離アーキテクチャ

## 原文リンク

[Difyで社内問い合わせAIを作ってみた — 情シス・人事・経費の質問に答える5つのKnowledge](https://zenn.dev/makinestai/articles/dify-vs-claude-ops-rag-20-cases)
