---
title: "Claude Codeに「忘れない記憶」と「自己改善ループ」を組み込む設計【.claude/rules】"
url: "https://zenn.dev/cutlet_of_pork/articles/27c640d785217c"
date: 2026-06-09
tags: [Claude Code, メモリ管理, 自己改善, プロンプトエンジニアリング, CLAUDE.md, hooks, コンテキスト最適化]
category: "agent-arch"
related: [2055, 7413, 2953, 5970, 5158]
memo: "[Zenn LLM] Claude Codeに「忘れない記憶」と「自己改善ループ」を組み込む設計【.claude/rules"
processed_at: "2026-06-09T09:05:46.022055"
---

## 要約

Claude Codeのセッション間記憶断絶問題を「2層メモリ構造」と「自己改善ループ」で解決する設計手法。第1層はCWDごとにエンコードされたパス（~/.claude/projects/<CWD>/memory/）に格納する環境固有のauto memoryで、MEMORY.mdは索引ポインタのみを持ち本文は個別ファイルに分離することでトークン消費を抑制する。第2層はGit管理された~/.claude/memory/に昇格させる全環境共有知見ベースで、git push/pullにより複数PCで知見を同期できる。自己改善ループは3つの仕組みで構成される。①paths遅延ロード：~/.claude/rules/配下のMarkdownファイルにpathsフロントマターを付与することで特定ファイル編集時のみルールをロードし、常時ロードするコア原則ファイルを最小化する。実例では33ファイル・毎ターン55kトークンの固定費を5k程度まで削減できる。②失敗3回→ルール昇格（Compounding Engineering）：同じ失敗が3回蓄積されたらhookが検知してrules/に汎化ルールを追記し、次セッション以降自動遵守させる。ルールにはWhy（理由）と代替案をセットで記述することで遵守率を向上させる。否定形（NEVER）は肯定形より遵守率が高い。③候補自動生成→/promote-candidates：~/.claude/tmp/以下にskill/agent/hook/script候補ファイルを自動生成し、セッション終了前にまとめてレビュー・昇格することで繰り返しパターンを恒久資産化する。設計原則はCLAUDE.mdを100〜150行以内に保つポインタ駆動設計、定着したルールの定期Pruning、「次回の自分への引き継ぎ書」としての記述スタイルの3点。監査エージェント開発への示唆としては、エージェントが繰り返す失敗パターン（ツール呼び出し誤り、検証ロジックの誤適用等）を自動ルール化する仕組みとして直接応用可能であり、LangGraphのノード設計においても同様のメモリ階層化が有効と考えられる。

## アイデア

- 失敗3回でルール昇格する「Compounding Engineering」パターンは、LangGraphの監査エージェントにおけるReActループの失敗検知・ルール更新機構として直接実装可能
- pathsフロントマターによる遅延ロードは、トークン固定費を55k→5k級に削減できるという具体的な数値があり、大規模エージェントシステムのコスト最適化設計として汎用性が高い
- メモリを「足す」だけでなく「定着したら削除（Pruning）」する引き算の管理原則は、RAGシステムのドキュメント鮮度管理やベクトルDBのチャンク削除戦略にも応用できる概念

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **hookシステム** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_2055 Claude Codeのトークン消費を半分にする——800時間の運用データから見つけた実践テクニック
- /deep_7413 Claude Code の CLAUDE.md 設計パターン完全ガイド
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間
- /deep_5158 グローバル CLAUDE.md には開発哲学を書く：~/.claude/rules/ との使い分け指針

## 原文リンク

[Claude Codeに「忘れない記憶」と「自己改善ループ」を組み込む設計【.claude/rules】](https://zenn.dev/cutlet_of_pork/articles/27c640d785217c)
