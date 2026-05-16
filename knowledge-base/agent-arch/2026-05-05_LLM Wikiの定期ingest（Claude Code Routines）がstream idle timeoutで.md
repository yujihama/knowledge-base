---
title: "LLM Wikiの定期ingest（Claude Code Routines）がstream idle timeoutで落ちたので対策した話"
url: "https://zenn.dev/biscuit/articles/claude-routines-ingest-timeout"
date: 2026-05-05
tags: [Claude Code Routines, stream idle timeout, サブエージェント, SKILL.md, バッチ処理, 中間commit, LLM Wiki, 自動化]
category: "agent-arch"
related: [2821, 3089, 3239, 1641, 1965]
memo: "[Zenn LLM] LLM Wikiの定期ingest（Claude Code Routines）がstream idle timeoutで落ちたので対策した話"
processed_at: "2026-05-05T12:07:21.825658"
---

## 要約

個人の知識管理システム「LLM Wiki」において、Claude Code Routinesによる定期ingest処理が「API Error: Stream idle timeout - partial response received」で失敗する問題が発生した。原因調査と対策の記録。

【システム構成】raw/ディレクトリ内のクリッピングファイル（ingested: false）を検出し、URLフェッチ・wikiページ生成・biasチェック・index/log更新を経て ingested: true にマーク、ブランチ作成→commit→PR→squash mergeまでを自動実行するRoutine。

【問題の二重構造】ログ解析で判明した原因は2つ。(1) Claudeが「効率化のため」として自主的にAgentツール（Taskツール）でサブエージェントを起動し、28件中14件をまとめて処理させた結果、長時間実行でメインセッションのストリームがアイドル化しタイムアウト。(2) サブエージェントの処理完了前に全28ファイルへ ingested: true を先行書き込み。タイムアウト後「処理済みフラグのみ存在してwikiページが未生成」のファイルが大量発生した。

【対策1: バッチ上限・処理順・中間commitの整備】`grep -rl 'ingested: false' raw/` の結果を `xargs -0 ls -tr` でmtime昇順ソートし `head -8` で上限8件に制限。古いファイルから順に処理され、処理されないまま放置されるファイルを排除。1ファイルの全工程（URL取得〜index/log更新）完了後に `git commit -m 'auto-ingest: <タイトル略称>'` を打つファイル単位の中間commitを追加。タイムアウト時でもcommit済み進捗が保持される。

【対策2: SKILL.mdでの明示的制約】「Agentツール（Taskツール）使用禁止。Read・Write・Edit・WebFetchを直列実行すること」「ingested: trueのマークはStep 8（各ファイル処理完了直後）のみ」をSKILL.mdに直接記述。曖昧な表現ではなく「禁止」と明示することでClaudeの挙動を制御できた。

【対策3: モデル変更の検討】現行はclaude-opus-4-6で運用。処理件数増加時はclaude-sonnet-4-6への切り替えも選択肢（/schedule updateで変更可）。ingestのような定型処理であればSonnetでも品質上実用十分とする判断。

【教訓】タイムアウトの主因はバッチ上限を明示しなかった設計側の問題。Routinesのような非監視自動化では「やっていいこと」より「やってはいけないこと」をSKILL.mdに書くほうが有効。処理量と権限の境界を明示的に切る設計がエージェント自動化の核心。

## アイデア

- メインセッションがサブエージェントへ委任中にアイドル化する構造的タイムアウト問題：エージェントの並列化・委任とストリームキープアライブの相性の悪さは、長時間自動化処理全般に潜む設計上の落とし穴
- SKILL.mdへの明示的禁止記述によるLLM挙動制御：「なんとなく禁止っぽい」記述では効かず、直接的表現が必要という知見は、監査エージェントのガードレール設計（過剰権限行使の抑制）にそのまま応用できる
- ファイル単位の中間commitによる冪等性確保：タイムアウト耐性のある進捗保持設計で、障害発生時に再実行可能なチェックポイント機構を構成する。長時間処理を要する監査エージェントのタスク分割設計の参考になる

## 前提知識

- **Claude Code Routines** → /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- **stream idle timeout** (TODO: 読むべき)
- **Agentツール / Taskツール** (TODO: 読むべき)
- **SKILL.md** → /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- **git commit（中間コミット）** (TODO: 読むべき)

## 関連記事

- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_3089 LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った
- /deep_3239 Claude Code で LLM Wiki を育てる——第二の脳の作り方
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点

## 原文リンク

[LLM Wikiの定期ingest（Claude Code Routines）がstream idle timeoutで落ちたので対策した話](https://zenn.dev/biscuit/articles/claude-routines-ingest-timeout)
