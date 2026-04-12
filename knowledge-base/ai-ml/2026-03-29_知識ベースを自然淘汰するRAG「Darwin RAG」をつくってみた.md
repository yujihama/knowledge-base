---
title: "知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた"
url: "https://zenn.dev/midomo/articles/14ca85959aa1cc"
date: 2026-03-29
tags: [RAG, Thompson Sampling, XCS, 進化計算, LLM-as-judge, 知識ベース自動更新, Gemini]
category: "ai-ml"
memo: "[Zenn LLM] 知識ベースを自然淘汰するRAGをつくってみた"
processed_at: "2026-03-29T21:57:51.181899"
---

## 要約

Thompson Sampling + LLM による突然変異・交差・淘汰を用いて、RAGの知識ベース（ルール集）を自動進化させる「Darwin RAG」の実装報告。XCS（Extended Classifier System）の枠組みをLLMで再実装した形で、1,900回以上の実験で進化なしと比べて+11〜18ppの正答率向上を確認。特筆すべきはV字回復実験で、API仕様変更によりルールが全て陳腐化した場合でも自力回復し、静的なStaleルール使用時（正答率1%）を大幅に上回る87%を達成した。依存ライブラリはgoogle-genaiのみ、知識ベースはJSONファイル1枚で構成。主要な知見として「間違ったルールは知識がない状態より有害」「モデル固有の失敗パターンはドメイン知識より重要な場合がある」「Mutationが主効果（+10pp）でCrossoverは補助的（+1.1pp）」の3点を挙げている。

## 要点

- 古いRAGルールはルールなしより正答率を下げる（1% vs 69%）——知識ベースの鮮度管理は監査AIでも死活問題
- LLMによるMutationはXCSのビット操作より少ない世代で意味的に有効なルール更新が可能（3世代で局所ルール→汎用原則）
- 報酬をSandbox Pass/Failに限定することで自己評価バイアスを排除でき、軽量構成（JSON+API）での自律進化ループが成立する
## 関連記事

- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成
- /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）
- /deep_49 MARCH: LLMハルシネーション検出のためのマルチエージェント強化自己チェックフレームワーク
- /deep_260 Learn Your Way: 生成AIによる教科書の再構想

## 原文リンク

[知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた](https://zenn.dev/midomo/articles/14ca85959aa1cc)
