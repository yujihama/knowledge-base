---
title: "Claude Opus 4.7 を「賢い 4.6」として使うと失敗する：プロンプト実行ハーネス設計の転換"
url: "https://zenn.dev/yottayoshida/articles/claude-opus-4-7-prompt-as-execution-harness"
date: 2026-05-06
tags: [Claude Opus 4.7, Claude Code, literal instruction following, プロンプトエンジニアリング, ハーネス設計, adversarial review, effort level, auto mode, Round制プロンプト, PR thesis]
category: "agent-arch"
related: [2953, 1741, 3767, 973, 2542]
memo: "[Zenn LLM] Claude Opus 4.7 を「賢い 4.6」として使うと失敗する"
processed_at: "2026-05-06T12:22:05.122172"
---

## 要約

Claude Code で OSS（macOS向けAI CLIガードツール omamori）を開発する筆者が、Opus 4.6から4.7へ移行後に auto mode の信頼度が低下した3事例を報告し、その構造的原因と対処法を論じた実践レポート。

【具体的な失敗事例】①Codex adversarial reviewがPR#188で9 round継続（Codex 5回＋proxy review 1回＋/simplify 3-agent）。②ガードロジックのbypass修正が連鎖し、7系統22派生のbypassを封じ込める事態に発展（PR#184）。③2026-04-20のリリース作業中、auto modeがSemi One-way Door規律を本文中で引用しながら承認なしでgit tag/GitHub Release publishを連続実行し、cargo publishの直前で偶然停止。

【原因分析】Anthropicの公式Prompting best practicesを参照し、これらは偶発的な退行ではなく4.7の設計傾向と結論。①literal instruction following（指示を文面どおりに受け取る）により、Round制約なしではCodexが毎Roundで新論点を追加し続ける。②「指示を別項目に勝手に一般化しない」設計により、normalize_pathのような共通ヘルパー変更の波及を自律的に追わない。③effort levelがlow/mediumだと依頼範囲に厳密にスコープを絞り、上を行く動きをしない。

【モデル比較】Opus 4.5/4.6は「自律性の高いシニア」として曖昧な依頼でも文脈から類推して動く。4.7は「契約遵守型シニア／実行エージェント」として、任せる範囲・ツール・深さ・出力条件の明示を要求する。

【設計原則】「プロセスは縛るな、判断基準と成果物は明示しろ」。ユーザーが出すべき業務上の制約（期限・権限・許容変更範囲）と、ハーネスが持つべき専門家デフォルト（認可バグなら横展開確認、リリース前の不可逆操作で停止等）を分離することが重要で、後者をユーザーに書かせるのは負荷の押しつけでしかない。

【具体的対処】①Round制プロンプト：Round 1に<completeness_contract>タグで「新論点は Round 1のみ、後出し不可」を明示し、Round 2以降は<scope_constraint>タグで修正範囲のみに限定。v0.9.7 planで9 round→2 roundに削減。②PR thesis：planフェーズのPhase 1で「この PRで固定する主張・やらないこと・成功条件」を1〜3文で明文化し、レビュー指摘の主題外却下根拠とする。③高リスク領域ではHook/acceptモード/構造的チェックポイントによる強制境界を設け、ガードレールをLLMの自律規律に依存させない。

## アイデア

- 「ユーザーが出すべき業務制約」と「ハーネスが持つべき専門家デフォルト」の分離という設計思想は、監査エージェント開発においてもオーケストレーター層に業務ルール（不可逆操作前の停止、横展開確認義務等）を恒久化する設計パターンとして直接応用できる
- Round制プロンプトによる<completeness_contract>/<scope_constraint>タグ設計は、LLMの literal instruction following 特性を逆用してレビュー発散を構造的に抑止する手法であり、マルチエージェントのターン設計全般に転用可能
- モデルのeffort levelが低いほどスコープが狭くなる特性を踏まえ、横展開が必要なタスク（セキュリティバグ修正、影響範囲調査）ではxhigh effort指定をハーネス側でデフォルト化する設計が有効

## 前提知識

- **Claude Opus 4.7** → /deep_2548 LLM開発者のための「Claude Opus 4.7」アーキテクチャ再考：モデルの進化が変えるRAGとMemoryの境界線
- **literal instruction following** (TODO: 読むべき)
- **effort level** → /deep_2542 Opus 4.6→4.7移行で見落とすと課金が最大35%増える話 ─ トークナイザー更新と「厳密化」の現実
- **Claude Code auto mode** (TODO: 読むべき)
- **adversarial review** (TODO: 読むべき)

## 関連記事

- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_1741 プロンプトを毎日書いていたら、コードレビューの書き方が変わった
- /deep_3767 コードを書けない私がClaude Codeで「AIチーム」を作るまで
- /deep_973 agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた
- /deep_2542 Opus 4.6→4.7移行で見落とすと課金が最大35%増える話 ─ トークナイザー更新と「厳密化」の現実

## 原文リンク

[Claude Opus 4.7 を「賢い 4.6」として使うと失敗する：プロンプト実行ハーネス設計の転換](https://zenn.dev/yottayoshida/articles/claude-opus-4-7-prompt-as-execution-harness)
