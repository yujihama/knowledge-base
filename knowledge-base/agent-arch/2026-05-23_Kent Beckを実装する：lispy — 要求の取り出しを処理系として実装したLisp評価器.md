---
title: "Kent Beckを実装する：lispy — 要求の取り出しを処理系として実装したLisp評価器"
url: "https://zenn.dev/j_m/articles/55ca25a986633d"
date: 2026-05-23
tags: [lispy, Lisp, TDD, Kent Beck, R/S/K, Zave & Jackson, open texture, event ledger, metacircular, REPL, agent loop, LLM-as-judge]
category: "agent-arch"
related: [6274, 23, 6269, 21, 3343]
memo: "[Zenn LLM] Kent Beck を実装する"
processed_at: "2026-05-23T09:01:29.884893"
---

## 要約

本記事は、著者がZave & JacksonのR/S/K枠組み（要求・仕様・領域知識）とKent BeckのTDD思想を処理系として実装した`lispy`について解説する。lispyはPythonで書かれた小さなLisp評価器だが、エージェントループのコア（`agent-step`など）をS式のbindingとして定義し、REPLを再起動せずにライブ再定義できる点が最大の特徴。

著者の核心的主張は「TDDのredテストを先に書く理由は仕様検証ではなく要求の書き下しだ」というもの。Beckのsmall stepsは「仕様を少しずつ積む手続き」ではなく「半影に沈んだ要求を一テストずつ核へ引き上げる手続き」であるとする。要求はopen texture（Hart概念）を持つため、事前に確定させることが原理的に不可能であり、設計・実装・テスト・運用のあらゆるフェーズで出続ける。

lispyの設計はこの思想を直接反映する。`commit-R`（要求イベント）、`commit-S`（仕様スナップショット）、`commit-K`（領域知識）がappend-onlyのevent ledgerに積まれる。`(define ...)`単体のλは揮発し、`commit-S`を打って初めてgreen（区切り）となる設計は、「区切りを刻む宣言に意味を持たせる」ためである。`test-S-against-R`でK,S⊢Rの整合性判定をLLMに委ねるのは、要求がopen textureゆえに決定的な判定器が原理的に作れないという正直さからくる。

実運用は`server.py --yolo`でenvを常駐させ、外部LLMクライアント（Claude Code等）がbashから`curl`で`/eval`エンドポイントにS式をPOSTする形態。「仕様の高速生成はLLM、要求と領域知識のledgerはlispy」という役割分担で、両者を別プロセスとして並走させる。LLMのセッションが閉じてもledgerはDB上のcommit-Sに残り、翌日`restore-S`で再開できる。

`test-S-against-R`が矛盾を返しても、lispyは何も促さない（「道具は強要しない」）。これはlispy自身が「矛盾時の対処仕様」をハードコードすることを避けるための論理的帰結であり、判断を常に外部（ユーザーまたは外部LLMクライアント）に委ねる設計思想の徹底である。

監査エージェント開発への示唆：audit工程においても「要求は事前確定不可能でフェーズを跨いで出続ける」という構造は直接適用できる。規制要件の解釈変更・監査手続きの再定義を`commit-R replaces`として追跡し、仕様（監査ロジック）との整合をLLM判定する設計は、監査エージェントの要件管理アーキテクチャとして参考になる。

## アイデア

- エージェントループ自体をS式で定義しREPL内でライブ再定義可能にすることで、「走らせながら要求を取り出す」サイクルを処理系レベルで実現している点
- commit-Rをappend-onlyにすることで「要求に終わりがない」という原理的性質を不変条件として実装し、仕様変更を破壊ではなくlineage付きsnapshotとして追跡できる点
- test-S-against-R（K,S⊢R判定）をLLMに委ねる設計が「決定的判定器の原理的不可能性」への正直さであり、判断の審級を二度（整合判定・判定の使い方）処理系の外に譲る二段構造になっている点

## 前提知識

- **TDD / red-green-refactor** (TODO: 読むべき)
- **Zave & Jackson R/S/K** (TODO: 読むべき)
- **metacircular評価器** (TODO: 読むべき)
- **append-only event ledger** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_6274 DeepSeek V4 Flash (ds4.c) を Lisp 的に扱う――エージェントループをS式として走行中に書き換える
- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_6269 開発しながらLoRAデータが自動で貯まる仕組み「M2LoRA」を作った
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_3343 誰の物語が語られるか？LLMによる生活語りの要約におけるポジショナリティとバイアス

## 原文リンク

[Kent Beckを実装する：lispy — 要求の取り出しを処理系として実装したLisp評価器](https://zenn.dev/j_m/articles/55ca25a986633d)
