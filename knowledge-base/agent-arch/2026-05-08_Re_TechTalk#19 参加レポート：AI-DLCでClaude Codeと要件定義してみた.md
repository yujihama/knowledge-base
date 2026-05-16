---
title: "Re:TechTalk#19 参加レポート：AI-DLCでClaude Codeと要件定義してみた"
url: "https://zenn.dev/hkdeveloper/articles/260415-re-techtalk-ai-dlc"
date: 2026-05-08
tags: [Claude Code, AI-DLC, 要件定義, Inception, Hooks, aidlc-state.md, Vibe Coding, LLM活用]
category: "agent-arch"
related: [94, 2961, 4228, 2055, 2957]
memo: "[Zenn LLM] Re:TechTalk#19 参加レポート - AI-DLCでClaude Codeと要件定義してみた"
processed_at: "2026-05-08T12:11:23.880005"
---

## 要約

2026年4月15日開催のオンラインイベントRe:TechTalk#19にて、umitsuさんがClaude Codeを用いたAI-DLC（AI-Driven Development Lifecycle）による要件定義体験を発表した内容のレポート記事。

AI-DLCはAWSのawslabsが公開するリポジトリ（aidlc-workflows）に基づく方法論で、ソフトウェア開発ライフサイクル全体をAIが主導する3フェーズ構成：Inception（何を/なぜ作るか）・Construction（どう作るか）・Operation（どう運用するか）からなる。2026年4月時点でOperationフェーズはプレースホルダー的位置づけ。

InceptionフェーズはWorkspace Detection・Reverse Engineering（Brownfieldのみ）・Requirements Analysis・User Stories・Workflow Planning・Application Design・Units Generationの7ステージで構成され、AIが主導して人間に質問を投げかけ、人間は「承認者・監督者」として答えるスタイルが特徴。Constructionフェーズでは、DDDによるFunctional Design、非機能要件・テックスタック選定（NFR Requirements）、アーキテクチャパターン適用（NFR Design）、AWSサービスへのInfrastructure Design、Code Generationと段階的に進む。

発表者が前年（2025年4月）に体験したClaude Codeによるrequirements.md対話ヒアリングとAI-DLCの比較が核心で、前回体験はInceptionフェーズに相当するが、AI-DLCはそれをセッション継続性（aidlc-state.mdで中断・再開可能）・チーム開発対応・全操作のタイムスタンプ監査ログ・全ライフサイクルカバーへと体系化・拡張したものと整理されている。

実践上の工夫として3点が紹介された：①aidlc-docs配下の編集を全許可して確認プロンプトによる作業中断を防止、②Claude CodeのHooks機能でaidlc-state.mdの更新をトリガーにgit commit/pushを自動化、③Claude Code生成物をさらにcodexで二重レビューする二段階AI評価体制。

現実的課題として「ドキュメント多すぎ問題」が挙がり、aidlc-docs/inception・constructionの各配下にplansやrequirementsなど大量のmdファイルが生成されるため、git管理の是非が議論された。結論として「すべて把握せず、必要なドキュメントにアクセスできる状態を維持する」割り切りが提案されている。

監査エージェント開発への示唆：AI-DLCの「全操作タイムスタンプ記録による監査ログ」は内部監査AI設計において証跡管理と整合性を保つ構造的アプローチとして参照価値がある。また、人間を「承認者・監督者」として役割定義する設計思想はヒューマン・イン・ザ・ループ型エージェント設計と直接対応する。

## アイデア

- aidlc-state.mdによるセッション継続性：LLMのコンテキストウィンドウ切れ問題をステート永続化ファイルで解決するアーキテクチャパターンは、長期タスクを扱うエージェント設計全般に応用できる
- Claude Code Hooksをaidlc-state.mdの更新イベントにバインドしてgit push自動化する設計：エージェントの状態変化を外部システム連携のトリガーとして使う疎結合なオーケストレーション手法
- AI生成ドキュメントをさらに別AIでレビューする二段階AI評価チェーン：LLM-as-judgeパターンをドキュメント品質保証に適用するアプローチで、監査AI文脈では自動レビューの多層化として参照できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **AI-DLC** (TODO: 読むべき)
- **Vibe Coding** → /deep_14 Vibe Coding XR：XR BlocksとGeminiによるAI+XRプロトタイピングの高速化
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Human-in-the-Loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト

## 関連記事

- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計
- /deep_2055 Claude Codeのトークン消費を半分にする——800時間の運用データから見つけた実践テクニック
- /deep_2957 Claude Codeで80Kトークンを2,100に削減する方法：廃棄設計による97%削減アーキテクチャ

## 原文リンク

[Re:TechTalk#19 参加レポート：AI-DLCでClaude Codeと要件定義してみた](https://zenn.dev/hkdeveloper/articles/260415-re-techtalk-ai-dlc)
