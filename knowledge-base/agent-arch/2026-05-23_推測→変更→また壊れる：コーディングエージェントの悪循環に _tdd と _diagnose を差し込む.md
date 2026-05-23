---
title: "推測→変更→また壊れる：コーディングエージェントの悪循環に /tdd と /diagnose を差し込む"
url: "https://zenn.dev/53able/articles/71c91cb2ba61fd"
date: 2026-05-23
tags: [Claude Code, TDD, エージェントスキル, デバッグ手法, mattpocock/skills, RED/GREEN, 回帰テスト]
category: "agent-arch"
related: [2824, 4228, 26, 1429, 4753]
memo: "[Zenn LLM] 推測→変更→また壊れる：コーディングエージェントの悪循環に /tdd と /diagnose を差し込む"
processed_at: "2026-05-23T09:02:31.223314"
---

## 要約

AIコーディングエージェントにバグ修正を依頼すると「直しました」と返ってくるが実際には直っていない、という悪循環の根本原因は「pass/failの判定基準がない」ことにある。エージェントはコードを読んで推測し変更を加えるが、その変更が正しいかどうかを確認するステップが指示されないと抜けてしまう。この問題を解決するのがmattpocock/skillsが提供する `/tdd` と `/diagnose` の2つのスキルコマンドである。

`/tdd` はTest-Driven Development（テスト駆動開発）のRED/GREEN/REFACTORサイクルをエージェント向けに適用する。まず失敗するテストを1つ書かせ、それが確かに失敗することを確認してから実装に入る。「全テストを先に書いて実装して」と指示すると、エージェントは存在しない関数の仕様を想像してテストを書き、そのテストに合う実装を作るという自己完結した循環に陥る。1つのループに分けることでこれを防ぐ。テスト対象はprivate methodではなくpublic interfaceとし、内部実装を変更してもテストが壊れない設計を維持する。またモックより本物のコードパスを優先し、コンポーネント間の結合部バグを見逃さないようにする。

`/diagnose` は壊れた挙動を追う際にエージェントがすぐ修正に飛びつくのを抑制する手順である。流れは「Signal設定→Reproduce→Minimise→Hypothesize→Instrument→Fix+regression test→Cleanup+Postmortem」。まず「この入力に対してこの出力が出れば正常」というSignal（判定基準）を定義し、次にバグを再現し、再現を最小化してから3〜5個の仮説を並べ、ログやassertによるInstrumentで事実を観測し、確認してから修正する。修正後は回帰テストを残し、デバッグ用のログは片付け、Postmortemで「型で防げたか」「境界でバリデーションできたか」等の設計観点を記録する。

インストールは `npx skills@latest add mattpocock/skills` で行い、`/setup-matt-pocock-skills` でissue tracker・triage labels・CONTEXT.md・ADRの配置を記録すると他スキルとの共通語彙として活用できる。監査エージェント開発への示唆としては、エージェントに「考えて直して」と渡すのではなく「この判定基準を満たすように進めて」という構造化された指示を渡すパターンが、LangGraphベースの複雑なエージェントパイプラインのデバッグにも直接応用できる。

## アイデア

- エージェントへの指示を「解決して」ではなく「この判定基準を満たせ」という形に変換することで、推測ループではなく確認ループを強制できる
- /diagnose のSignal-first設計：修正より先に成否判定基準を定義させることで、変更前後の差分を根拠として使えるようにする発想
- 全テストを先に書かせると自己完結した循環（自分で書いた仕様→自分で実装→通る）に陥るため、1テスト1実装の小ループに分割することでエージェントの推測を構造的に抑制できる

## 前提知識

- **TDD / RED-GREEN-REFACTOR** (TODO: 読むべき)
- **Claude Code スキル** (TODO: 読むべき)
- **テストダブル（mock/stub/fake）** (TODO: 読むべき)
- **public interface テスト** (TODO: 読むべき)
- **LLMエージェントのデバッグループ** (TODO: 読むべき)

## 関連記事

- /deep_2824 プロンプトの再現性をAIに自動チューニングさせる方法 〜 暗黙知を排除する
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計
- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[推測→変更→また壊れる：コーディングエージェントの悪循環に /tdd と /diagnose を差し込む](https://zenn.dev/53able/articles/71c91cb2ba61fd)
