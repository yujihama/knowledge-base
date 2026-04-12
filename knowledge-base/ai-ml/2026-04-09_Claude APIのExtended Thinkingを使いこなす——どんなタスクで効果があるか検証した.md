---
title: "Claude APIのExtended Thinkingを使いこなす——どんなタスクで効果があるか検証した"
url: "https://zenn.dev/ai_eris_log/articles/claude-extended-thinking-20260407"
date: 2026-04-09
tags: [Claude API, Extended Thinking, budget_tokens, claude-sonnet-4-6, LLM推論, コスト最適化, 思考プロセス可視化]
category: "ai-ml"
memo: "[Zenn LLM] Claude APIのExtended Thinkingを使いこなす——どんなタスクで効果があるか検証した"
related: [407, 1641, 972, 248, 609]
processed_at: "2026-04-09T21:39:25.430009"
---

## 要約

Claude APIのExtended Thinking（拡張思考）機能を4種類のタスクで実験的に比較検証した記事。Extended Thinkingは`thinking`パラメータで`budget_tokens`を設定することで有効化され、モデルが回答前に内部思考プロセスを展開する。`max_tokens`は`budget_tokens`より大きくする必要がある。

検証したタスクは①数学の証明問題、②複数制約つきスケジューリング最適化、③200行Pythonコードのバグ修正、④単純なQ&Aの4種類。通常モード（thinking=disabled）とbudget_tokens=8000のExtended Thinkingを比較した。

結果として、単純な数学証明や知識Q&Aでは品質差がなく、コスト（7.5倍）に見合わなかった。一方、5人のメンバーへのスプリントタスク割り当てのような多変数・多制約最適化では、通常モードが制約を見落とした箇所をExtended Thinkingが制約を列挙しながら矛盾を潰す思考プロセスを経ることで制約違反をほぼゼロにした。200行コードのバグ修正では、修正の副作用を事前チェックする思考が有効に働いた。

budget_tokensのタスク別目安として、simple_qa=不要、math_proof=2000、code_review=5000、complex_planning=10000、multi_constraint_opt=16000を導出。コスト面ではSonnet 4.6での実験で通常比4〜8倍（単純Q&A¥0.02→¥0.15、複雑最適化¥0.12→¥0.62）になるが、やり直しが減るためトータルコストが下がるケースもある。

思考ブロック（block.type=="thinking"）の内容が読めるため、「なぜその結論に至ったか」の追跡が可能で、監査・説明責任が求められる用途で有用な特性を持つ。向いているタスクは複数制約の同時充足、副作用考慮が必要なコード変更、論理的矛盾の発見、依存関係のある多ステップ計画立案。向いていないタスクは知識Q&A、翻訳、定型コード生成、リアルタイム処理。

## アイデア

- 思考ブロック（block.type=="thinking"）が外部から読めることで、モデルの判断根拠を追跡・監査できる——LLM-as-judgeや監査エージェントのデバッグに応用可能
- budget_tokensをタスク複雑度に応じて動的に切り替えるルーティング戦略（BUDGET_MAPパターン）は、LLMオーケストレーション層での最適化パターンとして汎用的に活用できる
- 多制約最適化で通常モードが制約を見落とす一方Extended Thinkingが見落とさなかった事実は、制約充足率を定量評価指標として使えることを示唆する
## 関連記事

- /deep_407 API vs ローカルLLM、感覚で選ぶのをやめるための判断フレームワーク
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_972 論文「Learning to Reason with LLMs」を実運用視点で解説：企業導入で注意すべき5つのリスク
- /deep_248 研究ブレークスルーと実世界応用の「マジックサイクル」加速：Google Research最新成果
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話

## 原文リンク

[Claude APIのExtended Thinkingを使いこなす——どんなタスクで効果があるか検証した](https://zenn.dev/ai_eris_log/articles/claude-extended-thinking-20260407)
