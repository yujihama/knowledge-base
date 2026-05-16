---
title: "ベクトルDB比較（TiDB/Chroma/Pinecone）：ローカルLLMコードレビューRAGへの適用実験"
url: "https://zenn.dev/hakaru/articles/tidb-rag-code-review-vector-comparison"
date: 2026-05-15
tags: [RAG, ベクトルDB, TiDB, ChromaDB, Pinecone, bge-large, HNSW, コードレビュー, ローカルLLM, Ollama]
category: "ai-ml"
related: [5027, 4177, 4325, 4176, 4029]
memo: "[Zenn LLM] ローカルLLMって本当に開発に使える？（番外編）ベクトルDB比較、TiDB/Chroma/Pinecone"
processed_at: "2026-05-15T09:06:56.348651"
---

## 要約

M3 Ultra（96GB）+ Ollama環境でSwift/MIDIプロジェクトのコードレビュー自動化を進めるシリーズの番外編。Claude・Codex・Geminiの合議で蓄積した421件のレビュー事例をRAGのデータソースとして活用し、TiDB Serverless・ChromaDB・Pinecone Serverlessの3種類のベクトルDBを実条件で比較した。

エンベディングモデルはbge-large（1024次元）を使用。diff入力の512トークン制限に対して1200→800→500→300文字と段階的にトランケーションするリトライ戦略で対処。類似diff上位2件のsynthesized_reviewをプロンプト先頭に注入し、llama3.3:70b-m2lora-v1がレビューを生成する構成。

20件のコミットを対象にした比較結果：RAGなしの平均スコア4.27に対し、TiDB +1.03（5.30）、Chroma +1.50（5.77）、Pinecone +1.60（5.87）。Pineconeが数値上最良だがサンプル20件では誤差範囲。ChromaDBはpip install後3行で動作し、セットアップコストがほぼゼロで最も実用的。TiDB ServerlessはHNSWインデックスを持つがANN検索とWHEREフィルタの同時使用が不可という制約があり、フィルタなしで多めに取得後にPython側で処理する回避策が必要。

TiDB固有機能として「品質重み付きRAG」を実験。weighted_dist = dist / avg_scoreでSQLワンクエリによる類似度×品質の複合ランキングを実装。10件での比較では生距離平均6.25に対し重み付き5.70と逆効果。仮説として「スコアが高いレビュー＝典型的な整ったコードへのレビュー」であり、今の差分と文脈が合わない事例を引き込むリスクがある。「品質が高い事例が参考になる」より「文脈が近い事例が参考になる」の方がRAGでは優位という結果。

逆効果ケースとして9fd81f6（NaNガード追加、ノーRAG 7.33→TiDB 3.67）でも確認：注入されたレビューが「isFNaN チェックのオーバーヘッド」に関するもので完全に無関係な内容だった。元から高スコアなdiffへのRAG注入はノイズ化しやすい傾向も判明。

監査エージェント開発への示唆：RAGの品質評価軸として「類似度」と「参照事例の品質」を混在させると文脈ズレが生じやすい。LangGraphベースのレビューパイプラインでも、過去事例をRAGに使う際はシンプルなベクトル類似度検索の方が複合スコアより安定する可能性がある。

## アイデア

- 品質重み付きRAG（dist/avg_score）は直感に反して純粋な類似度検索より精度が低下した：「高品質な参照事例」と「文脈が合う参照事例」は一致しないことが実験で示された
- TiDB ServerlessのHNSWはANN検索とWHEREフィルタの同時使用が不可という制約があり、SQL統合の強みを活かすにはフルスキャン型クエリへの切り替えが必要になる設計上のトレードオフ
- bge-largeの512トークン制限をリトライ戦略（1200→800→500→300文字）で動的に回避するパターンは、エンベディングAPIのエラーハンドリングとして汎用的に応用できる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ベクトル類似度検索** (TODO: 読むべき)
- **HNSW** → /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）
- **bge-large** (TODO: 読むべき)
- **コサイン距離** (TODO: 読むべき)

## 関連記事

- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_4325 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第6回・完結）── ハルシネーションを4段ロケットで削る話
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4029 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤

## 原文リンク

[ベクトルDB比較（TiDB/Chroma/Pinecone）：ローカルLLMコードレビューRAGへの適用実験](https://zenn.dev/hakaru/articles/tidb-rag-code-review-vector-comparison)
