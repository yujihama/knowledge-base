---
title: "OpenHarness：1.1万行のPythonでAI Agentの「黒箱」を丸裸にする"
url: "https://zenn.dev/lumichy/articles/openharness-agent-architecture-2026"
date: 2026-05-10
tags: [OpenHarness, Agent Loop, Pydantic, MCP, マルチエージェント, Claude Code, オープンソース, フック, 権限管理, スキルシステム]
category: "agent-arch"
related: [4520, 1788, 3504, 1783, 1789]
memo: "[Zenn LLM] OpenHarness：1.1万行のPythonでAI Agentの「黒箱」を丸裸にする"
processed_at: "2026-05-10T09:27:41.653762"
---

## 要約

香港大学HKUDSチームが公開したOpenHarnessは、Claude Codeのコアアーキテクチャを1.1万行のPython（93.7%がPython）で再実装したAgent Harnessフレームワーク。GitHubで11.8K Star・2K Forkを記録。Claude Codeの51万行・1,884ファイルに対し、OAuth認証・テレメトリ・React UI・エンタープライズ権限管理などの非本質機能を全て削ぎ落とし、Harnessの本質のみを残した「読めるAgent」として設計されている。

アーキテクチャは10のサブシステムで構成される。中核となるAgent Loop（engine/）はwhile Trueループで「モデルに聞く→ツール実行→結果を返す→また聞く」を繰り返す単純な構造。43個のビルトインツール（tools/）はPydanticによる入力バリデーションとJSON Schema自己記述を持ち、権限チェック・フックと統合される。スキルシステム（skills/）はMarkdownファイルで知識を定義し、~/.openharness/skills/にファイルを置くだけでカスタムスキル追加が可能。Anthropic公式スキルエコシステムとの互換性もある。

権限管理（permissions/）は3段階モードとパス・コマンドレベルのルールでrm -rf /やDROP TABLE等の危険操作をブロック。フックシステム（hooks/）はPreToolUse/PostToolUseでツール実行前後にカスタムロジックを挟める。MCP（Model Context Protocol）クライアントはHTTP transport・自動再接続に対応。メモリシステムはMEMORY.mdによるクロスセッション永続記憶を実現。コーディネーター（coordinator/）はサブエージェント生成・委任・バックグラウンドタスク管理を担う。

対応モデルはAnthropic（Claude Sonnet 4.6/Opus 4.6）、OpenAI（GPT-5.4）、DeepSeek、Qwen、Gemini、Groq、Ollama（ローカルモデル）、GitHub Copilot（OAuth認証でサブスク活用）と幅広い。ohmoは同フレームワーク上に構築された個人用Agentで、Telegram/Slack/Discord/Feishuと接続し、soul.md（長期性格）・identity.md・memory/による永続的アイデンティティ管理を持つ。

制約として、テレメトリ・HA構成・エンタープライズ認証が削除されているためプロダクション直投入は非推奨。TypeScript版なし。監査エージェント開発への示唆として、Pydantic統合ツール定義・権限制御の多段階設計・フックによる監査ログ挿入パターンは、LangGraph + ReActベースの監査エージェント設計に直接応用可能な実装例を提供している。

## アイデア

- Agent Loopの本質がwhile Trueの単純ループであることを1.1万行で証明した点：51万行の商用実装から非本質機能を除去することで「Agentアーキテクチャの教科書」を生成するアプローチ
- スキル定義をMarkdownファイルに統一した設計：人間もLLMも同一フォーマットで読み書きでき、Anthropic公式スキルエコシステムとの互換性を確保しつつ拡張性を保つ
- PreToolUse/PostToolUseフックによる監査ログ挿入パターン：ツール実行前後にカスタムロジックを挟める構造は、監査エージェントの証跡記録・承認ゲート実装に直接転用可能

## 前提知識

- **Agent Loop** (TODO: 読むべき)
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Pydantic** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Tool Calling** → /deep_946 HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_3504 harness engineering を5層で整理する — Pythonで1から書いて見えたこと
- /deep_1783 Claude Codeで8体AIエージェント組織を作った6日間 — 人間とAIはどんな対話をしたか
- /deep_1789 Claude Code 基礎ガイド：AIの全体像からMCP活用まで

## 原文リンク

[OpenHarness：1.1万行のPythonでAI Agentの「黒箱」を丸裸にする](https://zenn.dev/lumichy/articles/openharness-agent-architecture-2026)
