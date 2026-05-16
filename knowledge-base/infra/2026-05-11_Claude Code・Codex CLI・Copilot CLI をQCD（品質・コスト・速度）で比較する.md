---
title: "Claude Code・Codex CLI・Copilot CLI をQCD（品質・コスト・速度）で比較する"
url: "https://zenn.dev/nnakapa/articles/lab-16-rpi4-qcd"
date: 2026-05-11
tags: [Claude Code, Codex CLI, GitHub Copilot CLI, QCDベンチマーク, LLMコードレビュー, ISO/IEC 25010, Raspberry Pi, bandit, ruff, ブラインド採点]
category: "infra"
related: [1429, 4753, 2953, 430, 2688]
memo: "[Zenn LLM] Claude Code・Codex CLI・Copilot CLI を QCD で比較する（オトナの自由研究 #16）"
processed_at: "2026-05-11T12:42:01.733622"
---

## 要約

Raspberry Pi 4（4GB, Ubuntu 24.04 arm64）上で Claude Code（Opus 4.7 / effort=xhigh）、Codex CLI（GPT-5.5 / medium）、GitHub Copilot CLI（GPT-5.4 / medium）の3つのAIコーディングCLIに90回（3エージェント×3タスク×10試行）タスクを解かせ、品質（Q）・コスト（C）・速度（D）の3軸で定量比較した実証研究。

品質評価はISO/IEC 25010:2023を参考に5軸（Functional 40%、Reliability 20%、Security 15%、Maintainability 15%、Safety 10%）を設計し、ルールベース採点（bandit/ruff/スコープdiff）とLLM採点（Opus 4.7とGPT-5.5のブラインドブレンド採点）を50:50でミックスした複合スコアQ_effectiveを用いた。動かないコードは0点、致命的失敗は50点上限とするpass_gateを設けることで「動くが危険なコード」の高得点逃げを防止している。

主な結果は以下の通り。品質（Q_eff）は98.9/99.0/99.2と3者が0.3pt差で実質互角。速度はClaude Codeが中央値37秒で他の2者（55〜57秒）より約35%速い。コストはClaude Codeが平均$0.244/タスク、Codex CLIが$0.313（T2の長文tierで7/10試行が272Kトークン超えとなり2x課金が発生）、Copilot CLIがリクエスト単価$0.04で6〜8倍安い。90試行累計コストは$17.92で、実用的な選択指針は「迷ったらClaude Code、コスト優先ならCopilot CLI」。

QCD本筋から派生した最大の発見は、LLMコードレビューにおけるモデル間挙動差。LLM採点で採用したOpus 4.7とGPT-5.5の採点結果を軸単位で集計すると、モデルごとに評価傾向が異なることが判明し、コードレビューをLLMに委ねる場合はCLIツール選択よりもモデル選択が先決という結論に至った。スコアの食い違い（7pt以上）は180件中14件で、技術的に正しい指摘側に寄せた補正が7件行われた。実験設計面では、タスクにSQL LIKE句エスケープ漏れやos.replaceの別FSエラー等の隠しトラップを仕込み、見かけ上のテスト通過だけでは検出できない品質劣化を炙り出す手法が参考になる。

## アイデア

- pass_gate（致命的失敗を50点上限でキャップ）を設けることで、重み付き平均だけでは見逃すSQLインジェクション等の危険なコードが高得点に化けるスコアリング上の抜け穴を塞ぐ設計が監査エージェントの評価設計にそのまま転用できる
- コードレビューをLLMに任せる際、CLIツール選択よりもモデル選択が評価傾向に大きく影響するという発見は、LLM-as-judgeを組み込む監査システムにおいてjudgeモデルを固定せず複数モデルでクロスチェックする必要性を示唆する
- Codex CLI × T2タスクで272Kトークン超えが70%の試行で再現し長文tier（2x課金）が発動したことは、エージェントに機能追加タスクを与える際のコスト分散リスクを示しており、監査エージェントの本番運用でのコスト上限設計に活かせる

## 前提知識

- **ISO/IEC 25010** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **bandit/ruff** (TODO: 読むべき)
- **pass_gate設計** (TODO: 読むべき)
- **APIトークン課金モデル** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」

## 原文リンク

[Claude Code・Codex CLI・Copilot CLI をQCD（品質・コスト・速度）で比較する](https://zenn.dev/nnakapa/articles/lab-16-rpi4-qcd)
