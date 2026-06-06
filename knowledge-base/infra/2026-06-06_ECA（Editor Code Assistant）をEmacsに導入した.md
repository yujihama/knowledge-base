---
title: "ECA（Editor Code Assistant）をEmacsに導入した"
url: "https://zenn.dev/wakamenod/articles/ae8a4ab4b625bb"
date: 2026-06-06
tags: [ECA, Emacs, LLM, LM Studio, ローカルLLM, コーディングアシスタント, qwen3]
category: "infra"
related: [2862, 7414, 5162, 3088, 5037]
memo: "[Zenn LLM] ECA(Emacs)を導入した"
processed_at: "2026-06-06T09:00:28.302688"
---

## 要約

ECAはEmacsに統合されたLLMベースのコーディングアシスタントで、eca-emacsパッケージとして提供されている。`M-x eca`コマンドで起動するとエディタ右側にチャットウィンドウが開き、Anthropic・OpenAIなどのクラウドプロバイダ、またはLM Studioで起動したローカルLLM（例: qwen3.6-35b-a3b）を利用できる。クラウドの場合は`/login`でプロバイダ認証を行い、`/model`でモデルを選択する。ローカルLLMの場合は`~/.config/eca/config.json`にOpenAI互換APIのエンドポイント（例: http://localhost:1234）とモデル名を記載することで認証なしで利用可能。エージェントモードは`plan`と`code`の2種類があり、`C-c C-b`で切り替える。`plan`モードはコード変更を実行できず、設計・計画専用。`code`モードではDiff付きで変更提案が提示され、`C-c C-a`で個別適用、`C-c C-y`でセッション内の以降の変更を全て自動適用、`C-c C-r`で却下できる。チャットはタブ管理によりスレッド単位で分離でき、`C-c C-n`で新規作成、`C-c C-f`で選択、`C-c C-k`で削除が可能。コンテキスト指定では`@`でファイル・バッファ内容を丸ごと送信、`#`でファイルパスを渡す、`@cursor`でカーソル位置のコードと位置情報を送信できる。Rewrite（特定コード書き換え）やCompletion（コード補完）機能も実装されているが、記事執筆時点ではまだ活用途中とのこと。エージェントアーキテクチャとして、planとcodeの役割分離はLLMエージェントの典型的なreflect/actパターンに対応しており、監査エージェント設計においてもレビュー・承認フロー設計の参考になる。

## アイデア

- planとcodeのエージェントモード分離により、設計フェーズと実装フェーズを明示的に切り分けることで、LLMによる意図しないコード変更を防ぐ設計パターンを実装している
- OpenAI互換API経由でLM Studioのローカルモデルを接続できるため、クラウドAPIキー不要・プライバシー保護の観点からオンプレ利用が容易
- `C-c C-y`による「以降の変更を全自動適用」モードは、信頼度が高い作業では効率化できる一方、監査的観点では変更の追跡可能性とレビューポイントの消失リスクがある

## 前提知識

- **LLM API** → /deep_7066 乗り換え検討用：主要LLM API料金を9社・3階層（フラッグシップ/mini/nano）で比較 2026年5月更新
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Emacs Lisp** (TODO: 読むべき)
- **エージェントモード** (TODO: 読むべき)
- **LM Studio** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_7414 M1 Pro 32GBでQwen3.6-35B-A3Bを本気で使ってみた正直な話
- /deep_5162 GitHub CopilotのバックエンドをLM Studioのローカルモデル（Qwen3.6 35B-A3B）に差し替える手順と検証結果
- /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる

## 原文リンク

[ECA（Editor Code Assistant）をEmacsに導入した](https://zenn.dev/wakamenod/articles/ae8a4ab4b625bb)
