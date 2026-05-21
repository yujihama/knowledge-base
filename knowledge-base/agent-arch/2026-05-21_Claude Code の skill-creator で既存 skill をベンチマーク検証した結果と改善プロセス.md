---
title: "Claude Code の skill-creator で既存 skill をベンチマーク検証した結果と改善プロセス"
url: "https://zenn.dev/redamoon/articles/article45-claude-code-skill-creator-benchmark"
date: 2026-05-21
tags: [Claude Code, skill-creator, benchmark, eval, SKILL.md, Zenn, LLM評価]
category: "agent-arch"
related: [1045, 5907, 4228, 769, 2250]
memo: "[Zenn LLM] Claude Code の skill-creator で既存 skill を検証してみた"
processed_at: "2026-05-21T12:00:44.722769"
---

## 要約

Claude Code には `.claude/skills/` 配下の SKILL.md を作成・改善・評価する skill-creator という機能が用意されている。本記事では、著者が自作した Zenn 技術記事執筆ガイドライン集「zenn-blog-writing」skill を対象に、skill-creator の benchmark モードで2イテレーションの定量評価を実施した結果をまとめている。

benchmark は「タスク定義」「期待する出力条件」「採点ロジック（rubric）」をセットで管理し、skill あり・なしの2条件で複数の eval を実行してスコアを比較する仕組みである。

iteration-1では3つの eval を実施。eval-1（AI表現レビュー）は skill あり 5/5 対 skill なし 4/5、eval-2（新規記事作成）は両者 5/6 の同スコアながら FAIL の性質が異なり、eval-3（frontmatter修正）は skill あり 7/7 対 skill なし 5/7 という結果となった。総合通過率は skill あり 94.4%、skill なし 77.8% で 16.7% の差が生じた。

コスト面では skill あり条件が約 3300 tokens 多く消費し、処理時間は約 4 秒増加した。

iteration-1 の分析からスコア同率でも FAIL の原因が本質的に異なることが判明した。skill ありの FAIL はターミナル出力コードブロックへの言語指定（text/console）が skill 未定義であったためのルール漏れであり、skill なしの FAIL は「Node.js」「GitHub Actions」のように Zenn がエラーとする記号・スペース含む topics 表記を使用したという仕様理解不足に起因する。

この分析をもとに3点の改善を実施した。①frontmatter テンプレート（title・emoji・type のダブルクォート必須）を skill 冒頭に集約、②「GitHub Actions → githubactions」「CI/CD → cicd」等 topics 変換パターン表の拡充、③ターミナル出力への text/console 言語指定の明記。

iteration-2 では skill あり が全 18 アサーションで 100% 満点を達成。skill なしも 77.8% → 83.3% に微増したが、2イテレーション連続で同一アサーション（topics大文字、クォートスタイル）が FAIL しており確率的ばらつきと判断している。

記事の結論として、skill の価値は「モデルが知らないことを教える」より「Zenn 固有の慣習を毎回確実に適用させる」点にあると整理された。topics の小文字規則や frontmatter のクォートスタイルは一般的な Markdown 知識からは導出できないプラットフォーム固有ルールであり、モデルが自発的に守ることは稀である。benchmark はスコアの数値化だけでなく「FAIL の性質を区別する」ために活用すべきものとまとめられている。監査エージェント開発への示唆として、ドメイン固有ルール（内部統制基準、監査手続きの書式等）を skill として明文化し定期的に benchmark で検証する運用は、エージェントの出力品質の維持・可視化に直接応用できる。

## アイデア

- skill の有無でスコアが同率でも FAIL の性質（ルール漏れ vs 仕様知識不足）が本質的に異なるという観点は、エージェント評価設計全般に応用できる重要な視点
- benchmark を「スコアを出す」目的ではなく「FAIL の原因を分類・可視化する」ツールとして位置づける考え方は、コードのテストにおけるデバッグ哲学に対応している
- プラットフォーム固有の慣習（Zenn の topics 小文字規則等）はモデルが自発的に学習しないため skill への明文化が唯一の信頼できる対処手段という知見は、ドメイン特化エージェント設計の原則として整理できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **SKILL.md** → /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- **LLM評価・eval** (TODO: 読むべき)
- **prompt engineering** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **rubric採点** (TODO: 読むべき)

## 関連記事

- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_5907 ひと月でADRを40本近く書いたら何が変わったか — Claude Code規範運用1ヶ月の失敗録
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計
- /deep_769 Math-VerifyによるOpen LLMリーダーボードの数学評価修正
- /deep_2250 Karpathyが指摘したLLMコーディングの失敗パターンと、コミュニティが作ったCLAUDE.mdの全貌

## 原文リンク

[Claude Code の skill-creator で既存 skill をベンチマーク検証した結果と改善プロセス](https://zenn.dev/redamoon/articles/article45-claude-code-skill-creator-benchmark)
