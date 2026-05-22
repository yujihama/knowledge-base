---
title: "DeepSeek V4 Flash (ds4.c) を Lisp 的に扱う――エージェントループをS式として走行中に書き換える"
url: "https://zenn.dev/j_m/articles/73cd078357b7b0"
date: 2026-05-22
tags: [DeepSeek V4 Flash, ds4.c, Lisp, S式, metacircular, REPL, エージェントループ, 自己書き換え, code=data]
category: "agent-arch"
related: [484, 5946, 64, 2364]
memo: "[Zenn LLM] DeepSeek V4 Flash (ds4.c) を Lisp 的に扱う"
processed_at: "2026-05-22T09:03:48.929252"
---

## 要約

DeepSeek V4 Flash（284Bパラメータ）をローカル実行するための専用推論エンジン ds4.c（DwarfStar 4）が公開されたことを契機に、著者はLisp風のエージェントフレームワーク「lispy」を実装した。

通常のエージェントループ（Claude Code等）はPythonやTypeScriptの関数として静的に固定されており、「tool呼び出し前にcritiqueを挟む」といった小さな変更でもコード修正・再ビルド・再起動が必要になる。lispyはこの問題をLispのcode=dataの性質で解決する。agent-stepをPythonの関数ではなくS式のbindingとしてREPLに配置し、走行中に`(define agent-step ...)`を打ち直すだけで評価規則を即時差し替えられる。

技術的な構成は以下の通り。`llm-call`・`dispatch-tool`・`append-turn`・`make-turn`等の単発primitive（約10個）はPythonで実装し、その上に乗る「呼び出しと結果と再帰の組み立て方」＝エージェントループの規則をS式で記述する。Scheme風の評価器がこのS式を解釈・実行する。

最も特徴的な機能は「LLMによる自己書き換え」。`to-sexp`でagent-stepの現行定義を文字列化→LLMに改良案をS式1つで返させる→`read-sexp`でパース→`eval`でbindingを更新、という4ステップがLispの標準機能だけで完結する。これはJohn McCarthyが1960年の論文でLispの評価器をLisp自身で記述した「metacircular evaluator」の構造を、LLMという新しい層で拡張したもの。

コンテキスト管理については、LLMがコンテキスト長の圧迫を検知した場合に新セッションを自動開始する「renew」機能を実装。通常の要約引き継ぎではなく検索機能を使う設計で、要約の二重適用による情報劣化を避ける。

安全弁として`init.lispy`（seed定義ファイル）を用意しており、自己書き換えで評価器が壊れた際は`(load "init.lispy")`で元の状態に復帰可能。自己書き換えの影響範囲は評価規則レイヤーのみで、Python実装の基盤primitiveには届かない設計になっている。

監査エージェント開発への示唆として、エージェントループをデータとして扱い走行中に差し替える設計は、LangGraphでワークフロー定義を動的変更する場合のコスト（再デプロイ不要）に相当し、審査・承認フローの動的な組み替えや、実行中のcritique注入に直接応用できる。

## アイデア

- エージェントループ自体をS式のbindingとして表現することで、走行中に`define`一発で評価規則を差し替えられる――Pythonベースのフレームワークでは再起動が必要な変更がREPLで即時完了する
- LLMにagent-stepの現行定義を渡して改良版S式を返させ`eval`で取り込む自己書き換えループ――McCarthyの1960年論文のmetacircular evaluator構造にLLMを組み込んだ初めての実用例として位置づけられる
- critique挿入・cost計測・retry追加といった横断的関心事を「実験」と「実装」の区別なくREPLで試せるため、フィードバックループが大幅に短縮される――監査エージェントのフロー動的変更にも転用可能

## 前提知識

- **Lisp/S式** (TODO: 読むべき)
- **metacircular evaluator** (TODO: 読むべき)
- **エージェントループ** → /deep_64 Open Responses: オープンな推論APIスタンダードの概要
- **DeepSeek V4 Flash** (TODO: 読むべき)
- **REPL** → /deep_5215 AIワークフローのテストケースを作る：golden case / regression / incident replay

## 関連記事

- /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- /deep_5946 カスタマーバック・エンジニアリングによるAIイノベーションの推進
- /deep_64 Open Responses: オープンな推論APIスタンダードの概要
- /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす

## 原文リンク

[DeepSeek V4 Flash (ds4.c) を Lisp 的に扱う――エージェントループをS式として走行中に書き換える](https://zenn.dev/j_m/articles/73cd078357b7b0)
