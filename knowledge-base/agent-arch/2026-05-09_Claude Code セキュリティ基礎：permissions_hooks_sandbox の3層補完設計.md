---
title: "Claude Code セキュリティ基礎：permissions/hooks/sandbox の3層補完設計"
url: "https://zenn.dev/trailfusionai/articles/ai-news-20260427071327-7b032f"
date: 2026-05-09
tags: [Claude Code, セキュリティ, permissions, Hooks, sandbox, プロンプトインジェクション, 3層防御]
category: "agent-arch"
related: [2961, 2203, 2537, 94, 2689]
memo: "[Zenn LLM] Claude Code Security Basics — permissions/hooks/sandbox の3層補完設計"
processed_at: "2026-05-09T12:50:16.368284"
---

## 要約

2026年4月23日、AWS クラウド事業本部の川原征大氏が公開した62スライドの「Claude Code Security Basics」が3日で24,000 viewsを記録した。本記事はそのフレームワークをZenn向けに体系化したもので、Claude Codeの安全運用を「抑止／制限／隔離」の3軸で整理している。

【3層防御モデルの構成】
第1層「抑止（Deterrence）」はCLAUDE.mdやシステムプロンプトによる宣言的な制約で、プロンプトインジェクションで容易に突破されるため被害が最も大きい。第2層「制限（Restriction）」はpermissions.denyとHooksによる機械的なブロックで、既知パターンのみ対応可能。第3層「隔離（Isolation）」はsandbox／コンテナ／VMによる実行環境の封じ込めで、万一突破されても被害を環境内に限定する。

【permissions設定の実装例】
settings.jsonのpermissions.denyには`.env`、`.pem`、`.aws/credentials`の読み取り、`rm -rf *`、`git push --force`、`curl * .env*`、`chmod 777 *`等を列挙する。パスマッチングは「最初にマッチした行が勝つ」ため、denyを先頭に置く必要がある。`Read(//**/.env*)`の`//`は絶対パスのワイルドカードプレフィックスで、相対パス指定の`Read(./.env)`では効果が限定される点に注意が必要。

【Hooks実装の詳細】
PreToolUseイベントでBashとWebFetchにguardスクリプトを設定する。`guard-bash.sh`はstdinからJSON形式でコマンドを受け取り（`jq -r '.tool_input.command'`）、`.env`、`.pem`、`rm -rf /`、`curl ... | bash`等のパターンをgrepで検出してexit 2でブロックする。`guard-fetch.sh`はURLのドメインをallowlistで検証し、許可外ドメインへのアクセスをexit 2で遮断する。重要な落とし穴として「exit 1ではブロックされない」点があり、必ずexit 2を使用する必要がある。

【設定スコープの優先順位】
Managed（MDM配布、最強）→ User（~/.claude/settings.json）→ Project（リポジトリ内、チーム共通）→ Local（.claude/settings.local.json、gitignore対象）の順で適用される。

【プロンプトインジェクション対策】
外部HTMLやGitHub Issue本文に埋め込まれた悪意ある命令への対処として、CLAUDE.mdへの明記（抑止）、WebFetch後のBash実行をask権限に格下げ＋ドメイン許可リスト（制限）、sandboxで認証情報をマウントしない（隔離）の3層対応を推奨している。

監査エージェント開発への示唆：エージェントが外部データ（監査証跡、APIレスポンス等）を処理する際のプロンプトインジェクションリスクは実際の脅威であり、この3層モデルはLangGraphベースの監査エージェントのセキュリティ設計にそのまま応用可能。特にHooksによる動的コマンド検査は、エージェントが自律的にツール実行する際の最終防衛線として重要。

## アイデア

- exit 2でのみブロックが発動するHooksの仕様は、既存のbashスクリプト慣習（exit 1がエラー）と異なり、誤実装が発生しやすい設計上のトラップである
- Read(//**/.env*)の//プレフィックスが絶対パスワイルドカードとして機能する点は、相対パス指定との挙動差を生む非自明な仕様で、セキュリティホールになりやすい
- WebFetch後のBash実行をask権限に格下げする「動詞連鎖制限」の考え方は、エージェントの行動空間を制限するReAct型エージェント設計の安全装置として汎用的に応用可能

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **PreToolUse Hook** → /deep_3093 承認していない git tag を Claude Code に打たれた話 — LLM Agent の構造的 Rule Violation
- **permissions.deny** (TODO: 読むべき)
- **sandbox隔離** (TODO: 読むべき)

## 関連記事

- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- /deep_2537 サブエージェントが実はレポートを書けていなかった──Clade v1.17.1〜v1.18.1
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_2689 「並列は速い」は本当か──subagent 76% DENIED検証とCladeの選択

## 原文リンク

[Claude Code セキュリティ基礎：permissions/hooks/sandbox の3層補完設計](https://zenn.dev/trailfusionai/articles/ai-news-20260427071327-7b032f)
