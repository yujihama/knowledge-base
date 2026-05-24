---
title: "Gemma 4搭載の小説執筆AIエージェント【NovelPilot】"
url: "https://zenn.dev/doraking/articles/4a32fc457e473c"
date: 2026-05-24
tags: [Gemma4, マルチエージェント, Next.js, 構造化出力, OpenRouter, パイプライン, TypeScript]
category: "agent-arch"
related: [2962, 1641, 90, 3, 3002]
memo: "[Zenn LLM] Gemma 4 搭載の小説執筆AIエージェント【NovelPilot】"
processed_at: "2026-05-24T09:06:01.169304"
---

## 要約

NovelPilotは、Gemma 4を推論エンジンとして使用する、マルチエージェント構成の小説制作Webアプリ。Next.js App Router + TypeScript + Tailwind CSSで構築され、Vercelにデプロイされている。ユーザーが1つのプロンプトを入力すると、9つの専門エージェント（Premise Architect → Character Director → World Builder → Plot Strategist → Chapter Architect → Prose Writer → Style Editor → Continuity Detective → Publisher Agent）が順次実行され、作品コンセプト・登場人物設定・世界観・プロット・章立て・本文・伏線管理・矛盾チェック・紹介文を生成する。各エージェントは前エージェントの構造化出力（JSON）とStory Bibleを入力として受け取り、累積的な文脈の中で推論を行う。エージェント間の状態はReact stateで管理し、lib/useStoryProject.tsがクライアント側のパイプライン制御を担当。Gemma 4の呼び出しはlib/gemma.tsに抽象化されており、OpenRouter経由のLive ModeとAPIキー不要のMock Modeを切り替え可能。特徴的な機能として、Foreshadowing Tracker（伏線をitem/introducedIn/status/suggestedPayoffの構造化JSONで管理）とContinuity Detective（category/severity/issue/evidence/suggestedFixの形式で矛盾を分類・提案）がある。LLMの出力をそのまま表示せずJSON構造として扱い、タイムライン・カード・レポート等のUIコンポーネントに変換する設計思想が核心。UI/UXはPrompt Launcher → Agent Workspace → Completed Novel Readerの3段階遷移で構成され、A4フォーマットのPDF出力にも対応。ハッカソンMVPのためDB・認証は省略。監査エージェント開発への示唆として、専門機能を持つエージェントを逐次接続しStory Bible相当の累積コンテキストを渡すパターンは、監査手続きの各フェーズ（証拠収集→リスク評価→発見事項統合→報告書生成）を逐次エージェントで処理する設計に直接応用可能。また、構造化JSON出力でLLMの結果をUI部品として扱う手法は、監査レポートの差異検出や根拠管理においても有効。

## アイデア

- 9エージェントを逐次チェーンし、各エージェントが前段の構造化出力とStory Bible（累積コンテキスト）を受け取る設計により、単一LLM呼び出しでは困難な長文・複雑構造の一貫性を保持する手法
- LLMの出力をプレーンテキストではなくJSONとして強制することで、伏線管理表・矛盾チェックレポート・登場人物カード等のインタラクティブなUIコンポーネントに変換できるというアーキテクチャ方針
- Continuity Detectiveがcategory/severity/evidence/suggestedFixを構造化出力として返す設計は、LLM-as-judgeパターンの実装例であり、監査AIにおける発見事項の重要度分類・根拠提示・是正提案への応用が直接可能

## 前提知識

- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **構造化出力 / JSON mode** (TODO: 読むべき)
- **Gemma 4** → /deep_766 Gemma 4 へようこそ：デバイス上で動くフロンティア・マルチモーダルモデル
- **Next.js App Router** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_2962 Windows上のLLMとxangiを接続し、BOT同士で会話させる
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説
- /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- /deep_3002 AIは役割だけでどこまで本気の議論ができるのか：マルチAIファシリテーター会議ツールの開発記録

## 原文リンク

[Gemma 4搭載の小説執筆AIエージェント【NovelPilot】](https://zenn.dev/doraking/articles/4a32fc457e473c)
