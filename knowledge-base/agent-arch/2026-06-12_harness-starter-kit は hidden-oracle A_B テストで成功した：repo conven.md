---
title: "harness-starter-kit は hidden-oracle A/B テストで成功した：repo convention が coding agent の精度を 0/12 から 11/12 に改善"
url: "https://zenn.dev/yuuaan/articles/55501dd45e2522"
date: 2026-06-12
tags: [harness-starter-kit, coding-agent, A/Bテスト, hidden-oracle, AGENTS.md, Codex, file-boundary, repo-convention, benchmark]
category: "agent-arch"
related: [7927, 7339, 23, 1641, 1794]
memo: "[Zenn LLM] 8. ようやく言える：harness-starter-kit は hidden-oracle A/B テストで成功した"
processed_at: "2026-06-12T09:05:17.802595"
---

## 要約

harness-starter-kit（coding agent 向けのリポジトリ規約整備フレームワーク）の有効性を、hidden-oracle 方式の A/B テストで定量的に検証した報告。

【テスト設計】Flask アプリを題材に、harness なし（flask-no-harness）と harness あり（flask-yes-harness）の 2 つのリポジトリを用意。4 つの API 実装タスク（stock risk report API, supplier readiness API, bundle quote API, reservation preview API）を各 3 回、計 24 回 OpenAI Codex（reasoning_effort=medium, service_tier=priority）で実行。

【hidden oracle の意義】従来の visible oracle 方式ではテストコードが agent から見えるため、harness なしでも oracle から命名規則や response shape を逆算できてしまう。今回は採点ロジックを benchmark runner 側に隠し、agent が参照できるのは prompt・リポジトリ内コード・AGENTS.md・conventions・check script のみとした。これにより harness 本来の効果を純粋に測定できる。

【成功判定条件】pytest 通過だけでなく、(1) agent 正常終了、(2) git diff --check 通過、(3) hidden oracle 通過、(4) wrong-file edits なし、(5) forbidden-file edits なし、の 5 条件をすべて満たす必要がある。

【結果】no-harness: 12 回中 0 成功、wrong-file edits 11 件、timeout 3 件。yes-harness: 12 回中 11 成功、wrong-file edits 0 件、timeout 0 件。

【失敗要因の分析】no-harness の失敗原因は Flask の実装能力不足ではなく、リポジトリ固有の context 不足。endpoint 命名・response shape・supplier map・safety stock ルール・ドキュメント配置場所を agent が推測で補完した結果、誤った場所へのファイル編集が多発した。

【harness の効果メカニズム】yes-harness では AGENTS.md・coding conventions・domain glossary・decision records・check_harness.py・ドキュメント配置ルール・sandbox 再試行防止ルールを整備。モデル自体の能力を上げるのではなく、人間の慣習として暗黙に存在していた情報を agent が読み取れる形式に変換することで、contract discovery・file-boundary discipline・documentation placement が改善された。

【監査エージェント開発への示唆】監査 AI においても、証跡の保存先・命名規則・変更禁止ファイルの境界・検証コマンドといった repo-local convention を AGENTS.md や check script として明示することで、agent の誤動作（意図しないファイル改変、規約違反の成果物生成）を抑制できる可能性がある。本手法は LangGraph ベースのエージェント設計においてもそのまま適用可能。

## アイデア

- visible oracle から hidden oracle へ切り替えることで、harness の純粋な効果（convention 整備の有無）を測定できる点。no-harness 側がテストコードから逆算して不当に高スコアを出す問題を設計で排除している
- 「動くコードを書けるか」ではなく「repo のやり方に従っているか」を成功基準の中心に据えた多条件スコアリング設計。pytest 通過だけでなく wrong-file edits・forbidden-file edits・hidden oracle 通過を全て要求する
- agent が新しいセッションを開始するたびに『今プロジェクトに入ったばかりの人』状態になるという特性に対し、暗黙知を repo 内の明示的 convention に変換することで毎回の口頭説明コストをゼロにする発想

## 前提知識

- **coding agent** → /deep_6122 Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）
- **AGENTS.md** → /deep_8 LLMに「マジカルバナナ」式連想想起を実装したら会話が変わった
- **hidden oracle** (TODO: 読むべき)
- **file-boundary violation** (TODO: 読むべき)
- **benchmark runner** (TODO: 読むべき)

## 関連記事

- /deep_7927 harness-starter-kitは魔法ではない — エラーを早く表に出すためのフレームワーク
- /deep_7339 Claude Code 最大の要望 AGENTS.md 対応——5,200超のreactionsの痛みと今すぐできる回避策
- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_1794 長期埋め込み（LTE）によるバランスの取れたパーソナライゼーション

## 原文リンク

[harness-starter-kit は hidden-oracle A/B テストで成功した：repo convention が coding agent の精度を 0/12 から 11/12 に改善](https://zenn.dev/yuuaan/articles/55501dd45e2522)
