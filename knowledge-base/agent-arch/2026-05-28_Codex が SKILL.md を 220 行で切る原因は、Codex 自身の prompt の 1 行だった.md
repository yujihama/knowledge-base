---
title: "Codex が SKILL.md を 220 行で切る原因は、Codex 自身の prompt の 1 行だった"
url: "https://zenn.dev/haru0416/articles/codex-skill-md-220-root-cause"
date: 2026-05-28
tags: [Codex CLI, SKILL.md, prompt engineering, agent harness, OpenAI, Claude Code, gpt-5.5, render.rs]
category: "agent-arch"
related: [6601, 6679, 1045, 5907, 4228]
memo: "[Zenn LLM] Codex が SKILL.md を 220 行で切る原因は、Codex 自身の prompt の 1 行だった"
processed_at: "2026-05-28T21:04:12.803427"
---

## 要約

Codex CLI が SKILL.md を 220 行前後で打ち切る現象の根本原因を特定した技術調査記事。原因は codex-rs/core-skills/src/render.rs 内の定数 SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS に含まれる「Read only enough to follow the workflow」という 1 文。この指示が skill 起動時に model へ渡る prompt に含まれており、model は「enough」をそれぞれの prior で解釈する結果、gpt-5.5 では cap=220（76%）、gpt-5.4 では cap=260（71%）という model 依存の打ち切りが発生する。

著者は ~/.codex/sessions/ の全 209 セッションを解析し、71 セッションで SKILL.md への sed 読み込みが合計 143 回発生したことを確認。model を変えるだけで cap 分布が逆転することを実測で示した。さらに claudex 経由で Codex CLI の prompt を経由せず gpt-5.5 を動かした 11 セッションでは sed による部分読みが 0/11 だったことから、問題は model ではなく Codex CLI の prompt に起因すると結論付けた。また「cap-test」skill で line 221 以降を明示的に読むよう指示すると gpt-5.5 で 7/7、gpt-5.4 で 4/4 が二手目を実行したことから、model 自体は partial 読みに固執していないことも確認。

Agent Skills 仕様では activation 時に「the entire file」をロードし、推奨上限は 500 行 / 5000 tokens とされており、Codex CLI の prompt 内 wording と正面から矛盾している。openai/codex#16479 として 2026-04-01 に Issue が立ち、proposed patch（「Read only enough」→「read its SKILL.md in full」）と PR まで存在するが、openai/codex は invitation 制で外部 PR を受け付けず、OpenAI チームからの応答ゼロのまま約 2 ヶ月放置されている。v0.134.0 時点でも render.rs の prompt 文字列は 1 文字も変わっておらず、update では解消しない。なお live main には同一 wording が SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS と SKILLS_HOW_TO_USE_WITH_ALIASES の 2 箇所存在し、既存 patch は片方しかカバーしていないため、current main への rebase と両箇所の更新が必要。

## アイデア

- LLM への指示文に「enough（十分）」のような曖昧な副詞が含まれると、model ごとの prior によって解釈が分岐し、同一 harness でも再現性のない動作差が生じる実例
- 同一 model を異なる harness（Codex CLI vs claudex）で動かすだけで挙動が逆転することから、agent の動作バグの切り分けには『model』と『harness の system prompt』を独立変数として制御する実験設計が有効
- OSS プロジェクトで invitation 制 PR ポリシーを採用すると、外部コントリビュータが patch を用意しても merge できず、既知バグが長期放置されるガバナンスリスクがある

## 前提知識

- **Codex CLI** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する
- **SKILL.md / Agent Skills** (TODO: 読むべき)
- **system prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **LLM prior** (TODO: 読むべき)
- **sed 部分読み** (TODO: 読むべき)

## 関連記事

- /deep_6601 Codex が SKILL.md を 220 行で打ち切っていた話
- /deep_6679 ハーネスエンジニアが知っておくべき Claude Code Plugin の落とし穴：環境変数・事前置換・sensitive の tier 別挙動
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_5907 ひと月でADRを40本近く書いたら何が変わったか — Claude Code規範運用1ヶ月の失敗録
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計

## 原文リンク

[Codex が SKILL.md を 220 行で切る原因は、Codex 自身の prompt の 1 行だった](https://zenn.dev/haru0416/articles/codex-skill-md-220-root-cause)
