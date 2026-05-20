---
title: "LangGraphエージェントに3種類の記憶をTiDBで実装する──脅威インテリジェンスで学ぶSQL×ベクトル×全文検索"
url: "https://zenn.dev/12ban/articles/c26ce3079e226b"
date: 2026-05-20
tags: [LangGraph, TiDB, ベクトル検索, BM25, MITRE ATT&CK, IOC, TTP, 脅威インテリジェンス, RAG, sentence-transformers]
category: "agent-arch"
related: [5132, 9, 5769, 2739, 2605]
memo: "[Zenn 機械学習] LangGraphエージェントに3種類の記憶をTiDBで実装する──脅威インテリジェンスで学ぶSQL×ベクトル×全文検索"
processed_at: "2026-05-20T09:10:27.258100"
---

## 要約

LangGraphで構築したAIエージェントがセッション間で記憶を失う問題を解決するため、TiDB CloudのSQL・ベクトル検索・全文検索（BM25）を1つのDBに集約して3種類の永続記憶を実装する手法を紹介。脅威インテリジェンスの3ユースケース（IOC照合・TTP類似検索・脅威アクター調査）をそれぞれの記憶タイプに対応させている。

【Week1：エピソード記憶＝IOCのSQL完全一致検索】
IPアドレス・ドメイン・ファイルハッシュなどのIOC（侵害指標）は、完全一致で「あるかないか」を即座に判定する必要があるためSQLが最適。TiDB上にUNIQUE KEY付きのiocテーブルを作成し、pymysqlで`SELECT * FROM ioc WHERE value = %s`を1行叩くだけの検索関数をLangGraphのtoolとして登録。abuse.chやOSINTからのサンプルデータで185.220.101.1→TorExitNode、malware-c2.example.com→APT29-C2などを正確に返すことを確認。

【Week2：セマンティック記憶＝TTPのベクトル検索】
MITRE ATT&CKの公式JSON（約80MB）から697件のテクニックを取得し、`paraphrase-multilingual-MiniLM-L12-v2`（384次元、ローカル動作）でembeddingを生成してTiDBのVECTOR(384)型カラムに投入。`VEC_COSINE_DISTANCE`関数でコサイン類似度検索を実行。日本語クエリ「PowerShellを使った外部接続」が英語で記述されたT1059.001に類似度スコア0.812でヒットすることを確認。OpenAI APIのクォータ切れや英語専用モデル（all-MiniLM-L6-v2）の日本語精度不足を経験し、多言語対応モデルに切り替えた実装上のつまずきも記載。

【Week3：手続き記憶＝脅威アクターのBM25全文検索】
「Lazarus」検索時にLazarus Groupだけでなく関連グループ（Kimsuky、Andariel）も関連度順にヒットさせたいというニーズにBM25全文検索が対応。TiDBのFULLTEXT INDEXを活用したthreat_actorテーブルを設計。

【LangGraphへの統合】
3つの検索関数をtoolとして登録し、LangGraphのReActエージェントが入力に応じてIOC照合・TTP特定・アクター調査を自律的に選択・実行して脅威レポートを生成。pgvector＋Elasticsearch＋RedisのDB3本構成を1本のTiDB Cloudに集約することで、接続管理・スキーマ整合性・運用コストを削減できる点が本記事の主張。監査エージェントへの応用として、インシデントレポートのRAGやコントロールマッピングの類似検索に同様のアーキテクチャが転用可能。

## アイデア

- SQL・ベクトル検索・BM25全文検索を単一DBに集約し、検索特性の異なる3種類の記憶（エピソード・セマンティック・手続き）をLangGraphのtoolとして統一的に扱う設計は、監査エージェントのコントロール照合・リスク類似検索・規制文書検索にそのまま転用できる
- `paraphrase-multilingual-MiniLM-L12-v2`をローカル動作させることでAPIコスト・クォータ問題を回避しつつ、日本語クエリで英語コーパス（ATT&CK）にクロスリンガル検索できる点は、日本語監査基準と英語フレームワーク（COSO, COBIT）のマッピングへの応用が期待できる
- ReActエージェントが入力の性質（完全一致が必要か・意味検索が必要か・キーワード検索が必要か）を自律判断してtoolを選択する構造は、単一クエリタイプへの過適合を避けるマルチモーダル検索エージェントの実装パターンとして参考になる

## 前提知識

- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ベクトル検索** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **BM25** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **MITRE ATT&CK** → /deep_5658 オープンソースSIEMにおけるMITRE ATT&CK強化行動プロファイリングによるコンテキスト認識型Web攻撃検知

## 関連記事

- /deep_5132 RAGの精度を上げる：チャンキングとハイブリッド検索をGoで実装した記録
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_5769 長期LLMペルソナ一貫性のための異種時系列メモリガバナンスフレームワーク（ARPM）
- /deep_2739 制約の多い公共部門環境でAIを実用化する：SLMという選択肢
- /deep_2605 制約の多い公共セクター環境でAIを実用化する：SLMという現実解

## 原文リンク

[LangGraphエージェントに3種類の記憶をTiDBで実装する──脅威インテリジェンスで学ぶSQL×ベクトル×全文検索](https://zenn.dev/12ban/articles/c26ce3079e226b)
