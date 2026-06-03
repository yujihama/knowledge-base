---
title: "【実録】同じ指示を2回出した日、AIがGCPを7万円分焼き尽くした話（OpenClaw転換劇 Vol.2）"
url: "https://zenn.dev/i_ichi/articles/openclaw-agent-vol2"
date: 2026-06-03
tags: [Retry Storm, Silent Fallback, Context Collapse, Memory Persistence, Circuit Breaker, GCP, OpenRouter, 自律AIエージェント, コスト管理, OpenClaw]
category: "agent-arch"
related: [1641, 5160, 2203, 5807, 2978]
memo: "[Zenn LLM] 【実録】同じ指示を2回出した日、AIがGCPを7万円分焼き尽くした話（OpenClaw転換劇 Vol.2）"
processed_at: "2026-06-03T21:01:16.042470"
---

## 要約

個人運用の自律AIエージェント環境「OpenClaw」で発生した実際のコスト爆発事故の詳細報告。2026年3月20日、メインエージェントへの重複指示と音声エージェントの並列最適化実験が同時に崩壊し、一晩でGCP費用7万円（無料枠5万円蒸発＋超過2万円）が発生した。

根本原因は4つの障害パターンの連鎖。①Memory Persistence Failure（記憶永続化の失敗）：エージェントが「書いた」と報告してもファイル書き込み前にセッションが切断されるNon-commit Executionと、書き込み検証ループの欠如。②Silent Fallback：OpenRouter経由でgoogle-vertex/gemini-3.1-pro-previewがレートリミットに達した際、エラーを出さずにgemini-2.5-pro→gemini-2.5-flash-liteへ自動縮退。ログ上は正常動作に見える。③Context Collapse：軽量モデルが複雑な実装コンテキストを維持できずハルシネーションを連発。④Retry Storm：異常状態が保存されないまま（non-commit）高頻度で再試行が繰り返され、GCP側から「不正リトライ過多」と判定されAPIプロジェクトが凍結。さらに別プロジェクトへ自動切替が走り被害が拡大した。

GCP Budget Alertsは設定済みだったが、課金データ反映の数時間タイムラグをRetry Stormの速度が上回ったため機能しなかった。気づきが1日遅れていれば月額150万円規模になっていた計算。

同様の事故は2026年の業界で頻発しており、データ拡充エージェントが週末で230万コール/$47Kを消費した事例、429エラーがretry loopを引き起こし80時間で$3,847消費した事例、autonomous refactoringに$4,200が消えた事例が報告されている。「Retry Storm」「Silent Fallback」「Context Collapse」は産業標準の障害パターン名として定着している。

設計上の対策として4つの防壁を提示：①Commit Verification（ファイル書き込み後に決定論的コードで内容を正規表現アサート）、②Fallback Detection（下位モデルへの縮退を検知したら即Abort）、③Retry Circuit Breaker（秒間APIリクエスト数に物理閾値を設け超過時に回線遮断）、④Human Approval Gate（課金発生する方針転換や並列処理起動に人間の明示的承認を必須化）。この事故を機にOpenClawは「完全自律AI」から人間がハーネスとなる「半自律構造」へ転換した。監査エージェント開発においても、エージェントが自律的にAPI呼び出しを繰り返す構造を設計する場合、同様のCircuit BreakerとHuman Approval Gateが必須となる。

## アイデア

- Silent Fallbackが最も危険な障害モードである点：モデル縮退がログ上でエラーとして現れないため、軽量モデルがハルシネーションを連発しながらシステムが「正常動作中」と見える状態が最も検知困難
- Non-commit ExecutionとRetry Stormの相乗効果：書き込みが永続化されないため毎回初期状態から壊れた処理を再生産し、これがリトライの無限ループを駆動するという構造的な脆弱性
- 「AIを賢くする」のではなく「壊れた時に物理的に止める仕組み」が本質：Commit Verification・Fallback Detection・Circuit Breaker・Human Approval Gateという4つの決定論的防壁の設計思想が、監査エージェントのような高信頼性が求められるシステムに直接応用可能

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **Rate Limiting** (TODO: 読むべき)
- **Circuit Breaker** → /deep_5030 AIエージェントのツール設計を本番品質に高める：スキーマ進化・障害モード・契約テストの実装戦略
- **OpenRouter** → /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- **GCP Billing** (TODO: 読むべき)

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_5160 通勤中に育てたAIが、放置していたアイデアを勝手に形にした【OpenClawエージェント4体を止めるまで①】
- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- /deep_5807 全くの素人がOpenClawにハマって85日目にやめた話
- /deep_2978 中国のテック労働者がAIドッペルゲンガー訓練を迫られ反発——「同僚スキル」と「反蒸留」ツールの攻防

## 原文リンク

[【実録】同じ指示を2回出した日、AIがGCPを7万円分焼き尽くした話（OpenClaw転換劇 Vol.2）](https://zenn.dev/i_ichi/articles/openclaw-agent-vol2)
