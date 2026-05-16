---
title: "化学データをDuckDBで扱えるようにする自作拡張機能「ducksmiles」を作った"
url: "https://zenn.dev/amana/articles/fb537174583854"
date: 2026-05-09
tags: [DuckDB, SMILES, RDKit, Rust, 化学データ, SELFIES, InChI, PDB, コミュニティ拡張機能, SQL前処理]
category: "infra"
related: [1936, 4406, 771, 971, 393]
memo: "[Zenn 機械学習] 化学データをDuckDBで扱えるようにする自作拡張機能を作った"
processed_at: "2026-05-09T09:39:33.995185"
---

## 要約

化学系データコンペの追試をきっかけに、DuckDBのコミュニティ拡張機能「ducksmiles」を開発した。Rustで実装されており、DuckDB上でSQLを使ってSMILES・InChI・PDB・CIF・XYZ等の化学データ形式を直接操作できる。

従来のRDKitはGoogle Colab上での動作不安定（ランタイム再起動が必要）、pandasバージョン競合、複数ツールとの連携が必要といった問題があった。ducksmilesはこれらの問題をDuckDB単体で解決する。

主な機能は5つ。①mol_formula()/mol_weight()によるSMILES→分子式・分子量の計算（公開CSV/Parquet/S3のHTTPS URLを直接read_csv_autoに渡してSQL1行で完結）。②inchi_formula()/inchi_connections()/inchi_hydrogens()によるInChI文字列の各層（分子式・結合・水素・電荷・立体）への直接分解（RDKitでは一度分子オブジェクトに変換が必要な処理を文字列のまま実行）。③smiles_to_selfies()/selfies_to_smiles()によるSMILES⇄SELFIES相互変換（RDKitでは別パッケージselfiesが必要な処理をDuckDB単体で完結）。④structure_atom_count()/structure_chain_count()/structure_residue_count()/structure_model_count()によるPDB構造ファイルのメタ情報集計（RCSB PDBのHTTPS URLを直接read_textに渡し、複数ファイルを一括集計可能）。⑤不正なSMILESや空文字が混在してもエラー停止せずNULLを返す設計で、数百万件規模のバッチ処理に対応。

DuckDBの標準機能（CSV/Parquet/Iceberg/S3/HTTPダイレクトURL）とそのまま接続できるため、データ取り込みから前処理まで単一ツールで完結できる。化学データの多フォーマット問題（SMILES、InChI、SDFなど）に対し、コミュニティエクステンション機構を活用してドメイン固有の処理をSQLで統合するアーキテクチャは、監査AIにおける異種データソース（XBRL、CSVログ、API出力等）の前処理パイプライン設計にも応用できる考え方。

## アイデア

- DuckDBのコミュニティエクステンション機構を使えば、ドメイン固有データ形式（化学・生物・地理等）をSQLに統合できる。監査領域でもXBRL・GL形式等をDuckDB拡張として実装する同様のアプローチが有効かもしれない
- 不正データをエラーではなくNULLで返す設計はバッチ処理の堅牢性に直結する。大量の非構造化データを扱う監査エージェントでも、パース失敗をNULL化して継続処理するパターンは重要
- InChIの各層（formula/connections/hydrogens/charge/stereo）をSQL関数で直接分解する設計は、複合フォーマットの文字列を構造化する汎用パターンとして応用可能。JSONやXMLの部分抽出と同様の概念

## 前提知識

- **DuckDB** → /deep_904 Hugging Face HubでオープンなMLデータセットを共有する方法
- **SMILES記法** (TODO: 読むべき)
- **RDKit** → /deep_145 MolEvolve: 解釈可能な分子最適化のためのLLM誘導型進化探索
- **InChI** (TODO: 読むべき)
- **SELFIES** (TODO: 読むべき)

## 関連記事

- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法
- /deep_4406 化学者のための機械学習：XGBoostによる分子物性予測パイプライン（モデル評価・重要特徴量把握）
- /deep_771 チャンクからブロックへ：Hugging Face Hubにおけるアップロード・ダウンロードの高速化
- /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- /deep_393 OpenAI、PythonツールチェーンメーカーのAstralを買収へ

## 原文リンク

[化学データをDuckDBで扱えるようにする自作拡張機能「ducksmiles」を作った](https://zenn.dev/amana/articles/fb537174583854)
