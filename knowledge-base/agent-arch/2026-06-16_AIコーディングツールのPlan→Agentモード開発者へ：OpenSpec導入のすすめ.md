---
title: "AIコーディングツールのPlan→Agentモード開発者へ：OpenSpec導入のすすめ"
url: "https://zenn.dev/ihdk77/articles/955be718b412f1"
date: 2026-06-16
tags: [OpenSpec, 仕様駆動開発, SDD, Claude Code, GitHub Copilot, Spec Kit, Kiro, AIコーディング, Planモード, Agentモード]
category: "agent-arch"
related: [1736, 6475, 4470, 2361, 6333]
memo: "[Zenn LLM] AIコーディングツールでの開発（Planモード→Agentモード）に慣れてきた人へ 次はOpenSpec導入のすすめ"
processed_at: "2026-06-16T09:08:05.106019"
---

## 要約

GitHub CopilotやClaude CodeなどのAIコーディングツールでPlanモード→Agentモードの仕様駆動開発（SDD）に慣れてきた開発者向けに、OSSフレームワーク「OpenSpec」を紹介する記事。

Plan→Agent開発で著者が感じた3つの課題：①計画がチャット内の一時成果物にとどまり資産化されない、②指示の粒度やモデルの応答揺れで計画品質がばらつく、③複数ツール・複数メンバー間で前提がずれやすい。

OpenSpecはこれらを解決する軽量SDDフレームワークで、GitHubスター数46.7k（v1.3.1、2026年4月リリース）、30以上のAIツールに対応。APIキーやMCPサーバー追加は不要。基本コマンドは`propose`（計画作成）・`apply`（実装）・`archive`（完了計画保管）の3つ。`npm install -g @fission-ai/openspec@latest`と`openspec init`の2ステップで導入完了。

`propose`実行時に`openspec/changes/<作業名>/`配下にproposal.md・specs/・design.md・tasks.mdの4種ファイルが自動生成され、変更単位で仕様と設計が永続化される。`archive`実行で`openspec/changes/archive/YYYY-MM-DD-<作業名>/`に日付付き保存。`sync`コマンドで最新仕様を`openspec/specs/`（マスター）へ反映可能。

著者がClaude Codeで検証した結果、1日5機能の実装・改修を完了し、手動修正がほぼ不要な品質を実現。tasks.mdに「動作確認を行うこと」と記載するとエージェントがDockerコンテナ内でPythonファイルを実行し結果・速度まで提示した。一方、トークン消費量は従来比約1.5〜2倍に増加する点が課題で、各コマンド前に`/clear`でチャットをクリアする対策が有効。

類似ツールとの比較では、GitHub公式の「Spec Kit」（95.4kスター、30以上対応）、AWS公式の「Kiro」（月50クレジット無料・Pro $20/月〜、専用IDE移行が前提）、KiroインスパイアのOSS「cc-sdd」（17スキル搭載）が挙げられる。Copilotを既に使っている場合はOpenSpecかSpec Kitが第一候補。

監査エージェント開発への示唆：propose→apply→archiveの変更単位での仕様永続化は、監査証跡の自動生成・変更理由の記録という観点でGRC（ガバナンス・リスク・コンプライアンス）管理と親和性が高い。複数エージェントが同一仕様ファイルを参照する設計は、LangGraphなどマルチエージェント構成での仕様整合性維持にも応用できる。

## アイデア

- propose→apply→archiveの変更単位での仕様永続化により、チャット一時成果物だった計画をプロジェクト資産に昇格させる設計思想
- 30以上のAIツールに対して共通コマンドセットを配布する「スキルファイル自動展開」方式でツールロックインを低減する仕組み
- tasks.mdのチェックボックスをエージェントがリアルタイム更新することで、長時間実行エージェントの進捗を人間が追跡可能にするUX設計

## 前提知識

- **仕様駆動開発（SDD）** (TODO: 読むべき)
- **AIコーディングエージェント** → /deep_3774 Claude Codeに「/create-design-md」を自作して、0→1開発のUIブレをなくした話
- **Plan/Agentモード** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える

## 関連記事

- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_6475 コードレビューを6段階にしたら、AIと人間の分業が見えた
- /deep_4470 SPReAD 研究計画調書作成を伴走支援する Skill を作ってみた
- /deep_2361 MCPサーバー開発におけるTool数の上限について考える
- /deep_6333 Google I/O 2026：コーディングAIでの挽回、科学AI、そして業界ドラマ

## 原文リンク

[AIコーディングツールのPlan→Agentモード開発者へ：OpenSpec導入のすすめ](https://zenn.dev/ihdk77/articles/955be718b412f1)
