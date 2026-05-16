---
title: "仕様書自体をバグチェックで育てる: PPPC executor v3.0 → v3.2 の進化ログ"
url: "https://zenn.dev/guardrail/articles/b30e82f631ca17"
date: 2026-05-07
tags: [DSL, プロンプト設計, PPPC, LLM仕様書, バグチェック, 完遂判定, 仕様駆動開発]
category: "agent-arch"
related: [3176, 3095, 1251, 1736, 2999]
memo: "[Zenn LLM] 仕様書自体をバグチェックで育てる: PPPC executor v3.0 → v3.2 の進化ログ"
processed_at: "2026-05-07T09:42:03.921061"
---

## 要約

PPPC（Promise Purpose Process Complete Protocol）は、AI応答の「完遂」を厳密に定義するためのDSLプロトコル。完遂判定には Purpose_Achieved / MustFixLine_Met / User_Ready_Next / Handover_Ready / Critical_Remaining=0 の5条件を全て満たすことを要求し、残課題を Deferred/Blocked/Rejected に分類して次ターンへ引き継ぐ構造をYAMLライクなDSLで記述する。

v3.0からv3.2への4段階の進化で、段階ごとに異なる種類の問題が検出された。v3.0→v3.1（レビュー）では4件のCriticalが発見された。代表例はC1: must_fix_lineがcompletion_gate.checksの判定条件に接続されておらず「宣言と実装の乖離」が生じていた点、C2: PPPC-NODEのlineフィールドが未定義、C3: turn_execution_flowにMust-Fix Line設定ステップが欠落、C4: output_ruleとdefault_response_structureで必須項目が不一致。

v3.1→v3.1.1（バグチェック）では7件のBugが発見され、最も致命的なのがBUG-01。critical_checkの質問が「〜していないか」形式（yes=健全、no=問題あり）であるにも関わらず、decision_ruleが「1つでもyesがあればcomplete=false」となっており論理が反転していた。人間の読み手は脳内補正で通過するが、LLMは文字通り実装するため健全な応答が毎回「未完」判定になる致命的バグ。修正ではanswer_semanticsフィールドを追加してyes/noの意味を明示し、判定ルールをnoベースに反転した。BUG-02〜04は上位定義が下位の変更を追従していない整合性不足、BUG-05〜07は未定義フィールドや暗黙前提の明文化不足。

v3.1.1→v3.2（Update）では11件の改善が適用された。主要変更として、critical_check/completion_gate/strict_judgement/handover_protocol/completion_certificateの各セクションにrole:フィールドを追加し参照関係を自明化。/absolute_rules（絶対ルール集約）、/critical_fix_definition.escalation（criticalが解消できない場合の逃げ道）、/meeting_turn_behavior.completion_mapping（目的不明ターンでの判定読み替え）の3セクションを新設。またenglish_keys（構造コード・機械処理用）とjapanese_keys（ユーザー可読表示用）の命名規則を明文化した。

得られた原則は3つ: ①レビュー（設計視点）とバグチェック（実装視点）は別タスクとして分離する、②LLM実装を前提にすると人間の脳内補正に頼れないため文字通りのロジックで検証する、③role:とnote:は記述コストが低い割に誤用率を大きく下げる保険として積極的に書く。監査エージェント開発においては、判定ロジックの宣言と実装の乖離チェック、yes/no方向の明示的な定義、上位・下位定義の整合性維持プロセスが直接応用可能。

## アイデア

- 「〜していないか」形式の質問とyes=NGの判定ルールの組み合わせは、人間には自然に読めるがLLMに文字通り実装させると論理反転する典型的なバグパターンであり、LLM向けDSL設計の盲点を示す
- レビュー（設計視点）とバグチェック（実装視点）を明示的に別フェーズとして分離することで、それぞれの粒度に最適化した検証ができるという仕様書開発プロセスの知見
- role:とnote:フィールドを各セクションに付与するだけで誤用率が下がる「無料の保険」という概念は、監査エージェントの判定ルール設計でも判定根拠の明示化に直接応用できる

## 前提知識

- **DSL設計** (TODO: 読むべき)
- **LLMプロンプトエンジニアリング** → /deep_1252 DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化
- **YAML** → /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- **判定ロジック** (TODO: 読むべき)
- **エージェント完遂条件** (TODO: 読むべき)

## 関連記事

- /deep_3176 実行可能モデルのレンズを通した人間行動の理解
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_1251 マルチターン医療診断のベンチマーク：保留・誘惑・自己修正（MINT）
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_2999 ハーネスとか無視してAIで普通に開発した話

## 原文リンク

[仕様書自体をバグチェックで育てる: PPPC executor v3.0 → v3.2 の進化ログ](https://zenn.dev/guardrail/articles/b30e82f631ca17)
