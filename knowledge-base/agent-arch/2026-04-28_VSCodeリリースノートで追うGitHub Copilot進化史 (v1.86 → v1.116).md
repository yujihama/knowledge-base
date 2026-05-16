---
title: "VSCodeリリースノートで追うGitHub Copilot進化史 (v1.86 → v1.116)"
url: "https://zenn.dev/headwaters/articles/efbb71c684d0a0"
date: 2026-04-28
tags: [GitHub Copilot, VS Code, Agent Mode, MCP, Copilot Edits, マルチエージェント, LLM統合]
category: "agent-arch"
related: [2550, 88, 3000, 628, 2361]
memo: "[Zenn LLM] VSCodeリリースノートで追うGitHub Copilot進化史 (v1.86 → v1.116)"
processed_at: "2026-04-28T12:38:41.911706"
---

## 要約

本記事は、VS Code v1.86（2024年1月）からv1.116（2026年4月）までの31バージョンのリリースノートを横断し、GitHub Copilotが「補完拡張機能」から「VS Code標準搭載のエージェント実行基盤」へ変貌した過程を5つの時期に分けて整理したものである。

第1期（2024年前半、v1.86〜v1.91）では、#file・#codebase・rename suggestions・terminal inline chatといった基本部品が出そろい、エディタ・チャット・ターミナルの3接点が設計された。Chat API / Language Model APIがstableになり、外部拡張が正式参加できる土台が固まった時期である。

第2期（2024年後半、v1.92〜v1.96）では、ベースモデルがGPT-4oへ更新され、.github/copilot-instructions.mdによるcustom instructionsが「設定値」から「共有ファイル」へ移行。v1.95でCopilot Edits（preview）が登場し、ワーキングセット指定による複数ファイル同時編集が可能になった。v1.96のCopilot Free公開により広くユーザーに開放された。

第3期（2025年前半、v1.97〜v1.102）が最大の構造変化期。v1.97でCopilot EditsがGA、Next Edit Suggestions（NES）とAgent Mode（experimental）が登場し、文脈探索・ファイル編集・エラー確認・terminal実行の一気通貫処理が始まった。v1.99でAgent ModeがStableのChat viewへ統合され、Ask/Edit/AgentのUnified Chat viewに再編。MCP server supportも投入された。v1.102ではCopilot Chat拡張がMITライセンスでOSS化され、MCPがGAに到達した。

第4期（2025年後半、v1.103〜v1.110）では、GPT-5・GPT-5 mini・Claude Sonnet 4.5など複数モデルが並立し、Plan agent・Handoffs・subagents・coding agent・Git worktreeによる並列background agentが実装された。MCP marketplace・GitHub MCP Server・MCP Apps・Copilot Memory toolなど外部能力の統合が製品の中心テーマとなった。Agent Sessionsビューが追加され、ローカル/GitHub/CLIをまたぐエージェント管制面として機能し始めた。

第5期（2026年、v1.111〜v1.116）では、週次リリース体制へ移行し、Copilot拡張がbuilt-in extension化されてVS Code本体に吸収される形になった。AIが最初から組み込まれたIDEとしての完成形に近づいている。

この進化は、監査エージェント開発の観点では、MCP・Agent Sessions・custom instructionsによる多段階タスク分解と外部システム統合のアーキテクチャパターンとして参照価値が高い。特にPrompt files（.prompt.md）・Instructions files（.instructions.md）による指示の資産化と再利用の設計は、LangGraphベースの監査ワークフロー設計にも直接応用できる。

## アイデア

- Copilot Editsの登場（v1.95）からAgent Mode（v1.97）への移行がわずか2バージョン・3ヶ月という短期間で行われており、「複数ファイル編集UI」が「自律実行エージェント」への橋渡し構造として機能した点は、エージェント設計の段階的移行モデルとして参考になる
- MCP（Model Context Protocol）がv1.99でserver support投入、v1.102でGAという約3ヶ月のGA化サイクルを経て、marketplace・GitHub MCP Server・Apps・Memory・Pluginsへと拡張されていく過程は、オープンなツール統合プロトコルが製品の中核に吸収されるパターンを示している
- .prompt.mdと.instructions.mdによる「指示の資産化」という設計思想は、プロンプトをコードと同様にバージョン管理・再利用・共有する開発文化への転換を示しており、LangGraphのワークフロー定義やシステムプロンプト管理の標準化に応用できる

## 前提知識

- **GitHub Copilot** → /deep_1739 8リポジトリに同じ変更を並列展開したら、Copilotレビューのばらつきがシグナルになった話
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **Agent Mode** (TODO: 読むべき)
- **Copilot Edits** (TODO: 読むべき)
- **Language Model API** (TODO: 読むべき)

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較
- /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- /deep_2361 MCPサーバー開発におけるTool数の上限について考える

## 原文リンク

[VSCodeリリースノートで追うGitHub Copilot進化史 (v1.86 → v1.116)](https://zenn.dev/headwaters/articles/efbb71c684d0a0)
