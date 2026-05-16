---
title: "Ubuntu Server に Docker と GPU ドライバをインストールする"
url: "https://zenn.dev/bbsfish/articles/f3c409fc25c38f"
date: 2026-04-24
tags: [Docker, NVIDIA, GPU, Ubuntu, CUDA, nvidia-container-toolkit, LLM, ubuntu-drivers]
category: "infra"
related: [1496, 2643, 1267, 828, 1621]
memo: "[Zenn LLM] Ubuntu Server に Docker と GPU ドライバをインストールする"
processed_at: "2026-04-24T12:26:08.268487"
---

## 要約

Ubuntu Server 24.04.3 LTS 上に LLM 実行環境を構築するための手順を記録した記事。対象 GPU は NVIDIA GeForce GTX 1660 SUPER（VRAM 6GB）。手順は3段階に分かれる。

第1段階は Docker のインストール。apt のパッケージリストを更新後、ca-certificates・curl・gnupg をインストールし、Docker 公式の GPG キーを /etc/apt/keyrings/docker.asc に登録する。次に Docker の apt リポジトリを sources.list.d に追加し、docker-ce・docker-ce-cli・containerd.io・docker-buildx-plugin・docker-compose-plugin を一括インストールする。sudo なしで docker コマンドを実行するため、現在のユーザーを docker グループに追加し、再ログインで反映させる。

第2段階は GPU ドライバのインストール。ubuntu-drivers devices で推奨ドライバを確認し、ubuntu-drivers install で自動インストールする。再起動後に nvidia-smi を実行し、Driver Version 580.126.09・CUDA Version 13.0 として GTX 1660 SUPER が認識されることを確認。

第3段階は NVIDIA Container Toolkit のインストール。Docker コンテナ内から GPU を利用するために必須のコンポーネント。nvidia.github.io からリポジトリ設定を取得し、nvidia-container-toolkit をインストール後、nvidia-ctk runtime configure --runtime=docker で Docker ランタイムを設定、systemctl restart docker で再起動する。最後に nvidia/cuda:12.2.0-base-ubuntu22.04 イメージを使ったコンテナ内で nvidia-smi が正常動作することを確認し、GPU パススルーが機能していることを検証する。

ローカル LLM 環境の構築（Ollama 等との組み合わせ）や、監査エージェントのバックエンドとして GPU を活用するコンテナ化推論サービスの基盤として直接適用可能な手順。

## アイデア

- ubuntu-drivers install による推奨ドライバの自動選択は、手動でドライババージョンを指定するより安全で、カーネルとの互換性問題を回避しやすい
- NVIDIA Container Toolkit の nvidia-ctk runtime configure により Docker デーモンに GPU ランタイムを登録することで、--gpus all フラグだけでコンテナに GPU をパススルーできる設計になっている
- GTX 1660 SUPER（VRAM 6GB）は量子化（GGUF Q4等）された 7B クラスのモデルをローカル推論するには十分であり、低コストで LLM 実行環境を構築できる最小構成の一例として参考になる

## 前提知識

- **Docker Engine** (TODO: 読むべき)
- **NVIDIA Container Toolkit** (TODO: 読むべき)
- **CUDA** → /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- **ubuntu-drivers** (TODO: 読むべき)
- **nvidia-smi** → /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成

## 関連記事

- /deep_1496 Mustafa Suleyman：AIの発展は近い将来に壁にぶつかることはない——その理由
- /deep_2643 ムスタファ・スレイマン：AIの進化は壁に当たらない——その理由
- /deep_1267 SafeCoder vs. クローズドソースコードアシスタント：エンタープライズ向けオープンソースコード生成の比較
- /deep_828 PyTorchにおけるGPUメモリの可視化と理解
- /deep_1621 Mustafa Suleyman：AIの発展は近いうちに壁にぶつからない――その理由

## 原文リンク

[Ubuntu Server に Docker と GPU ドライバをインストールする](https://zenn.dev/bbsfish/articles/f3c409fc25c38f)
