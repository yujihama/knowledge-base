---
title: "行列積の低レベル最適化 — 手書き NEON で Register Blocking"
url: "https://zenn.dev/ux_xu/articles/mlir-matmul-register-blocking"
date: 2026-06-13
tags: [NEON, Register Blocking, SIMD, 行列積, MLIR, Loop Tiling, ARM, fmla, 低レベル最適化, aarch64]
category: "infra"
related: [6931, 6364, 6411, 2326, 5838]
memo: "[Zenn 機械学習] 行列積の低レベル最適化 — 手書き NEON で Register Blocking"
processed_at: "2026-06-13T09:10:18.946264"
---

## 要約

本記事は、ARM NEON intrinsics を用いた Register Blocking（レジスタブロッキング）によって行列積（N=1024）をナイーブ実装比で約18.8倍高速化する手法を解説する。前回の Loop Tiling（約2.6倍）では、タイル内のkループで毎回 C[i][j] をメモリからロードし積和後にストアするため、TK=64なら64回の書き戻しが発生していた。Register Blocking はこれを解決するもので、出力ブロック Mr×Nr（本記事では4×4=16要素）をfloat32x4_t型の変数 c0〜c3 としてレジスタに保持し、kループ終了後に1回だけ vst1q_f32 で書き戻す構造を取る。変数を配列でなく個別変数として宣言するのは、コンパイラがスタックではなくレジスタに割り当てることをほぼ保証するためである。積和演算には vfmaq_f32（ARM FMA命令 fmla に対応）を用い、4要素を1命令で処理する。A[i][k] のスカラー値は vdupq_n_f32 で4要素にブロードキャストして c0〜c3 に使い回すため、ロード命令も1/4に削減される。外側構造はTM=TN=TK=64のキャッシュタイル（3重ループ）がA・B・CをL1キャッシュに収め、その内側でMR=4ステップごとにマイクロカーネルを呼ぶ2段構成。実測結果はM5（Docker aarch64）で552ms→76ms（7.22倍）、Pi5（Cortex-A76）で2399ms→175ms（13.7倍）、Pi4（Cortex-A72）で3679ms→814ms（4.52倍）。Pi4とPi5の差は同一コードでもCortex-A76のOoO実行幅とパイプライン深度の違いによる。最終的な最適化の積み上げはLoop Tiling（キャッシュ帯域削減）＋Register Blocking（キャッシュ書き戻し削減）＋SIMD（演算スループット最大化）の3層。手書きNEONはISA依存の課題があるため、次回はMLIR Transform Dialectによる宣言的なtile+vectorize変換で同等構造をISA非依存で生成する方向を示している。監査エージェント開発への直接的な示唆は薄いが、大規模テンソル演算の最適化思想（メモリ階層ごとの書き戻しコスト最小化）はオンデバイス推論基盤やローカルLLMインフラ構築の文脈で参照価値がある。

## アイデア

- C[i][j]の書き戻しをkループ外の1回に集約するだけでTK=64倍のトラフィック削減になるという、アルゴリズム変更なしの純粋な実装上の工夫で7倍超の高速化が得られる点
- float32x4_tをconfigの配列ではなく個別変数（c0, c1, c2, c3）で宣言することでコンパイラのレジスタ割り当てを強制するという、C言語レベルでのレジスタ制御テクニック
- MLIR Transform Dialectの transform.structured.tile_using_for + transform.structured.vectorize で同等の2段タイル構造をISA非依存に宣言できるが、fmul+faddの2命令分離でfmlaと差が残るという、コンパイラ抽象化のコストとトレードオフ

## 前提知識

- **SIMD / intrinsics** (TODO: 読むべき)
- **Loop Tiling** (TODO: 読むべき)
- **ARM NEON** (TODO: 読むべき)
- **キャッシュ階層** (TODO: 読むべき)
- **MLIR** → /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）

## 関連記事

- /deep_6931 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（opt / llc で NEON 命令を出す）
- /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）
- /deep_6411 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する
- /deep_2326 VFA：グローバル最大値の事前計算によるFlash Attentionのベクトル演算削減
- /deep_5838 Raspberry Pi 5 + M.2 HAT + LLM8850 で NPU を使おうとして DKMS ビルドに阻まれた話

## 原文リンク

[行列積の低レベル最適化 — 手書き NEON で Register Blocking](https://zenn.dev/ux_xu/articles/mlir-matmul-register-blocking)
