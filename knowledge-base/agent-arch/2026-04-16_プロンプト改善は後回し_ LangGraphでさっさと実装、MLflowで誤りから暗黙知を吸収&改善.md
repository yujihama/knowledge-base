---
title: "プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善"
url: "https://zenn.dev/nttdata_tech/articles/11f406b0f1cfd4"
date: 2026-04-16
tags: [LangGraph, MLflow, GEPA, プロンプト最適化, LLM-as-a-judge, 暗黙知形式知化, structured_output, StateGraph]
category: "agent-arch"
related: [564, 897, 41, 745, 858]
memo: "[Zenn LLM] プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善"
processed_at: "2026-04-16T12:42:56.178836"
---

## 要約

NTT DATAによる実践レポート。LangGraphとMLflowを組み合わせて、プロンプトの手動改善サイクルから脱却する手法を紹介する。

【背景と課題】生成AIアプリ開発において、プロンプト改善は「1つ直すと別の問題が出る」もぐらたたき状態になりやすい。特に既存業務の置き換えでは、暗黙の業務ルールがドキュメント化されていないため、LLMに正しい判断基準を与えられない問題が頻発する。

【実装概要】メール本文と添付ファイルを入力とし、個人情報漏洩リスクをOK/WARN/NGの3段階で判定→リスクありなら自動書き直し→再評価するワークフローをLangGraphで構築。StateとしてEmailRiskStateを定義し、checker_agent・rewrite_agent・recheck_agentの3ノードを直列につないだStateGraphを実装。各ノードには@mlflow.traceデコレータを付与し、入出力をMLflow Tracesに記録する。

【プロンプト自動最適化】MLflow GenAI機能のoptimize_prompts()とGEPA（Gradient-Enhanced Prompt Adaptation）手法を使い、正解ラベル付きサンプルデータからchecker_agentのプロンプトを自動改善。評価指標はlabel_accuracy（OK/WARN/NGのラベル一致率）とreason_alignment（LLM-as-a-judgeによる判定理由の整合性評価）を0.8:0.2で加重合算。

【学習結果】初期プロンプトには「無関係の第三者の個人情報はNG」という1ルールのみ記述。数十件のサンプルから学習後、初期に明示していなかった「業務目的が明確な窓口案内はWARN」「送信者本人の連絡先共有はOK」という暗黙ルール2件を自動で抽出・文書化することに成功。人間が気づいていなかった判断基準の形式知化を実現した。

【監査エージェント開発への示唆】正解データ（監査調書・過去指摘事項）さえ収集できれば、監査判断の暗黙知（ベテラン監査人の経験則）をLLMが自動でプロンプトに落とし込むアプローチが適用可能。LangGraphで骨格を先行実装→MLflowで実行ログ収集→GEPA最適化という3ステップのパイプラインは、監査エージェントの精度改善サイクルに直接転用できる。

## アイデア

- GEPAによるプロンプト自動最適化で、初期プロンプトに明示していなかった暗黙ルール（業務目的が明確な窓口案内はWARN、送信者本人の連絡先はOK）を数十件のサンプルから自動抽出・文書化できた点。暗黙知の形式知化をLLMに委譲できることを実証した
- label_accuracyだけでなくreason_alignment（判定理由の整合性をLLM-as-a-judgeで評価）を最適化目標に含めることで、ラベルが合っていても理由が間違っているケースを排除し、実務信頼性を高める評価設計
- 「まず動くものをLangGraphで実装→MLflowでログ収集→課題が蓄積したらGEPAで自動改善」という段階的アプローチ。高精度になるまで待たずにアーリーアクセス版を展開してフィードバックを集める戦略が、監査エージェントのMVP開発にそのまま応用可能

## 前提知識

- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **MLflow Tracing** (TODO: 読むべき)
- **GEPA** (TODO: 読むべき)
- **LLM-as-a-judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **structured_output** (TODO: 読むべき)

## 関連記事

- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由
- /deep_897 時系列説明のためのLLM-as-a-Judge：参照なし評価フレームワーク
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_745 ケース適応型マルチエージェント審議による臨床予測：CAMP
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介

## 原文リンク

[プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善](https://zenn.dev/nttdata_tech/articles/11f406b0f1cfd4)
