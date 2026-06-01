---
title: "KotonohaとLLM Wikiの違い：育つ知識ベースから、意味変化を監査する文脈OSへ"
url: "https://zenn.dev/tomyuk/articles/3748a3dccfdd27"
date: 2026-06-01
tags: [LLM Wiki, Kotonoha, RDE, 意味監査, 文脈管理, Obsidian, RAG, AI協働, 知識ベース]
category: "agent-arch"
related: [4186, 2821, 2404, 5840, 4235]
memo: "[Zenn LLM] KotonohaとLLM Wikiの違い：育つ知識ベースから、意味変化を監査する文脈OSへ"
processed_at: "2026-06-01T21:00:37.475940"
---

## 要約

本記事は、生成AI時代の知識管理における2つのアプローチ——LLM WikiとKotonoha——の設計思想を比較する。LLM Wikiは、RAGの限界（毎回検索するだけで知識が積み上がらない）を克服するため、LLMにMarkdown Wikiを継続的に編集・保守させる仕組みである。元資料（Raw Sources）をLLMが読み込み、要約・分類・リンク生成を経てWikiに反映し、次回以降の作業に引き継ぐ。この設計は軽快で実装しやすく、個人Wiki・研究メモ・社内ナレッジに適する。一方Kotonohaは、LLM WikiをSynthesis Layerとして取り込みつつ、その上位に「意味変化の監査」機能を置く。Kotonohaが問うのは「AIが整理した知識は、元の文脈からどう変わったか」であり、仮説が方針に格上げされていないか、未検証の内容が事実のように見えていないか、実装上の都合が思想的主張にすり替わっていないかを可視化・記録する。中核概念はRDE（Resonant Deviation Evaluator）で、生成物の品質評価ではなく意味変化の構造的監査を行う。RDEは保存・変換・補完・未解決・逸脱リスク・次回更新方針の6観点で評価し、Level 0（誤字修正→自動承認）からLevel 4（公開文書→RDEログ必須）の5段階で人間レビューの要否を判定する。UIは単なる表示画面ではなく、source・generated・reviewed・accepted・unresolved・drift-riskの6状態をバッジやレーンで区別し、責任境界を可視化する「認知的足場」として設計される。ディレクトリ構成はsources/・context/・wiki/・audit/・decisions/・handoff/・schema/に分かれ、audit/配下にrde-log.md・drift-candidates.md・unresolved.mdを置く。2026-05リリース「First UI hardening baseline」はこの全構想の最初の足場であり、UI堅牢化・文脈可視化・意思決定分離・監査準備・ハンドオフ基盤整備の5点を優先する。監査エージェント開発への示唆：AI生成物とhuman-approvedの判断を明示的に分離するRDE的レイヤーは、LangGraphベースの監査エージェントにおいても、エージェントの推論結果と人間の最終承認を区別するステート設計に直接応用できる。

## アイデア

- RDE（Resonant Deviation Evaluator）の5段階レベル分類は、監査エージェントにおける「LLMの推論結果を人間レビューに回すかどうかの閾値設計」に直接転用できる構造的フレームワーク
- LLM生成物の状態をsource/generated/reviewed/accepted/unresolved/drift-riskの6種類でラベリングするUI設計は、マルチエージェントシステムにおける情報出所追跡（provenance tracking）の実装パターンとして参考になる
- Handoff Layerに作成日時・対象範囲・未解決事項・既知の不確実性を含める設計は、LangGraphのStateに監査証跡メタデータを埋め込む手法と対応しており、エージェント間の文脈引き継ぎの堅牢性を高める

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LLM Wiki** → /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- **Obsidian** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **Markdown** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた
- **provenance tracking** (TODO: 読むべき)

## 関連記事

- /deep_4186 Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_5840 ObsidianのメモがAIで自動的に記事になる──第二の脳の発信パイプラインを構築した話
- /deep_4235 M³-VQA：マルチモーダル・多エンティティ・多ホップ視覚的質問応答ベンチマーク

## 原文リンク

[KotonohaとLLM Wikiの違い：育つ知識ベースから、意味変化を監査する文脈OSへ](https://zenn.dev/tomyuk/articles/3748a3dccfdd27)
