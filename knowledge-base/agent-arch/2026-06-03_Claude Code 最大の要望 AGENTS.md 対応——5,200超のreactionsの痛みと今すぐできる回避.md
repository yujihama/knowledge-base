---
title: "Claude Code 最大の要望 AGENTS.md 対応——5,200超のreactionsの痛みと今すぐできる回避策"
url: "https://zenn.dev/yurukusa/articles/agentsmd-interop-5-paths-2026"
date: 2026-06-03
tags: [AGENTS.md, CLAUDE.md, Claude Code, マルチエージェント, ツール間互換性, pre-commit hook, Cursor, Codex]
category: "agent-arch"
related: [5029, 6563, 7298, 1643, 1783]
memo: "[Zenn LLM] Claude Code 最大の要望 AGENTS.md 対応——5,200 を超える reactions の痛みと今すぐできる回避策"
processed_at: "2026-06-03T21:02:38.947663"
---

## 要約

Claude Codeのリポジトリ（anthropics/claude-code）において、Issue #6235「AGENTS.md対応」が累計5,200超のreactionsを獲得しており、2位（717）の7倍以上という突出した要望となっている。2025年8月21日起票から9ヶ月以上未対応のまま。

問題の本質は、AIコーディングツールごとに指示書ファイルの名前・場所が異なる点にある。Claude CodeはCLAUDE.mdを読み、CursorはAGENTS.mdと並行で.cursorrulesを読み、CodexとAmpはAGENTS.mdに対応済み。AGENTS.mdはcoding agentがコードベースを理解するための業界標準（https://agents.md/）として収束しつつあるが、Claude Codeのみが独自経路を維持している。

複数ツール併用ユーザーにとってこの差異は深刻で、記事著者は「1日複数回の指示書ずれ確認で年100時間以上が消費されていた」と報告している。

公式対応を待つ間の回避策として5つが提示されている。①CLAUDE.mdに「@AGENTS.md」の1行を書いてAGENTS.mdを取り込む方式（公式が第一に推奨。Windowsでも権限不要、/initコマンドでAGENTS.md内容を自動取り込み可能）。②シンボリックリンクで実体を1ファイルに統一（設定2分、維持コストほぼゼロ、ただしWindows/WSLは管理者権限が必要）。③pre-commit hookによるコミット時の自動同期（チーム運用向け）。④SessionStart hookで整合性を確認するagents-md-sync-checker（著者が配布するMITライセンスのhook集cc-safe-setupに収録、14日間で1,580名以上が利用）。⑤CI差異検出（チームの最終防波堤として）。

著者自身はシンボリックリンク＋SessionStart hookの組み合わせを採用し、年100時間超の確認コストをほぼゼロに削減。現時点での最短手順は①の取り込み方式（CLAUDE.mdに1行追記のみ）。

監査エージェント開発への示唆：複数LLMエージェントを並行運用するマルチエージェントシステムでは、各エージェントへの指示・制約の一貫性維持が品質保証の観点で重要。AGENTS.md統合問題は「エージェント間の共通コンテキスト管理」という汎用的な設計課題を体現しており、監査ワークフローで複数ツールを組み合わせる際の参照アーキテクチャとして参考になる。

## アイデア

- AGENTS.mdが業界標準として収束しつつある中でClaude Codeのみ独自経路を維持している構図は、エージェント間インターオペラビリティの標準化競争の縮図であり、MCP（Model Context Protocol）のような共通規格策定の難しさを示している
- 「@AGENTS.mdの1行取り込み」という解決策は、設定ファイルの継承・参照モデルとして他の設定管理（Dockerfile、.gitconfig等）でも使われる古典的パターンであり、シンプルながら実効性が高い
- SessionStart hookによる整合性チェックという発想は、監査エージェントにおける「実行前の前提条件検証」パターンと同型であり、エージェントの信頼性確保に応用できる

## 前提知識

- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **AGENTS.md** → /deep_8 LLMに「マジカルバナナ」式連想想起を実装したら会話が変わった
- **Claude Code hooks** → /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- **pre-commit** (TODO: 読むべき)
- **シンボリックリンク** (TODO: 読むべき)

## 関連記事

- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_6563 コードを書けない私がClaude Codeで「AIチーム」を回すまで
- /deep_7298 multi-agent-shogunをメイドにしてQOLを上げてみた
- /deep_1643 Claude Codeの「アドバイザー」と「サブエージェント」── Maxプランでの使い方
- /deep_1783 Claude Codeで8体AIエージェント組織を作った6日間 — 人間とAIはどんな対話をしたか

## 原文リンク

[Claude Code 最大の要望 AGENTS.md 対応——5,200超のreactionsの痛みと今すぐできる回避策](https://zenn.dev/yurukusa/articles/agentsmd-interop-5-paths-2026)
