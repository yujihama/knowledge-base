---
title: "LLM Wikiが育つほどAI解説が賢くなる：知識増幅ループのつくり方"
url: "https://zenn.dev/biscuit/articles/llm-wiki-knowledge-amplification-loop"
date: 2026-05-05
tags: [Claude Code, LLM-Wiki, Obsidian, knowledge-management, RAG, human-in-the-loop, automation, routine]
category: "agent-arch"
related: [2954, 2821, 2404, 1962, 2963]
memo: "[Zenn LLM] LLM Wikiが育つほどAI解説が賢くなる：知識増幅ループのつくり方"
processed_at: "2026-05-05T12:07:54.116245"
---

## 要約

Claude Code Routineを活用したパーソナルナレッジベース「LLM Wiki」の改善事例。従来のSlack配信フロー（記事URLと短い要約を毎朝投稿）では3つの問題があった：①wikiの既存知識との接続が生まれない、②Slackは流れて消えてしまう、③確認行為が知識蓄積に紐づかない。これを解決するため、設計を「知識増幅ループ」に刷新した。

コアとなる変更は2点。第一に、Claude Code Routineの役割を「記事を選ぶ」から「既存wikiを参照しながら自分専用の解説を書き起こす」に拡張した。生成される解説ファイルは3セクション構成（何が書かれているか／構造的な読み解き／wikiとの接続）で、frontmatterにはwiki_connections（既存wikiページ名）とknowledge_gap（wikiに未収録の領域）が記録される。第二に、承認ゲートをObsidian上に実装した。RoutineはObsidianのvault配下のraw/inbox/に解説ファイルをreview_status: pendingで保存し、ユーザーがapprovedに変更したものだけがwiki-ingestを経由してwiki/に取り込まれる。

review_statusは当初approved: true/falseの二値だったが、「見たが取り込まないと決めた」と「まだ未レビュー」が区別できないため、pending／approved／rejectedの3値に移行した。Obsidian上ではMetadata MenuプラグインのCycle型として実装し、クリック一発で値を巡回できる。Obsidian Basesプラグインによるダッシュボードでpendingのみをフィルタ表示し、レビュー待ちキューを管理する。

wiki-ingestルーティンはapprovedファイルを検出すると、wiki_connectionsの既存ページを更新し、knowledge_gapに対応する新規ページを作成してingestedをtrueに更新する。このループにより、知識ベース→解説生成→承認→知識ベース更新が循環し、Routineが次回参照する知識が徐々に厚くなっていく。設計原則として「80% AI・20% 人間」を掲げ、キュレーションの最終判断は人間が担うことをアーキテクチャレベルで保証している。監査エージェント開発においても、AIが生成した分析結果に人間承認ゲートを挟む同型の設計パターンとして応用できる。

## アイデア

- review_statusをpending/approved/rejectedの3値にすることで「未レビュー」と「意図的に却下」を区別し、過去に弾いた記事をAIが再選出するのを防げる設計
- wiki_connectionsとknowledge_gapをfrontmatterに構造化することで、Obsidianで開いた瞬間に「自分の知識地図のどこに置くか」が決まっており、承認コストを最小化している
- 知識ベース→解説生成→承認→知識ベース更新のループにより、参照知識が蓄積されるほどRoutineが生成する解説の文脈精度が向上するという自己強化構造

## 前提知識

- **Claude Code Routines** → /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- **Obsidian** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **frontmatter** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト

## 関連記事

- /deep_2954 ObsidianとClaude Codeで「育つ知識ベース」を作った話
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- /deep_2963 SOWでシンプルにClaude Codeを活用する

## 原文リンク

[LLM Wikiが育つほどAI解説が賢くなる：知識増幅ループのつくり方](https://zenn.dev/biscuit/articles/llm-wiki-knowledge-amplification-loop)
