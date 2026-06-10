---
title: "TabM入門：Deep Ensembleを1つのMLPに詰め込む、テーブルデータ向けNNの新定番"
url: "https://zenn.dev/mkawa_pani/articles/e10d91c60dd7d5"
date: 2026-06-10
tags: [TabM, Deep Ensemble, BatchEnsemble, テーブルデータ, MLP, RealMLP, アンサンブル学習, 数値Embedding]
category: "ai-ml"
related: [1429, 113, 2698, 6642, 7518]
memo: "[Zenn 機械学習] TabM入門：Deep Ensembleを1つのMLPに詰め込む、テーブルデータ向けNNの新定番"
processed_at: "2026-06-10T21:16:45.398821"
---

## 要約

TabMは、Yandex Researchが提案したテーブルデータ向けニューラルネットワークで、Deep Ensembleの予測精度をパラメータ効率よく1つのモデルに内包する設計が特徴。通常のDeep Ensembleはk個のMLPを独立に学習するためコストがk倍になるが、TabMはBatchEnsembleの発想を採用し、大きな重み行列Wをサブモデル間で共有しつつ、各サブモデルiにはd次元の小さなベクトルr_iとs_iのみを持たせる。具体的には各層の演算がl_i(x) = s_i ⊙ W(r_i ⊙ x) + b_iとなり、メンバーごとの追加パラメータはO(3d)で済む。d=512の場合、完全分離なら1層あたり約26万パラメータ増えるところが約1,500で済む。TabMはMLP Ensemble→TabM packed→TabM naive→TabM mini→TabM（最終形）という段階的な改良の流れで設計されており、最終形では初期化を工夫し、最初のアダプター以外を1に近い値から始めることでTabM miniに近いシンプルな状態からスタートし、学習が進むにつれて各層のアダプターが動く構造を採る。TabM miniは入力変換のみをサブモデルごとに変化させる極限まで削ぎ落とした構成で、実践上は通常のTabMと同等以上の性能を示す場面もある。強さの源泉は2つあり、一つはアンサンブル全体の出力を見ながら同時学習できること（個々のbest epochではなく平均予測としてのbest epochを選べる）、もう一つは重み共有が強い正則化として過学習を抑えること。出力はshape(batch_size, k, output_dim)でk方向に平均して最終予測を得る。数値特徴量のEmbedding（Piecewise Linear EmbeddingsやPeriodic Embeddings）との組み合わせでさらに性能が向上する場合がある。RealMLPが単体MLPを前処理・活性化関数・初期化・学習スケジュールで徹底強化するのに対し、TabMはアンサンブルを効率的に内包する構造的アプローチであり、誤差の出方が異なるため両者のアンサンブルも有効とされる。監査エージェント開発における示唆として、TabMの「大部分の表現を共有しつつ小さな差分で多様性を生む」という設計思想は、複数の判断ヘッドを持つエージェントや、同一バックボーンから複数の監査観点を出力するマルチタスクモデルの設計に応用できる可能性がある。

## アイデア

- BatchEnsembleによりメンバーごとの追加パラメータをO(3d)に抑えつつDeep Ensembleと同等の多様性を実現する重み共有の構造は、複数の判断基準を持つ監査エージェントの効率的な実装パターンとして参考になる
- TabM miniの実験結果として「入力変換のみ変えるだけで十分な多様性が生まれる」という知見は、テーブルデータにおける特徴量スケールの重要性を示しており、特徴量エンジニアリングの設計指針として有用
- アンサンブル全体の損失を見ながら同時学習する（TabM packed以降の設計）ことで個々のbest epochではなく平均予測としてのbest epochを最適化できる点は、マルチヘッド出力を持つモデルの学習戦略として汎用的に応用できる

## 前提知識

- **Deep Ensemble** → /deep_6528 クロスバリデーションはDeep Ensembleではない：不確実性推定における落とし穴
- **BatchEnsemble** (TODO: 読むべき)
- **MLP** → /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- **テーブルデータ向けNN** (TODO: 読むべき)
- **RealMLP** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_2698 説明可能な金融不正検知のためのShapley値ガイド型適応アンサンブル学習と米国規制コンプライアンス検証
- /deep_6642 言語切り替えトリガーはLLM内部で潜在的な迂回路を通る：バックドア回路の解析
- /deep_7518 表形式データ拡張手法 part17：SMOTEBoost

## 原文リンク

[TabM入門：Deep Ensembleを1つのMLPに詰め込む、テーブルデータ向けNNの新定番](https://zenn.dev/mkawa_pani/articles/e10d91c60dd7d5)
