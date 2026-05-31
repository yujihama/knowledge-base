---
title: "Claude Codeの.claude/の賞味期限がきれてしまう問題を半年運用しながら直し続けた話"
url: "https://zenn.dev/rkpg/articles/claude-code-self-improving-skill-loop"
date: 2026-05-31
tags: [Claude Code, プロンプト管理, 自己改善ループ, CLAUDE.md, ワークフロー自動化, 品質評価, スキル設計]
category: "agent-arch"
related: [6563, 2953, 2978, 2930, 3117]
memo: "[Zenn LLM] Claude Codeの.claude/の賞味期限がきれてしまう問題を半年運用しながら直し続けた話"
processed_at: "2026-05-31T09:04:32.703427"
---

## 要約

Claude Codeの.claude/配下に置くルールファイル（CLAUDE.md、agents/等）は、書いた瞬間から劣化が始まるという問題提起と、それへの実践的な対処法を半年間の運用ログをもとに紹介した記事。

著者はブログ執筆ワークフローで ghostwriter.md にルールを追記し続けたが、50行→100行→200行と肥大化するにもかかわらず「だ/である調」「参考文献漏れ」「内部リンク形式違い」といった同じ修正指示が毎週繰り返された。根本原因は「ルールを追記しているだけで観察できていなかった」ことと気づき、log→review→amend→evalの4スキルによる自己修正ループを設計した。

各スキルの具体的構成：
- /skill:log：ワークフロー完了時に構造化JSONログ（id, skill, corrections[], errors[], quality_signals等）を.claude/skills/logs/に自動出力。correctionsにはどのルールファイルが原因かをsource_fileとして記録。
- /skill:review：ログが5本溜まると自動発火。issue を recurring（3回以上）/memory化/任意amend に分類し、TOP ISSUESとしてレポート生成。頭の印象ではなく機械的な頻度集計で改善対象を特定。
- /skill:amend：recurringと判定されたissueを対象ルールファイルに実際に適用。change_typeは instruction_strengthening/addition/removal/reorder/output_format_change/tool_usage_change/trigger_refinement/workflow_changeの8種類。「削る」「並び替える」も選択肢に含める点が重要。
- /skill:eval：amend後に3回以上ログが溜まった段階でBefore/After比較。EFFECTIVE/PARTIALLY_EFFECTIVE/INEFFECTIVE/HARMFULの4段階判定。HARMFULならgit checkoutでロールバック。

実績として「参考文献漏れ」issueの発生率が1/5（20%）→0/4（0%）に低下。半年でログ30本・review 6本・amendment 9本を運用。

落とし穴として①ログ自体の記録漏れ、②review後にamendに進まない週の発生、③instruction_additionだけを繰り返すことによるルールファイル肥大化（エージェントが冒頭しか読まなくなる問題）を挙げ、肥大化対策としてinstruction_reorderとinstruction_removalを意識的に組み込む設計を採用している。またCLAUDE.mdやMEMORY.md本体のサイズ超過で部分ロードが発生した事故を受け、別ファイル（.claude/rules/memory-hygiene.md）で剪定ルールを切り出した。

監査エージェント開発への示唆：エージェントへの指示ファイルを「静的ドキュメント」ではなく「継続的に観察・改訂するループの対象」として設計する考え方は、LangGraphやReActベースの監査エージェントにおけるプロンプト管理にも直接応用可能。特にJSONログを起点とした定量的な品質トラッキングとロールバック機構は、監査ワークフローの信頼性向上に転用できる。

## アイデア

- ルールファイルの劣化を「観察できていないこと」として定義し、JSONログによる機械的な頻度集計でヒューリスティックな印象バイアスを排除する設計が秀逸
- amend のchange_typeに「削る（removal）」「並び替える（reorder）」を明示的に含めることで、instruction_addition一辺倒による肥大化→読み飛ばしの悪循環を構造的に防止している
- ループ自身が腐る（review.mdの手順漏れを3週間後に再発）という事例を自己観察ログに記録し、メタプロセスの改善サイクルにフィードバックする再帰的な設計思想

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **JSONスキーマ設計** (TODO: 読むべき)
- **git checkout（ロールバック）** (TODO: 読むべき)

## 関連記事

- /deep_6563 コードを書けない私がClaude Codeで「AIチーム」を回すまで
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_2978 中国のテック労働者がAIドッペルゲンガー訓練を迫られ反発——「同僚スキル」と「反蒸留」ツールの攻防
- /deep_2930 中国のテックワーカーたちが「AIの分身」を訓練し始め、反発も起きている
- /deep_3117 中国のテックワーカーたちがAIドッペルゲンガーのトレーニングを命じられ、反発を始めている

## 原文リンク

[Claude Codeの.claude/の賞味期限がきれてしまう問題を半年運用しながら直し続けた話](https://zenn.dev/rkpg/articles/claude-code-self-improving-skill-loop)
