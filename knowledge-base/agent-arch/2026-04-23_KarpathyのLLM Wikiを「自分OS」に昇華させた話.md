---
title: "KarpathyのLLM Wikiを「自分OS」に昇華させた話"
url: "https://zenn.dev/hayatetakeda/articles/e0254eeb4cd15f"
date: 2026-04-23
tags: [LLM-Wiki, ナレッジ管理, Claude-Code, RAG, Karpathy, 個人OS, スキル設計, アーカイブ原則]
category: "agent-arch"
related: [1116, 1334, 2103, 861, 112]
memo: "[Zenn LLM] Karpathyの「LLM Wiki」を「自分OS」に昇華させた話"
processed_at: "2026-04-23T12:08:35.886894"
---

## 要約

Andrej KarpathyがGistに公開した「LLM Wiki」コンセプトを出発点に、著者が個人の知識管理システムを設計・実装した記録。KarpathyのWikiは「Raw Sources → Wiki Pages → Schema/Index」の3層構造で、LLMがソース取り込み時に知識をコンパイルして蓄積する。RAGが毎回ゼロから検索するのに対し、LLM Wikiは一度理解した知識を統合・保持するため、次クエリへの引き継ぎが可能な点が本質的な違いだ。著者はKarpathyの設計が「外向き」（エンティティと概念の関係記述）に特化していると気づき、「いつ・どういう状態で考えたか」という自分コンテキストが欠落していると判断。これを補うため、Wiki領域をKnowledge（技術・外部情報）、Decisions（意思決定ログ）、Self（思考・行動パターン）の3領域に分割し、その交差点にSynthesis層を追加した。ディレクトリ構造はRaw層（生ソース・不変）、Sources層（構造化済み・read専用）、Wiki層（LLM完全管理・自己増殖）の3層に分かれる。各ジャンルは_index.md/_log.md/_overview.mdの3点セットを持ち、LLMが次セッション開始時にこれらを読むだけで現在のWiki状態を把握できる設計になっている。自動化レベルは領域ごとに差別化しており、Knowledgeは新規作成・追記を完全自動化するが、Decisionは確認後のみ実行、Selfは提案のみで書き換えを禁止している。パターン抽出と矛盾指摘は必ず人間を介在させる。理由は「LLMが勝手に『あなたはこういう人』を固定化する」自己成就的予言リスクを避けるためだ。Decisions領域にはアーカイブ原則を適用し、意思決定ログは書き換えず、新しい判断はsuperseded_byフィールドで連鎖させる。これにより「思考の化石層」と「現在の地図」を両立させる。Claude Codeのスキルとして実装したingestフローでは、STEP 3.5「影響範囲アセスメント」（内部処理・ユーザー非表示）を挟むことで、処理開始前に変更影響を俯瞰し精度を向上させる。Phase 1の最小実装はingest/query/morning/eveningの4コマンドとschemaテンプレート2種のみとし、Synthesis層やlint・パターン抽出はデータ蓄積後のPhase 2以降に委ねている。監査エージェント開発への示唆として、Decisions領域のアーカイブ原則（判断日固定・superseded_byチェーン）は、監査証跡管理や内部統制の判断ログ設計に直接応用可能な設計パターンだ。

## アイデア

- RAGが「毎回ゼロから検索」するのに対し、LLM WikiはソースをコンパイルしてWikiとして蓄積する非対称アーキテクチャ——コンテキスト効率の問題を「事前統合」で解く発想
- Selfフローでの「朝の自由記述（フレームなし）→LLMが裏で構造化→夜に構造化質問」という非対称設計が、LLMによる自己成就的予言バイアスを防ぐ実用的な仕組み
- Decisions領域のsuperseded_byチェーン＋date固定というアーカイブ原則は、監査証跡管理における「判断の不変性保証」と構造的に同型であり、内部統制ログ設計に転用できる

## 前提知識

- **LLM Wiki** → /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Obsidian** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **フロントマター** (TODO: 読むべき)

## 関連記事

- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_2103 製造業RAG運用編：監査ログ + イベント駆動再インデックスを実装する
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた

## 原文リンク

[KarpathyのLLM Wikiを「自分OS」に昇華させた話](https://zenn.dev/hayatetakeda/articles/e0254eeb4cd15f)
