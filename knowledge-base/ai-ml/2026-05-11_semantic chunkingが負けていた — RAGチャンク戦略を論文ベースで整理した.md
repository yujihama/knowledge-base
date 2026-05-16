---
title: "semantic chunkingが負けていた — RAGチャンク戦略を論文ベースで整理した"
url: "https://zenn.dev/archfill/articles/rag-chunk-strategy-2026"
date: 2026-05-11
tags: [RAG, チャンク戦略, semantic chunking, embedding, Vectara, 固定サイズ分割, Recursive Character Splitting, Agentic Search, ベクトル検索]
category: "ai-ml"
related: [5261, 1787, 2739, 2605, 2764]
memo: "[Zenn LLM] semantic chunkingが負けていた — RAGチャンク戦略を論文ベースで整理した"
processed_at: "2026-05-11T21:30:37.960733"
---

## 要約

RAG構築時のチャンク戦略において、「semantic chunkingが最も精度が高い」という直感が論文によって否定されていることを整理した記事。Vectara Inc.が2024年10月に発表した論文「Is Semantic Chunking Worth the Computational Cost?」では、HotpotQA・MIRACLなど10のベンチマークデータセットを用いて固定サイズ分割・Recursive分割・semantic chunkingを比較評価した結果、固定サイズ分割が5データセット中3つで最良の結果を示し、semantic chunkingは計算コストに見合う一貫した性能向上をもたらさないと結論付けている。semantic chunkingが精度を下回る主因は「細片化」にある。文のembedding類似度を基に意味変化点で分割するため、チャンクサイズが過小になりやすく、検索ヒット自体は成功してもLLMの文脈生成に必要な情報量が不足し、回答精度が低下する構造になる。加えてインデックス構築時に全文のembedding生成と類似度計算が必要なためコストも高い。2025年4月のarXiv論文（arXiv:2504.19754）でも同様のトレードオフが確認されており、Contextual Retrievalは意味的一貫性を改善するが計算コストが増大、Late Chunkingは効率的だが関連性・完全性を犠牲にする傾向があるとされ、「高度な手法ほど精度が高い」という前提は2025年時点でも成立していない。Markdownコンテンツへの推奨戦略は「H1〜H3ヘッダーによるセクション分割 → 各セクション内でRecursive 512トークン分割 → overlap 10%」の3ステップ構成。ヘッダーで意味的境界を構造から取ることでsemantic chunkingの目的をコストゼロで近似できる。コードブロック・テーブル・リストは途中で分割すると意味が壊れるため単独チャンクとして保持する。overlapについても、複数研究で「計測上の性能向上に寄与しない」という結果が出ており、0%でも問題ない可能性が高いとされる。また補足として、Claude Codeの作者Boris Chernyが「初期はRAG＋ローカルベクトルDBを採用したが、Agentic Search（Glob/Grep/Read）に切り替えた」と発言していることを引用し、頻繁に変わるコードベースのようなドメインでは静的インデックスより動的探索の方が精度・鮮度・セキュリティ面で優れるという判断を紹介。チャンク最適化より先にアーキテクチャ選択がRAG精度に効いてくる場合があるという視点を提示している。監査エージェント開発への示唆：内部監査文書（規程・調書・ガイドライン等）はMarkdown化されることが多く、Header分割＋Recursive 512トークンの戦略がコスト対効果で最も実用的。また文書が頻繁に改訂される監査環境では、静的RAGよりAgentic Searchの採用を検討する価値がある。

## アイデア

- semantic chunkingは検索ヒット精度ではなくLLM文脈生成段階で劣後する：チャンクが小さすぎて文脈が不足するという「細片化」問題は、retrieval精度とgeneration精度を分けて評価しないと見落とされやすいアーキテクチャ上の盲点
- Markdownヘッダーによる構造的分割がsemantic chunkingの代替になる：文書構造（H1〜H3）を意味的境界として利用することで、embedding計算コストをかけずにsemantic chunkingの目的を近似できるという発想は、構造化ドキュメント主体の業務システムに直接応用可能
- Claude CodeのRAG廃止判断がアーキテクチャ選択の問い直しを促す：「静的インデックス vs 動的エージェント探索」という二択は、鮮度・セキュリティ・信頼性のトレードオフを含むアーキテクチャ意思決定であり、チャンク戦略の最適化より上位の設計判断として位置づけられる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **embedding** → /deep_33 2時間ごとに自分を再構築する — 自律AIエージェントの記憶アーキテクチャ
- **ベクトル検索** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **Recursive Character Splitting** (TODO: 読むべき)
- **Agentic Search** (TODO: 読むべき)

## 関連記事

- /deep_5261 『三国志』を使って最小構成のRAGを実装してみた
- /deep_1787 LLMの2大カテゴリ：質疑応答モデルとEmbeddingモデルの違い
- /deep_2739 制約の多い公共部門環境でAIを実用化する：SLMという選択肢
- /deep_2605 制約の多い公共セクター環境でAIを実用化する：SLMという現実解
- /deep_2764 制約のある公共部門環境でAIを実用化する：SLMという現実解

## 原文リンク

[semantic chunkingが負けていた — RAGチャンク戦略を論文ベースで整理した](https://zenn.dev/archfill/articles/rag-chunk-strategy-2026)
