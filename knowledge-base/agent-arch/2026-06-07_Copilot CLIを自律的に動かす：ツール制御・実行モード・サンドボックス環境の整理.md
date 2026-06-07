---
title: "Copilot CLIを自律的に動かす：ツール制御・実行モード・サンドボックス環境の整理"
url: "https://zenn.dev/nozomu/articles/ddbda3456cf077"
date: 2026-06-07
tags: [GitHub Copilot CLI, エージェント制御, preToolUse フック, Docker Sandboxes, autopilot, サンドボックス, ツール権限管理]
category: "agent-arch"
related: [2550, 7106, 3086, 4228, 1834]
memo: "[Zenn LLM] Copilot CLIを自律的に動かす"
processed_at: "2026-06-07T21:15:15.299758"
---

## 要約

GitHub Copilot CLIをエージェントとして自律的に動作させる際に、安全性と利便性を両立するための設定方法を体系的に整理した記事。整理の軸は「できること（権限）」「動かし方（モード）」「実行環境」の3層構造。

**ツール制御層**では、`--available-tools`（許可リスト）と`--excluded-tools`（拒否リスト）でモデルに見せるツール自体を絞り込む。さらに`--allow-tool`/`--deny-tool`で個別操作の承認可否を制御し、`deny`は`allow`より優先される。例として`shell(git:*)`を許可しつつ`shell(git push)`のみ拒否するといった粒度の制御が可能。ネットワークアクセスは`--allow-url`/`--deny-url`でドメイン単位、ファイルアクセスは`--add-dir`でディレクトリ単位に限定できる。対話中に承認した判断は`~/.copilot/permissions-config.json`にプロジェクトパスごとに永続化される。

**条件付き制御**には`preToolUse`フックを活用する。ツール実行前にシェルスクリプトを呼び出し、stdoutにJSONを返すことで許可・拒否・確認・引数変更を動的に決定できる。単純なコマンド名マッチングではなく、lockfileの`postinstall`有無や削除ファイル数など文脈依存の判断が実装可能。フックのログを蓄積して運用ルールを育てるアプローチも紹介されている。

**実行モード**はinteractive（対話）、plan（計画先行）、autopilot（多段自律実行）の3種。`--max-autopilot-continues`で継続回数に上限を設定できる。`-p`/`--prompt`オプションでCI・スクリプトからの単発実行も可能。`/goal`で目標を固定して脱線を防ぎ、`/fleet`で複数サブエージェントへの並列タスク分散ができる。

**実行環境**については、`--allow-all-tools`/`--allow-all-paths`/`--allow-all-urls`（これらをまとめた`--allow-all`および`--yolo`）はホスト環境での常用を避け、Docker Sandboxes（microVM）やCIでの利用を推奨。`sbx run copilot`でサンドボックス内にCopilot CLIを起動でき、デフォルトで`--yolo`モードが適用される。ただしワークスペースディレクトリはホストにマウントされるため、ファイル変更はホストに即時反映される点に注意が必要。監査エージェント開発への示唆として、エージェントの権限設計を「認識層（見せるツール）→承認層（allow/deny）→条件判定層（フック）→環境層（サンドボックス）」の4段階で考えるフレームワークは、LangGraphベースのReActエージェントにおけるツール呼び出し制御設計にそのまま応用できる。

## アイデア

- 「認識層→承認層→条件判定層→環境層」という4段階の権限設計フレームワークは、LangGraphやMCPベースのエージェントシステムにおけるツール呼び出し制御の設計パターンとして汎用的に応用できる
- preToolUseフックでlockfileや差分を動的に解析して許可判断する仕組みは、監査エージェントにおける操作ログ検証や異常検知ロジックの実装アイデアに直結する
- フックのログから「よく許可している操作」を抽出してエイリアス化・ルール化するアプローチは、エージェントの運用ポリシーをデータドリブンで育てるフィードバックループとして興味深い

## 前提知識

- **GitHub Copilot CLI** → /deep_2823 GitHub Copilot CLIの使い方を学ぶ方法
- **エージェントツール呼び出し** (TODO: 読むべき)
- **Docker microVM** (TODO: 読むべき)
- **preToolUse フック** (TODO: 読むべき)
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_7106 ローカルLLM（gpt-oss:20b）にWebアプリを自律生成させた実験：28秒で完成、セキュリティテスト22件全PASS
- /deep_3086 なぜ、Claude CodeもCodexもエージェントではありえないのか？
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計
- /deep_1834 Lutum: 高度なハーネスエンジニアリングのためのRust製LLM SDK

## 原文リンク

[Copilot CLIを自律的に動かす：ツール制御・実行モード・サンドボックス環境の整理](https://zenn.dev/nozomu/articles/ddbda3456cf077)
