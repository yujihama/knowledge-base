---
title: "UnslothとHugging Face Jobsで無料でAIモデルをファインチューニングする方法"
url: "https://huggingface.co/blog/unsloth-jobs"
date: 2026-03-31
tags: [Unsloth, HuggingFace-Jobs, LoRA, SFT, fine-tuning, Claude-Code, LFM2.5, TRL, Trackio, UV]
category: "infra"
memo: "[HF Blog] Train AI models with Unsloth and Hugging Face Jobs for FREE"
related: [1397, 265, 335, 1449, 994]
processed_at: "2026-03-31T21:07:12.737589"
---

## 要約

本記事は、Unslothライブラリと Hugging Face Jobs（フルマネージドクラウドGPU環境）を組み合わせ、LLMのファインチューニングを低コスト・高速に実行する方法を解説している。

【技術的背景】Unslothは標準的な手法と比較して約2倍の学習速度、約60%のVRAM削減を実現するファインチューニングフレームワーク。LoRA（低ランク適応）を活用し、4bit量子化（load_in_4bit=True）でモデルをロードする。対象モデルはLiquidAI/LFM2.5-1.2B-Instructで、1GB未満のメモリで動作し、CPU・スマートフォン・ラップトップへのオンデバイスデプロイに対応。

【実行方法】HF CLIを用いて `hf jobs uv run` コマンドでトレーニングジョブを投入する。パラメータとしてGPUフレーバー（a10g-small等）、シークレット（HF_TOKEN）、タイムアウト、データセット（例: mlabonne/FineTome-100k）、エポック数、出力リポジトリを指定可能。スクリプトはUVのインライン依存関係形式で記述され、依存パッケージ（unsloth, trl>=0.12.0, datasets, trackio）が自動インストールされる。

【コーディングエージェント統合】Claude Code / Codexなどのコーディングエージェントからスキルとして呼び出せる。Claude Codeでは `/plugin install hugging-face-model-trainer@huggingface-skills` でインストール後、自然言語プロンプトでジョブ投入が可能。エージェントはトレーニングスクリプトを自動生成し、HF Jobsへ投入、Trackioによるリアルタイム損失曲線のモニタリングURLを返す。

【コスト感】1B未満のモデルはt4-small（約$0.40/時間）、1〜3Bはt4-medium（約$0.60/時間）、3〜7BはA10G small（約$1.00/時間）、7〜13BはA10G large（約$3.00/時間）。LFM2.5-1.2Bのような小規模モデルなら数ドルでファインチューニング完了。さらに現在、Unsloth Jobs Explorers組織への参加で無料クレジットと1ヶ月Proサブスクリプションが提供されている。

【学習スクリプト構成】FastLanguageModel.from_pretrained→get_peft_model（r=16, lora_alpha=32）→SFTTrainer（SFTConfig）の順で構成。push_to_hub=TrueとTrackioレポートを組み合わせることで、学習完了後の自動モデル公開とモニタリングが実現。

## アイデア

- コーディングエージェント（Claude Code）をトレーニングジョブの投入・監視インターフェースとして使う設計パターン：自然言語指示→スクリプト生成→クラウドジョブ投入→モニタリングURLの返却という一連のパイプラインをエージェントが完結させる
- UVのインライン依存関係（# /// script形式）を使ってPythonスクリプト単体でパッケージ管理を完結させる手法：Dockerfileやrequirements.txtなしに再現可能な実行環境を定義できる
- 1B規模のモデルを$数ドルでタスク特化ファインチューニングし、CPU・スマホ等エッジデバイスにデプロイするというパターン：大規模LLM API依存からの脱却と特定ドメインへの適応を低コストで実現
## 関連記事

- /deep_1397 StackLLaMA: RLHFでLLaMAをトレーニングするための実践ガイド
- /deep_265 RapidFire AIによるTRLファインチューニングの最大20倍高速化
- /deep_335 DPO学習におけるバッチサイズと勾配累積がlossに与える影響を検証
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_994 TGI Multi-LoRA：1回のデプロイで30モデルを同時配信

## 原文リンク

[UnslothとHugging Face Jobsで無料でAIモデルをファインチューニングする方法](https://huggingface.co/blog/unsloth-jobs)
