---
title: "Claude Code の .claude 設定を育てた話 — 53スキル・12エージェント・15環境ルールの自律開発インフラ"
url: "https://zenn.dev/cutlet_of_pork/articles/db6a3837e1eaee"
date: 2026-05-20
tags: [Claude Code, MCP, Hooks, Gemini CLI, Serena, Context Rot, マルチエージェント, トークン効率化, CLAUDE.md, worktree隔離]
category: "agent-arch"
related: [5970, 3377, 2102, 3002, 5032]
memo: "[Zenn LLM] Claude Code の .claude 設定を育てた話"
processed_at: "2026-05-20T09:08:10.098819"
---

## 要約

Claude Code を数ヶ月運用する中で ~/.claude/ ディレクトリを「自律開発インフラ」へ発展させた実践記録。設計の根本原則は「トークンは生鮮食品」——Claude のトークンは判断・編集にのみ使い、調査・検索・コミットメッセージ生成は Gemini CLI や Serena MCP に外部委任する「ハイブリッド委任原則」を採用。

CLAUDE.md は 200 行以内のポインタ専用ファイルとし、詳細は rules/ ディレクトリに分割格納する。rules/ は _core（5ファイル：言語・トークン節約・出力フォーマット・セッション開始・CoT推論）、workflows（13ファイル）、tools（9ファイル）、environments（15ファイル：WindowsのPowerShell落とし穴・pywinautoのUIA vs 物理クリック等）、team（1ファイル）で構成される。

settings.json では effortLevel: "medium"（Pro プランで5時間ローリング上限を避けるため）、CLAUDE_CODE_AUTO_COMPACT_WINDOW: "400000"（1Mトークンモデルでも300〜400k付近からContext Rotが始まるため早期自動コンパクト）、CLAUDE_CODE_MAX_OUTPUT_TOKENS: "64000" を設定。

Hooks はプロンプト指示と異なり強制力を持つ。SessionStart で Serena 自動起動、PreToolUse(Bash) で UNCパス検出と main ブランチへの force push ブロック、PostToolUse(Write/Edit) で Ruff/ESLint 自動実行、PostCompact で CLAUDE.md 再注入（圧縮後の指示消失防止）を実装。

スキル 53 個はスラッシュコマンドとして提供。description フィールドの精度が選択精度に直結するため最重要。代表例：/bp-research（Zenn・Qiita・Reddit・HN を Gemini CLI で並列検索し rules/ に自動反映、30日スロットリング付き）、/commit-push-pr（Gemini CLI でメッセージ自動生成→コミット→プッシュ→PR作成）。

エージェント 12 個はサブエージェントとして特化。tech-lead（タスク分解・委任）、security-auditor（OWASP Top10準拠静的解析）、build-validator、test-writer（TDDベース）等を並列実行可能。大規模変更時は必ず isolation: "worktree" を指定——未指定で実際にファイル削除事故が発生した実績あり。

メモリは3層構造：auto memory（~/.claude/projects/配下、セッション横断の作業記録）、Serena memories（アーキテクチャ決定・バグ根本原因のプロジェクト紐づけ）、claude-mem MCP（時系列観測履歴：search→timeline→get_observations の3層取得）。

監査エージェント開発への示唆：Hooks による強制品質担保の仕組みは、LangGraph ベースの監査エージェントにおけるガードレール実装（PreToolUse 相当のバリデーションノード挿入）の設計参考になる。また claude-mem の3層メモリ取得パターンは、長期稼働エージェントのコンテキスト管理戦略として転用可能。

## アイデア

- CLAUDE.md をポインタ専用（200行以内）に抑え詳細を rules/ に分割することで Instruction Overload を回避しつつ必要時だけ参照するアーキテクチャ
- PostCompact Hook で CLAUDE.md を自動再注入することでコンテキスト圧縮後の指示消失を防ぐ——コンテキスト管理を Claude 任せにせずシステムレベルで保証する発想
- 大規模エージェント委任時に isolation: 'worktree' を必須とする運用ルール——実際のファイル削除事故から学んだ、エージェントの自律性とリスク管理のトレードオフ解決策

## 前提知識

- **Claude Code Hooks** → /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **Context Window管理** (TODO: 読むべき)
- **サブエージェント委任** (TODO: 読むべき)
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間
- /deep_3377 Claude Code 効き目順30 — ~/.claude/ で一番効く順に並べた実測レシピ集
- /deep_2102 Clade v1.14.5 ── Claude Code上のフレームワークを他の構成と正直に比べてみた
- /deep_3002 AIは役割だけでどこまで本気の議論ができるのか：マルチAIファシリテーター会議ツールの開発記録
- /deep_5032 AIに任せたはずなのに人間がコピペ中継している——A2A AgentCardで解消した

## 原文リンク

[Claude Code の .claude 設定を育てた話 — 53スキル・12エージェント・15環境ルールの自律開発インフラ](https://zenn.dev/cutlet_of_pork/articles/db6a3837e1eaee)
