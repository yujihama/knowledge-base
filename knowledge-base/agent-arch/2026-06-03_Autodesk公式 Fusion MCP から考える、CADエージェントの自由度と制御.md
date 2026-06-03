---
title: "Autodesk公式 Fusion MCP から考える、CADエージェントの自由度と制御"
url: "https://zenn.dev/0xliclog/articles/4bb44fd7163352"
date: 2026-06-03
tags: [MCP, Fusion360, CADエージェント, DSL, LLM-as-executor, Verify層, AutoCAD, script実行方式]
category: "agent-arch"
related: [5476, 5887, 5862, 5947, 5669]
memo: "[Zenn LLM] Autodesk公式 Fusion MCP から考える、CADエージェントの自由度と制御"
processed_at: "2026-06-03T09:03:26.731353"
---

## 要約

AutodeskがリリースしたFusion MCPを実際にClaude Desktopから接続して検証した結果と、CADエージェント設計における「script実行方式」vs「DSL方式」のトレードオフを整理した記事。

Fusion MCPが公開するツールはfusion_mcp_read・fusion_mcp_execute・fusion_mcp_updateの3つのみ。create_boxやextrude等の個別CAD操作ツールは存在せず、execute.scriptにPythonスクリプトを渡してFusion APIを呼び出す構成になっている。LLMはまずread.apiDocumentationでAPI仕様を確認し、Pythonスクリプトを生成してexecute.scriptで実行、結果をprint()出力で受け取り、read.screenshotで視覚確認、失敗時はupdate.undoで戻すというループで動作する。

この設計の最大のメリットは自由度の高さで、Fusion APIで書ける処理はすべてLLMがその場でスクリプトとして組み立てられる。一方でデメリットとして、操作だけでなく観測（モデル構造の走査）・検証（操作後の正否確認）もすべてLLM生成スクリプトに依存する点が挙げられる。execute.scriptがsuccess: trueを返しても、それはPythonのrun()関数が例外なく終了したことを示すにすぎず、CADタスクとして正しく完了したかは別途確認が必要。read.screenshotも見た目確認には有効だが、CADデータとしての正確性（appearance/materialの一致、変更漏れ、参照関係の整合性等）の確認には不十分。

実務向けCADエージェントにはVerify層が必要で、著者は①個別オブジェクトの操作後チェック（body.appearance.id == expected等）、②スコープ全体の整合性（変更対象の網羅性・変更禁止対象の不変性）、③システムレベルの不変条件（bounding box異常、タイムライン破損等）の3層構成を提案している。

著者自身が開発するAutoCADエージェントではDSL（操作手順JSON）をLLMに生成させ、C#側で検証してから.NET API経由で実行する方式を採用。Fusion MCPのscript実行方式に比べ自由度は落ちるが、スキーマ検証・危険操作の制限・ログ追跡・Verify組み込みが容易になる。script実行方式は未知の操作への対応力が高く、DSL方式は決定論的な制御がしやすいというトレードオフがあり、どちらが正解ではなく用途に応じた設計判断が求められる。監査エージェント開発への示唆として、LLM生成コードの実行に依存する構成では「実行成功≠タスク達成」という点を設計に組み込むVerify層の重要性が高い。

## アイデア

- execute.scriptのsuccess: trueはPython例外なし終了を示すだけで、CADタスク達成の確認にはならないという「実行成功≠タスク達成」の概念は、監査エージェントのツール実行結果検証にも直接応用できる
- 操作・観測・検証をすべてLLM生成スクリプトに寄せる設計と、DSLで中間表現を挟んで検証可能にする設計のトレードオフ整理は、エージェント設計一般に適用できるフレームワーク
- CAD向けVerify層の3層構成（個別オブジェクトチェック／スコープ整合性／システム不変条件）は、ファイル操作・DB操作等の副作用を持つエージェントの検証設計パターンとして汎用性がある

## 前提知識

- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Fusion API** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **DSL** → /deep_485 なぜLLMにDSLを直接書かせないのか — Nia Drawing Languageの4層アーキテクチャ
- **LLM tool use** (TODO: 読むべき)

## 関連記事

- /deep_5476 金融部門への先進AI技術導入：ガバナンス後追いとエージェント化の現在地
- /deep_5887 金融部門への先進AI技術の実装：ガバナンス後追いとボトムアップ採用の現実
- /deep_5862 金融部門への先進AI技術の実装：ガバナンス後追いとボトムアップ導入の現実
- /deep_5947 金融部門における先進AI技術の実装：ガバナンス後追いと人材ギャップの課題
- /deep_5669 金融部門における先進AI技術の実装：ガバナンス不在のボトムアップ導入が招くリスクと次のステップ

## 原文リンク

[Autodesk公式 Fusion MCP から考える、CADエージェントの自由度と制御](https://zenn.dev/0xliclog/articles/4bb44fd7163352)
