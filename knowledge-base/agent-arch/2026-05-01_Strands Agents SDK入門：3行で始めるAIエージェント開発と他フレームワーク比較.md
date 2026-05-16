---
title: "Strands Agents SDK入門：3行で始めるAIエージェント開発と他フレームワーク比較"
url: "https://zenn.dev/0h_n0/articles/d509a8830be75b"
date: 2026-05-01
tags: [Strands Agents SDK, model-driven, MCP, Steeringフック, マルチエージェント, AWS Bedrock, LangGraph比較, Agents-as-Tools, Swarm, Handoffs]
category: "agent-arch"
related: [2550, 88, 3241, 3000, 628]
memo: "[Zenn LLM] Strands Agents SDK入門 3行で始めるAIエージェント開発と他フレームワーク比較"
processed_at: "2026-05-01T12:21:59.092902"
---

## 要約

Strands Agents SDKは、AWSが2025年5月にOSSとしてリリースしたAIエージェントフレームワークで、2026年4月時点で累計1,400万ダウンロードを超えている。設計思想の核は「model-driven（モデル駆動型）」で、LLMの推論能力に計画・判断を委ね、開発者はModel・Tools・Promptの3要素だけを定義すれば動作する。LangGraphのような明示的なグラフ設計やフロー制御コードが不要なため、最小構成は3行のPythonコードで実現できる。

ツール定義は@toolデコレータを使い、関数のDocstringがLLMへのツール説明として自動使用される。Model Context Protocol（MCP）をネイティブサポートしており、数千の既存MCPサーバーをコードなしで接続可能。ツールのセマンティック検索による動的フィルタリングも備える。

特徴的な機能として「Steeringフック」がある。エージェントの実行ループにbefore_tool/after_modelなどのフックを挿入し、ジャストインタイムのガイダンスを提供する。公式ベンチマーク（600回の評価実行）では、Steeringフック付きエージェントが100%のタスク精度を達成し、プロンプトのみ（82.5%）やハードコード・ワークフロー（80.8%）を上回った。

v1.0ではマルチエージェントパターンが4種類公式サポートされた。①Agents-as-Tools：専門エージェントをツールとして登録しオーケストレータが動的委任、②Swarm：共有メモリを通じた中央集権なしの自律型チーム協調、③Graph：条件分岐を含む決定論的ワークフロー（LangGraphに近い制御）、④Handoffs：対応不能時に会話履歴を保持したまま人間に引き継ぐ機能。

LangGraphとの比較では、Strandsはコード量を削減できる反面、ワークフローの各ステップを厳密に制御したい場合はLangGraphが適する。CrewAIはロールベースの協調が強みだが、Strandsはより軽量でツール中心。OpenAI Agents SDKはOpenAI依存だが、StrandsはBedrock・OpenAI・Anthropic・Ollamaなど多プロバイダー対応。

監査エージェント開発への示唆として、Steeringフックによるbefore_toolフックでの危険操作ブロック・入力検証パターンは、監査エージェントのガードレール実装に直接応用可能。また4種類のマルチエージェントパターンのうち、Graphパターンは承認フロー・段階的処理に適しており、内部統制ワークフローの自動化に親和性が高い。

## アイデア

- Steeringフックによる『ジャストインタイム介入』がプロンプト詰め込み（82.5%）やハードコードワークフロー（80.8%）より高精度（100%）を達成した点は、エージェントの信頼性向上において実行ループへの動的介入が静的定義より優れることを示す実証データとして注目に値する
- DocstringをLLMへのツールスキーマとして自動利用する設計は、コード自体がエージェントへの仕様書になるという開発体験の統一であり、スキーマ定義の二重管理問題を根本から排除している
- 4つのマルチエージェントパターン（Agents-as-Tools/Swarm/Graph/Handoffs）を単一SDKで提供し、制御粒度に応じて使い分けられる設計は、エージェントアーキテクチャ選定における『制御 vs 自律』のトレードオフを明示的に整理したフレームワーク設計として参考になる

## 前提知識

- **ReAct / ツール使用型LLM** (TODO: 読むべき)
- **MCP (Model Context Protocol)** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **マルチエージェントオーケストレーション** → /deep_1561 リーダーシップクラスシステムにおける高スループット材料スクリーニングのためのマルチエージェントオーケストレーション
- **AWS Bedrock** (TODO: 読むべき)

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_3241 VSCodeリリースノートで追うGitHub Copilot進化史 (v1.86 → v1.116)
- /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較
- /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 原文リンク

[Strands Agents SDK入門：3行で始めるAIエージェント開発と他フレームワーク比較](https://zenn.dev/0h_n0/articles/d509a8830be75b)
