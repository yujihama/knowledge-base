---
title: "Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す"
url: "https://zenn.dev/tre_conigli/articles/claude-code-skill-improvement-cycle"
date: 2026-04-10
tags: [Claude Code, Custom Skills, observability, feedback-loop, LLM-ops, posthoc-logging]
category: "agent-arch"
memo: "[Zenn LLM] Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す"
related: [1429, 430, 1335, 609, 107]
processed_at: "2026-04-10T21:02:58.213891"
---

## 要約

Claude Code の Custom Skills は、作成直後は正常に動作しても数週間後に出力品質が劣化する問題がある。原因は3つ：①会話終了とともにユーザーの修正フィードバックが消える「フィードバックの揮発」、②想定用途と実際の利用がズレていく「前提の漂流」、③どのモジュールが実行されたか記録が残らない「観測の不在」。この問題に対し、著者は「capturing-run-update-logs」というSkillを自作した。Skill実行後に呼び出すだけで、環境検出・ファイル収集・差分比較・バンドル生成を自動実行し、`skill-update-log.zip`を出力する。最大の設計上の工夫は収集情報を確度で3層に分類することだ：「deterministic」（ファイル・diff・traceで確認できる事実）、「context-extracted」（チャットから読み取れること）、「inferred」（仮説）。各エントリには`source`と`confidence`が必ず付与され、推測を事実として扱うミスを防ぐ。出力バンドルには`manifest.json`・`environment.json`・`shell_trace.json`・`git_status.json`・`llm_update_prompt.md`などが含まれ、別セッションに渡すことで具体的な改善案が得られる。また、実行環境（ローカルCLI/サンドボックス）とSkillの性質（bash-heavy/prompt-heavy）の2軸でデータ収集戦略を切り替える設計も特徴的で、「shell-rich」「shell-light」「artifact-only」の3クラスに分類している。記事執筆Skillへの適用例では、ユーザーの「段落が長い」「Slack向けフォーマットに」という2回のフィードバックから、`destination`変数の追加・短段落ガイドの追加・short variantの追加という3つの改善案が導出された（いずれもconfidence: medium）。最小実践として、Skill使用直後に「何を直したか（事実）」「なぜ必要だったか（推定）」「どのファイルを変えれば再発しないか（推定）」の3点を記録し、同じパターンが2回以上起きたらSkillファイルを修正するというサイクルを推奨している。

## アイデア

- 事実・context抽出・推定の3層分類でログの信頼度を明示する設計は、LLMが生成した情報の不確実性管理に直接応用できる汎用パターン
- 実行環境（ローカルCLI vs サンドボックス）とSkillの性質（bash-heavy vs prompt-heavy）の2軸でデータ収集戦略を動的に切り替える設計は、環境依存性の高いエージェントシステムに有効
- Skill自身がSkillを改善するための材料（zip bundle）を生成し、次セッションに渡すというメタ改善ループは、エージェントの自己改善アーキテクチャの具体的実装例
## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_107 ヴォイニッチ写本は何語か？ — 5つのテキストとの統計比較で600年の謎を分類する

## 原文リンク

[Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す](https://zenn.dev/tre_conigli/articles/claude-code-skill-improvement-cycle)
