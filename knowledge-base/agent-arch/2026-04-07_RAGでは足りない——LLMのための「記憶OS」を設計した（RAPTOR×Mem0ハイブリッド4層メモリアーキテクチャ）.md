---
title: "RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）"
url: "https://zenn.dev/haboshi/articles/ai-memory-architecture-raptor-mem0"
date: 2026-04-07
tags: [RAPTOR, Mem0, memory-architecture, RAG, LLM-as-Judge, pgvector, HNSW, 非単調推論, 忘却設計, 矛盾検出, Supabase, pg_cron, MapReduce]
category: "agent-arch"
memo: "[Zenn LLM] RAGでは足りない——LLMのための「記憶OS」を設計した"
processed_at: "2026-04-07T09:08:13.307411"
---

## 要約

会話の中で生まれた判断・意思決定をRAGでは捕捉できないという問題意識から、「判断を覚える」記憶システムを設計・本番運用した事例。RAGが保存済み文書を検索するのに対し、本設計は会話中の判断（例:「認証はSupabase Authに決定」）を抽出・蓄積し、矛盾を自動検出する。

アーキテクチャの核心は認知心理学に基づく4層メモリ階層（L0〜L3）。L0は日次の具体的判断（エピソード記憶）、L1は週次の傾向（意味記憶）、L2は月次のスキーマ、L3は年次のメタ認知に対応し、pg_cronで日次バッチ処理（睡眠時記憶整理の実装）を行う。

RAPTOR（再帰的階層要約・クラスタリング）とMem0（コンフリクト検出・マージ）を融合し、「圧縮しながら矛盾も追跡する」設計を実現。矛盾検出ではL0の新規トピックとL1の既存トピックをGINインデックスで高速照合し、4分類（contradiction/update/new_development等）で判定。矛盾は削除せず[矛盾あり]フラグを付与して共存させる（McCarthy (1980)の非単調推論に依拠）。

忘却設計はEbbinghausの忘却曲線を実装。検索のたびにaccess_countをインクリメントし、last_accessed_atが3ヶ月以上前かつaccess_count≤1の記憶は積極圧縮、access_count≥5は詳細維持。コスト制御として矛盾検出のLLM呼び出しを1日10回（MAX_CHANGE_DETECTION_CALLS=10）に上限キャップし定数時間に収束させる。

要約はGoogleのMapReduceパラダイムを応用。Map（軽量モデルで並列要約）→Reduce（上位モデルで統合）の2フェーズ構成。忠実性検証はLLM-as-Judge（Zheng et al., 2023）でfaithfulness_scoreを計算し品質モニタリングに使用。

検索はL3から降下するLevel-Down方式。スコアは「類似度×0.8+recency×0.2」でRecency Boostをかけた後、LLMリランキングで意図的関連性を補完。maxDepth=1〜3で抽象度を制御可能。

DBはSupabase（PostgreSQL+pgvector）。embeddingはHNSW（IVFFlatはデータ量少時に精度低下を実測で確認）、key_topicsはGIN配列インデックスで矛盾検出を高速化。Claude Code内部のDream Systemとの比較では、Dream Systemが「閉じた世界（Claudeのみ）」であるのに対し、本設計はClaude/Codex等ツール横断の「開いた世界」を前提とし、ベンダーロックインを回避する点が差別化要素。

## アイデア

- 「判断単位」での記憶抽出という概念：会話ログ全体でなく意思決定のみを抽出・蓄積することで、矛盾検出が実用的なコストで可能になる設計思想
- コスト制御を定数時間に収束させるアーキテクチャ：N²になりうる矛盾検出をGINインデックスによるトピックフィルタ＋1日10回キャップで定数化する手法
- 忘却をフィードバックループとして実装：access_countによる使用頻度追跡→[重要]タグ付与→Reduceプロンプトでの詳細維持という3段階の忘却制御ループ

## Yujiの取り組みへの示唆

監査エージェントは複数セッション・複数ツールにまたがって判断を積み重ねるため、「過去の監査判断との矛盾検出」はそのまま内部統制チェックの精度向上に直結する。LangGraphのワークフロー内にL0記憶抽出ノードを組み込み、pg_cron＋pgvectorで判断履歴を永続化する構成はPydanticモデルとの相性も良い。LLM-as-Judgeによるfaithfulness_scoreはRLAIF/LLM-as-judgeを研究中のYujiにとって監査エビデンスの品質スコアリングへの応用として参考になる。ツール横断の記憶設計（Claude/Codex等を横断）は、Deloitteのマルチエージェント監査システムにおける知識共有基盤として検討価値がある。

## 原文リンク

[RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）](https://zenn.dev/haboshi/articles/ai-memory-architecture-raptor-mem0)
