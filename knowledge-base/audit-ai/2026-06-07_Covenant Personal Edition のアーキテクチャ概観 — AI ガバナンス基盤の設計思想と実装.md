---
title: "Covenant Personal Edition のアーキテクチャ概観 — AI ガバナンス基盤の設計思想と実装"
url: "https://zenn.dev/exapolicy/articles/f3a84172f0089c"
date: 2026-06-07
tags: [AIガバナンス, ローカルファースト, LLMルーティング, DLM, Tauri, Ollama, audit.jsonl, Fail-Closed, PII検知, 説明責任]
category: "audit-ai"
related: [1516, 4521, 3642, 7602, 4750]
memo: "[Zenn LLM] Covenant Personal Edition のアーキテクチャ概観 — AI ガバナンス基盤の設計思想と実装"
processed_at: "2026-06-07T09:03:51.773071"
---

## 要約

Covenant Personal Editionは、個人事業主・フリーランス・小規模事業者向けのAIガバナンス管理アプリ。「契約と認証で守る」SaaS主流アプローチに対し、「自分で握る」ローカルファースト設計を採用する。技術スタックはTauri + React + TypeScript（フロントエンド）、Pythonサイドカー（バックエンド）、プロセス間通信はHTTPリスナーを持たない標準入出力経由のJSON-RPC 2.0。データ永続化はSQLite + JSONL、ポリシー定義はYAML（org.yaml / project.yaml の階層構造）で人間可読・Git管理可能。

コア機能である Gate Pipeline は6段構成（Gate 0〜3）。Gate 0が正規化などの前処理、Gate 1がPII・ソースコード・機密用語の正規表現による静的検知、Gate 2がYAMLポリシー照合、Gate 2.5が軽量LLMによる意図判定、Gate 2.8が無害プレフィルタ（Gate 3の計算コスト削減目的）、Gate 3がLlama 3.1 8B等のローカルLLMによる倫理性・安全性の2軸スコアリング（1.0〜10.0の連続値）。「評価（AI）→判定（ポリシー）→判断（人間）」の三段構造で責務を分離し、AI に最終意思決定を委ねない設計はPMBOK第8版の説明責任要件に対応する。判定不能時はFail-Closedで「保留」または「ブロック」を選択。

DLM（Data Lifecycle Management）は情報をL1（公開情報）〜L4（極秘・マイナンバー等）の4段階に分類し、LLMダイナミックルーティングを実装。L1はクラウドAI送信可、L2はポリシー設定次第、L3はローカルLLM処理、L4は全LLMへの送信をブロックしaudit記録のみ。「連鎖伝播問題」（高機密入力後スレッド全体が永久に高セキュリティ要件に縛られる問題）を、thread_max（監査用ウォーターマーク、単調増加）とpayload_level（スライディングウィンドウで動的計算、ユーザー入力のみ参照）の2軸分離で解決。

audit.jsonlには送信タイムスタンプ・機密レベルラベル・ルーティング先・ブロック理由を記録するが、プロンプト本文は意図的に残さない設計（プライバシー確保と説明責任の両立）。「漏洩しないことを約束する」ではなく「何が起きたか自分で検証できる」Verifiable Accountabilityを実現する。

限界として、ローカルPC自体の物理セキュリティはユーザー責任、クラウドAIへの送信後のリスクはCovenant範囲外、dGPU非搭載PC環境ではGate 3が184秒程度かかる事例あり、ポリシー定義・更新もユーザー責任と明示。監査エージェント開発への示唆として、Gate PipelineのFail-Closed原則とevaluation/judgment/decisionの三段分離はLangGraphベースの監査エージェントにおけるヒューマンインザループ設計の参考になる。

## アイデア

- thread_max（単調増加の監査ウォーターマーク）とpayload_level（スライディングウィンドウによる動的計算）を分離することで、連鎖伝播問題を解決しつつ高機密スレッドでも対話の進行とともにクラウドAIへ復帰できる設計
- HTTPリスナーを持たない標準入出力経由JSON-RPC 2.0によるプロセス間通信で、SSRF・不正API認証・マルチテナントデータ漏洩をアーキテクチャレベルで排除する手法
- audit.jsonlにプロンプト本文を残さず機密レベルラベルと件数のみを記録することで、Covenant自体が機密情報の蓄積源になるリスクを構造的に回避しつつVerifiable Accountabilityを実現するトレードオフ設計

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Tauri / Rust** (TODO: 読むべき)
- **JSON-RPC 2.0** (TODO: 読むべき)
- **SQLite** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **LLM評価・ルーブリック** (TODO: 読むべき)

## 関連記事

- /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは
- /deep_4521 責任あるAIから、責任を扱えるAIへ――AIエージェント時代に必要な責任経路という補助線
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_7602 教皇の回勅「Magnifica Humanitas」がAI時代における個人の指針を示す
- /deep_4750 なぜ「責任経路工学」だったのか：証拠連鎖を超えたAI責任設計の補助線

## 原文リンク

[Covenant Personal Edition のアーキテクチャ概観 — AI ガバナンス基盤の設計思想と実装](https://zenn.dev/exapolicy/articles/f3a84172f0089c)
