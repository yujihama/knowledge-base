---
title: "無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した"
url: "https://zenn.dev/bayar/articles/357285c1e785e5"
date: 2026-05-20
tags: [MCP, colab-mcp, Feynman, Google Colab, 論文復元, AIエージェント, Claude Code, GPU, マルチエージェント, 研究自動化]
category: "agent-arch"
related: [1245, 4520, 3379, 51, 4899]
memo: "[Zenn 機械学習] 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した"
processed_at: "2026-05-20T21:04:02.236869"
---

## 要約

本記事は、Feynman（AIリサーチエージェント）とcolab-mcp（Google ColabのMCPサーバー）を組み合わせ、文献調査から実GPU実験まで費用ゼロで自動化する研究パイプラインの構築手順を解説する。

パイプラインの構成は3層：Feynmanが研究インテリジェンス層として論文の監査（`feynman audit`）と復元計画生成（`feynman replicate`）を担い、Claude Codeがオーケストレーション層として計画をcolab-mcpへ橋渡しし、Google Colab（T4 GPU）が計算実行層として機能する。

colab-mcpは2026年3月にGoogleが公開したMCPサーバーで、AIエージェントがブラウザ上のColabノートブックを直接操作できる。Claude Codeからセルの生成・コード実行・出力取得がプログラマティックに行え、無料T4 GPUを活用できる点が核心的な価値だ。

ワークフローは5フェーズ：①`feynman lit`や`feynman deepresearch`による文献偵察、②`feynman audit`によるarXiv論文とコード実装の差分監査（ハイパーパラメータ不一致・データ前処理の省略・評価指標のズレを検出）、③`feynman replicate`による復元計画のMarkdown出力（依存関係リスト・ハイパーパラメータ・期待指標レンジ含む）、④Claude Code経由でのColab自動実行、⑤Feynmanによる論文結果との差異分析。

実装上の注意点として、公式colab-mcpはGPUランタイム制御ツールを削除しており、コミュニティfork（SebastianGilPinzon版）を使うことでGPU切り替えやツール事前登録の問題を回避できる。Colabのアイドル切断対策にはkeep-aliveスレッドセルが必須。

現状の制約は、FeynmanのデフォルトがDockerサンドボックスで動作しcolab-mcpと直接連携していない点で、著者はFeynmanをforkして実行バックエンドをcolab-mcpに置き換える計画を持つ。完成すれば「仮説生成→GPU実験→結果判断→レポート生成」の自律ループになる。

監査エージェント開発への示唆：`feynman audit`が論文主張とコード実態のギャップを構造的に抽出するアプローチは、監査エビデンスと実装の整合性チェックに転用できる。MCPを介してエージェントが外部計算環境を直接制御するパターンは、LangGraphベースの監査エージェントがクラウドリソースをオーケストレーションする際の参照アーキテクチャになりうる。

## アイデア

- `feynman audit`による論文主張とコード実装の差分検出（ハイパーパラメータ不一致・評価指標のズレ）が、研究再現性の構造的な検証手段として機能している点
- MCPプロトコルを介してAIエージェントがブラウザ上のColabノートブックを直接操作するアーキテクチャにより、ローカル環境とクラウドGPUのオーケストレーションを単一のエージェントループで完結させている点
- 現状は「流水線（Feynman→Claude Code→Colab）」だが、FeynmanのバックエンドをDockerからcolab-mcpに置き換えることで閉じた自律研究ループにする設計方針が明確に示されている点

## 前提知識

- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **Google Colab / T4 GPU** (TODO: 読むべき)
- **AIエージェント / マルチエージェント** (TODO: 読むべき)
- **arXiv論文復元** (TODO: 読むべき)
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_1245 AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α
- /deep_51 SaaSを個人開発して運営しているが、本当に「SaaS is Dead」を感じ始めている
- /deep_4899 OpenHarness：1.1万行のPythonでAI Agentの「黒箱」を丸裸にする

## 原文リンク

[無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した](https://zenn.dev/bayar/articles/357285c1e785e5)
