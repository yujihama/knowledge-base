---
title: "🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド"
url: "https://huggingface.co/blog/stable_diffusion"
date: 2026-04-11
tags: [StableDiffusion, Diffusers, LatentDiffusionModel, VAE, CLIP, U-Net, ClassifierFreeGuidance, HuggingFace, text-to-image, DDIM]
category: "ai-ml"
memo: "[HF Blog] Stable Diffusion with 🧨 Diffusers"
related: [1302, 1495, 1535, 1389, 1265]
processed_at: "2026-04-11T21:05:29.167405"
---

## 要約

Stable DiffusionはCompVis・Stability AI・LAIONの研究者らが開発したテキスト→画像生成の潜在拡散モデル（Latent Diffusion Model）。LAION-5Bデータベースのサブセットから512×512ピクセル画像で学習されており、HuggingFaceの🧨 Diffusersライブラリを通じて利用可能。

【アーキテクチャの概要】モデルは3つの主要コンポーネントで構成される。①VAE（Variational Autoencoder）：画像をピクセル空間から64×64の潜在空間へ圧縮・復元。②CLIPテキストエンコーダー：テキストプロンプトを768次元の埋め込みベクトルに変換。③U-Net：潜在空間上でノイズ除去を反復実行するデノイザー。推論時はランダムノイズからスタートし、T=50ステップのデノイズを経て最終的に潜在表現をVAEデコーダーで画像化する。

【Classifier-Free Guidance（CFG）】guidance_scaleパラメータ（推奨値7〜8.5）でテキスト条件付けの強度を制御。具体的には「条件付きノイズ予測」と「無条件ノイズ予測」の差をスケーリングして合算することで、プロンプトへの追従度と画質のトレードオフを調整する。

【実装上のポイント】StableDiffusionPipelineのfrom_pretrained()でモデルをロード後、pipe.to('cuda')でGPUに転送するだけで推論可能。GPU RAMが10GB未満の場合はfloat16精度（revision='fp16', torch_dtype=torch.float16）を使用することで動作する。num_inference_steps=15では構造は保たれるが細部品質が低下するため、デフォルトの50ステップが実用的。

【画像サイズの制約】height・widthは8の倍数必須。512×512が基本で、512を下回ると品質劣化、両辺が512超になると画像領域の繰り返しが生じグローバルコヒーレンスが失われる。非正方形画像は一辺を512固定にするのが推奨。

【カスタマイズ】Diffusersはモジュール化設計のため、スケジューラー（DDIMScheduler、LMSDiscreteScheduler等）の差し替えが容易。DDIMはDDPMと同品質を50→20ステップで達成可能。img2imgパイプラインではstrengthパラメータ（0.0〜1.0）で元画像をどれだけ変化させるかを制御し、inpaintingではマスク領域のみを再生成できる。

## アイデア

- 潜在空間（64×64）でノイズ除去を行いVAEで512×512に復元するアーキテクチャは、高解像度画像生成の計算コストをピクセル空間の1/64に削減する設計として参照価値がある
- Classifier-Free GuidanceはLLMのRLHF/RLAIFにおけるKLペナルティと概念的に類似しており、条件信号への追従度とサンプル多様性のトレードオフを明示的に制御するメカニズムとして比較検討できる
- Diffusersのスケジューラー差し替え設計（DDPMをDDIMに交換するだけで推論ステップを50→20に削減）は、エージェントのサブコンポーネントを疎結合に保つアーキテクチャ設計の参考事例になる

## 関連記事

- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1495 VQ-Diffusion：離散潜在空間における条件付き拡散モデル
- /deep_1535 JAX / Flax で Stable Diffusion を高速推論する方法
- /deep_1389 無料Google ColabでDeepFloyd IFをDiffusersで動かす方法
- /deep_1265 Würstchen：42倍圧縮による高速・低コスト画像生成拡散モデルの紹介

## 原文リンク

[🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド](https://huggingface.co/blog/stable_diffusion)
