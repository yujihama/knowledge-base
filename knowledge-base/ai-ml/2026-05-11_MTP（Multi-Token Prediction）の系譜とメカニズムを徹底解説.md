---
title: "MTP（Multi-Token Prediction）の系譜とメカニズムを徹底解説"
url: "https://zenn.dev/acrosstudioblog/articles/ad05d752e3c038"
date: 2026-05-11
tags: [MTP, Multi-Token Prediction, Speculative Decoding, DeepSeek-V3, Blockwise Parallel Decoding, Teacher Forcing, 推論高速化, Causal Chain, vLLM]
category: "ai-ml"
related: [4297, 419, 1434, 902, 4181]
memo: "[Zenn LLM] MTP（Multi-Token Prediction）の系譜とメカニズムを徹底解説"
processed_at: "2026-05-11T09:41:48.883018"
---

## 要約

MTP（Multi-Token Prediction）は、従来のLLMが抱える「1ステップ1トークン生成」というメモリ律速ボトルネックを解消するアーキテクチャ手法。本記事はその歴史的系譜を3つの論文をたどりながら解説する。

【背景】Decoder-only LLMは推論時に毎ステップ、巨大パラメータのメモリ読み込み・KV-Cache更新・全層Forward passを繰り返すため、計算律速ではなくメモリ律速となる。MTPはこれを「1ステップ複数トークン生成」に転換することで解消する。

【Google BPD（2018, NIPS）】最初のマイルストーン。メインのDecoder-only Transformerに複数の予測ヘッド（Head_k）を接続し、k個の未来トークンを1回で生成→Verifyで正解との一致を並列検証→連続一致分をAcceptする3フェーズ方式。k=4のパイプライン化で理論上約4倍の推論高速化。ただし主眼は推論加速のみ。

【Meta MTP（2024, ICLR）】学習フェーズでの表現力向上と収束加速を主眼とする。共有Transformerバックボーンに独立したTransformer層（MHA+2層FFN）を持つ複数ヘッドを取り付け、1回のForward passで複数位置のLossを計算してバックプロパゲーション。学習シグナルが数倍になりデータ効率が飛躍的向上。構造自体はBPDと本質的に同等だが動機が異なる。

【DeepSeek V3/R1のMTP】MetaのMTPをさらに洗練し「因果連鎖（Causal Chain）」を導入。D個のMTPモジュールを直列接続し、深度k-1の隠れ状態h^{k-1}_iと実トークンのEmbedding(t_{i+k})をRMSNorm後に結合→投影行列M_kで次元dに圧縮→深度固有のTransformer層TRM_kで処理→共有のOutHeadで語彙分布P^kを出力。各深度の予測が独立でなく直前の深度の内部表現を条件付けるため予測精度が高い。学習はTeacher Forcing（正解Embeddingを強制入力）で誤差蓄積を防ぎ安定化。推論時は①MTPヘッドを切り離してメインモデル単体でデプロイ（学習品質の恩恵のみ享受）、②MTPモジュールをSelf-speculative Decodingのドラフター（Free-runningモード）として活用し複数トークン高速生成の2択。外部ドラフトモデル不要でバックボーンの潜在空間を共有するため受容率が高い点が特徴。LLMの推論効率化の標準パラダイムになり得る手法として注目される。

## アイデア

- DeepSeekの「因果連鎖（Causal Chain）」設計：並列独立ヘッドではなく直列モジュールにすることで、深度k-1の隠れ状態を深度kの条件として引き渡す構造が予測精度を高める点は、Residual Connectionの思想をシーケンス方向に拡張したものとして捉えられる
- Teacher ForcingによるMTPの学習安定化：因果連鎖での誤差蓄積問題を正解Embeddingの強制入力で解決するトレードオフは、推論時のFree-runningとのギャップ（Exposure Bias）を生むが、実用上は十分な受容率を確保できるという割り切りが興味深い
- MTPヘッドを「切り離す」選択肢の価値：推論時にドラフターとして使わなくても、学習時の豊富な勾配シグナルで鍛えられたメインモデル自体の品質向上が得られるという「学習補助器」としての側面は、LoRAなどのアダプター的発想と共通する設計思想を持つ

## 前提知識

- **Decoder-only Transformer** → /deep_4878 HealthFormer：生成的マルチモーダル生理モデルによる臨床介入シミュレーション
- **KV-Cache** → /deep_235 Waypoint-1: Overworldによるリアルタイムインタラクティブ映像拡散モデル
- **Speculative Decoding** → /deep_1379 アライメントフィードバックを用いたマルチドラフター投機的デコーディング
- **Teacher Forcing** (TODO: 読むべき)
- **Autoregressive生成** (TODO: 読むべき)

## 関連記事

- /deep_4297 システム統合型Speculative DecodingによるRL後学習ロールアウトの高速化
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法
- /deep_902 日本語LLMオープンリーダーボードの公開
- /deep_4181 投機的デコーディングはなぜ速いのか？トイモデルで検証する

## 原文リンク

[MTP（Multi-Token Prediction）の系譜とメカニズムを徹底解説](https://zenn.dev/acrosstudioblog/articles/ad05d752e3c038)
