---
title: "GitHub Copilotで既存ソフトウェアを改修するためのコンテキスト設計"
url: "https://zenn.dev/asagezenn/articles/b827be281ff2cd"
date: 2026-05-07
tags: [GitHub Copilot, コンテキスト設計, Custom instructions, Agent Skills, 既存ソフトウェア改修, Windows, AIエージェント]
category: "agent-arch"
related: [3094, 2823, 2817, 2550, 2203]
memo: "[Zenn LLM] GitHub Copilotで既存ソフトウェアを改修するためのコンテキスト設計"
processed_at: "2026-05-07T09:43:43.998467"
---

## 要約

GitHub CopilotなどのAIエージェントを使った既存ソフトウェア改修において、意図通りの変更が行われない根本原因は「AIが与えられた情報の範囲内でしか判断できない」という制約にある。コードベースや学習データだけでは、ソフトウェアの運用ルールや前提知識を把握できないため、開発者が明示的にコンテキストを設計・提供する必要がある。

本記事では、Windows向け既存ソフトウェアの改修経験から導き出された体系的なコンテキスト一覧を提示している。フォルダ構成・コンポーネント構成（exe/dll/config、サービス、タスクスケジューラ、依存関係・起動順序）・サーバー構成・ネットワーク構成（プロトコル、ポート番号、動的割り当て規則）・データベース構成（テーブル・カラム単位の役割）・ログ（命名規則、出力先、保持期間・サイズ、削除方法）・権限（実行アカウントと権限）・パッケージング（含めるべきファイルと除外すべきファイル）・技術スタックの9カテゴリに分類されている。

提供方法としては、GitHub Copilotの4種のカスタマイズ機能を使い分ける。`.github/copilot-instructions.md`（Custom instructions）にはフォルダ・コンポーネント・サーバー・ネットワーク・技術スタックなど全作業共通の前提知識を記述する。`.github/instructions/*.instructions.md`（Path-specific custom instructions）にはプロジェクト・フォルダ単位の技術スタック情報を配置する。`.github/agents/*.md`（Custom Agents）には権限・パッケージング情報を持つインストール専門エージェントを定義する。`.github/skills/*/SKILL.md`（Agent Skills）にはDB・ログ関連のスキルを定義し、必要時に自動または手動で呼び出す。コンテキストが膨大な場合は`docs/`フォルダにファイルとして保存し、プロンプトで`@`参照を使って明示的に読み込ませる方式も紹介している。

監査エージェント開発への示唆として、LangGraphベースのReActエージェントにおいても同様の問題が生じうる。エージェントへのシステムプロンプトやツール定義に、対象システムの構成情報（DB スキーマ、API仕様、権限モデル）を体系的に渡す設計が応答品質に直結する。Copilotの4層カスタマイズ構造（全体共通→パス固有→専門エージェント→スキル）は、LangGraphのグラフ設計やMCPのコンテキスト提供方式と概念的に対応しており、参考になる設計パターンである。

## アイデア

- AIへのコンテキスト提供を9カテゴリに体系化し、各カテゴリをCopilotの4種カスタマイズ機能（Custom instructions / Path-specific / Custom Agents / Agent Skills）に対応付けるマッピング設計が実践的
- パッケージングコンテキストに「AIエージェント向けファイルを含めてはいけない」という除外ルールを明示する発想は、CI/CDでの意図しないファイル混入を防ぐ観点から応用可能
- コンテキストの粒度に応じてファイル配置場所を変える（全体共通はcopilot-instructions.md、大容量はdocs/フォルダ＋@参照）という階層化戦略は、LLMのコンテキストウィンドウ効率化にも直結する

## 前提知識

- **GitHub Copilot** → /deep_1739 8リポジトリに同じ変更を並列展開したら、Copilotレビューのばらつきがシグナルになった話
- **Custom instructions** (TODO: 読むべき)
- **Agent Skills** → /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_3094 LLMに図面情報を全部見せる設計をやめた話
- /deep_2823 GitHub Copilot CLIの使い方を学ぶ方法
- /deep_2817 AIマルチセッション運営で気づいた7つの原則 — 3日間で270万行を消して見えた景色
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク

## 原文リンク

[GitHub Copilotで既存ソフトウェアを改修するためのコンテキスト設計](https://zenn.dev/asagezenn/articles/b827be281ff2cd)
