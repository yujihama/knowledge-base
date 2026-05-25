---
title: "【Fedora Linux × IntelliJ】新世代AIエージェント Antigravity 導入・連携ガイド"
url: "https://zenn.dev/dewins/articles/antigravity-intellijidea"
date: 2026-05-25
tags: [Antigravity, Gemini CLI, MCP, IntelliJ IDEA, Go, Fedora Linux, IDE連携, Artifacts]
category: "infra"
related: [6081, 5476, 5887, 5862, 5947]
memo: "[Zenn LLM] 【Fedora Linux × IntelliJ】新世代AIエージェント Antigravity 導入・連携ガイド"
processed_at: "2026-05-25T09:03:07.442238"
---

## 要約

GoogleがGemini CLIを後継プラットフォーム「Google Antigravity（agy）」へ移行することを発表し、本記事はFedora Linux + zsh環境へのインストールからIntelliJ IDEA連携までの手順をまとめたものである。

Antigravity CLIはOllamaと同様にGo言語で実装されたシングルバイナリで、軽量・高速動作が特徴。最大の新機能は「Artifacts」で、AIが生成したコード・設計図・ドキュメント等の成果物をIDEの右パネルに自動整理し、ダブルクリックでプロジェクトへ即適用できる。成果物はプロジェクトディレクトリではなく `~/.gemini/antigravity-cli/brain/` 配下のセッションIDごとのフォルダに集約される設計で、Gitの差分を汚さず、人間の承認を経てから反映できる安全な構造を実現している。

このブレイン領域への集約により、バージョン更新やセッション切れによるコンテキスト喪失を回避し、異なるエディタ・ターミナル間でもコンテキストをシームレスに共有できる。IntelliJとのIDE連携はMCP（Model Context Protocol）を介して行われ、CLIとIDEプラグイン「Antigravity Companion」が共通プロトコルで通信しながら成果物をArtifactsパネルへ同期する。

インストールはcurl経由のシェルスクリプト1行で完了し、`~/.local/bin/agy` に配置される。更新も `agy update` 1コマンドで対応。初回起動時はGoogle OAuth認証・カラーテーマ選択・ワークスペース信頼確認のインタラクティブセットアップが走る。IntelliJ側ではSettings → Tools → Antigravity CompanionでCLIの絶対パスを指定し、「Start Antigravity Session」ボタンでセッションを起動するとIDEコンテキストとの自動同期が完了する。

監査エージェント開発への示唆として、MCPプロトコルによるツール間コンテキスト共有の仕組みはマルチエージェントシステムにおけるメモリ永続化・成果物管理の参考モデルになりうる。エージェントが生成した中間成果物を共通領域に格納し、人間レビューを挟んで本番適用するHuman-in-the-Loopフローは、監査プロセスの品質管理設計と構造的に一致している。

## アイデア

- 成果物をプロジェクト外の共通ブレイン領域（~/.gemini/antigravity-cli/brain/）に集約し、MCPで複数ツール間同期する設計は、エージェントのメモリ永続化アーキテクチャとして応用可能
- AIの生成物を直接プロジェクトに書き込まず右パネルで待機させ人間承認後に反映するフローは、Human-in-the-Loop設計のUI実装例として参考になる
- Gemini CLIからAntigravityへの移行はGoogleのAIエージェント基盤をGo製シングルバイナリに統一する動きであり、ローカルLLMツール（Ollama等）との技術スタック共通化トレンドを示唆する

## 前提知識

- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **Gemini CLI** → /deep_4743 異なるLLMによるコードレビューでSelf-Enhancementバイアスを軽減する
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Go言語シングルバイナリ** (TODO: 読むべき)
- **Human-in-the-Loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト

## 関連記事

- /deep_6081 Claude Code の .claude 設定を育てた話 — 53スキル・12エージェント・15環境ルールの自律開発インフラ
- /deep_5476 金融部門への先進AI技術導入：ガバナンス後追いとエージェント化の現在地
- /deep_5887 金融部門への先進AI技術の実装：ガバナンス後追いとボトムアップ採用の現実
- /deep_5862 金融部門への先進AI技術の実装：ガバナンス後追いとボトムアップ導入の現実
- /deep_5947 金融部門における先進AI技術の実装：ガバナンス後追いと人材ギャップの課題

## 原文リンク

[【Fedora Linux × IntelliJ】新世代AIエージェント Antigravity 導入・連携ガイド](https://zenn.dev/dewins/articles/antigravity-intellijidea)
