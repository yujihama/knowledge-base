---
title: "Claudeに自分専用の秘書を育てさせる — GitHub × Claude Code で AI の長期記憶を作る"
url: "https://zenn.dev/hobomokha/articles/9381d939aef2bd"
date: 2026-06-12
tags: [Claude Code, CLAUDE.md, 長期記憶, コンテキスト管理, GitHub, パーソナライゼーション, LLM]
category: "agent-arch"
related: [5029, 3506, 3004, 6491, 2249]
memo: "[Zenn LLM] Claudeに自分専用の秘書を育てさせる — GitHub × Claude Code で AI の長期記憶を作る"
processed_at: "2026-06-12T09:03:10.991283"
---

## 要約

LLMはセッションをまたいで記憶を保持できないという制約を、GitHubプライベートリポジトリを外部記憶ストアとして活用することで解決するアプローチを解説したハンズオン記事。

仕組みの核心は「コンテキストの設計」にある。同じClaudeモデルでも、ユーザーのプロフィール情報を含むファイルを読み込んだ状態と何も知らない状態とでは、出力品質に大きな差が生まれる。これをシステム化するために、GitHubリポジトリをAIの長期記憶置き場として使い、Claude Codeがそのファイルを読み書きする構成を取る。

Claude Codeを選ぶ理由として、リポジトリルートにCLAUDE.mdを置くだけでセッション開始時に自動ロードされる仕組みが挙げられる。この自動読み込み機能により、毎回手動でコンテキストを与える手間が不要になる。

リポジトリの構成は以下の通り：CLAUDE.md（Claudeへの行動指示書）、master_profile.md（ユーザーの自己理解・価値観・職業情報を蓄積する正典ファイル）、domains/配下にwork.md・life.mdなどテーマ別ログファイル。CLAUDE.md内には「推測を事実として書かない」「流動的情報には[FLOW]タグを付ける」「master_profile.mdは明示的依頼なしに直接編集しない」などの行動ルールを記述する。

ハンズオンの流れ：(1) GitHubでPrivateリポジトリを作成、(2) Claude Codeのコネクタ設定でGitHubと接続、(3) Claudeにリポジトリ構造を自動生成させる、(4) 一問一答形式でユーザー情報をmaster_profile.mdに蓄積、(5) 新規セッションでファイルを読み込んだ状態の回答品質を体感する。

発展的な使い方として、domains/にfinance.md（家計）やreading.md（読書ノート）を追加する、会話の区切りに「今日の相談をまとめて保存して」と依頼して会話ログを自動保存する、CLAUDE.mdに参照ファイルと出力フォーマットの指示を細かく記述してClaudeの動作を制御する、などが示されている。また、GitHubのファイルはプレーンテキストのためChatGPTのカスタム指示へのコピペや他LLMへの転用も可能で、一度整備すれば複数のAIサービスで「自分を知っているモード」を再現できる点も言及されている。

必要なものはClaude Pro（月$20）とGitHub無料アカウントのみ。監査エージェント開発への示唆として、エージェントの「コンテキスト管理」設計においてCLAUDE.mdのような外部指示ファイルをセッション開始時に自動ロードするパターンは、LangGraphのStateやPydanticモデルによるプロファイル管理と組み合わせて監査エージェントの長期的な案件コンテキスト保持にも応用可能。

## アイデア

- CLAUDE.mdの自動ロード機構を利用した外部記憶パターン：リポジトリルートのCLAUDE.mdでmaster_profile.mdの参照優先順位と行動ルール（[FLOW]/[FIXED]タグ、差分案提示フロー）を定義し、セッションをまたいだ一貫したコンテキスト注入を実現している点
- GitHubをベクトルDBではなくプレーンテキストストアとして使うことで、複数LLMサービス間でコンテキストをポータブルに共有できる設計思想
- 「推測を事実として書かない」「明示的依頼なしにmaster_profile.mdを直接編集しない」という制約をCLAUDE.mdに記述することで、AIの自律的な記憶改ざんリスクを制御するガバナンス設計

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **GitHub API** → /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた

## 関連記事

- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_3004 LLMに長期記憶を実装して、失敗にいたる
- /deep_6491 Claude Codeを使い倒すための設定術：CLAUDE.md・自動メモリ・コンテキスト管理の3本柱
- /deep_2249 Claude Codeの設定はどこに書くべきか ― プロンプト・RULES・スキル・エージェントの使い分け

## 原文リンク

[Claudeに自分専用の秘書を育てさせる — GitHub × Claude Code で AI の長期記憶を作る](https://zenn.dev/hobomokha/articles/9381d939aef2bd)
