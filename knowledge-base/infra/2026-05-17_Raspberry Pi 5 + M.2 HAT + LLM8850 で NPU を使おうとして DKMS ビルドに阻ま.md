---
title: "Raspberry Pi 5 + M.2 HAT + LLM8850 で NPU を使おうとして DKMS ビルドに阻まれた話"
url: "https://zenn.dev/koounosuke/articles/45a24758b6feb8"
date: 2026-05-17
tags: [Raspberry Pi 5, LLM8850, NPU, DKMS, axcl_host, PCIe, エッジAI, Reproducible Builds, カーネルドライバ, aarch64]
category: "infra"
related: [3908, 2875, 4198, 154, 1744]
memo: "[Zenn LLM] Raspberry Pi 5 + M.2 HAT + LLM8850 で NPU を使おうとして DKMS ビルドに阻まれた話"
processed_at: "2026-05-17T21:00:37.922910"
---

## 要約

Raspberry Pi 5 に M.2 HAT 経由で LLM8850（Axera製 NPU搭載AIアクセラレータ）を接続し、エッジ環境でのLLM推論基盤を構築しようとした記録。ハードウェア接続自体は成功し、`lspci` で「Axera Semiconductor Co., Ltd Device 0650」として PCIe 認識まで確認できた。しかし NPU ドライバ `axcl_host.ko` の DKMS ビルドが失敗し、`/dev/axcl_host` デバイスファイルが生成されず、`axcl-smi` によるNPU状態確認にも至れなかった。

失敗の直接原因は、ドライバソース（axclhost 3.6.5）内の C マクロ `__DATE__` / `__TIME__` の使用。これらはコンパイル時刻をバイナリに埋め込むマクロであり、Reproducible Builds（再現可能ビルド）の観点から問題とされる。現在の Raspberry Pi OS Lite のカーネル（6.18.29+rpt-rpi-2712）のビルド環境では `-Werror=date-time` フラグが有効になっており、この警告がエラーとして扱われてビルドが中断された。ドキュメント通りに手順を踏んでも失敗する理由は、axclhost のドキュメントが特定の OS・カーネルバージョンの組み合わせで検証されており、Raspberry Pi OS の `apt full-upgrade` によるカーネル更新で想定環境とのズレが生じたため。

対応策として3つの選択肢が示されている。①ドライバソースの `axcl_module_version.h` 内の `__DATE__`・`__TIME__` を固定文字列に `sed` で置換して DKMS 再ビルドする方法（公式外対応だが原因を理解しながら進められる）、②カーネルを 6.12 系に切り替えてドライバとの相性問題を回避する方法、③Ubuntu 24.04 LTS に環境を切り替えて動作実績のある環境に合わせる方法。

エッジAI環境構築の教訓として、OS・Linuxカーネル・カーネルヘッダー・DKMS・NPUドライバ・SDK/runtimeのすべてのバージョンが整合して初めて動作するという制約が浮き彫りになった。SBCベースのエッジAI研究では「挿せばすぐ動く」という前提が成立しないケースが多く、ドライバのバージョン固定と環境の再現性確保が重要な運用課題となる。監査エージェント開発におけるエッジ推論基盤の構築でも同様の問題に直面する可能性があり、環境のバージョン管理戦略（Dockerによる隔離、Ubuntu LTSへの統一等）を事前に検討する価値がある。

## アイデア

- DKMS ビルド失敗の原因が `__DATE__`/`__TIME__` マクロという盲点：NPUドライバの動作不良がハードウェア障害ではなくコンパイラの Reproducible Builds ポリシーに起因するという診断プロセスが、エッジAIデバッグの典型パターンを示している
- カーネルバージョンとドライバの相性問題の普遍性：apt upgrade によって外部ドライバが突然ビルド不能になるリスクは、NPU/GPU/PCIeデバイスを使うエッジAI研究全般に共通する制約であり、バージョン固定戦略の必要性を示唆する
- `dkms status` の `added` と `installed` の違い：`added`（登録済み）と `installed`（ビルド・インストール済み）を混同するとトラブルシュートの起点を誤る。状態確認コマンドの出力の意味を正確に理解することがハードウェア系デバッグの基本

## 前提知識

- **DKMS** (TODO: 読むべき)
- **Linux カーネルモジュール** (TODO: 読むべき)
- **PCIe** (TODO: 読むべき)
- **Reproducible Builds** (TODO: 読むべき)
- **NPU/AIアクセラレータ** (TODO: 読むべき)

## 関連記事

- /deep_3908 音声AIの300ms――人はなぜAIとの会話に違和感を覚えるのか
- /deep_2875 第4回海事コンピュータビジョンワークショップ（MaCVi 2026）：チャレンジ概要
- /deep_4198 心臓の縁で：宇宙飛行士向けスマートヘルスセンサーにおけるオンデバイス心臓特徴抽出のための超低消費電力FPGAベースCNN
- /deep_154 ロボティクスAIを組み込みプラットフォームへ展開：データセット収録・VLAファインチューニング・オンデバイス最適化
- /deep_1744 リレー支援型活性化統合SIMによる無線物理ニューラルネットワーク

## 原文リンク

[Raspberry Pi 5 + M.2 HAT + LLM8850 で NPU を使おうとして DKMS ビルドに阻まれた話](https://zenn.dev/koounosuke/articles/45a24758b6feb8)
