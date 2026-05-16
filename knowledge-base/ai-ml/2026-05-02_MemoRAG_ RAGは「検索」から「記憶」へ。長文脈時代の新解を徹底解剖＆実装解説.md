---
title: "MemoRAG: RAGは「検索」から「記憶」へ。長文脈時代の新解を徹底解剖＆実装解説"
url: "https://zenn.dev/lluminai_tech/articles/21e34d3f7bc495"
date: 2026-05-02
tags: [MemoRAG, RAG, 長文脈処理, Memory Token, RLGF, LangChain, FAISS, KVキャッシュ圧縮]
category: "ai-ml"
related: [858, 2255, 1064, 857, 1116]
memo: "[Zenn LLM] MemoRAG: RAGは「検索」から「記憶」へ。長文脈時代の新解を徹底解剖＆実装解説"
processed_at: "2026-05-02T12:39:49.462358"
---

## 要約

MemoRAG（arXiv:2409.05591）は、北京大学・BAIIらが提案した長文脈対応RAGフレームワーク。従来RAGの根本的欠陥である「クエリとドキュメントの表現ズレ」と「全体把握が必要な曖昧なクエリへの対応不足」を、「グローバルメモリ」概念の導入で解決する。

従来RAGは Y=Θ(q, Γ(q,C)) という一本道で、クエリqでドキュメントCを直接検索する。MemoRAGは3ステップに分解する：(1) グローバルメモリθ_memからクエリに対する「手がかり（Clues）y」を生成、(2) そのCluesでドキュメントを検索して証拠Eを取得、(3) 証拠Eと元クエリqで最終回答Yを生成。人間が「本を読んで記憶し、必要な部分だけ読み返す」認知プロセスを模倣している。

メモリ圧縮には「Memory Tokens」を導入。通常のTransformer Attentionに加え特殊トークンX^mを用意し、コンテキストを圧縮率β（4〜64倍）でMemory Tokenに凝縮する。β=64の場合、128KトークンのLLMで約800万トークンのコンテキストまでスケール可能と報告されている。

Memory Moduleの学習は3段階：(1) Pre-training（生テキストの記憶）、(2) SFT（質問に対し適切な手がかりを出す教師あり学習）、(3) RLGF（Reinforcement Learning with Generation Feedback）。RLGFでは、生成した手がかりを使って実際に検索・回答生成し、その品質をフィードバックとしてpreference-based ranking loss（L=-log σ(R(y+)-R(y-))）で最適化する。これによりMemory Moduleは「単なる要約機」から「優秀な検索プランナー」へ進化する。

評価はLongBench、InfiniteBench、UltraDomainという長文脈ベンチマークで実施し、GraphRAG等のベースラインを上回る結果を示す。実装面ではPython/LangChain/FAISSを用いたコンセプト実装が紹介されており、fast LLM（GPT-3.5-turbo）でClues生成、smart LLM（GPT-4o）で最終回答生成という2モデル構成で再現可能。監査エージェント開発への応用として、「契約書のリスクを全件列挙」「複数ドキュメント横断の関係性把握」など全体把握が必要なタスクへの適用が直接的に示唆される。なお、Memory Module自体のスクラッチ学習（Pre-training+SFT+RLGF）はコスト高だが、公式学習済みモデルが提供されている。

## アイデア

- RLGFによるMemory Moduleの学習：生成した手がかりの「検索・回答品質」を報酬としてpreference ranking lossで最適化することで、要約ではなく「検索に有用な手がかり生成」に特化させる点が独創的
- 圧縮率βによるスケーリング：Memory Tokenへの情報圧縮でβ=64時に128K→800万トークンまでスケール可能という設計は、ロングコンテキストモデルのコスト問題への実用的代替案
- 監査エージェントへの直接応用：「契約書の全リスク列挙」や「複数ドキュメント横断の伏線・関係性把握」など、断片検索では対応不可能なタスクをClues生成経由で解決できる構造

## 前提知識

- **RAG（Retrieval-Augmented Generation）** (TODO: 読むべき)
- **Transformer Attention** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **RLHF/RLAIF** (TODO: 読むべき)
- **FAISS** → /deep_487 Nishika 日本酒銘柄画像検索コンペ 7位解法（備忘録）

## 関連記事

- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_1064 Intel Gaudi 2とXeonを活用したコスト効率の高いエンタープライズRAGアプリケーション構築
- /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[MemoRAG: RAGは「検索」から「記憶」へ。長文脈時代の新解を徹底解剖＆実装解説](https://zenn.dev/lluminai_tech/articles/21e34d3f7bc495)
