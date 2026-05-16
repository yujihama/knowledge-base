---
title: "Parse Guard：LLMアプリに「読んだつもり」をさせない入力検証パターン"
url: "https://zenn.dev/kanaria007/articles/5c0b35e0c6d670"
date: 2026-05-08
tags: [Parse Guard, 入力検証, LLMアプリ設計, observation_status, limited mode, RAG, action boundary, TypeScript, ワークフロー制御, エラーハンドリング]
category: "agent-arch"
related: [1116, 3898, 2794, 1334, 2103]
memo: "[Zenn LLM] Parse Guard：LLMアプリに読んだつもりをさせない入力検証パターン"
processed_at: "2026-05-08T09:42:50.276293"
---

## 要約

LLMアプリケーションで頻発する「入力が不完全なのに処理を続行してしまう」問題に対処するための設計パターン「Parse Guard」を解説した記事。Parse Guardは、LLMに入力を渡す前、またはLLMの出力を次の処理に渡す前に、入力が最低限の条件を満たしているかをシステム側で構造化して判定するゲートである。

核心的な問題意識は、LLMはRAG検索結果が空でも・添付ファイルが読めなくても・必須フィールドが欠けていても「それらしい出力」を生成できてしまう点にある。これは単なるハルシネーションとは異なり、「システム側が処理続行の条件を明示していないこと」が根本原因である。

最小設計として、入力に `observation_status`（`pending` / `parsed` / `partial` / `blocked`）を持たせる。`parseGuard()` 関数は `GuardDecision` として `{ok: true, mode: "normal"}` / `{ok: true, mode: "limited", limitations: string[]}` / `{ok: false, reason: string}` の3パターンを返す。`present_fields` と `required_fields` の差分から `missing_fields` を再計算し、外部から渡された値をそのまま信用しない設計が重要。

`limited` モードでは処理を完全停止せず、「不足情報を聞き返す」「draft のみ生成」「support-only として要約のみ」といった限定的な処理を許可する。LLMへのプロンプトにも `limitations` を明示的に渡し、断定表現を禁止する。さらに出力後の structured check で、`limited` モードなのに断定表現や根拠なき事実が含まれていれば再生成・人間レビューに差し戻す。

前記事で定義した `support-only` / `review-only` / `effect-bearing` のアクション境界とも統合され、`partial` 状態では `effect-bearing`（外部状態を変更するアクション）を禁止する。また `limited` モードで作成した `review-only` 提案を承認後にそのまま `effect-bearing` に昇格させることも禁止し、必ず欠損情報を補完した上でParse Guardを再実行する2段階ゲートを設ける。

RAGにも同パターンを適用し、`RetrievalCheck`（`sufficient` / `insufficient` / `empty`）でチェックする。スコア閾値0.7（ドメインに応じて調整）未満は `insufficient` として限定モードに落とす。添付ファイルでも `received`（受け取り）と `parsed`（テキスト抽出成功）を分離した `AttachmentParseResult` で管理する。

監査エージェント開発への示唆として、監査証跡の収集・エビデンスの読み込みが不完全な状態で統制評価や指摘事項生成に進む事故を防ぐ直接的なパターンである。`effect-bearing` 禁止の境界制御は、不完全証跡に基づく誤った監査結論の自動出力を防ぐアーキテクチャ上の安全弁として特に有効。

## アイデア

- 「読んだ」と「読めた」を構造化データとして分離するという発想は、LLMの確率的生成の不確実性をシステムアーキテクチャ層で吸収するアプローチとして汎用性が高い
- limited/normal/blockedの3モード分岐により、binary（止める/進める）ではなく「どのモードなら安全に進められるか」を返す設計が、実務的なユーザー体験と安全性を両立する
- limited モードで作った提案を effect-bearing に昇格させる前に Parse Guard を再実行する「2段階ゲート」は、人間の承認が安全性を保証しないという重要な原則を明示している

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **TypeScript型システム** (TODO: 読むべき)
- **ワークフロー境界設計** (TODO: 読むべき)
- **ハルシネーション対策** → /deep_10 LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装

## 関連記事

- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する

## 原文リンク

[Parse Guard：LLMアプリに「読んだつもり」をさせない入力検証パターン](https://zenn.dev/kanaria007/articles/5c0b35e0c6d670)
