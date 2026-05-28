---
title: "【全5回】Graph Neural Networks入門と最前線——GCNの基礎から創薬・不正検知の産業応用まで"
url: "https://zenn.dev/salt2/articles/gnn-introduction-series"
date: 2026-05-28
tags: [GNN, GCN, GraphSAGE, GAT, PyTorch Geometric, Graph Transformer, 不正検知, 創薬, 知識グラフ, WLテスト]
category: "ai-ml"
related: [3910, 5410, 758, 2325, 5826]
memo: "[Zenn 機械学習] 【全5回】Graph Neural Networks入門と最前線——GCNの基礎から創薬・不正検知の産業応用まで"
processed_at: "2026-05-28T09:10:44.504411"
---

## 要約

本シリーズはGraph Neural Networks（GNN）を「理論・実装・業務応用」の三軸で体系的に解説した全5回構成のZenn Booksである。

第1回では、なぜ既存のMLでグラフを扱えないかという問いから出発し、非ユークリッド構造・可変サイズという制約を整理した上で、スペクトラルグラフ理論→ラプラシアン行列→チェビシェフ近似→GCN（Kipf & Welling, ICLR 2017）という導出を丁寧にトレースしている。ノード分類・グラフ分類・リンク予測の主要タスクの全体像もここで掴める。

第2回では、GCNが抱えていた「大規模グラフへのスケール困難」「隣接ノードの重み付け不能」という問題に対し、GraphSAGE（Hamilton et al., NeurIPS 2017）・GAT（Veličković et al., ICLR 2018）・MPNN（Gilmer et al., ICML 2017）がそれぞれどう解決したかを比較し、手法選択の指針を示している。

第3回は実装特化の回で、PyTorchのAutograd（計算グラフの動的構築）を解説した上で、PyTorch GeometricのMessagePassing基底クラスを継承したGCN層をスクラッチ実装している。Coraデータセット（論文引用ネットワーク）でノード分類タスクを完全実装し、PyGの組み込みGCNConvとの比較も行う。

第4回は研究動向のキャッチアップ回で、Weisfeiler-Lehman（WL）同型テストによる表現力の理論的上限、Over-smoothing問題とDropEdge（Rong et al., ICLR 2020）による対策、Graph Transformer（Dwivedi et al., 2020）、GIN（Xu et al., ICLR 2019）、さらにGNN×LLM融合の潮流まで横断的に整理している。

第5回は業務応用で、不正検知（GraphConsis, Liu et al. 2020）・交通流量予測・創薬（GNN Drug Discovery Survey, Berry & Cheng 2025）・知識グラフ推論（R-GCN, Schlichtkrull 2018）の4ドメインを取り上げ、各ドメインでのグラフ定義方法・代表論文・実務課題を整理している。手法選択のための意思決定チェックリストも提供されており、「GNNを業務に使えるか判断したい」実務者に直接的に有用。

監査エージェント開発への示唆として、不正検知ドメイン（第5回）は特に関連が深い。取引ネットワークや組織間の資金フローをグラフとして定義し、GraphConsisのような手法で異常エッジ・ノードを検出するアプローチは、監査における異常仕訳検知や関連当事者取引の分析に直接応用可能である。

## アイデア

- WL同型テストによるGNNの表現力の理論的上限という概念：GNNが「区別できないグラフ」の存在を数学的に示し、GINはその上限に達する設計として提案されている点が理論的に興味深い
- Over-smoothingへのDropEdgeによる対処：深いGNNでノード表現が均質化する問題に対し、学習時にランダムにエッジを削除することで多様な近傍サンプリングを実現するアプローチは、Dropoutのグラフへのアナロジーとなっている
- 不正検知へのGraphConsis適用：不正ノードが正常ノードと意図的に接続することで検知を回避しようとするカモフラージュ問題に対し、隣接ノード間の特徴一貫性を考慮した集約を行う設計は、監査における関連当事者ネットワーク分析に直接転用可能

## 前提知識

- **GCN** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **PyTorch Geometric** → /deep_2325 【Julia×Python】サロゲートモデル構築(基礎編) 第3回：Python(PyG)によるGNN学習と推論パイプライン
- **スペクトラルグラフ理論** (TODO: 読むべき)
- **MessagePassing** (TODO: 読むべき)
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界

## 関連記事

- /deep_3910 【Julia×Python】サロゲートモデル構築(応用編) 第6回：学習ループ・評価と連載総括（GNN と PINN・MLP の比較）
- /deep_5410 推薦システム向け動的グラフ×類似度対応アテンションGNN（DG-SA-GNN）
- /deep_758 トークン1つで十分か？LLMベースのグラフQA向けグラフプーリングトークン
- /deep_2325 【Julia×Python】サロゲートモデル構築(基礎編) 第3回：Python(PyG)によるGNN学習と推論パイプライン
- /deep_5826 金融部門における先進AI技術の実装——ガバナンスより先行した導入がもたらす逆説

## 原文リンク

[【全5回】Graph Neural Networks入門と最前線——GCNの基礎から創薬・不正検知の産業応用まで](https://zenn.dev/salt2/articles/gnn-introduction-series)
