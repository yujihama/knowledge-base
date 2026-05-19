---
title: "Cloud Natural Language API活用術：不適切ワードを自動ブロック"
url: "https://zenn.dev/e_agency/articles/78e1da8d6db59b"
date: 2026-05-19
tags: [Cloud Natural Language API, テキストモデレーション, Google Cloud, BigQuery, Cloud Run Functions, NLP, データパイプライン, コンテンツフィルタリング]
category: "infra"
related: [396, 1615, 1661, 1709, 1753]
memo: "[Zenn 機械学習] Cloud Natural Language API活用術：不適切ワードを自動ブロック"
processed_at: "2026-05-19T21:01:56.450550"
---

## 要約

Google CloudのCloud Natural Language APIを用いて、テキストデータ内の不適切ワードを自動検知・除外するデータパイプラインを構築する実装解説記事。企業データの約80%を占めるテキストデータ（顧客アンケート、口コミ等）には、スパムや誹謗中傷などのノイズが混入するリスクがあるが、従来のNGワード辞書による対策は隠語・造語への対応不能、過剰検知、運用負荷の高さという限界を抱えていた。本APIはGoogleの事前学習済みモデルをREST API経由で利用でき、感情分析・エンティティ分析・構文解析・コンテンツ分類・テキストモデレーションの5機能を提供する。テキストモデレーションは月間5万リクエストまで無料、以降は1リクエスト$0.0005と、LLMによる判定と比較して大幅に安価。実装シナリオとして、外部API（Yahoo DS Insight等）から取得した検索キーワードをBigQueryに格納する前処理として、Cloud Run FunctionsからAPIを呼び出し、Toxic・Sexual・Profanity等16カテゴリのスコア（0〜1）を取得し、閾値0.5以上のキーワードに除外フラグを付与する構成を解説。最適化として、2文字以下はAPIスキップ、20文字以上は無条件除外、time.sleep(0.1)でレート制限（1分600件）を回避するチューニングを紹介。さらにBigQuery リモート関数を用いてBigQuery内でSQL実行だけでAPIを呼び出す発展的アーキテクチャも実装例付きで解説しており、外部バッチ連携の運用負荷を排除できる。監査エージェント開発観点では、LLMを使わず特化型APIで低コスト・高スループットなデータ品質保証レイヤを構築する設計パターンは、監査ログや内部文書の自動スクリーニングにも応用可能。

## アイデア

- BigQueryリモート関数でSQL内からAPIを直接呼び出すパターンにより、ETLパイプラインの外部依存を排除しデータウェアハウス中心のアーキテクチャが実現できる
- 2文字以下スキップ・20文字以上無条件除外という事前足切りルールでAPIコストを削減しながらレート制限も同時に緩和する二段階フィルタ設計が実用的
- LLMではなく特化型モデレーションAPIを選択することで、トークンコストを大幅削減しつつ月間5万件無料枠内で中小規模ユースケースをゼロコスト運用できる

## 前提知識

- **REST API** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **Cloud Run Functions** (TODO: 読むべき)
- **BigQuery リモート関数** (TODO: 読むべき)
- **テキストモデレーション** (TODO: 読むべき)
- **従量課金モデル** (TODO: 読むべき)

## 関連記事

- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_1615 🤗 Datasetsにおける音声・画像データセット対応の新ドキュメント公開
- /deep_1661 機械学習ディレクターの洞察 第3回：金融業界編
- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）
- /deep_1753 機械学習の専門家インタビュー：Margaret Mitchell（倫理的AI研究の先駆者）

## 原文リンク

[Cloud Natural Language API活用術：不適切ワードを自動ブロック](https://zenn.dev/e_agency/articles/78e1da8d6db59b)
