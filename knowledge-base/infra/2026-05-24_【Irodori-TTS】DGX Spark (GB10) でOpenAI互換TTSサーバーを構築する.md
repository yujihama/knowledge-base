---
title: "【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する"
url: "https://zenn.dev/michy/articles/52c163a166454d"
date: 2026-05-24
tags: [Irodori-TTS, DGX Spark, GB10, SM_121, Docker, OpenAI互換API, TTS, NVIDIA NGC, torchaudio shim, aarch64]
category: "infra"
related: [409, 4043, 3908, 5160, 5794]
memo: "[Zenn LLM] 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する"
processed_at: "2026-05-24T09:03:55.786828"
---

## 要約

NVIDIA DGX Spark（GB10 / SM_121）上でIrodori-TTSをOpenAI互換HTTP APIとしてLANに公開するDockerサーバー（voiceGenServer）の構築手順を解説した記事。GB10はCUDA compute capability 12.1（SM_121）という新アーキテクチャのため、PyPIで配布される通常のPyTorch wheel（cu128対応版）では「RuntimeError: nvrtc: error: invalid value for --gpu-architecture (-arch)」が発生し動作しない。これを回避するため、NVIDIA NGCが提供するGB10対応コンテナ「nvcr.io/nvidia/pytorch:26.01-py3」（torch 2.10.0a0+a36e1d39eb.nv26.01、CUDA 13.1）をベースイメージとして採用する。Dockerfileでは、Irodori-TTSのrequirements.txtからtorch/torchaudio/torchcodecの3パッケージをgrep -vで除外してインストールし、NGCコンテナのGB10対応torchが通常版で上書きされないようにしている。また、Linux aarch64ではtorchcodecのwheelが存在しないため除外が必須となる。torchaudioはNGCコンテナに含まれていないが、Irodori-TTS本体がtorchaudio.load/save/functional.resample/functional.lfilterを呼び出すため、サーバー起動スクリプト（docker/run_server.py）でsys.modules["torchaudio"]に最小限のshimを差し込む方式で対応。具体的にはsoundfile.read/writeでload/saveを代替し、resampleはtorch.nn.functional.interpolate（modeはlinear）で実装、lfilterはscipy.signal.lfilterで代替する。sentencepiece>=0.1.99,<0.2はPython 3.12/Linux aarch64でソースビルドも失敗するため、sentencepiece==0.2.1を明示指定。compose.yamlではIrodori-TTS・Irodori-TTS-Server・dockerディレクトリをボリュームマウントし、コード変更時はdocker compose restartのみで再起動不要とする設計。APIエンドポイントはポート8088で公開され、IRODORI_API_KEYによるBearer認証もサポート。モデルはAratako/Irodori-TTS-500M-v3、コーデックはAratako/Semantic-DACVAE-Japanese-32dimを使用。監査エージェント開発への直接的な示唆は少ないが、新世代GPUアーキテクチャ（SM_121）向けDockerイメージ構築の実践的知見として、ローカルLLMインフラ構築（RTX 3090等）における依存関係競合の回避パターンとして参考になる。

## アイデア

- sys.modulesへのshim差し込みパターン：本体コードを変更せずにtorchaudioの依存を丸ごとsoundfile/scipy/torch.nn.functionalで代替する手法は、ライブラリ互換性問題の汎用的な回避策として応用できる
- 新アーキテクチャGPU（SM_121）でのPyTorch互換性問題：PyPIのcu128 wheelがSM_121に非対応という制約と、NGCコンテナのsm_120互換動作による回避策は、最新GPU導入時の典型的な落とし穴を示している
- requirements.txtからの選択的除外パターン：grep -v -E で特定パッケージ群を除外してインストールするDockerfileの手法は、ベースイメージ提供のライブラリを保護する際の再利用可能なレシピになる

## 前提知識

- **CUDA compute capability** (TODO: 読むべき)
- **NVIDIA NGC コンテナ** (TODO: 読むべき)
- **Docker / Compose** (TODO: 読むべき)
- **PyTorch wheel** (TODO: 読むべき)
- **TTS（テキスト音声合成）** (TODO: 読むべき)

## 関連記事

- /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_3908 音声AIの300ms――人はなぜAIとの会話に違和感を覚えるのか
- /deep_5160 通勤中に育てたAIが、放置していたアイデアを勝手に形にした【OpenClawエージェント4体を止めるまで①】
- /deep_5794 社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解

## 原文リンク

[【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する](https://zenn.dev/michy/articles/52c163a166454d)
