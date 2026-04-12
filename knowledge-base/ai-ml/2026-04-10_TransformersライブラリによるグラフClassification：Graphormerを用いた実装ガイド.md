---
title: "TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド"
url: "https://huggingface.co/blog/graphml-classification"
date: 2026-04-10
tags: [Graphormer, グラフTransformer, グラフ分類, HuggingFace Transformers, OGB, ogbg-molhiv, GNN, 分子グラフ, Trainer API]
category: "ai-ml"
memo: "[HF Blog] Graph Classification with Transformers"
related: [1482, 370, 501, 687, 746]
processed_at: "2026-04-10T12:09:56.261783"
---

## 要約

本記事は、HuggingFaceのTransformersライブラリを使ってグラフ分類タスクを実装する実践的チュートリアルである。現時点でTransformersに統合されているグラフTransformerモデルはMicrosoftのGraphormerのみであり、これを中心に解説している。

データはHugging Face Hub上のOGB（Open Graph Benchmark）リポジトリからStanfordの`ogbg-molhiv`データセット（分子グラフの HIV 活性二値分類）を`datasets`ライブラリで取得する。グラフデータの形式はJSONL形式で、各グラフは`edge_index`（隣接リスト形式の2並列整数リスト）、`num_nodes`（整数）、`y`（ラベル）、`node_feat`（ノード特徴量）、`edge_attr`（エッジ属性）の5フィールドで表現される。

前処理ではGraphormer専用の`preprocess_item`関数と`GraphormerDataCollator`を使い、ノードの入次数・出次数、ノード間最短経路行列などGraphormerが必要とする構造的特徴量を自動生成する。大規模グラフではストレージコスト軽減のため`on_the_fly_processing=True`でDataCollator内でのオンザフライ処理も可能。

モデルは`clefourrier/pcqm4mv2_graphormer_base`チェックポイントからファインチューニングし、`num_classes=2`と`ignore_mismatched_sizes=True`を指定して下流タスク用の分類ヘッドを差し替える。トレーニングはHugging FaceのTrainerAPIで行い、`per_device_train_batch_size=64`、`gradient_accumulation_steps=10`、`num_train_epochs=20`を設定。グラフデータはOOMを起こしやすいため`auto_find_batch_size=True`でバッチサイズ自動調整も有効化している。CPU（Intel Core i7）での学習は約1日かかる。

Graphormerのアーキテクチャ的特徴として、グラフ全体の表現を得るために特殊な「仮想ノード」をすべてのノードに接続して使う点、Transformerのアテンションバイアス項に空間エンコーディング（最短経路長）・エッジエンコーディング（エッジ属性の平均）・中心性エンコーディング（次数情報）を加算する点が挙げられる。これによりグラフ構造の大局的・局所的情報を同時にTransformerへ注入している。

## アイデア

- グラフ構造をTransformerのアテンションバイアスとして注入する設計（空間エンコーディング・エッジエンコーディング・中心性エンコーディングの加算）は、任意のグラフ構造化データを標準的なTransformerで扱う汎用的な方法論として応用できる
- 仮想ノード（全ノードと接続するスーパーノード）によるグラフ全体表現の取得は、エージェントシステムにおける「グローバルコンテキストノード」設計のアナロジーとして興味深い
- HuggingFaceのTrainer APIがグラフデータにも適用でき、OOMを自動回避する`auto_find_batch_size`やgradient accumulationとの組み合わせが実用的なスケーリング戦略を提供している
## 関連記事

- /deep_1482 部分観測下における制御指向原子炉熱水力予測のためのグラフニューラルODEデジタルツイン
- /deep_370 設計段階でのスパース化によるクロスモダリティ予測：信頼性と効率的学習のためのL0ゲート表現
- /deep_501 設計によるスパース性を持つクロスモダリティ予測：信頼性と効率的学習のためのL0ゲーテッド表現
- /deep_687 疎学習による分枝戦略の改善で混合整数計画ソルバーを高速化
- /deep_746 疎学習による分岐決定の高速化：混合整数計画ソルバーへのML適用

## 原文リンク

[TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド](https://huggingface.co/blog/graphml-classification)
