---
title: "ZeroGPU Spacesを事前コンパイル（AoT）で高速化する方法"
url: "https://huggingface.co/blog/zerogpu-aoti"
date: 2026-04-06
tags: [ZeroGPU, PyTorch, AoT-compilation, AOTInductor, torch.export, HuggingFace-Spaces, Flux, FP8量子化, FlashAttention-3, H200]
category: "infra"
memo: "[HF Blog] Make your ZeroGPU Spaces go brrr with ahead-of-time compilation"
processed_at: "2026-04-06T21:02:02.976609"
---

## 要約

Hugging Face ZeroGPUは、アイドル時にGPUを占有しないジャストインタイム方式でNvidia H200（MIG 3g.71gbスライス）を提供するサービス。通常のtorch.compileはZeroGPUのフォークプロセス方式と相性が悪く、毎回数十秒〜数分のコンパイル時間が発生してしまう。本記事はこの問題を解決するPyTorchのAhead-of-Time（AoT）コンパイル手法を解説している。AoTコンパイルはtorch.export + AOTInductorを使い、モデルを一度だけコンパイルして保存し、後続の全プロセスで即座にリロードできる仕組み。具体的な手順は4段階：①spaces.aoti_captureヘルパーでtransformerへの入力引数を捕捉、②torch.export.exportでExportedProgramとして計算グラフをエクスポート、③spaces.aoti_compile（torch._inductor.aot_compileのラッパー）でコンパイル済みバイナリを生成、④pipe.transformerをコンパイル済みモデルに差し替えて推論に使用。FluxのようなDiffusion Modelでは主にtransformer（デノイザー）コンポーネントが計算の大半を占めるため、そこだけをターゲットにコンパイルする設計。実績として、Flux・Wan・LTXモデルで1.3×〜1.8×のスピードアップを達成。さらに発展的なテクニックとして、FP8量子化（メモリ削減と推論高速化）、Dynamic Shapes（可変解像度への対応）、複数モデルコンポーネント間の重み共有、FlashAttention-3統合、Regional Compilation（画像の特定領域のみコンパイル）なども紹介。コンパイル済みグラフはHugging Face Hubにアップロードして共有・再利用も可能で、spaces.aoti_load_from_hubで即時ロードできる。ZeroGPUのProユーザー・Team/Enterpriseメンバーはスペース作成が可能で、Pro等は8倍のクォータを取得できる。2025年後半には7g.141gbのフルスライスも提供予定。

## アイデア

- torch.compileとAoTコンパイルの使い分け：短命プロセス（コンテナ、サーバーレス）ではJITのキャッシュ復元に数分かかるため、AoT方式で事前生成したバイナリをHubから即ロードするパターンが有効
- spaces.aoti_captureのコンテキストマネージャ設計：実際には実行せず引数だけを捕捉する「ドライラン」パターンは、テスト・デバッグやモデルの入力形状検証にも応用できる汎用的な設計パターン
- コンパイル済みグラフのHub共有により、チーム内で最適化済みモデルを再利用できるMLOpsワークフローが実現可能—毎回コンパイルするコストを排除できる
## 関連記事

- /deep_83 ClaudeとHugging FaceでAI画像生成：MCP連携による実践ガイド
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1611 近接方策最適化（PPO）：方策更新を安定させるクリッピング手法
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_809 ホークス過程の大規模並列厳密推論

## 原文リンク

[ZeroGPU Spacesを事前コンパイル（AoT）で高速化する方法](https://huggingface.co/blog/zerogpu-aoti)
