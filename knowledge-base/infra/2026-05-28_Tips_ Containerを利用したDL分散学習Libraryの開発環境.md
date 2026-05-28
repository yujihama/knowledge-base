---
title: "Tips: Containerを利用したDL分散学習Libraryの開発環境"
url: "https://zenn.dev/kaz20/articles/ff41dfdcd48613"
date: 2026-05-28
tags: [Singularity, Apptainer, NGC, NeMo, Megatron-LM, HPC, VS Code, Pylance, 分散学習, コンテナ開発環境]
category: "infra"
related: [1879, 1489, 6322, 429, 505]
memo: "[Zenn LLM] Tips: Containerを利用したDL分散学習Libraryの開発環境"
processed_at: "2026-05-28T21:00:32.133982"
---

## 要約

東京科学大学博士課程の著者が、GPUスパコン（HPC）環境でDeep Learning Frameworkの開発を行う際の環境構築手法をまとめたTips記事。Swallow LLMの開発で実際に使用された知見に基づく。

背景として、NeMo・Megatron-LM・PyTorch・CUDAなど複雑な依存関係を持つLLM/VLM/VLA学習ライブラリをconflictなくインストールする難しさがある。また、NVIDIAへのバグ報告時はNGC PyTorchなどの公式コンテナ環境での動作確認が推奨されており、Python venvベースの環境では不十分な場合がある。

主な課題は、Singularity/Apptainerコンテナ内でコードを実行しつつ、VS Codeのログインノード側でimport補完・定義ジャンプを機能させる点。これが解決されないと、開発速度の低下やコードリーディングの誤解を招く。

解決策として3方式を比較している。①local venv（ログインノード上に.venvを作成）はシンプルだがCUDA・MPI等システムライブラリの再現が難しい。②container attach（VS Code ServerをコンテナINで動作）は実行環境への忠実度が高いが、ユーザーごとにコンテナセッションが必要でCPU/メモリを消費する。③sandbox mirror（SIFをサンドボックス展開してVS Code/Pylanceが参照）はIDE用の常駐コンテナが不要で実行環境に近いimport解決が得られる。

推奨手法はsandbox mirror方式。具体的には、`singularity build --sandbox nemo-26.0.2-sandbox nemo-26.0.2.sif`でNGC NeMoコンテナのSIFをsandbox展開（SIF:20GB→sandbox:45GB）し、共有ストレージに移動。VS Codeの`.vscode/settings.json`に`python.analysis.extraPaths`としてsandbox内のsite-packagesパス（python3.12/site-packages等）を追加する。これによりログインノード上のVS Codeがコンテナ内と同一のimportツリーを参照でき、補完・定義ジャンプが機能する。コード実行は従来通り`singularity exec`でSIFコンテナ内で行う。

Kubernetes環境では②のcontainer attach方式が素直とも言及している。唯一の欠点はsandboxのストレージ消費（約2倍）であり、不要なsandboxの定期削除が必要。

## アイデア

- SIFをsandbox展開してVS CodeのPylanceに参照させるsandbox mirror方式は、常駐コンテナなしで実行環境と同一のimport解決を実現する軽量アーキテクチャ
- 実行環境（SIFコンテナ）とIDE参照環境（sandbox）を分離することで、ユーザーごとのコンテナセッション管理やCPUリソース消費を回避できる設計思想
- python.analysis.extraPathsによる複数site-packagesパス指定は、コンテナ内の複雑なPythonパスレイアウト（opt/venv, usr/local/lib, usr/lib等）をIDEに教える汎用的なパターンとして応用可能

## 前提知識

- **Singularity/Apptainer** (TODO: 読むべき)
- **NGC PyTorch** (TODO: 読むべき)
- **NeMo** → /deep_3637 NeMo Agent Toolkit 実践運用編 — Guardrails × Langfuse による本番品質管理
- **Megatron-LM** (TODO: 読むべき)
- **VS Code Remote SSH** (TODO: 読むべき)

## 関連記事

- /deep_1879 🤗 Accelerate 紹介：あらゆるデバイスでPyTorchトレーニングスクリプトをそのまま実行
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_6322 連合学習のための型付きテンソル言語
- /deep_429 大規模AIシステムにおける戦略的レバーとしてのスループット最適化：データローダーとメモリプロファイリング革新からの証拠
- /deep_505 大規模AIシステムにおけるスループット最適化：データローダーとメモリプロファイリングの革新からの実証

## 原文リンク

[Tips: Containerを利用したDL分散学習Libraryの開発環境](https://zenn.dev/kaz20/articles/ff41dfdcd48613)
