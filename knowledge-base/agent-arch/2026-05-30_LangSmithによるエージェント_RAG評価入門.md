---
title: "LangSmithによるエージェント/RAG評価入門"
url: "https://zenn.dev/highthreee/articles/d323f4dcfdc493"
date: 2026-05-30
tags: [LangSmith, RAG評価, LLM-as-judge, エージェント評価, LangChain, openevals, Offline evaluation, Trajectory評価]
category: "agent-arch"
related: [41, 858, 2692, 3233, 6677]
memo: "[Zenn LLM] LangSmithによるエージェント/RAG評価入門"
processed_at: "2026-05-30T21:00:44.339528"
---

## 要約

LangSmithはLangChainエコシステムに含まれるLLMアプリケーション評価プラットフォームであり、トレース・データセット管理・実験比較・Evaluatorを統合的に提供する。本記事では、エージェントおよびRAGの評価設計の考え方と、民法RAGを題材にした具体的な実装例を解説する。

評価対象の分解が重要で、LLM call（形式・指示追従）、Retrieval（関連文書の取得精度）、Tool call（ツール選択と引数の正確性）、Trajectory（手順の妥当性）、Final response（ユーザー要求への適合）の5層に分けて考える。最初は5〜10件程度の手作りデータセットから始め、「良い出力とは何か」を定義することが推奨されている。

LangSmithの主要概念として、Dataset（入力と期待出力のセット）、Example（1件のテストケース）、Target function（評価対象の本体）、Experiment（Dataset×バージョンの実行結果）、Evaluator（採点関数）、Feedback（scoreとコメント）、Run/Trace（実行の全中間ステップ記録）がある。

評価モードはOffline（デプロイ前・開発中、正解データあり）とOnline（本番トレース対象、reference-free中心）の2種類。モデル比較のような用途にはOffline evaluationが適している。

Evaluatorは4種類：Human evaluation（主観・ドメイン知識）、Code evaluator（形式チェック・完全一致・決定的判定）、LLM-as-judge（正確性・関連性・groundedness）、Pairwise evaluation（2出力の優劣比較）。実務ではCode evaluatorで機械判定できる項目を先に定義し、LLM-as-judgeと組み合わせる構成が扱いやすい。

RAG評価は4軸で構成される：Correctness（回答vs参照回答、正解データ必要）、Answer relevance（回答vs質問、reference-free）、Groundedness（回答vs検索文書、reference-free）、Retrieval relevance（検索文書vs質問、reference-free）。LLMのみを変更した実験では、retrieverが同じであれば検索結果は変わらず、回答差分はgeneration側に起因すると切り分けられる。

具体例では、e-Gov法令APIから取得した民法XMLをRecursiveCharacterTextSplitterでchunk化し、InMemoryVectorStore＋Ollamaのllama3 embeddingで構築したRAGを評価対象とした。Datasetには質問・期待回答・期待条文番号の3要素を持つ3件のExampleを登録。Code evaluatorで期待条文がtop k（k=4）に含まれるかをmetadataで判定し、LLM-as-judgeにはopenevals の`create_llm_as_judge`とCORRECTNESS_PROMPTを使用（モデル: openai:o3-mini）。`client.evaluate()`にtarget functionとevaluatorsリストを渡すことで、GeminiモデルのバージョンA・Bを同一Datasetで比較するExperimentを実行し、LangSmith UI上でスコアを横並び比較できる。

監査エージェント開発への示唆：監査手続きの実行エージェントでも、ツール選択の正確性をCode evaluatorで定量的に検証し、最終判断の妥当性をLLM-as-judgeで評価する2層構造が有効。Trajectory評価を取り入れることで、正しい結論に至った場合でも手順の効率性や網羅性を継続的に改善できる。

## アイデア

- 評価をFinal response・Single step・Trajectoryの3層に分解することで、失敗箇所（retrieval側かgeneration側か）を系統的に切り分けられる点
- Code evaluatorで決定的判定（条文番号の一致等）を先に定義し、その上にLLM-as-judgeを重ねる2層評価構成が実務的に扱いやすいという設計原則
- model_nameを引数化したtarget functionのファクトリパターンにより、同一DatasetでLLMバージョンを差し替えたExperimentを容易に比較できる実装手法

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LangChain/LangGraph** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **ベクトル検索** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **トレーシング** → /deep_398 LLMで「見える運用」へ――可観測性を強化する実務メモ（OpenTelemetry GenAI / Langfuse / Phoenix）

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2692 Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】
- /deep_3233 Langfuse vs LangSmith vs Helicone — LLM観測・デバッグツール比較【2026年版】
- /deep_6677 LLM観測性ツール5社の実装思想を並べてみた

## 原文リンク

[LangSmithによるエージェント/RAG評価入門](https://zenn.dev/highthreee/articles/d323f4dcfdc493)
