---
title: "PodmanのコンテナLinuxでNVIDIA GPU(Geforce RTX)を使ったローカルLLM環境を構築してみた"
url: "https://zenn.dev/onigiri_tomyz/articles/a33f87996eea92"
date: 2026-04-24
tags: [Podman, NVIDIA, llama-cpp-python, Gemma3, GGUF, Gradio, CUDA, ローカルLLM, コンテナ, Fedora]
category: "infra"
related: [1146, 2403, 1423, 399, 710]
memo: "[Zenn LLM] PodmanのコンテナLinuxでNVIDIA GPU(Geforce RTX)を使ったローカルLLM環境を構築してみた"
processed_at: "2026-04-24T12:29:00.786686"
---

## 要約

Fedora 43 Server上でPodmanコンテナを使い、GeForce RTX 4070 Ti Super（16GB VRAM）でGemma 3をローカル実行するLLMチャット環境の構築手順を詳述した記事。KVM仮想化からコンテナへの移行理由はリソース効率の改善。

ホストOS側ではNouveauドライバの無効化（grub設定・initramfs更新）、CUDA Toolkit（runfileローカルインストール）、NVIDIA Container Toolkitのインストールが必要。Fedora固有の手順が示されているが、Podman対応ディストリビューションであれば応用可能。

Dockerfileのベースイメージはnvidia/cuda:12.6.3-devel-ubuntu24.04。RTX 4070 Ti Super（Ada Lovelaceアーキテクチャ、CUDAアーキテクチャ番号89）向けに`CMAKE_ARGS="-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=89"`を指定してllama-cpp-pythonをソースビルドする点が肝。libcuda.so.1のシンボリックリンクをビルド時に手動作成することで、コンテナビルド時のリンカエラーを回避する。サービス管理にはsystemdではなくsupervisordを採用（コンテナでの一般的手法）。

モデルはHugging FaceからGemma 3 12B GGUF形式（Q6_K量子化）をダウンロード。16GB VRAMに対してQ6_Kが最適とGeminiが推奨。モデルファイルはイメージに含めず、コンテナ起動時にバインドマウントで注入する設計とし、モデル変更時の再ビルドを不要にしている。

WebUIはGradioを採用。app.pyでllama-cpp-pythonのLlamaクラスを使い、n_gpu_layers=-1で全レイヤーをVRAMにオフロード、n_ctx=8192、n_batch=512を設定。Gemma 3のプロンプトフォーマット（<|im_start|>/<|im_end|>）に対応したチャット履歴管理を実装。コンテナ起動コマンドではGPUデバイスパススルー（--device nvidia.com/gpu=all）とモデルディレクトリのバインドマウントを指定。ブラウザからポート7860でアクセス可能。GLM-4.7（UD-Q3_K_XL）でも同様の手法が適用可能と言及されている。

## アイデア

- モデルファイルをイメージに含めずバインドマウントで注入する設計により、モデル差し替えのたびに数十GBのイメージ再ビルドを回避できる実用的なパターン
- CUDAアーキテクチャ番号（89=Ada Lovelace）をCMAKE_ARGSで明示指定することで、llama-cpp-pythonをGPUアーキテクチャ最適ビルドする手法
- libcuda.so.1のシンボリックリンク手動作成というビルド時ハック——コンテナビルド環境にGPUが存在しない状況でCUDA対応バイナリをビルドするための回避策として汎用性が高い

## 前提知識

- **llama-cpp-python** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)
- **NVIDIA Container Toolkit** (TODO: 読むべき)
- **Podman** (TODO: 読むべき)
- **CUDA** → /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル

## 関連記事

- /deep_1146 1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった
- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_710 OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド

## 原文リンク

[PodmanのコンテナLinuxでNVIDIA GPU(Geforce RTX)を使ったローカルLLM環境を構築してみた](https://zenn.dev/onigiri_tomyz/articles/a33f87996eea92)
