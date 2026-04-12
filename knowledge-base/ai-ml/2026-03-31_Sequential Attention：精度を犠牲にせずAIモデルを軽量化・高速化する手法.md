---
title: "Sequential Attention：精度を犠牲にせずAIモデルを軽量化・高速化する手法"
url: "https://research.google/blog/sequential-attention-making-ai-models-leaner-and-faster-without-sacrificing-accuracy/"
date: 2026-03-31
tags: [Sequential Attention, subset selection, feature selection, model pruning, sparsification, greedy algorithm, NP-hard, Orthogonal Matching Pursuit, embedding dimension tuning, Google Research]
category: "ai-ml"
memo: "[Google AI Blog] ​Sequential Attention: Making AI models leaner and faster without sacrificing accuracy"
processed_at: "2026-03-31T12:05:51.372217"
---

## 要約

GoogleリサーチのThomas FuとKyriakos Axiotisが提案するSequential Attentionは、大規模MLモデルの効率化に向けたサブセット選択アルゴリズム。特徴量選択・埋め込み次元チューニング・重みプルーニングなど、多くのML最適化タスクを「サブセット選択問題」として統一的に扱える汎用フレームワークである。

サブセット選択はNP困難問題であり、従来の貪欲法は各ステップで全候補を再評価・再学習する必要があり計算コストが高かった。Sequential Attentionはこの問題を、Attentionメカニズムを用いた逐次的な意思決定プロセスとして定式化することで解決する。具体的には、既に選択済みの候補群をコンテキストとして使いながら、各ステップで最も重要な次の候補（最高Attentionスコアの特徴量）を追加していく。このスコア計算はモデル訓練プロセスに組み込まれており、追加コストを最小化している。

特徴量選択への応用では、Attentionスコアを「周辺利得（marginal gain）」の代替プロキシとして使用し、1回のforward passで効率的な貪欲選択を実現。線形回帰に適用した場合、数学的にOrthogonal Matching Pursuit（OMP）と等価であることが証明されており、理論的な信頼性も確保されている。プロテオミクス・画像・行動認識のベンチマークで最先端の精度を達成。

ブロックスパース化（SequentialAttention++）では、微分可能プルーニング（学習可能なパラメータを重要度プロキシとして使用）と組み合わせ手法（最適なスパース構造を探索するアルゴリズム）を統合。ブロック単位でゼロ化することでハードウェアの行列演算アクセラレーションを活用でき、非構造化プルーニングよりも推論性能が優れる。Google Adsの本番システム（数十億パラメータ規模）に適用し、モデルサイズを削減しながら精度を維持することを実証。

主要な利点は三点：①並列処理によるスコア計算の効率化、②Attentionスコアによるモデル内部の解釈可能性、③大規模候補数へのスケーラビリティ。

## アイデア

- Attentionスコアを「周辺利得の安価なプロキシ」として使うアイデアは、再学習なしに貪欲選択を1パスで実現するという発想の転換であり、他の組み合わせ最適化問題への応用可能性が広い
- 微分可能手法と組み合わせ最適化を統合（SequentialAttention++）するアプローチは、両者の長所を活かしつつ短所を補う設計思想として参考になる
- 線形モデルでのOMP等価性の証明という理論的保証が、実用的なヒューリスティックに数学的根拠を与えており、アルゴリズムの信頼性評価の方法論として示唆がある
## 関連記事

- /deep_248 研究ブレークスルーと実世界応用の「マジックサイクル」加速：Google Research最新成果
- /deep_191 Generative UI: あらゆるプロンプトに対応するリッチでカスタムなビジュアル・インタラクティブUX
- /deep_167 GIST：データ多様性と有用性を同時最大化するスマートサンプリングの新アルゴリズム
- /deep_190 EVの充電ポート空き予測：シンプルな線形回帰モデルによるレンジ不安の軽減

## 原文リンク

[Sequential Attention：精度を犠牲にせずAIモデルを軽量化・高速化する手法](https://research.google/blog/sequential-attention-making-ai-models-leaner-and-faster-without-sacrificing-accuracy/)
