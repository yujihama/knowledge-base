---
title: "WantedlyのPlaywright自動化で3回連続404——CDPセッション越しにフォームへ辿り着くまでの1時間"
url: "https://zenn.dev/taito_ichinose/articles/ichinose-post-4486"
date: 2026-05-08
tags: [Playwright, CDP, ブラウザ自動化, Python, Brave, React, Wantedly, Claude Code, Ollama]
category: "infra"
related: [2950, 2404, 1736, 3186, 2872]
memo: "[Zenn LLM] WantedlyのPlaywright自動化で3回連続404——CDPセッション越しにフォームへ辿り着くまでの1時間"
processed_at: "2026-05-08T21:10:13.879526"
---

## 要約

macOS + Python 3.12 + Playwright（CDP経由でBrave接続）の構成で、WantedlyのプロフィールページをPlaywright自動化しようとした際に発生した404エラーの原因特定と解決プロセスを記録した実践記事。

問題の核心は「URLのハードコード」と「アカウント状態依存のUIフロー」の組み合わせ。`/users/edit`に直接`goto()`しても404が返り、`/users/me/edit`や`/profile/edit`に変えても同じ結果だった。スクリーンショットで確認するとWantedlyドメインへの到達・セッション維持は確認できたため、URLの誤りではなく「ユーザーIDが確定していないとプロフィール編集ページが存在しない」というサービス設計上の問題と判明した。

新規Wantedlyアカウントでは、初回ログイン後に必ず`wantedly.com/id/{ユーザー名}`形式のIDを確定させるウィザード画面が挟まる。このウィザードを完了させないとプロフィール編集ページのURLが存在しないため、直接`goto()`すると無条件で404になる。スクリプトはこのウィザードを無視していたため、毎回弾かれていた。

解決は5ステップで実施。①`goto()`直後に`page.url`をログ出力して実際のリダイレクト先を可視化。②URLに`setup`が含まれるか`h1`に「IDを設定」が見えたらウィザードフローに入る分岐を追加。③ウィザード完了後の`page.url`から動的にユーザー名を抽出（`wantedly.com/id/{username}`形式）。④`/users/edit`への直接`goto()`をやめ、プロフィールページを開いてから「プロフィール項目を追加・生成」ボタンをクリックする方式に変更。⑤ReactフォームへのnativeセッターパターンでInputイベントを発火（`fill()`だけではReactに状態変化が伝わらない）。

Reactアプリへの入力問題（`fill()`が効かない）は、`Object.getOwnPropertyDescriptor`でHTMLTextAreaElement.prototypeのvalueセッターを取得し、`dispatchEvent(new Event('input', { bubbles: true }))`でInputイベントを手動発火することで解決。このパターンはCoconaraの自動化でも実証済みのものを流用した。

監査エージェント開発への示唆として、エージェントが外部Webサービスと連携する際、「アカウント状態に応じて画面フローが変わるサービス」に対してURLハードコードは脆弱である。遷移後の現在地（`page.url`）を確認してから次アクションを決定する「状態確認→行動」パターンはReActエージェントの基本構造と一致しており、ブラウザ操作エージェント設計においても同様のステートフルな状態管理が必要になる。

## アイデア

- 「現在地確認→行動決定」パターン：goto()直後にpage.urlを取ることでリダイレクト先を把握し、アカウント状態依存のフローに対応できる——これはReActエージェントのObserve→Reasonと同型の構造
- Reactフォームへのnativeセッターパターン：fill()だけではReactの仮想DOMに状態変化が伝わらず、Object.getOwnPropertyDescriptorでprototypeセッターを直接呼び出し＋dispatchEventで解決する手法は他サービスにも転用可能
- 「一度解決した詰まりのスニペットを自動化ライブラリとして蓄積する」開発スタイル：CoconaraのReact入力パターンをWantedlyでそのまま流用できた事例は、LLMによるコード生成と相性が良いパターンカタログ運用の有効性を示す

## 前提知識

- **Playwright CDP** (TODO: 読むべき)
- **ChromeDevTools Protocol** (TODO: 読むべき)
- **React仮想DOM** (TODO: 読むべき)
- **dispatchEvent** (TODO: 読むべき)
- **launchd** (TODO: 読むべき)

## 関連記事

- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_3186 エージェントオーケストレーション：マルチエージェントAIが変えるホワイトカラー業務の全貌
- /deep_2872 file-splitter：ローカルLLM時代のファイル分割ツール

## 原文リンク

[WantedlyのPlaywright自動化で3回連続404——CDPセッション越しにフォームへ辿り着くまでの1時間](https://zenn.dev/taito_ichinose/articles/ichinose-post-4486)
