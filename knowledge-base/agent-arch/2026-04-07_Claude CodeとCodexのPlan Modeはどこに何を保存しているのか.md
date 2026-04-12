---
title: "Claude CodeとCodexのPlan Modeはどこに何を保存しているのか"
url: "https://zenn.dev/t__nabe/articles/e075c352723d9c"
date: 2026-04-07
tags: [Claude Code, Codex, Plan Mode, JSONL, セッション管理, エージェントツール, settings.json]
category: "agent-arch"
memo: "[Zenn LLM] Claude CodeとCodexの Plan Mode はどこに何を保存しているのか"
processed_at: "2026-04-07T09:11:55.832939"
---

## 要約

Claude CodeとOpenAI CodexそれぞれのPlan Modeにおける、プランファイルとセッションログの保存構造・紐づけ方式を実装レベルで比較・整理した技術記事。

Claude CodeのPlan modeはPermission modeの一つで、コードベースの読み取りとシェルコマンドの実行は許可しつつ、ソースコードの編集は行わない読み取り専用モード。プランはMarkdownファイルとして`~/.claude/plans/`に保存され、ファイル名は「形容詞＋動名詞＋名詞」のランダム生成（例: `polymorphic-napping-llama.md`）で内容推測が困難という課題がある。`settings.json`の`plansDirectory`でカスタムディレクトリへの変更も可能（プロジェクトルートからの相対パス）。

セッションログは`~/.claude/projects/<encoded-path>/`配下にUUID v4形式のJSONLファイルとして保存され、プランとの紐づけはJSONL内の`slug`フィールド（プランファイル名から拡張子を除いた値）で行われる間接参照方式。1つのプランに対して複数のセッションが存在し得る（中断・再開、別ブランチ作業など）。サブエージェントは親セッションの`subagents/`サブディレクトリに`agent-`プレフィックス付きJSONLとして格納される。

Codexはこれとは根本的に異なる設計で、プラン情報はセッション外の独立ファイルではなく、セッションJSONL（`~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<session-id>.jsonl`）内にイベントとして埋め込まれる。進捗チェックリストは`update_plan`ツール呼び出しとして、最終プランは`<proposed_plan>...</proposed_plan>`タグで囲まれたブロックとして記録される包含方式。`~/.codex/plans/*.md`はJSONLから抽出したmaterialized cacheに過ぎず、source of truthではない。

セッション再開はClaude Codeが`claude --resume <UUID>`、Codexが`codex resume <UUID>`。Codexは`--last`で直近セッション、`--all`でcwdをまたいだ一覧表示にも対応。

記事後半では、これらの知見を活用してClaude CodeとCodexのプランを統合管理するツール「Agent Plans」の開発も紹介。カンバンビュー、MilkdownエディタによるWYSIWYG編集、行単位レビューモードなどを実装し、Claude Codeプランは直接読み書き、CodexセッションログはJSONLから仮想プランとして読み取り専用で抽出する設計を採用している。

## アイデア

- プランとセッションの紐づけが「外部ファイル参照（slug）」と「JSONL包含」という対照的な設計になっており、それぞれトレードオフが異なる（Claudeは1プランに複数セッションを自然に対応、Codexは1セッション内に複数plan更新を格納）
- Claude Codeのplan modeの読み取り専用制約はハードな技術的制限ではなく、システムプロンプトによる自制であるという点——プロンプトエンジニアリングによってモードの境界が実装されている
- plansDirectoryをプロジェクトリポジトリ内（例: `.plans/`）に設定することで、プランをgitで版管理でき、コードとプランの変遷を紐づけて追跡できる運用が可能になる
## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_1425 COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う

## 原文リンク

[Claude CodeとCodexのPlan Modeはどこに何を保存しているのか](https://zenn.dev/t__nabe/articles/e075c352723d9c)
