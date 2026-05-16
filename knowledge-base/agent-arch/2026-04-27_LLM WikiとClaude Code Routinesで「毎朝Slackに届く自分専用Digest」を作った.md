---
title: "LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った"
url: "https://zenn.dev/biscuit/articles/llm-wiki-daily-digest-routines"
date: 2026-04-27
tags: [Claude Code Routines, LLM Wiki, Slack MCP, push型パイプライン, git管理状態ストア, 定期実行エージェント, 重複排除]
category: "agent-arch"
related: [2821, 1965, 900]
memo: "[Zenn LLM] LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った"
processed_at: "2026-04-27T12:11:44.083703"
---

## 要約

LLM Wikiはpull型のシステムであるため、蓄積した知識を能動的に引き出さないと活用されないという課題に対し、Claude Code Routinesを使ったpush型Digestパイプラインを構築した事例。毎朝AM7:00（JST）に自動実行され、Slackの#llm-wiki-digestチャンネルへ関連記事5件を投稿する。

キュレーションの軸はwiki/index.md（知識領域・タグ・エンティティの全体像）とbrand-foundation/positioning.md（中長期目標・テーマ）の2ファイルのみ。プロンプトは毎回これら2ファイルを読み直す設計にしているため、Routine側のプロンプトを変更せずにwikiやpositioningを更新するだけで挙動が変わる。

重複排除はDBやKVSではなく、wiki/digests/YYYY-MM-DD.mdというMarkdownファイルをgit管理することで実現。Routineは毎朝このディレクトリを全読みして過去投稿済みURLリストを生成してから記事検索に入る。Slack投稿フォーマットは「記事タイトル・URL・関連タグor wikiページ｜一言コメント（なぜ今日の自分に関係するか）」の3行構成で、5件に絞ることで朝の可処分時間内に消化できる量を維持している。

Routineは5ステップで定義：①コンテキスト読み込み、②投稿済みURL収集、③Web検索（英日両対応）で記事5件選定、④Slack投稿、⑤ダイジェストログをMarkdownで記録しブランチ→commit→push→PR作成。このgitフローは既存のwiki-ingestルーティンと同じauto-digest/*ブランチ命名規則・PRパターンに統一されており、複数の自動化パイプラインが混在しても起源の判別が容易。

Routinesはクラウド側で動作するためPCを起動しておく必要がない。使用モデルはclaude-opus-4-6、MCPコネクタはSlack。残課題として、検索クエリ設計がRoutine任せで日による精度差がある点、ソースが有名メディアに偏る点、Slackリアクションを次回の選定にフィードバックするループ未実装の点が挙げられている。

監査エージェント開発への示唆：定期実行エージェントがgit管理ファイルを状態ストアとして使うパターンは、監査ログの自動蓄積・重複チェック・エビデンス管理の設計にそのまま転用できる。Routineのself-contained promptとwiki側への関心分離は、監査エージェントにおけるルール定義とエージェント実行ロジックの分離設計とも親和性が高い。

## アイデア

- 重複排除にDBを使わず投稿ログをwikiと同一リポジトリのMarkdownで管理することで、外部ストレージ不要かつgit履歴でメタ分析が可能な設計にしている点
- Routineのプロンプトをself-containedにしてwiki/index.mdとpositioning.mdを毎回読み直す設計にすることで、Routine再デプロイなしにwiki更新だけでキュレーション挙動を変更できるようにした点
- wiki-ingestとdigestで同一のbranch→PR→mergeパターンを採用し、自動化パイプラインの起源をgit logから即座に判別できる一貫性を確保している点

## 前提知識

- **Claude Code Routines** → /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **LLM Wiki** → /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- **Slack Webhook/MCP** (TODO: 読むべき)
- **git branch運用** (TODO: 読むべき)

## 関連記事

- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- /deep_900 ファイルからチャンクへ：HuggingFaceストレージ効率の改善

## 原文リンク

[LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った](https://zenn.dev/biscuit/articles/llm-wiki-daily-digest-routines)
