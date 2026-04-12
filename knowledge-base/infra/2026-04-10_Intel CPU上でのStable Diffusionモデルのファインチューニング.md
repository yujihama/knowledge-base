---
title: "Intel CPU上でのStable Diffusionモデルのファインチューニング"
url: "https://huggingface.co/blog/stable-diffusion-finetuning-intel"
date: 2026-04-10
tags: [Stable Diffusion, Intel Sapphire Rapids, AMX, IPEX, Textual Inversion, 分散学習, oneCCL, CPU推論, Diffusers, BF16]
category: "infra"
memo: "[HF Blog] Fine-tuning Stable Diffusion models on Intel CPUs"
processed_at: "2026-04-10T09:16:51.162411"
---

## 要約

本記事は、Intel第4世代Xeon（Sapphire Rapids）CPUクラスタ上でStable Diffusionモデルをファインチューニングする手順を解説したHugging Face公式ブログ（2023年7月）。従来GPUが前提だったDiffusionモデルのファインチューニングをCPUで実現した点が核心。

【ハードウェア構成】Intel Developer Cloud上の4ノード構成。各ノードはIntel Xeon Platinum 8480+（56コア×2ソケット、計224スレッド）を搭載。Sapphire RapidsにはAMX（Advanced Matrix Extensions）という新世代のディープラーニング向けハードウェアアクセラレータが内蔵されており、BF16・INT8演算を高速化する。

【ファインチューニング手法】Textual Inversionを採用。5枚の学習画像のみで新しい概念（「dicoo」というキャラクター）をモデルに埋め込む軽量手法。学習データ量が極めて少なく、フルファインチューニング不要な点が特徴。

【ソフトウェアスタック】Intel Extension for PyTorch（IPEX）を用いてU-NetとVAEを最適化（`ipex.optimize()`の2行追加のみ）。分散通信にはoneCCL（Intel oneAPI Collective Communications Library）を使用。HuggingFaceのAccelerateライブラリで4ノード分散訓練を制御。メモリ確保にはlibtcmalloc（gperftools）を採用しメモリ効率を向上。

【学習設定】`mpirun`で4ノード×`num_processes`プロセスを起動。学習ステップ数200、バッチサイズ1、BF16精度で実施。ノード間通信はCCL_ATL_TRANSPORT=ofiで設定。

【結果】4ノード分散で約35分のファインチューニングが完了。生成されたモデルはdicooキャラクターの外見特徴を再現しつつ、異なる背景・ポーズへの汎化が確認された。GPUなしでDistributed CPUファインチューニングが実用域に達したことを示す実証例。

【含意】クラウドGPUインスタンスのコストや可用性の問題を回避しつつ、企業向けカスタム画像生成モデルを構築できる可能性を示している。合成データ生成やコンテンツ制作など、エンタープライズユースケースへの応用が想定される。

## アイデア

- GPU不要のCPUクラスタ分散ファインチューニング：AMX内蔵のSapphire Rapids + IPEX + oneCCLの組み合わせにより、GPUなしで実用的な速度（200ステップ約35分）のStable Diffusionファインチューニングを実現。コスト・調達面での選択肢が広がる
- Textual Inversionによる超少数ショット概念学習：5枚の画像だけでモデルの重みを変えずに新概念を埋め込む手法は、ドメイン特化型画像生成（例：特定の書類フォーマットや図表スタイルの合成データ生成）に応用可能
- ipex.optimize()2行追加という最小変更での最適化：既存のHugging Face学習スクリプトへの変更が極小で済むため、既存パイプラインへのIntel最適化の組み込みコストが低く、段階的な移行が現実的

## Yujiの取り組みへの示唆

監査エージェント開発における合成データ生成の観点から参照価値がある。監査ドキュメント・財務諸表・内部統制フローなどの画像データをTextual Inversionで少数サンプルから生成する用途に応用できる可能性がある。ただしYujiの主軸であるLangGraph・Pydantic・GRPO/RLAIFとの直接的な技術的接点は薄く、インフラ選定（CPU vs GPU）の参考情報として位置づけるのが適切。ローカルLLMインフラ（RTX 3090）を検討中の観点からは、CPU-onlyのファインチューニング手法としての比較材料になり得る。

## 原文リンク

[Intel CPU上でのStable Diffusionモデルのファインチューニング](https://huggingface.co/blog/stable-diffusion-finetuning-intel)
