---
title: "Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群"
url: "https://zenn.dev/biscuit/articles/llm-wiki-context-rot-solution"
date: 2026-05-07
tags: [Context Engineering, Context Rot, LLM Wiki, RAG, Knowledge Base, Compaction, Context Pruning, Just-in-Time Retrieval, Obsidian, Claude Code]
category: "agent-arch"
related: [2821, 3776, 3239, 2404, 2954]
memo: "[Zenn LLM] Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群"
processed_at: "2026-05-07T21:17:35.185612"
---

## 要約

Chromaの研究チームが提唱し、Anthropicがブログで取り上げた「Context Rot」とは、長コンテキストに無関係・冗長な情報が混入することでモデルの推論精度が劣化する現象を指す。メカニズムはTransformerのn²アテンション計算による注意分散、トークン増加に伴う想起精度低下（Chroma実証）、トレーニングデータにおける長コンテキストサンプルの相対的不足の3要因に整理される。失敗パターンはContext poisoning（誤情報の後続強化）、Context distraction（履歴依存）、Context confusion（無関係情報への引きずられ）、Context clash（矛盾情報）の4つ。Salesforce×Microsoft Researchの共同研究では、シングルターンからマルチターンに変えるだけでモデル性能が平均39%低下し、OpenAI o3は98.1%→64.1%に落下した事例が報告されている。

Anthropicが整理した対策技法はCompaction（要約による継続）、Structured note-taking（外部永続化）、Sub-agent architectures（隔離・要約返却）の3つに加え、RAG、Tool loadout、Context pruningを加えた計6技法に整理できる。

筆者が運用するLLM Wiki（Andrej KarpathyとShann Holmbergが体系化したパターン）のアーキテクチャは、これら6技法と一対一で対応する。①raw/とwiki/の物理分離＋ingestによる蒸留 → Sub-agent architectures。②Obsidian上でのreview_statusによる人間承認ゲート（LLMは書き換え不可） → Context Pruning。③wiki/sources/（1〜2千トークン）からwiki/concepts/（1千トークン前後）への段階的蒸留 → Compaction。④スキーマ定義ファイル＋wiki/index.md（全ページTLDRカタログ）からGlob/Grep/Readで動的取得 → Just-in-Time Retrieval。⑤wiki/concepts/・wiki/syntheses/への永続化 → Structured note-taking。⑥週次lintによるリンク切れ・孤立ページ・矛盾・陳腐化・重複概念の検出・修正 → Context Poisoning予防とContext Clash解消のガベージコレクション。さらにbrand-foundation/（声・トーン・ポジショニング定義、LLM書き換え禁止）はAnthropicの「Right altitude」システムプロンプト設計に対応する静的アンカー層として機能する。

設計原則の核心は「コンテキストに何を載せないかをどう決めるか」に集約される。監査エージェント開発への示唆として、社内ドキュメントをベクトル化してRAGに流し込む前に、rawとして隔離すべき層・人間承認ゲートを通る昇格基準・ガベージコレクションの運用主体・チームの前提定義をナレッジとは別レイヤーに分離する設計を先に立てることが重要であり、エージェントの推論品質はコンテキスト設計という情報アーキテクチャの問題として捉えるべきである。

## アイデア

- 「Context Rotを防ぐ」問題を解くと知識ベース設計はContext Engineering 6技法に自然収束するという観察は、エージェントシステムの情報アーキテクチャ設計に直接応用できる普遍的な設計原則を示している
- review_statusフィールドをLLM書き換え禁止とすることでContext Pruningの判定主体を人間に固定し、ハルシネーション混入を防ぐ設計は、監査AIにおける人間-LLM権限分離の具体的実装パターンとして参照できる
- 「全部ベクトル化してRAGにする」前にraw隔離層・承認ゲート・GCの運用設計を先行させるという問いの立て方は、監査エージェントのナレッジ基盤構築において手戻りを防ぐ設計順序として重要

## 前提知識

- **Transformer attention** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Context window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **LLM Wiki** → /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- **Just-in-Time Retrieval** (TODO: 読むべき)

## 関連記事

- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_3776 LLM Wikiが育つほどAI解説が賢くなる：知識増幅ループのつくり方
- /deep_3239 Claude Code で LLM Wiki を育てる——第二の脳の作り方
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2954 ObsidianとClaude Codeで「育つ知識ベース」を作った話

## 原文リンク

[Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群](https://zenn.dev/biscuit/articles/llm-wiki-context-rot-solution)
