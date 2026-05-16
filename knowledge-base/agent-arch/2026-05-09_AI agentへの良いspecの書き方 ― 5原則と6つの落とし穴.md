---
title: "AI agentへの良いspecの書き方 ― 5原則と6つの落とし穴"
url: "https://zenn.dev/aiandao/articles/good-spec-for-ai-agents-20260502"
date: 2026-05-09
tags: [spec-driven-development, AGENTS.md, CLAUDE.md, Curse-of-Instructions, LLM-as-a-Judge, Plan-Mode, subagent, parallel-agents, MCP, RAG, Three-Tier-Boundary, Claude-Code, GitHub-Copilot]
category: "agent-arch"
related: [1247, 36, 2405, 4520, 1784]
memo: "[Zenn LLM] AI agent への良い spec の書き方 ― 5 原則と落とし穴"
processed_at: "2026-05-09T09:34:30.158067"
---

## 要約

Addy Osmani（Google Gemini チーム、O'Reilly著者）が提唱する「AIコーディングエージェント向け仕様書設計の5原則」を解説した記事。Claude Code・Cursor・GitHub Copilotなどの業務利用時に頻発する「指示の遵守率低下」「文脈の喪失」を解決するための実践的フレームワーク。

**5原則の概要：**
1. **高レベルvisionから始める**：人間は1段落のProject Goalだけを書き、詳細specはAIに生成させる。生成されたspec.mdはPlan Mode（read-only）で精査してからImplementへ移行。
2. **PRD構造化（Six Core Areas）**：GitHub 2,500件超のAGENTS.md/CLAUDE.md分析から導出した6セクション——Commands・Testing・Project Structure・Code Style・Git Workflow・Boundaries。最頻出かつ最重要の制約は「Never commit secrets」の1行。
3. **モジュラー分割**：OpenReviewの「Curse of Instructions」研究によると、プロンプトに指示を積めば積むほど各指示の遵守率が顕著に低下する。対策はspecをphase/componentで分割し、各タスクに必要なセクションだけを渡すこと。subagentは専門領域ごとに分け、parallel agentsは最初2〜3体に抑える。
4. **self-checkと境界線の組み込み**：Three-Tier Boundary System（Always/Ask first/Never）を採用。Self-Verificationプロンプト・LLM-as-a-Judge・Conformance Testingの3手法で品質管理。人間は常に「exec in the loop」として最終判断を保持。
5. **テスト・反復・進化**：「コード生成→テスト→失敗をspecに反映→再実行」のループを回す。specはgitで版管理し、RAGでベクトルDB化して関連箇所だけをagentに供給。MCPで context供給を自動化（Context7等）。

**6つの落とし穴：**曖昧なプロンプト・要約なしの長大コンテキスト投入・人間レビュー省略・vibe codingとproduction engineeringの混同・Simon Willisonの「Lethal Trifecta」（Speed×Non-determinism×Cost）・Six Core Areasのいずれかの欠落。

**監査エージェント開発への示唆：**LangGraph＋ReActで構築する監査エージェントにもそのまま適用可能。Boundaries設計（スキーマ変更はAsk first、secretsコミットはNever）はコンプライアンス要件と整合し、LLM-as-a-JudgeはGRCチェックリストの自動評価に直結する。spec自体をgit管理して監査証跡として活用するアプローチも示唆される。

## アイデア

- 「Curse of Instructions」：指示をプロンプトに積めば積むほど各指示の遵守率が下がるという現象は、GPT-4・Claudeでも確認されており、specの肥大化が逆効果になるメカニズムを実証的に裏付けている
- GitHub 2,500件超のAGENTS.md分析から「Never commit secrets」が最頻出の有効制約として浮上した事実は、エージェント設定ファイルのベストプラクティスを定性論ではなくデータで語れる珍しい事例
- Simon Willisonの「Lethal Trifecta（Speed×Non-determinism×Cost）」という3軸フレームワークは、AI品質劣化の構造的要因を整理する概念として監査・リスク評価文脈でも応用できる

## 前提知識

- **Plan Mode（Claude Code）** (TODO: 読むべき)
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **subagent / multi-agent** (TODO: 読むべき)

## 関連記事

- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[AI agentへの良いspecの書き方 ― 5原則と6つの落とし穴](https://zenn.dev/aiandao/articles/good-spec-for-ai-agents-20260502)
