---
title: "Claude Max 5xは本当に元が取れているのか？ jsonl実測データで検証する"
url: "https://zenn.dev/tottoko_hamu/articles/2026-05-22-000000"
date: 2026-05-29
tags: [Claude Code, Claude Max, トークンコスト, jsonl, API換算, claude-opus-4-7, claude-sonnet-4-6, prompt cache, コスト分析]
category: "other"
related: [5804, 89, 4030, 1429, 4753]
memo: "[Zenn LLM] Claude Max 5x は本当に元が取れているのか？ jsonl 実測データで検証する"
processed_at: "2026-05-29T09:04:53.804497"
---

## 要約

Claude Code が ~/.claude/projects/ 配下に保存する jsonl セッションファイルを解析し、Claude Max 5x（月額$100）の API 換算コストを定量評価した実測レポート。139個のセッションファイル（2026年5月7日〜22日の16日間）を対象に、input_tokens・cache_creation_input_tokens・cache_read_input_tokens・output_tokens の4種類のトークンを集計し、モデル別公式単価を乗じて API 換算コストを算出した。結果は16日間で$2,894（月換算$5,425）、Max月額$100の約55倍に相当する。なお当初は Opus 4.7 の単価を旧 Opus 4 の価格（input $15/MTok, output $75/MTok）で誤計算し$7,159という誤値を出したが、実際の単価（input $5/MTok, output $25/MTok）で修正した。コスト内訳ではOpus 4.7が全体の74%を占め、その理由は1回あたりの平均出力トークン数がSonnetの349tokに対しOpusは978tokと2.4倍多いことにある。さらにOpusコストの52%がcache_read_input_tokensによるもので、長セッションではコンテキストの繰り返し参照によりキャッシュ読み込みが急増する。高コストセッション上位はZenn Book構成見直し（$252）・引き継ぎ作業継続（$127）など長時間の執筆・設計タスクが占めた。用途別試算では、Sonnet中心・短セッションの場合でも API 換算$500〜$1,000/月相当でMax$100の5〜10倍の価値になると推定される。運用指針として、コスト節約ではなくレート制限マネジメントを意識し、Opusを複雑な設計・レビューに集中させる、cache_readを積極活用する、不要なセッション分割を避けて cache_creation コストを抑えるという3点を提示。監査エージェント開発への示唆として、Claude Codeを用いた長期セッションでLangGraphやPydanticを使った複雑な設計タスクを処理する場合、Opusのcache_readコストが支配的になるため、タスクの複雑度に応じたモデル選択とセッション設計が実用上のスループット最大化に直結する。

## アイデア

- jsonlのusageフィールドを集計するだけで、サブスクリプション vs API の実コスト比較が自前で定量化できる点。感覚的な「元が取れている」を数値化する方法論として再現性が高い
- Opusコストの52%がcache_read由来という事実。長セッションでは入力トークン単価の1/10で済むcache_readが大量発生するため、コンテキストを継続させる設計がコスト効率を左右する
- LLMが自身の知識カットオフ後にリリースされたモデルの単価を誤推定した事例。計算ツールとして使う際は単価などの前提データを人間が検証する必要があることを実例で示している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **prompt caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- **トークン課金モデル** (TODO: 読むべき)
- **jsonl** → /deep_89 Claude CodeとCodexのPlan Modeはどこに何を保存しているのか
- **Claude Opus/Sonnet** (TODO: 読むべき)

## 関連記事

- /deep_5804 Claude Codeを「観測」で育てる：操作の癖を自動学習するInstinct機能の作り方
- /deep_89 Claude CodeとCodexのPlan Modeはどこに何を保存しているのか
- /deep_4030 1日4000万トークン無料!? AIエージェントの「トークン破産」を防ぐ最強LLMプロバイダー比較
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[Claude Max 5xは本当に元が取れているのか？ jsonl実測データで検証する](https://zenn.dev/tottoko_hamu/articles/2026-05-22-000000)
