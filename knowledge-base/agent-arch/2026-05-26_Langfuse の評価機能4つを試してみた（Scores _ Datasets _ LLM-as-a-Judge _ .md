---
title: "Langfuse の評価機能4つを試してみた（Scores / Datasets / LLM-as-a-Judge / Annotation Queue）"
url: "https://zenn.dev/mochitec_tech/articles/90642b81ff5726"
date: 2026-05-26
tags: [Langfuse, LLM-as-a-Judge, LLMOps, evaluation, Annotation Queue, Datasets, Scores, 観測基盤]
category: "agent-arch"
related: [3136, 3096, 5462, 1615, 6557]
memo: "[Zenn LLM] Langfuse の評価機能4つを試してみた"
processed_at: "2026-05-26T21:00:39.260157"
---

## 要約

LangfuseはLLMアプリの評価・観測基盤（LLMOps）であり、本記事はそのUI上で使える評価機能4つを実際に操作したレポートである。

**Scores**：trace・observationに紐づく評価結果の共通フォーマット。数値・分類値を格納し、書き込み元に応じてSourceフィールドがAPI/EVAL/ANNOTATIONの3種類に自動付与される。Scoresタブから横断フィルタ・集計が可能だが、UIから直接手入力はできず、人間ラベルはAnnotation Queue経由、外部値はSDK/API経由で書き込む必要がある。

**Datasets**：繰り返し評価に使う入力セットを固定する機能。本番traceからの生成とUIでの直書きの2パターンがあり、各itemはinput・expected_output・metadataの3フィールドを持つ。同一Datasetに対して条件を変えた複数runを実行するとdataset runsとして並列比較ビューに表示され、スコアの悪化項目が一目で特定できる。Prompt Experimentsを使えばコード不要でUIのみで実験が回せる。

**LLM-as-a-Judge（Evaluator）**：LLM自身に評価させる自動評価器。managedテンプレート（Hallucination、Helpfulness、Context-Relevance、Toxicityなど）とカスタムプロンプトの2種類を選べる。設定時にVariable mappingでテンプレート変数（{{query}}、{{generation}}等）とtraceのフィールドをJSONPathで対応付ける。保存後は新規データが入るたびに自動スコアリングが走る。Score AnalyticsではEvaluatorスコアと人間ラベルのPearson相関が表示され、例として Helpfulness と human_relevance の相関が 0.328（Weak）という数値が得られた。Variable mappingのJSONPath誤りでスコアが全件0になるつまずきポイントがあり、trace詳細のevaluator spanで入力内容を確認することでデバッグできる。

**Annotation Queue**：ドメインエキスパートによる人間ラベル収集キュー。事前にScore Config（名前・型・値域）をNUMERIC/CATEGORICAL/BOOLEAN/TEXTから選んで登録し、Queueと紐付けてアノテーターに割り当てる。Score Configを未登録のままQueue作成画面に進むと詰まる（既存からの選択のみで新規作成不可）という落とし穴がある。

監査エージェント開発への示唆：LangfuseのEvaluator＋Annotation Queueの組み合わせは、監査判断の自動評価と人間レビューの一致度測定に直接応用できる。LLM-as-judgeが付けた監査リスクスコアと審査担当者ラベルのPearson相関をScore Analyticsで継続モニタリングすることで、エージェントの判断品質を定量的に追跡できる。

## アイデア

- Scoreのsourceフィールド（API/EVAL/ANNOTATION）による書き込み元の自動区別により、同一メトリクスでも自動評価と人間ラベルを分離して集計・比較できる設計が巧み
- Variable mappingのJSONPath誤りで全件スコア0という無音の失敗が起きる点は、LLM評価パイプライン構築時の典型的なデバッグ困難箇所であり、evaluator spanで入力確認するデバッグ手順が参考になる
- Prompt Experimentsでコード不要の並列run比較が可能な点は、プロンプトA/Bテストを非エンジニアのドメインエキスパートにも開放できる可能性を示している

## 前提知識

- **Langfuse** → /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **trace / span** (TODO: 読むべき)
- **JSONPath** (TODO: 読むべき)
- **Pearson相関** → /deep_3314 HoWToBench：Tree of Writingを用いたLLMの人間レベル文章生成能力の包括的評価

## 関連記事

- /deep_3136 Langfuse v4 で LLM アプリを計測・改善する — Sessions / Users / Scores 実践ガイド
- /deep_3096 そのAIアプリはテストされているか：LLMアプリの自動テスト実践論
- /deep_5462 AIシステムを社内に導入するならLangfuseも一緒に入れておくべき理由
- /deep_1615 🤗 Datasetsにおける音声・画像データセット対応の新ドキュメント公開
- /deep_6557 論文メモ：LLMの文化・地域バイアスをCROQで測る

## 原文リンク

[Langfuse の評価機能4つを試してみた（Scores / Datasets / LLM-as-a-Judge / Annotation Queue）](https://zenn.dev/mochitec_tech/articles/90642b81ff5726)
