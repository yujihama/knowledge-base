---
title: "Claude Opus 4.7 徹底レビュー ── xhigh・/ultrareview・タスク予算で何が変わったか"
url: "https://zenn.dev/soushu/articles/2026-04-17-claude-opus-4-7"
date: 2026-04-22
tags: [Claude Opus 4.7, Anthropic, Claude Code, タスク予算, xhigh, SWE-bench, エージェント制御, トークナイザー, ビジョンモデル]
category: "ai-ml"
related: [2542, 1788, 94, 2541, 2205]
memo: "[Zenn LLM] Claude Opus 4.7 徹底レビュー ── xhigh・/ultrareview・タスク予算で何が変わったか"
processed_at: "2026-04-22T12:10:39.330016"
---

## 要約

2026年4月16日、AnthropicはClaude Opus 4.7をリリースした。料金は据え置き（Input $5 / Output $25 per 1Mトークン）のままSWE-bench Verifiedが80.8%→87.6%、SWE-bench Proが53.4%→64.3%（GPT-5.4比+6.6pt、Gemini 3.1 Pro比+10.1pt）と大幅向上した。OSWorldで+5.1pt、Finance Agentで+4.3ptとエージェント用途全般が底上げされている。なお、SWE-bench Verified 93.9%を記録した実験モデル「Claude Mythos Preview」はサイバーセキュリティ能力が高すぎるとして非公開となっており、Opus 4.7はその商用抑制版と位置づけられる。

主な新機能は3つ。①xhighエフォートレベル：従来のhigh/maxの間に挿入された新推論レベルで、Claude Codeのデフォルトが全プラン共通でxhighに変更された。ユーザーは設定変更なしで推論品質の向上を享受できる。②/ultrareviewコマンド：変更差分を読み込み独立したレビューセッションを開くスラッシュコマンド。セキュリティ・パフォーマンス・設計・テスト容易性など網羅的な観点で指摘を行い、エッジケースやヌル安全性への言及が増える。Pro・Maxプランでは月3回まで無料。③タスク予算（Task Budgets）：エージェントループ全体（思考・ツール呼び出し・ツール結果・最終出力）に対してトークン上限を事前指定するパラメータ（`--task-budget 50000`）。従来のmax_tokensと異なり、モデル自身が残予算をカウントダウンしながら作業優先度を調整し、予算内でタスクを完結させようと振る舞う。CI組込みや本番エージェント運用でのコスト制御に直結する。

ビジョン性能も大幅改善し、画像入力上限がOpus 4.6の約1.15メガピクセルから3.75メガピクセル（長辺2,576px）に拡大。ビジョン系ベンチマークで54.5%→98.5%の改善が報告されている。注意点として、新トークナイザー採用により同一入力でもトークン数が1.0〜1.35倍に増加するため、実質コストが1〜3割増になるケースがある。APIパラメータはモデルID `claude-opus-4-7`、新パラメータ `task_budget`、新エフォート `effort: "xhigh"`（min/high/xhigh/maxの4段階）。Amazon Bedrockでも既にGA済み。監査エージェント開発においては、タスク予算によるコスト上限設定と/ultrareviewによる差分レビューの組み合わせが、品質担保とコスト管理の両面で即時活用可能な機能として注目される。

## アイデア

- タスク予算はmax_tokensによる強制打ち切りではなく『モデル自身が残予算を認識して作業優先度を動的に調整する』設計であり、エージェントの自律的なリソース管理という新しいパラダイムを示している
- /ultrareviewが『コードを書く文脈』と切り離されたサブセッションとして動作する点は、LLMの文脈依存バイアスをアーキテクチャレベルで回避しようとするアプローチとして興味深い
- Claude Mythos Preview（SWE-bench 93.9%）を公開せず商用抑制版のOpus 4.7を提供するという判断は、能力と安全性のトレードオフをAnthropicが製品戦略に明示的に組み込んでいることを示す事例

## 前提知識

- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **推論エフォートレベル** (TODO: 読むべき)
- **エージェントループ** → /deep_64 Open Responses: オープンな推論APIスタンダードの概要
- **トークナイザー** → /deep_158 翻訳か暗唱か？極低リソース言語の機械翻訳評価スコアの較正
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_2542 Opus 4.6→4.7移行で見落とすと課金が最大35%増える話 ─ トークナイザー更新と「厳密化」の現実
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？
- /deep_2205 なぜAnthropicは軍と戦う？1億ドルPartner NetworkとAI研究所の全貌

## 原文リンク

[Claude Opus 4.7 徹底レビュー ── xhigh・/ultrareview・タスク予算で何が変わったか](https://zenn.dev/soushu/articles/2026-04-17-claude-opus-4-7)
