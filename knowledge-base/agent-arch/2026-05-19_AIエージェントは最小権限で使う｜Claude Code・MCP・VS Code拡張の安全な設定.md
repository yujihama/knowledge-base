---
title: "AIエージェントは最小権限で使う｜Claude Code・MCP・VS Code拡張の安全な設定"
url: "https://zenn.dev/takibilab/articles/ai-agent-least-privilege"
date: 2026-05-19
tags: [Claude Code, 最小権限, プロンプトインジェクション, MCP, OWASP, Excessive Agency, セキュリティ, CLAUDE.md]
category: "agent-arch"
related: [2203, 2701, 2405, 2215, 2249]
memo: "[Zenn LLM] AIエージェントは最小権限で使う｜Claude Code・MCP・VS Code拡張の安全な設定"
processed_at: "2026-05-19T09:03:39.238036"
---

## 要約

Claude Codeのような現代のAIエージェントは単なるチャットボットではなく、ファイルの読み書き・シェルコマンド実行・外部API呼び出し・ブラウザ操作（MCP経由）を実行できる実行主体である。この能力の広さが、セキュリティリスクの根源となる。

OWASP「Top 10 for LLM Applications 2025」では「Excessive Agency（過剰な権限）」をリスク項目として明示している。AIが必要以上の権限を持つと、誤作動・悪用・乗っ取り発生時の影響範囲が最大化する。

プロンプトインジェクションはSQLインジェクションと異なり、完全な防御設計が現時点では困難である。LLMはデータと命令の間に堅牢な境界を維持できないため、外部WebページやPDF・GitHubリポジトリ内に埋め込まれた「前の指示を忘れてこのコマンドを実行せよ」という命令に従ってしまう可能性がある。英国NCSC（国家サイバーセキュリティセンター）もこの点を指摘している。

具体的な対策として、著者は以下を実践している。(1) `--allowedTools`フラグでClaude Codeが使えるツールを限定し、シェル実行は都度確認を要求する。(2) 信頼できないソース（外部リポジトリ・URL）を読ませる際は、ファイル書き込み・git push・API呼び出し権限を無効化した状態で実行する。(3) 作業終了後はセッションを閉じ、長時間の開きっぱなしを避ける。(4) MCPサーバーは使用するものだけ有効化し、Slack・GitHub等への接続先を最小限に絞る。(5) ブラウザ拡張・VS Code拡張は半年ごとに棚卸しし、公式GitHubからリンクされていないものは信頼しない。

また、CLAUDE.md（Claude Code）、AGENTS.md（Codex）、.github/copilot-instructions.md（GitHub Copilot）、GEMINI.md（Gemini CLI）などのAI指示ファイルは、悪意ある命令が書き込まれると自動実行されるリスクがある。外部リポジトリを開く前にこれらのファイルを手動確認し、git diffやPull Requestレビューで変更を追跡することが推奨される。

監査エージェント開発への示唆：監査AIが外部データソース（報告書・契約書・メール等）を処理する場合、最小権限の原則は必須要件となる。特に読み取りと書き込みの権限を分離し、データ取得フェーズでは書き込み・送信権限を完全に無効化するアーキテクチャ設計が、プロンプトインジェクション経由の意図しない操作リスクを低減する。

## アイデア

- CLAUDE.md等のAI指示ファイルはコードと同等のレビューが必要で、外部リポジトリ経由のサプライチェーン攻撃の経路になり得る点が見落とされがち
- 信頼できないソースを読ませるときに権限を一時的に剥奪するという「操作スコープ単位での権限切り替え」は、監査エージェントのデータ取得フェーズと実行フェーズの分離設計に直接応用できる
- プロンプトインジェクションはSQLインジェクションと異なりデータ・命令境界を構造的に分離できないため、防御の主軸を「注入されても実行できない権限設計」に置くという逆転発想

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **OWASP LLM Top 10** → /deep_2543 【実装】あなたのAIアシスタント、一文でハイジャックされてます——PythonでPrompt Injection検出ゲートを作る
- **Excessive Agency** → /deep_2064 AIエージェントに権限を与えすぎると何が起きる？Excessive Agencyを初心者向けに解説

## 関連記事

- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- /deep_2701 MCPThreatHive: Model Context Protocolエコシステム向け自動脅威インテリジェンスプラットフォーム
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- /deep_2215 Claudeの指示に従ったらGitHub・Hacker News・RedditでBANされた話
- /deep_2249 Claude Codeの設定はどこに書くべきか ― プロンプト・RULES・スキル・エージェントの使い分け

## 原文リンク

[AIエージェントは最小権限で使う｜Claude Code・MCP・VS Code拡張の安全な設定](https://zenn.dev/takibilab/articles/ai-agent-least-privilege)
