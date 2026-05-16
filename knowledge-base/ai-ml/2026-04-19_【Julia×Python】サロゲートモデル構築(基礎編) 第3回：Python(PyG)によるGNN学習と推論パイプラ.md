---
title: "【Julia×Python】サロゲートモデル構築(基礎編) 第3回：Python(PyG)によるGNN学習と推論パイプライン"
url: "https://zenn.dev/kohmaruworks358/articles/phase1-python-training"
date: 2026-04-19
tags: [GNN, PyTorch Geometric, GCNConv, サロゲートモデル, Julia, PyG, 物理シミュレーション, グラフ学習, MSELoss, 0-based Contract]
category: "ai-ml"
related: [1482, 370, 501, 687, 746]
memo: "[Zenn 機械学習] 【Julia×Python】サロゲートモデル構築(基礎編) 第3回：Python(PyG)によるGNN学習と推論パイプライン"
processed_at: "2026-04-19T12:23:44.585439"
---

## 要約

本記事は、物理シミュレーション（1次元ばね–質量系）をグラフニューラルネットワーク（GNN）で近似するサロゲートモデル構築シリーズの第3回。Julia側で生成したJSONデータをPython/PyTorch Geometric（PyG）で読み込み、2層GCN（Graph Convolutional Network）を用いてノード単位の回帰学習を行うパイプラインを実装する。

データ連携の核心は「0-based Contract」：Julia（1-based インデックス）でエクスポートする際に辺の端点インデックスを0-basedへ変換し、Python側では補正不要とする取り決め。これにより境界での都度補正が不要となり、再現性とコードレビューコストが低減する。JSONから`torch_geometric.data.Data`への復元は`catlab_json_to_data`関数が担い、`edge_index`を`torch.long`（int64）、`data.x`/`data.y`を`float32`へキャストする。

モデル構造は`TwoLayerGCN`（`torch.nn.Module`）：第1層`GCNConv`（in=2, hidden=16）→ReLU→第2層`GCNConv`（hidden=16, out=2）。数式では H¹ = σ(GCNConv₁(X, E))、Ŷ = GCNConv₂(H¹, E) と表現される。損失関数はMSELoss、最適化はAdam（lr=0.02）、100エポック学習。教師データyはJulia側でDifferentialEquations.jlにより数値積分した終端状態（t=t₁時点の位置・速度）。

可視化・デバッグの指針として、損失が下がらない場合はモデル容量や学習率より先に、予測対象時刻t₁・ばね定数と質量の比k/m・初期条件の物理設定を確認することを推奨している。

Phase 1の限界として「単一固定トポロジ（チェーン）」「単一相互作用（ばね）」前提を明示し、Phase 2では Catlab.jl の応用圏論（ACT）でエッジ種別を厳密に定義し、Heterogeneous GNN（Hetero GNN）へ拡張予定。監査エージェント開発への示唆として、異種グラフ（Hetero GNN）の設計パターンは、監査ワークフロー内でリスク・コントロール・証跡等の異なる種類のノード/エッジを扱うマルチエンティティグラフ表現に直接応用可能。

## アイデア

- Julia（1-based）とPython（0-based）のインデックス差異を「0-based Contract」としてJSONエクスポート時に一度だけ吸収する設計思想は、異言語間データ連携の再現性保証パターンとして汎用性が高い
- 物理シミュレーションのグラフ表現でedge_indexを「メッセージ経路の台帳」として固定し、学習対象を畳み込み重みのみに限定する設計が、サロゲートモデルの構造的解釈を容易にする
- Phase 2でのHetero GNN拡張（ばね・ダンパ等の異種エッジ）は、監査システムにおけるリスク・コントロール・証跡等の異種エンティティを扱うグラフ設計に直接応用可能

## 前提知識

- **GCN / GCNConv** (TODO: 読むべき)
- **PyTorch Geometric** (TODO: 読むべき)
- **メッセージパッシング** (TODO: 読むべき)
- **常微分方程式数値積分** (TODO: 読むべき)
- **グラフ表現学習** → /deep_1100 ホモフィリー考慮型教師あり対照的反事実データ拡張による公平グラフニューラルネットワーク

## 関連記事

- /deep_1482 部分観測下における制御指向原子炉熱水力予測のためのグラフニューラルODEデジタルツイン
- /deep_370 設計段階でのスパース化によるクロスモダリティ予測：信頼性と効率的学習のためのL0ゲート表現
- /deep_501 設計によるスパース性を持つクロスモダリティ予測：信頼性と効率的学習のためのL0ゲーテッド表現
- /deep_687 疎学習による分枝戦略の改善で混合整数計画ソルバーを高速化
- /deep_746 疎学習による分岐決定の高速化：混合整数計画ソルバーへのML適用

## 原文リンク

[【Julia×Python】サロゲートモデル構築(基礎編) 第3回：Python(PyG)によるGNN学習と推論パイプライン](https://zenn.dev/kohmaruworks358/articles/phase1-python-training)
