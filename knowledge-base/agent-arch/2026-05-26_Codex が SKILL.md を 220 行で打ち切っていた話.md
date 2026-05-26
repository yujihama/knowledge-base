---
title: "Codex が SKILL.md を 220 行で打ち切っていた話"
url: "https://zenn.dev/haru0416/articles/codex-skill-md-220-lines"
date: 2026-05-26
tags: [Codex CLI, SKILL.md, Agent Skills, progressive disclosure, Claude Code, sed, tool_call, Quaere, Terminal-Bench, harness]
category: "agent-arch"
related: [2550, 4661, 4520, 4242, 1045]
memo: "[Zenn LLM] Codex が SKILL.md を 220 行で打ち切っていた話"
processed_at: "2026-05-26T21:01:47.338809"
---

## 要約

Quaere というコーディングエージェント向けスキル集を開発中に、Codex CLI がSKILL.mdファイルを220行で打ち切るという挙動が発見された。441行あるquaere-evidenceスキルに対し、41タスク中39タスクで読み取りの最深行がきっかり220行に揃い、221行目以降は一度も読まれていなかった。

Codex CLIにはファイル読み取り専用ツールが存在せず、ファイル読み取りはモデルがshellコマンドを自分で生成して実行する。そのため `sed -n '1,220p' SKILL.md` というコマンドはCodex CLI側が固定で出しているのではなく、GPTモデルがtool_callのargumentsとして組み立てたものだ。Claude CodeやOpenCodeのようにハーネス側がスキル本文を丸ごとモデルに渡す経路では220問題は発生しない。

220という数字は「モデルが想定するSKILL.mdの長さ」に由来する。Agent Skillsの公式設計思想は本文を短く保つprogressive disclosureであり、仕様通りに書かれたSKILL.mdはだいたい200行に収まる。220はその「標準的な長さ＋少しの余白」に相当し、モデルにとってはこのコマンドで「スキルを丸ごと読んだ」つもりになっている。

この打ち切りにより、Quaereの各スキルで読まれない割合は14〜50%に達し、特に220行以降に配置されていたanti-patterns・stop condition・スキル連携手順といった「止まれ」を書いた重要部分が構造的に読まれていなかった。スキルチェーン（quaere-audit→evidence-gated-review→external-grounding等）においても全hopが220行上限で揃い、handoff記述が221行以降にあるとチェーンが起きない。

claudexを使ってハーネスをClaude Code側に差し替えてgpt-5.5を動かした3セッションでは、全件でSkillツール呼び出しが先行しsedは0件だった。これはハーネスのアーキテクチャが挙動を規定していることを示す。

結論として、220行打ち切りはバグではなく、モデルがAgent Skillsの仕様通りの前提を持った結果。対処法はCodexを変えることではなく、SKILL.md本体を200行以内に収め、長い例・anti-patterns・参照ドキュメントはreferences/に逃がすこと。これは公式ドキュメントにも記載されている指針だが、「行儀のいい書き方」ではなく「守らないと後半が物理的に読まれない制約」だと実測で裏付けられた点が本記事の核心的貢献である。

## アイデア

- モデルが学習データから獲得した「スキルファイルの典型的な長さ」がsedのパラメータとして具現化するという、訓練分布がツール使用挙動に直接影響する現象
- ハーネスのアーキテクチャ（ファイルを自前で注入するか、モデルにshellを書かせるか）が同一モデルの挙動を根本的に変えるという、インフラ設計の重要性
- スキルのanti-patternsやstop conditionといった「止める指示」が、ファイルの後半に置かれやすい構造的傾向と、モデルの読み取り上限の組み合わせにより、最も重要な部分が最も読まれないという逆説

## 前提知識

- **Codex CLI** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する
- **Agent Skills / SKILL.md** (TODO: 読むべき)
- **tool_call** (TODO: 読むべき)
- **progressive disclosure** → /deep_2249 Claude Codeの設定はどこに書くべきか ― プロンプト・RULES・スキル・エージェントの使い分け
- **sed コマンド** (TODO: 読むべき)

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_4661 Codex CLIを使った議事録→日報・週報・管理資料の自動生成アーキテクチャ
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_4242 信頼されていないエージェントスキルに対する構造化セキュリティ監査とロバスト性強化
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話

## 原文リンク

[Codex が SKILL.md を 220 行で打ち切っていた話](https://zenn.dev/haru0416/articles/codex-skill-md-220-lines)
