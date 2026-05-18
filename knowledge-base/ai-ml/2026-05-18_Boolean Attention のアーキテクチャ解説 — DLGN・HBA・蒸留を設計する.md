---
title: "Boolean Attention のアーキテクチャ解説 — DLGN・HBA・蒸留を設計する"
url: "https://zenn.dev/karumaru/articles/95f90906023133"
date: 2026-05-18
tags: [Boolean Attention, DLGN, Transformer, 知識蒸留, Straight-through Estimator, Speculative Decoding, 量子化, Perplexity, PyTorch, bilinear attention]
category: "ai-ml"
related: [113, 5761, 861, 4181, 4044]
memo: "[Zenn 機械学習] Boolean Attention のアーキテクチャ解説 — DLGN・HBA・蒸留を設計する"
processed_at: "2026-05-18T09:10:20.941908"
---

## 要約

本記事は、論理ゲートのみで言語モデルを構築し、Transformer（PPL 4.86）を上回るPPL 4.73を達成した「Boolean Attention（HBA）」の設計思想とアーキテクチャを解説したコード解説記事である。

核心的な設計原則は「Boolean量子化を深さ方向に伝播させない」こと。Transformerのattentionを「どの位置を見るか（routing）」と「V の加重平均（value aggregation）」の2ステップに分解し、離散化と相性の良いroutingだけにBoolean演算を適用する。value aggregationはfloat演算のまま維持することで、離散誤差を各レイヤー内に局所閉じ込めし、深さ方向への誤差爆発を構造的に防ぐ。

DLGN（Deep Differentiable Logic Gate Network）は、2入力ブール関数の全16種類のゲートをsoftmaxで混合することで勾配を流す。学習中はαが連続値として機能し、学習後にargmaxで1つのゲートに確定（hard collapse）。入力ペア選択も同様にsoftmaxで学習し、温度パラメータτにより学習初期（τ=1.0）から後期（τ→0.1）にかけてハードな離散化へと収束させる。

HBAのrouterはQK^Tの内積ではなく、Q·W_router·K^Tのbilinear形式を採用。bilinearは「QがXという特性を持つ時、KのYに注目する」という構造的なルールを学習できる点で、Boolean判断との相性が良い。w_routerにはspectral normを適用し、Lipschitz定数を1以下に抑えることで訓練の安定性を確保。訓練時はtanh(logits/τ)で連続近似し、推論時はsign(logits)で離散化するstraight-through estimator（Bengio 2013）を採用する。

温度スケジュールは「warm_hold」パターン：初期5エポックはτ=1.0でQ/K/V表現を育て、中期はτ=0.5でhold、後期にτ→0.1へdecay。最初から離散化を開始するとQ/K/Vが育つ前にrouter選択が固定されてしまう問題を回避する。

知識蒸留はHintonら（2015）の手法に基づき、α=0.3、T=8のハイパーパラメータで実装。教師（Transformer）と生徒（HBA）はアーキテクチャが完全に異なるが、出力語彙（vocab=61）上の確率分布が同一のため蒸留が成立する。born-again蒸留（Furlanello 2018）として機能し、教師のソフトラベルがデータオーグメンテーションの役割を果たしてPPL 4.73を実現。

実装上の重要な教訓として、訓練eval時と最終比較時でτが異なると「4.71 vs 8.72」という乖離が生じるバグが報告されており、評価条件は訓練条件と一致させる重要性が強調されている。応用先としてSpeculative Decodingのdraftモデル、エッジ推論（乗算不要なAND/OR演算）、電力制約環境での軽量LMが挙げられている。監査エージェント開発への示唆として、boolean routerの軽量・高速特性はリソース制約下でのエージェント推論コンポーネントに転用できる可能性がある。

## アイデア

- Boolean量子化の誤差を『深さ方向に伝播させない』ために、routingのみBoolean化しvalue aggregationをfloatに残すという局所閉じ込め設計は、量子化全般における誤差制御の設計パターンとして汎用的に応用できる
- 全16種類の2入力論理ゲートをsoftmaxで混合して微分可能にするDLGNのアプローチは、離散的な選択空間を連続緩和する手法として、強化学習のアクション選択や離散構造探索にも転用できる
- 温度パラメータτの『warm_hold』スケジュール（表現学習→hold→離散化）は、表現空間が成熟してから離散構造を固定するという汎用的な学習順序の原則を示しており、VQ-VAEや離散コードブック学習にも適用できる視点

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **知識蒸留** → /deep_2424 エンタープライズAIをオペレーティングレイヤーとして扱う：Ensembleが示す構造的優位性
- **Straight-through Estimator** (TODO: 読むべき)
- **Spectral Normalization** (TODO: 読むべき)

## 関連記事

- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_4181 投機的デコーディングはなぜ速いのか？トイモデルで検証する
- /deep_4044 多肉植物LMを育てる (1) — データセットの作成とモデル訓練まで

## 原文リンク

[Boolean Attention のアーキテクチャ解説 — DLGN・HBA・蒸留を設計する](https://zenn.dev/karumaru/articles/95f90906023133)
