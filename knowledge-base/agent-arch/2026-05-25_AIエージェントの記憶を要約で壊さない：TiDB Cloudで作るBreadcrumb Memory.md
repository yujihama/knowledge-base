---
title: "AIエージェントの記憶を要約で壊さない：TiDB Cloudで作るBreadcrumb Memory"
url: "https://zenn.dev/monruho/articles/342957c7356fb6"
date: 2026-05-25
tags: [Breadcrumb Memory, エージェントメモリ, long-term memory, TiDB Cloud, vector search, source recall, compact, Mastra, MemGPT, context window]
category: "agent-arch"
related: [3943, 2796, 2567, 2709, 3036]
memo: "[Zenn LLM] AIエージェントの記憶を要約で壊さない：TiDB Cloudで作るBreadcrumb Memory"
processed_at: "2026-05-25T09:04:52.532892"
---

## 要約

AIエージェントの長期記憶設計における「要約による情報損失」問題を解決するBreadcrumb Memoryという設計パターンを提案する記事。

従来のcompact（要約）アプローチでは、正規表現・SQL・ファイルパス・ポート番号などのexact valueがsummaryから再生成される際に微妙に壊れる問題がある。例えば「teacher.example.ed.jp と student.example.ed.jp を許可し alumni.example.ed.jp を除外する」という正規表現条件は、要約されると「学校用メールアドレスを許可する方針」という抽象表現に落とされ、後から再現できなくなる。

Breadcrumb Memoryの核心は「compactを記憶の圧縮ではなく索引の作成として扱う」こと。各メモリレコードはsummary（概要）、source_range（原文への参照: thread_id + start_index + end_index）、tags（構造化フィルタ用）、query_hints（将来の検索用語彙）、retrieve_when（使用場面の説明）、status（active/superseded/conflicted）、importanceスコアを持つ。

検索パイプラインはRetrieve → Decide → Recall → Extractの4段階。Retrieveではsummary/tags/query_hintsを対象にvector searchとSQLフィルタを組み合わせた軽量検索を行い、TiDB CloudのVEC_COSINE_DISTANCE関数でstatus='active'のレコードを最大10件取得。DecideではLLMが「summary_ok / exact_value_needed / ambiguous」の3分類を行い、exact valueが必要な場合のみsource_rangeへ戻る判断をする。Recallではsource_rangeを対象範囲として再検索・抽出を行い（全原文をそのままプロンプトに入れるのではない）、Extractで必要な情報だけを取り出す。

評価指標としてSource Hit@k（「答えられたか」ではなく「根拠へ戻れたか」）を中心に置く点が特徴的。これはMemGPTやMastra Observational Memoryの「observation + source recall」思想を、DB schema・query_hints設計・status管理・評価指標まで含めて長期開発支援向けに再整理したもの。

実装基盤はTiDB Cloudに限らずPostgreSQL+pgvectorやSQLite+local vector indexでも可能だが、SQL filter・vector search・full-text searchを単一クエリで扱える基盤が設計上自然に求められる。数日〜数週間継続するコーディング支援・研究実験ログ管理・論文整理といったユースケースに適する一方、短いFAQチャットボットには過重な設計となる。

監査エージェント開発への示唆：監査エージェントが過去の監査判断（例：特定の内部統制上の例外処理の承認条件）を長期にわたって参照する場面では、summaryからの再生成ではなくsource_rangeへの参照が不可欠。exact valueとしての判断基準・閾値・規制条文の引用は、Breadcrumb Memory的な設計で保持する必要がある。

## アイデア

- summaryを「記憶の圧縮」ではなく「原文への索引（地図）」として設計するという発想の転換が鋭い。query_hintsフィールドを意図的に設計することで、将来の検索ヒット率を事前にコントロールできる
- Retrieve→Decide→Recall→Extractの4段階パイプラインにより「常に全原文を読む」でも「summaryだけで無理やり答える」でもない中間設計が実現可能。Decideを一発判定にせず保守的に段階的に上げる設計が実用的
- 評価指標をSource Hit@k（根拠へ戻れたか）に置くことで、「答えっぽい回答を生成できたか」という見かけ上の精度ではなく「記憶の信頼性」を正確に測定できる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **vector search** → /deep_2668 制約された公共セクター環境でAIを実用化する：SLMが切り開く道
- **context window compression** (TODO: 読むべき)
- **MemGPT** → /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- **Observational Memory** (TODO: 読むべき)

## 関連記事

- /deep_3943 AIエージェントのメモリ管理完全ガイド 2026 — Mem0 vs Zep vs Letta vs Cognee
- /deep_2796 制約の多い公共セクター環境でAIを実用化する：SLMが切り開く道
- /deep_2567 制約された公共部門環境でAIを実運用する：SLMが切り拓く道
- /deep_2709 制約された公共部門環境でAIを実用化する：SLMが切り開く道
- /deep_3036 制約された公共セクター環境でAIを実用化する：SLMによるアプローチ

## 原文リンク

[AIエージェントの記憶を要約で壊さない：TiDB Cloudで作るBreadcrumb Memory](https://zenn.dev/monruho/articles/342957c7356fb6)
