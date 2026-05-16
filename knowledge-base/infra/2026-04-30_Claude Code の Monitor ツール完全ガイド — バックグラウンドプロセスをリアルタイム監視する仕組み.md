---
title: "Claude Code の Monitor ツール完全ガイド — バックグラウンドプロセスをリアルタイム監視する仕組み"
url: "https://zenn.dev/tkou15/articles/claude-code-monitor"
date: 2026-04-30
tags: [Claude Code, Monitor, バックグラウンド処理, リアルタイム監視, シェルスクリプト, CI/CD, ログ監視, run_in_background]
category: "infra"
related: [1740, 1428, 1429, 2953, 430]
memo: "[Zenn LLM] Claude Code の Monitor ツール完全ガイド — バックグラウンドプロセスをリアルタイム監視する仕組み"
processed_at: "2026-04-30T12:05:12.870142"
---

## 要約

Claude Code に組み込まれた Monitor ツールは、バックグラウンドで実行中のシェルコマンドの stdout を行単位でリアルタイムにストリーミング受信する機能である。動作フローは「ユーザーが監視対象を指示 → Claude が監視コマンドを生成 → Monitor がバックグラウンド実行 → 各行がイベント通知として Claude に送信 → Claude が即応」という5ステップで構成される。監視中も会話は継続可能であり、Claude は並行して他のタスクを処理できる点が最大の特徴である。

パラメータは4つ：実行コマンドを指定する `command`（必須）、通知に表示される `description`（必須）、デフォルト5分・最大1時間の `timeout_ms`（デフォルト300,000ms）、セッション終了まで実行を継続する `persistent`（デフォルトfalse）。200ms以内に連続して出力された行はバッチ処理されてコンテキスト消費を抑制する設計になっている。

既存の `Bash run_in_background` との違いは通知方式にある。`run_in_background` は完了時に1回だけ通知する「fire-and-forget型」であるのに対し、Monitor は stdout の各行をリアルタイム通知する「継続監視型」である。完了結果だけ必要な場合は `run_in_background`、経過をリアルタイムに追う場合は Monitor と使い分ける。

主なユースケースは4つ。①ログ監視：`tail -n 0 -f production.log | grep --line-buffered 'ERROR\|WARN'` でデプロイ後のエラー即時検知。②CI/PRポーリング：`gh run view` を30秒間隔でループし、完了時に conclusion（success/failure）を出力。③ファイル変更検出：`find ./dist -newer /tmp/last-check` を1秒間隔でチェックしビルド完了を検知。④テスト進捗追跡：`npm test 2>&1 | grep --line-buffered -E '^(PASS|FAIL)'` でサマリ行のみをフィルタリング。

ベストプラクティスとして特に重要なのが `grep --line-buffered` の付与で、これを忘れると grep がバッファリングを行いリアルタイム通知が届かない。また、出力量の制御（フィルタリングでコンテキスト消費を抑制）、ネットワークエラー時の `|| true` や `2>/dev/null` によるハンドリング、同時実行は1〜2個に抑えることが推奨される。監査エージェント開発においては、長時間実行する LangGraph ワークフローの進捗監視や、外部システム（CI/CD、ログ基盤）との連携ポーリングに直接応用可能な設計パターンである。

## アイデア

- stdout の各行をイベントとして Claude のコンテキストに流し込むアーキテクチャは、LangGraph の StreamEvent に近い設計思想であり、エージェントの「外部観察ループ」を宣言的に記述できる抽象化として興味深い
- 200ms バッチ処理によるコンテキストウィンドウ消費の最適化は、高頻度イベントを扱うストリーミングシステム設計の基本原則（マイクロバッチ）をLLMインターフェースに適用した実装例である
- persistent モードと timeout_ms の組み合わせにより、ワンショット監視とセッション全体監視を同一インターフェースで表現できる設計は、エージェントの「ライフサイクル管理」問題への一つの回答である

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Bash バックグラウンド実行** (TODO: 読むべき)
- **stdout ストリーミング** (TODO: 読むべき)
- **grep --line-buffered** (TODO: 読むべき)
- **CI/CDポーリング** (TODO: 読むべき)

## 関連記事

- /deep_1740 AIエージェントの安全性は『モデルの注意力』ではなく『ハーネスの設計』で守る
- /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話

## 原文リンク

[Claude Code の Monitor ツール完全ガイド — バックグラウンドプロセスをリアルタイム監視する仕組み](https://zenn.dev/tkou15/articles/claude-code-monitor)
