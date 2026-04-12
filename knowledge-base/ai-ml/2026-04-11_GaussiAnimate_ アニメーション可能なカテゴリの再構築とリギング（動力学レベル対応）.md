---
title: "GaussiAnimate: アニメーション可能なカテゴリの再構築とリギング（動力学レベル対応）"
url: "https://tldr.takara.ai/p/2604.08547"
date: 2026-04-11
tags: [3DGaussian, 4D再構築, リギング, アニメーション, 非剛体変形, MotionMatching, スケルトン抽出, NeRF代替]
category: "ai-ml"
memo: "[HF Daily Papers] GaussiAnimate: Reconstruct and Rig Animatable Categories with Level of Dynamics"
related: [1347]
processed_at: "2026-04-11T21:21:45.028882"
---

## 要約

GaussiAnimateは、4Dガウシアン表現を用いて動的な物体・キャラクターを再構築し、直感的に制御可能なアニメーション用リグを自動生成するフレームワークである。中核技術は「Skelebones（スケルボーンズ）」と呼ばれるScaffold-Skinリギングシステムで、3段階のパイプラインで構成される。

第1段階「Bones」では、時間的に一貫した変形可能ガウシアン（Deformable Gaussians）を自由形状ボーンに圧縮し、非剛体（non-rigid）な表面変形を近似する。従来の骨格ベース手法と異なり、形状表面に密着した自由形状ボーンを使うことで、皮膚や布などの複雑な局所変形も精密に捉えられる。

第2段階「Skeleton」では、カノニカルガウシアンから平均曲率スケルトン（Mean Curvature Skeleton）を抽出し、時系列方向に精錬することで、カテゴリ非依存・モーション適応型・トポロジー正確な運動学的構造を生成する。この骨格は特定キャラクタークラスに依存せず、動きのパターンに応じて適応的に構築される点が特徴的である。

第3段階「Binding」では、PartMM（Partwise Motion Matching）と呼ばれる非パラメトリックな部位別モーションマッチングにより、スケルトンとボーンを結合する。既存モーションの照合・検索・ブレンディングによって新規ボーンモーションを合成するため、少量データ（約1,000フレーム）でも高い汎化性を発揮する。

定量評価では、未見ポーズへの再アニメーション性能においてLinear Blend Skinning（LBS）比でPSNR+17.3%、Bag-of-Bones（BoB）比で+21.7%の改善を達成。PartMMアルゴリズムは低データ環境でもRMSEをLBS比48.4%削減し、GRUおよびMLPベースの学習手法を20%以上上回った。ガウシアン表現とメッシュ表現の双方に適用可能で、コードはcookmaker.cn/gaussianimateで公開予定。

## アイデア

- 自由形状ボーンと運動学的スケルトンを分離して設計する「Scaffold-Skin」の二層構造が、表現力と制御性のトレードオフを巧みに解決している点
- PartMM（部位別モーションマッチング）が非パラメトリックな検索・ブレンディングで低データ汎化を実現しており、データ不足環境での実用性が高い設計思想
- 「Level of Dynamics」という概念で4D形状の動力学的情報を圧縮・階層化するフレームワークは、時系列データの構造化表現として他分野への応用可能性がある

## 関連記事

- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[GaussiAnimate: アニメーション可能なカテゴリの再構築とリギング（動力学レベル対応）](https://tldr.takara.ai/p/2604.08547)
