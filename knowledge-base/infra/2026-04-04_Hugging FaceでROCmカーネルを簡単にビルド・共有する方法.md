---
title: "Hugging FaceでROCmカーネルを簡単にビルド・共有する方法"
url: "https://huggingface.co/blog/build-rocm-kernels"
date: 2026-04-04
tags: [ROCm, HIP, AMD GPU, MI300X, FP8, GEMM, PyTorch, kernel-builder, HuggingFace, Nix]
category: "infra"
memo: "[HF Blog] Easily Build and Share ROCm Kernels with Hugging Face"
processed_at: "2026-04-04T12:01:17.893624"
---

## 要約

Hugging Faceの`kernels`ライブラリと`kernel-builder`を使い、AMD GPU向けカスタムROCmカーネルを構築・テスト・共有するための実践的ガイド。従来のCMake/Nixによる複雑なビルド設定・コンパイラエラー・ABIの問題を抽象化し、CUDA・ROCm・Metal・XPUなど複数バックエンドに対応したポータブルなカーネル開発フローを提供する。

本記事では、AMD Developer Challenge 2025でグランプリを受賞したRadeonFlow GEMMカーネルを実例として使用。このカーネルはAMD Instinct MI300X（gfx942）向けに最適化されたFP8ブロックワイズ行列積（GEMM）実装で、`e4m3fnuz`形式（指数4bit・仮数3bit）を採用。FP8の狭いダイナミックレンジを補うため、128ブロック単位のスケーリングファクタ（a_scale: (K//128)×M in fp32、b_scale: (K//128)×(N//128) in fp32）を適用し、精度を維持しながら高スループットを実現する。

ビルドフローは以下の構成に従う：(1) プロジェクト構造として`build.toml`（ビルドマニフェスト）・HIPソースファイル（`.hip`拡張子）・ヘッダファイル（`.h`）・PyTorchバインディング（`torch_binding.cpp`）・再現性確保のための`flake.nix`を配置。(2) `build.toml`でバックエンドを`rocm`、対象アーキテクチャを`gfx942`と指定し、依存関係を宣言。(3) `torch_binding.cpp`でATEN演算子としてカーネルをPyTorchに登録し、Pythonから`ops.gemm.gemm_kernel()`として呼び出せるようにする。(4) `kernel-builder`のDockerコンテナを用いてローカルビルド・動作確認を実施。(5) Hugging Face Hubの`kernels-community`組織にリポジトリを公開し、`kernels`ライブラリ経由でインストール・利用可能にする。

共有後は`pip install kernels`のみでインストール可能となり、`from kernels import get_kernel`でカーネルを取得できる。再現性はNixflakeで担保されており、ビルド環境の差異による問題を排除する。AMD GPU向けの高性能カーネル開発・共有のエコシステムとして機能する。

## アイデア

- FP8（e4m3fnuz）＋ブロックワイズスケーリングにより、精度を犠牲にせず高スループットを実現する設計パターンは、LLM推論の量子化戦略として参考になる
- build.tomlによるマルチバックエンド（CUDA/ROCm/Metal/XPU）対応の統一ビルドマニフェストは、カーネルのポータビリティ確保の実践例として注目に値する
- Nixflakeで再現性を保証しHugging Face Hubで配布するフローは、カスタムカーネルのOSS化・コミュニティ共有の標準的な方法論を示している

## Yujiの取り組みへの示唆

監査エージェントシステムではGPU推論速度がボトルネックになる場面があり、ローカルLLMインフラ（RTX 3090予定）においてカスタムカーネルの利用・最適化手法として参考になる。特にFP8量子化＋スケーリングの設計はRTX 3090でのLLM推論高速化に応用できる可能性がある。ただし本記事はAMD MI300X向けであり、NVIDIAアーキテクチャへの直接適用にはCUDA版ガイドの参照が必要。

## 原文リンク

[Hugging FaceでROCmカーネルを簡単にビルド・共有する方法](https://huggingface.co/blog/build-rocm-kernels)
