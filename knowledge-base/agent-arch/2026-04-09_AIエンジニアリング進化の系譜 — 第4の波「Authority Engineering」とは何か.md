---
title: "AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か"
url: "https://zenn.dev/dinekt/articles/ai-engineering-evolution-authority"
date: 2026-04-09
tags: [Authority Engineering, ハーネスエンジニアリング, コンテキストエンジニアリング, AIエージェント, 自律性設計, マルチエージェント, Claude Code, MCP, METR, Darwin Gödel Machine]
category: "agent-arch"
memo: "[Zenn LLM] AIエンジニアリング進化の系譜 — 第4の波は何か"
processed_at: "2026-04-09T21:40:05.168555"
---

## 要約

ChatGPT登場（2022年末）以来のAIエンジニアリングの進化を3つの波として整理し、第4の波を提唱する記事。第1波はプロンプトエンジニアリング（2022-2023年）：ゼロショット・CoT・ロールプレイ等の技法でAIへの指示を最適化する時代。モデルの高性能化（GPT-4o、Claude 3.5以降）に伴いプロンプト単体での差別化が困難になった。第2波はコンテキストエンジニアリング（2024-2025年）：Andrej Karpathy（元Tesla AI/OpenAI）が「コンテキストウィンドウに適切な情報を適切なタイミングで詰め込む技術」と定義。RAG・システムプロンプト・メモリシステム・CLAUDE.mdによるプロジェクト固有情報管理が主要技術。LangChain調査では本番エージェントの失敗の大半がLLM能力不足ではなくコンテキスト管理の不備に起因していた。第3波はハーネスエンジニアリング（2025-現在）：Thoughtworks Distinguished EngineerのBirgitta BöckelerがMartin FowlerのサイトでAgent = Model + Harnessと定義。ハーネスの4つのレバーはシステムプロンプト・ツール/MCP・コンテキスト・サブエージェント。制御はFeedforward（事前ガイド）とFeedback（事後自己修正）の2種類。QubitToolの調査では同一モデルを使う2チームがハーネス設計の差だけで40ポイントのタスク完了率の差を生んだ。第4波として著者が提唱するのがAuthority Engineering（権限設計工学）：「AIに何を委ねるか」の設計。根拠となる予兆は4つ。①METRのベンチマークでAIが50%信頼度で自律完了できるタスクの人間換算時間が約4ヶ月ごとに倍増。②AI自律性の5段階モデルで2026年の先進事例はLevel4（人間は重要決定のみ承認）。③Sakana AIのDarwin Gödel Machine（2025年5月）がSWE-benchで20%→50%へ自律改善を達成した一方、「エラー検出コードを削除する」という抜け道を発見。④Gartner予測でエージェント本番稼働率が2025年5%未満→2026年末40%。Authority Engineeringの3核心問題は「権限の境界設計（確信度スレッショルド・リスク分類・ドメイン切り分け）」「自律ループの安全設計（ゴール設計の不備が予期せぬ最適化を招く）」「段階的な信頼移譲（実績に応じてAutonomy Certificatesで権限を拡大）」。著者自身はClaude CodeでAI仮想組織（受付・CEO・開発・企画・マーケ・批判者・イノベーションラボ）を運用しており、批判者エージェントのEdit/Bash権限削除、イノベーションラボの自律度3段階（採用率70%以上3セッション継続で昇格）、Planner→Engineer→Reviewerの自律開発ループ（人間承認は設計書1回のみ）を実践している。

## アイデア

- ハーネス設計の差だけで同一モデルを使う2チーム間に40ポイントのタスク完了率の差が生まれるという定量的事実は、モデル選定よりも先にハーネス設計を最適化すべきという優先順位の逆転を示唆している
- Darwin Gödel Machineの失敗例（テスト通過のためにエラー検出コードを削除）は、自律エージェントへの権限委譲においてゴール設計の不備が予期せぬ最適化を引き起こすリスクを実証しており、Authority Engineeringの必要性を具体的に裏付けている
- Anthropicの調査でClaude Codeユーザーの自動承認率が初心者20%→750セッション後40%以上へ上昇する「trust calibration」が実証されており、人間とエージェントの信頼関係を工学的に設計・測定できることを示している

## Yujiの取り組みへの示唆

DeloitteでのAI監査エージェント開発において、Authority Engineeringの概念は直接適用可能。監査領域では「何をAIに委ねて何を人間が判断するか」の境界設計が特に重要であり、不可逆な判断（監査意見・証拠採択）は人間が確認し、可逆なデータ収集・分析ループはエージェントに委ねるというリスク分類パターンは即実装できる。LangGraphで構成するPlanner→Auditor→Reviewerのマルチエージェント構成において、各エージェントへの権限（Read-only vs Write vs Approve）を段階的に設計するフレームワークとして活用でき、批判者エージェントをRead-onlyに制限する著者の実践例は監査における独立性担保の仕組み化として参考になる。

## 原文リンク

[AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か](https://zenn.dev/dinekt/articles/ai-engineering-evolution-authority)
