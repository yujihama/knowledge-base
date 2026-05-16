---
title: "Claude CodeのWebFetchは実際にはHaikuによる要約を返している：内部構造の解析"
url: "https://zenn.dev/zhizhiarv/articles/claude-code-webfetch-haiku-summary"
date: 2026-05-10
tags: [Claude Code, WebFetch, Haiku, LLM中間処理, プロキシ要約, トランケーション, リバースエンジニアリング, 著作権制約]
category: "infra"
related: [1429, 4753, 2953, 430, 2688]
memo: "[Zenn LLM] あなたのClaude CodeのWebFetch、実はWebをちゃんと読んでいない"
processed_at: "2026-05-10T09:32:05.274233"
---

## 要約

Claude CodeのWebFetchツールは、ユーザーが「200KBのページを読んだ」と思っていても、実際にはメインモデル（OpusやSonnet）にはHaiku（小型高速モデル）が生成した要約テキストしか届いていないことを解説した記事。

画面上には「Received 204.4KB (200 OK)」と表示されるが、これはfetchしたサイズであり、メインモデルが読むresultのサイズではない。Verboseモードを有効化すると、WebFetchツールがurlとpromptの両パラメータを必須で持ち、Haikuに要約させた結果のみをOpus/Sonnetに渡していることが確認できる。

Haikuによる要約をバイパスできる条件は以下の3つをすべて満たす場合のみ：(1) サイトがContent-Type: text/markdownをサポートしていること、(2) docs.python.org・developer.mozilla.org・react.dev・kubernetes.io・docs.aws.amazon.com等、80以上の信頼済みドメインリストに含まれること、(3) Markdownの長さが10万文字以下であること。zenn.devはこのリストに含まれないため常にHaiku経由となる。

トランケーション（切り捨て）も多段階で発生する。HTTPレスポンスは10MiB超で取得失敗、HTMLは先頭1MiB文字のみTurndownでMarkdown変換、Haikuへの入力は10万文字を超えると先頭10万文字で切断される。後半が切れても報告は一切なく、Haikuは不完全なコンテンツをもとに要約する。

さらにHaikuへの内部プロンプトには著作権保護の制約が英語でハードコーディングされており、原文の引用は125文字以内、歌詞の完全出力は禁止されている。日本語記事を読ませても英語の要約が返ることもある。これは「AIがAIの要約を読む伝言ゲーム」であり、ハルシネーションリスクの増大・細部情報の損失・ニュアンスの変質につながる。

2026年5月4日時点の検証で、過去のリバースエンジニアリング記事（2025年10月のMikhail Shilkov、Giuseppe Gurgone）と基本構造は同じであることが確認された。対策として/configでVerboseをONにして実際の挙動を可視化すること、または信頼済みドメインのMCPツールを優先使用することが推奨される。

## アイデア

- ツールの入出力サイズと実際にモデルが読むコンテンツサイズが乖離しており、UIが意図せず誤認を誘発する構造になっている点（Received 204.4KBと表示されても読んだのは数百文字の要約）
- 信頼済みドメインリスト（80+ドメイン）とContent-Type: text/markdownの組み合わせでのみバイパス可能という設計は、著作権保護とパフォーマンス最適化を同時に実現しようとした実用的なトレードオフ
- Haikuへの指示プロンプトが英語でハードコーディングされているため、日本語コンテキストでも要約が英語で返る問題は、多言語対応エージェント設計における言語コンテキスト伝播の見落としとして参考になる

## 前提知識

- **Claude Code WebFetch** (TODO: 読むべき)
- **Haiku（Anthropicモデル）** (TODO: 読むべき)
- **Turndown（HTML→Markdown変換）** (TODO: 読むべき)
- **信頼済みドメインリスト** (TODO: 読むべき)
- **LLMトークン制限** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」

## 原文リンク

[Claude CodeのWebFetchは実際にはHaikuによる要約を返している：内部構造の解析](https://zenn.dev/zhizhiarv/articles/claude-code-webfetch-haiku-summary)
