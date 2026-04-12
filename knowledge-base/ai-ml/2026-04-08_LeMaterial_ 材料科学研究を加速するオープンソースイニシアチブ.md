---
title: "LeMaterial: 材料科学研究を加速するオープンソースイニシアチブ"
url: "https://huggingface.co/blog/lematerial"
date: 2026-04-08
tags: [materials-science, dataset, DFT, graph-hashing, Weisfeiler-Lehman, Hugging Face, open-source, AI4Science, Optimade, de-duplication]
category: "ai-ml"
memo: "[HF Blog] LeMaterial: an open source initiative to accelerate materials discovery and research"
processed_at: "2026-04-08T12:30:47.992642"
---

## 要約

LeMaterialは、EntalpicとHugging Faceが主導するオープンソースの協調プロジェクトで、材料科学研究におけるデータの断片化問題を解決することを目的としている。第一弾として公開されたデータセット「LeMat-Bulk」は、Materials Project・Alexandria・OQMDという主要な材料データベースを統合・クリーニング・標準化したもので、670万エントリ・7種の材料特性を持つ統一フォーマットのデータセットを実現した。ライセンスはCC-BY-4.0。

背景として、既存の材料データベースはフォーマット・パラメータ・スコープがそれぞれ異なり、AI4Scienceや材料情報学の研究者がデータを効果的に活用する際の障壁となっていた。例えばMaterials Projectは酸化物や電池材料（Li, O, P）に偏っており、NOMADは量子化学計算に特化していて材料特性を網羅しないといった課題があった。Optimadeによる構造データの標準化の試みはあるものの、材料特性の不一致やデータバイアスへの対処は不十分だった。

LeMat-Bulkの主要な技術的貢献は以下の通り。（1）データ統合：PBE・PBESol・SCANの3種のDFT汎関数を含む複数ソースからのデータ収集・マージ。（2）データクリーニング：非互換な計算結果を特定・除去。（3）Optimade標準に基づくフィールドの統一フォーマット化。（4）材料フィンガープリント：結晶構造にボンディングアルゴリズム（EconNN等）を適用してグラフを抽出し、Weisfeiler-Lehmanアルゴリズムでハッシュを計算。これに組成・空間群情報を組み合わせた一意識別子を各材料に付与することで、重複除去・新規性検出・データセット間のマッピングを高速化する。

データセットはCompatibility（混合可能な計算のみ）・Non-compatible・LeMat-BulkUnique（重複排除済み）の複数サブセットで提供される。v1.1（2025年Q1予定）ではEquiformerv2・FAENetの学習済みモデルや材料類似度メトリクスの追加を計画。v1.2以降ではOC20・OC22などの表面データセット、MPTrj・OMat24のトラジェクトリデータの統合も予定されている。可視化にはCrystal Toolkit・Pymatgen・Dash（Materials Project製）を活用したMaterials Explorer Spaceが提供されている。

## アイデア

- Weisfeiler-Lehmanアルゴリズムを結晶グラフに適用したハッシュによる材料フィンガープリントは、グラフ同型性判定を利用した高速な新規性検出手法として、他のドメイン（分子・化合物データベース）への応用可能性がある
- 異なるデータソース間のフォーマット・バイアス・計算互換性の不整合を体系的に解決したデータ統合パイプラインの設計は、マルチソースデータを扱う任意のAI4Scienceプロジェクトのリファレンスアーキテクチャになりうる
- 670万エントリの統一済みデータセット上でEquiformerv2・FAENetのような等変ニューラルネットワークを訓練し、基礎材料モデルを構築するアプローチは、大規模基盤モデルの材料科学版（Materials Foundation Model）の実現に向けた具体的な実装例となっている

## 原文リンク

[LeMaterial: 材料科学研究を加速するオープンソースイニシアチブ](https://huggingface.co/blog/lematerial)
