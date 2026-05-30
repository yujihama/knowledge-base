---
title: "MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（opt / llc で NEON 命令を出す）"
url: "https://zenn.dev/ux_xu/articles/mlir-neon-vectorize-opt-llc"
date: 2026-05-30
tags: [MLIR, LLVM, NEON, SIMD, vectorize, opt, llc, AArch64, AI推論最適化, linalg dialect]
category: "infra"
related: [6364, 6411, 2326, 5838, 5797]
memo: "[Zenn 機械学習] MLIR 入門 — AI推論最適化の仕組みを低レベルから理解する（opt / llc で NEON 命令を出す）"
processed_at: "2026-05-30T09:10:08.943924"
---

## 要約

MLIR/LLVMツールチェーンを用いてAI推論の低レベル最適化を実証した記事。linalg dialectで記述したvec_add（1024要素のfloat32ベクトル加算）をMLIR経由でLLVM IRに変換した後、opt（LLVMミドルエンド最適化）とllc（バックエンドコード生成）の2段パイプラインでAArch64 NEON命令を生成するプロセスを詳細に解説する。

opt -O3を適用すると、スカラーのfadd命令が<4 x float>型のベクトル演算に変換される。ループ内の反復間データ依存がない・ポインタエイリアスなし・ターゲット属性+neon指定の3条件が揃ったときにvectorizeが発動する。生成されたIRではwide.loadとwide.load2の2ベクトル分がアンロールされ、1反復で8要素を処理する。

llcはIRに<4 x float>が存在して初めてfadd v0.4s（NEONの4並列float32加算命令）を出力できる。IRがスカラーのままでは llc -O3 でもNEON命令は生成されない。opt×llcのO0/O3の4通りの組み合わせを実測した結果、M5 Mac（N=1024、10000回平均）ではopt-O0/llc-O0の2379 nsに対し、opt-O3/llc-O3は89 nsで26.8倍の高速化。Raspberry Pi 5（cortex-a76）では5784 ns対269 nsで21.5倍。clang -O3直接コンパイル（M5: 93 ns、Pi5: 213 ns）とほぼ同等の性能が出ることを確認した。

opt単独（opt-O3/llc-O0）ではM5で10.5倍（SIMD幅4倍×アンロール2倍の理論値8倍超）、llc単独最適化（opt-O0/llc-O3）でも8.5倍が出ており、両者は独立した効果を持ちながら補完し合う。ldp q0, q1による8要素の一括ロードとfadd v*.4sによる4並列演算がアセンブリレベルで確認できる。MLIRパイプライン経由でもclang相当の性能が得られることが実証されており、ONNX→MLIR Loweringへの応用可能性を示唆する。

## アイデア

- NEONベクトル命令の生成はoptフェーズ（IRレベルのvectorize）で決定されており、llc -O3にしてもIRがスカラーのままではNEON命令が出ないという明確な責任分離
- opt -O3がwide.loadとwide.load2の2ベクトルアンロールを自動生成し、1ループ反復で8要素処理するコストモデル判断の具体例
- vector.memcheckブロックによる実行時エイリアスチェックとスカラーフォールバックの自動生成により、正確性を保ちながらvectorize最適化を適用する安全機構

## 前提知識

- **LLVM IR** (TODO: 読むべき)
- **SIMD / NEON** (TODO: 読むべき)
- **MLIR linalg dialect** (TODO: 読むべき)
- **AArch64アーキテクチャ** (TODO: 読むべき)
- **コンパイラ最適化パス** (TODO: 読むべき)

## 関連記事

- /deep_6364 MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）
- /deep_6411 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する
- /deep_2326 VFA：グローバル最大値の事前計算によるFlash Attentionのベクトル演算削減
- /deep_5838 Raspberry Pi 5 + M.2 HAT + LLM8850 で NPU を使おうとして DKMS ビルドに阻まれた話
- /deep_5797 MCPサーバーをRustではなく400行の純粋なC++20で書いた理由 〜巨大コード解析における密結合美学〜

## 原文リンク

[MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（opt / llc で NEON 命令を出す）](https://zenn.dev/ux_xu/articles/mlir-neon-vectorize-opt-llc)
