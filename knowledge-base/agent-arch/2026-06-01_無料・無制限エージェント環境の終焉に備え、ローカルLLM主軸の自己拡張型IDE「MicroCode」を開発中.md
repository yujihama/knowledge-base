---
title: "無料・無制限エージェント環境の終焉に備え、ローカルLLM主軸の自己拡張型IDE「MicroCode」を開発中"
url: "https://zenn.dev/volcane/articles/2c374c1ab99909"
date: 2026-06-01
tags: [ローカルLLM, Electron, 自律エージェント, GGUF, Monaco Editor, タスクオーケストレーション, self-healing, Tool Registry]
category: "agent-arch"
related: [5839, 2403, 3653, 6360, 5469]
memo: "[Zenn LLM] 無料 or 無制限のエージェント環境終焉に備え、完全無料のIDEを開発中"
processed_at: "2026-06-01T09:04:19.981750"
---

## 要約

GitHub Copilot、Claude Code、Codexなど主要AIコーディング支援サービスが使用量ベース課金へ移行する中、最後の砦だったGemini Code Assistも2026年6月16日にサービス終了を予定している。これを受け、開発者volcane氏はElectronベースの完全無料IDE「MicroCode」を開発中。VSCodeライクなUIを持ちながらゼロから構築されており、Cursor・Antigravityとは異なるオリジナル実装である。

MicroCodeの設計は4つの柱で構成される。(1) Plan: `plan_and_track`による永続タスク台帳と`hierarchical_task_orchestrator`による親子タスク分解でコンテキスト消失を防止。(2) Act: Monaco Editor上でファイル操作・PowerShell/CMDコマンド実行・内部ブラウザ・Git操作を自律ループへ統合。(3) Verify: `verification_cycle`が静的解析とテスト実行を完了ゲートとして扱い、`self_healing_escalator`が同一失敗の繰り返しを検出してユーザーへ選択肢を提示。(4) Learn: `knowledge_search`/`knowledge_capture`で過去の失敗・成功パターンをMarkdown Wikiとして蓄積し、`context_compactor`で長期記憶を圧縮。

ローカルLLM統合は、所定フォルダへGGUFファイルを配置するだけで自動ロードされドロップダウンから選択可能。外部APIへのコード送信なしに開発が完結するため、機密コードの取り扱いにも適する。ツール定義（JSON）と実装（Python `execute(**kwargs)`）を分離したTool Registryにより、ユーザーがエージェント経由でツールを追加・拡張できる成長型アーキテクチャを採用。

デスクトップマスコット機能では、作業中・エラー時・完了時にアニメーションで状態を視覚化し、バルーンクリックでIDEを最小化したままミニチャットから指示出しが可能。将来的にはモバイルアプリ化（MICROCO MOBILE）でリモート監視・指示・緊急停止にも対応予定。現時点で約90%完成しており、一行プロンプトからWebサイト・簡単なゲームの完成まで実証済み。残課題はサブエージェントによる並列処理とコンテキスト分離による高速化。監査エージェント開発への示唆としては、verification_cycleのような自動検証ループとself_healing_escalatorの失敗検出・エスカレーション設計が、監査手続きの自律実行における品質ゲートとして直接応用可能。

## アイデア

- verification_cycleで静的解析・テストを「完了ゲート」として機能させ、self_healing_escalatorで繰り返し失敗をエスカレーションする設計は、監査エージェントの手続き品質保証に直接転用できる
- ツール定義（JSON）と実装（Python）を分離したTool Registryにより、エージェント自身が新ツールを追加・拡張できる自己拡張ループは、HermesAgent的な「育つエージェント」概念の具体的実装例
- plan_and_trackによる会話履歴と独立した永続タスク台帳は、長期セッションでのコンテキスト消失問題への構造的解決策であり、LangGraphのステート管理と相補的なアプローチ

## 前提知識

- **ローカルLLM / GGUF** (TODO: 読むべき)
- **Electron** → /deep_4618 AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った
- **自律エージェントループ** (TODO: 読むべき)
- **Monaco Editor** (TODO: 読むべき)
- **タスク分解 / オーケストレーション** (TODO: 読むべき)

## 関連記事

- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド

## 原文リンク

[無料・無制限エージェント環境の終焉に備え、ローカルLLM主軸の自己拡張型IDE「MicroCode」を開発中](https://zenn.dev/volcane/articles/2c374c1ab99909)
