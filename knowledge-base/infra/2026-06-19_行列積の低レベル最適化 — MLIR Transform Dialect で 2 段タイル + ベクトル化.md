---
title: "行列積の低レベル最適化 — MLIR Transform Dialect で 2 段タイル + ベクトル化"
url: "https://zenn.dev/ux_xu/articles/mlir-matmul-transform-dialect"
date: 2026-06-19
tags: [MLIR, Transform Dialect, 行列積最適化, SIMD, AArch64, FMA, linalg, タイリング, ベクトル化]
category: "infra"
related: [8237, 6931, 6364, 7423, 6411]
memo: "[Zenn 機械学習] 行列積の低レベル最適化 — Transform Dialect で 2 段タイル + vectorize"
processed_at: "2026-06-19T09:08:08.500577"
---

## 要約

本記事はMLIRのTransform Dialectを用いて1024×1024のf32行列積を最適化した実験レポート。動作環境はApple M5 Air（Docker aarch64）、Raspberry Pi 5（cortex-a76）、Raspberry Pi 4（cortex-a72）で、MLIRバージョンはllvm-project 23.0.0git。

Transform Dialectは通常のコマンドラインオプション（--affine-loop-tileなど）と異なり、「どのopに・どの順で・何を適用するか」を.mlirファイル内に直接記述できる仕組み。最適化スケジュールとソースコードが同一ファイルに共存するため再現性が高く、ターゲットISAが変わっても同じスケジュールから異なる命令列を生成できる。

実装はlinalg.matmulに対して3段のtile_using_forを適用する構成：外側[64,64,64]でL1キャッシュブロッキング、内側[4,4,0]でレジスタブロッキング相当、k軸を[0,0,1]で1ステップずつ展開した後にtransform.structured.vectorizeを適用。内側[4,4,0]タイルにより、Cのロードとストアがkループの外側に1回ずつ移動し、手書きNEONでc0〜c3をレジスタに保持し続ける構造と等価になる点が核心。これはaffine-super-vectorizeでCのトラフィックがkループ内に残り続ける問題と対照的。

外側タイルサイズTの最適値はデバイスのL1キャッシュサイズに依存する。3T²×4≦L1の理論式に基づくと、M5（L1=128KB）の理論上限はT≈104だが実測最速はT=0（外側タイルなし）。Pi5（L1=64KB、T≈73）とPi4（L1=32KB、T≈52）は理論値に近いT=64で最速。M5はUnified Memoryの帯域が広いためキャッシュブロッキングのループオーバーヘッドが支配的になる。

手書きNEONとの速度比較ではM5で1.4倍、Pi5で3.1倍、Pi4で2.7倍の差が残る。主因はMLIRの標準loweringがarith.mulfとarith.addfを別opとして生成するため、LLVMがfmul+fadd→fmlaのFMA融合を行えない点。手書きのvfmaq_f32は1命令で積和を実行するが、Transform Dialectでは同等の計算にfmul+faddの2命令が必要となりデータ依存ストールも発生する。

シリーズ全体の改善幅（ナイーブ比）：Loop Tiling（affine）がM5×2.60、手書きNEONがM5×18.8、Transform DialectがM5×13.5。FMAギャップを埋めるにはarith.mulf+arith.addfをfma opに融合するカスタムパスが必要で、IREEなど本格的なMLコンパイラが独自loweringを持つ理由の一つと結論付けている。監査エージェント開発への直接的な示唆は少ないが、LLM推論バックエンドの最適化原理（キャッシュ階層・SIMD命令融合）の理解に寄与する。

## アイデア

- Transform Dialectによりキャッシュブロッキング・レジスタブロッキング・ベクトル化の3段最適化スケジュールをISA非依存で.mlirファイルに記述できる点は、MLコンパイラの移植性向上において本質的なアプローチ
- affine-super-vectorize vs Transform Dialectの比較で、Cのロードストアをkループ外に退避できるかどうかが性能の鍵であることを実測で明示した点が教育的
- FMA未融合という既知の問題がIREEなど産業用MLコンパイラが独自loweringを持つ設計上の必然性と直結しており、コンパイラ設計の深い動機を示している

## 前提知識

- **MLIR** → /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）
- **linalg Dialect** → /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）
- **SIMD / AArch64 NEON** (TODO: 読むべき)
- **ループタイリング** (TODO: 読むべき)
- **FMA（Fused Multiply-Add）** (TODO: 読むべき)

## 関連記事

- /deep_8237 行列積の低レベル最適化 — 手書き NEON で Register Blocking
- /deep_6931 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（opt / llc で NEON 命令を出す）
- /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）
- /deep_7423 データサイエンティストとして急成長する5つの習慣：現場エンジニアが実践するスキルアップ法
- /deep_6411 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する

## 原文リンク

[行列積の低レベル最適化 — MLIR Transform Dialect で 2 段タイル + ベクトル化](https://zenn.dev/ux_xu/articles/mlir-matmul-transform-dialect)
