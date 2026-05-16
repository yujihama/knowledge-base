---
title: "superpowersを解析して学ぶClaude Codeプラグイン設計"
url: "https://zenn.dev/keisuke_se/articles/f64a0e8cd5dd94"
date: 2026-05-07
tags: [Claude Code, plugin設計, SKILL.md, hooks, TDD, エージェント制御, superpowers, Skillツール, TodoWrite, Graphviz]
category: "agent-arch"
related: [2824, 94, 1045, 2961, 1834]
memo: "[Zenn LLM] superpowersを解析して学ぶplugin設計"
processed_at: "2026-05-07T21:41:04.569693"
---

## 要約

Claude Codeのプラグイン「superpowers」のソースコードを解析し、コーディングエージェントの行動制御設計を学んだ記録。superpowersは「エージェントが計画なしにいきなりコードを書き始める」「長期自律稼働ができない」「テストを書かない」という3つの問題を解決するフレームワーク。

仕組みの核心はSKILL.mdというMarkdownファイルへの行動規範の外部化と、セッション開始時の強制注入。hooks/session-startシェルスクリプトがusing-superpowers/SKILL.mdを読み込み、<EXTREMELY_IMPORTANT>タグ付きのJSONとして標準出力することでエージェントのコンテキストに挿入される。hooks.jsonにstartup・clear・compactイベントを定義することでセッション開始を検知する仕組み。

スキルの呼び出しにはReadツールではなくSkillツールを必須とする設計が重要。Readツールはファイル内容をテキストとして返すだけだが、Skillツールはプラットフォームが「スキルが呼び出された」と記録し、コンテンツが「アクティブな指示」としてコンテキストに入るため、エージェントがスキルを無視しにくくなる。スキルが適用できる可能性が1%でもある場合は必ず呼び出すルールで、スキップ条件を意図的に厳しく設計している。

スキルの適用順序はGraphviz（dot言語）のフローチャートとして埋め込まれており、エージェントがテキストとして読んで判断する。プロセス系スキル（brainstorming、systematic-debugging）→実装系スキル（test-driven-development、subagent-driven-development）の順序が定められている。

哲学的柱はTDD・YAGNI・DRYの3つ。TDDではRED→GREEN→REFACTORサイクルを強制し、テスト前に書いたコードは削除する。チェックリストがある場合はTodoWriteへの登録を義務化し、頭での追跡を禁止している。エージェントのサボりパターン（Red Flags）を列挙して反論を明示することで合理化を防ぐ設計も特徴的。

スキル一覧はbrainstorming・dispatching-parallel-agents・executing-plans・finishing-a-development-branch・receiving-code-review・requesting-code-review・subagent-driven-development・systematic-debugging・test-driven-development・using-git-worktrees・verification-before-completion・writing-plans・writing-skillsの13種類。commands/ディレクトリは次バージョンで削除予定の非推奨機能。

監査エージェント開発への示唆：SKILL.mdによる行動規範の外部化はLangGraphのエージェント設計にも応用可能。ワークフローの強制力をプロンプト内の文言設計で担保し、チェックリストをTodoWriteで管理する手法はReActエージェントの実行ステップ管理と親和性が高い。

## アイデア

- Skillツール vs Readツールの使い分けという設計判断：ファイルを「読む」のではなく「従うことを宣言する」という概念的な差異を実装レベルで強制する点が、エージェント行動制御の実践的知見として興味深い
- スキップ条件を「完全に関係ないと確信できる場合のみ」に設定し、1%でも可能性があれば強制呼び出しにする設計：エージェントの自己判断バイアスをルール設計で封じる手法
- エージェントの典型的な言い訳（Red Flags）を列挙して一つ一つ反論を明示する手法：合理化の余地を文書レベルで潰すというプロンプトエンジニアリングの実装パターン

## 前提知識

- **Claude Code hooks** (TODO: 読むべき)
- **SKILL.md** → /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- **TodoWrite / Tasks API** (TODO: 読むべき)
- **TDD（RED-GREEN-REFACTOR）** (TODO: 読むべき)
- **Graphviz dot言語** (TODO: 読むべき)

## 関連記事

- /deep_2824 プロンプトの再現性をAIに自動チューニングさせる方法 〜 暗黙知を排除する
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_1834 Lutum: 高度なハーネスエンジニアリングのためのRust製LLM SDK

## 原文リンク

[superpowersを解析して学ぶClaude Codeプラグイン設計](https://zenn.dev/keisuke_se/articles/f64a0e8cd5dd94)
