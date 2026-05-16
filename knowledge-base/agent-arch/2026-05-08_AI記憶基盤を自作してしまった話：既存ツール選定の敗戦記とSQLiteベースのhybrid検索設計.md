---
title: "AI記憶基盤を自作してしまった話：既存ツール選定の敗戦記とSQLiteベースのhybrid検索設計"
url: "https://zenn.dev/chemica_tan/articles/26e0a958cd6ee0"
date: 2026-05-08
tags: [RAG, hybrid検索, SQLite, graph-traversal, BM25, embedding, MCP, bi-temporal, memory, Graphiti, RRF]
category: "agent-arch"
related: [4335, 969, 9, 2831, 68]
memo: "[Zenn LLM] AI記憶ツールを調べていたら、SQLiteを叩いてもらっていた話 — まだ引き返せるので止めてください"
processed_at: "2026-05-08T21:14:43.825661"
---

## 要約

化学工学系のvibe coderが、AIとの長期作業における「記憶問題」を解決しようと既存ツールを調査・実使用した末に、自作記憶基盤「initias」を作ることになった経緯の記録。

問題の本質は「記憶がないこと」ではなく「思い出すのがダルいこと」だと気づいた点が核心。Cipherを数ヶ月運用したところ、検索に最悪40秒かかるケースがあり、結果としてAI・人間双方が積極的に使わなくなった。「引くのが重たい記憶は使われない記憶になる」という評価軸を実体験から導出した。

次に、AI agent memory / Graph-RAG / Claude Code系記憶機構 / ローカルhybrid検索基盤の4系統を網羅的に調査。評価条件はベンダーロックイン回避、ローカル完結、embedding非必須（フォールバック可）、サーバー常駐不要、graph検索経路保持、LLM per query回避など。脱落理由は「毎回embedding必須」「サーバー常駐前提」「LLM per query/ingest必須」「用途違い」「graph検索なし/cold start遅延」の5パターンに集約された。

GraphitiはBM25+embedding+graph traversal+RRFという構成で問題設定が最も近かったが、バックエンドにNeo4j・FalkorDB・Kuzuが必要。KuzuはAppleに買収されGitHubがarchived状態（2025年10月）、FalkorDBLiteは真のembeddedではないため、「個人がローカルで抱えられるembedded graph DB」の着地先がぽっかり空いていた。

結果として選んだのはSQLiteにedgesテーブルを置き、再帰CTE（共通テーブル式）でグラフを辿る構成。情報の実体はMarkdownファイルで保持してDBは再生成可能にし、ベンダーロックインを根本回避。検索は三層構造：FTS（BM25）で語彙ヒット→embedding（cosine）で意味ヒット→graph walk（BFS）で連想ヒット。特徴的なのはRRFによるスコア融合を行わず、3層の結果を「並べるだけ」にしている点。各層が別の問いに答えているため混ぜると役割が中和されるという設計判断。

約1ヶ月でactive node約1,960件・active edges 1,214本・edge判定ログ1,193件まで成長。設計上の失敗として「対称グラフ→有向グラフへの移行（数千本のedgeをbi-temporal無効化して積み直し）」「長文チャンク分割の廃止」「graph walkのseedをFTS top-2+embedding top-2のhybrid方式に変更」の3点を修正。

監査エージェント開発への示唆：（1）記憶/知識検索の評価軸として「検索レイテンシと使用頻度の相関」は見落とされやすいが実運用上クリティカル。（2）FTS/embedding/graph walkの非融合並列提示は、LLM-as-judgeが根拠層を識別するのに有効な設計パターン。（3）bi-temporal edge管理（削除でなく無効化日時付与）は監査ログとしての知識変遷追跡に直接応用可能。

## アイデア

- 「思い出すコスト」が記憶基盤の実用性を左右するという評価軸：検索レイテンシが40秒になると人間もAIも使わなくなるという実証は、RAGシステム設計において機能仕様より体験品質が支配的であることを示す
- FTS/embedding/graph walkの3層をRRFで融合せず並列提示する設計：各層が「語彙ヒット」「意味ヒット」「連想ヒット」という異なる問いに答えているため混ぜると情報が劣化するという判断は、LLM-as-judgeの根拠透明性設計にも応用できる
- SQLite+再帰CTEによるembedded graph traversal：KuzuのApple買収などembedded graph DBの選択肢が消去法で消えた結果、標準的なSQLで有向グラフを実装することが「撤退前提の仮設」として合理的という結論は、依存先リスク管理の実践例として参考になる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **BM25 / FTS** (TODO: 読むべき)
- **graph traversal / CTE** (TODO: 読むべき)
- **vector embedding** (TODO: 読むべき)
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法
- /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_2831 ElasticsearchのDense/BM25/SPLADEをRRFで統合した3-way検索をJMTEB 11タスクで精度検証
- /deep_68 Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践

## 原文リンク

[AI記憶基盤を自作してしまった話：既存ツール選定の敗戦記とSQLiteベースのhybrid検索設計](https://zenn.dev/chemica_tan/articles/26e0a958cd6ee0)
