---
title: "VQ-Diffusion：離散潜在空間における条件付き拡散モデル"
url: "https://huggingface.co/blog/vq-diffusion"
date: 2026-04-10
tags: [VQ-Diffusion, discrete-diffusion, VQ-VAE, VQGAN, latent-diffusion, CLIP, transformer, diffusers, text-to-image]
category: "ai-ml"
memo: "[HF Blog] VQ-Diffusion"
related: [1572, 1302, 1265, 1538, 1494]
processed_at: "2026-04-10T21:13:46.993506"
---

## 要約

VQ-Diffusion（Vector Quantized Diffusion）は、中国科学技術大学とMicrosoftが開発した条件付き潜在拡散モデルで、2022年11月にHugging Face Blogで紹介された。最大の特徴は、ノイズ付加・除去プロセスが連続空間ではなく離散的な量子化潜在空間上で動作する点にある。

【アーキテクチャ】
画像はVQ-VAE（具体的にはTaming TransformersのVQGANバリアント）によってトークン列にエンコードされる。画像をパッチ分割し、各パッチを固定サイズのコードブック内の最近傍ベクトルに置換することで、ピクセル空間の次元を圧縮する。このVQ-VAEは事前学習済みで、拡散モデルの学習中は凍結される。

【フォワードプロセス】
各潜在トークンは、ステップt-1からtへの遷移において3種類の状態変化を取る：(1)同じトークンのまま（確率αt+βt）、(2)別の潜在ベクトルにリサンプリング（各トークンへの確率βt）、(3)マスクトークンに変換（確率γt）。マスクされたトークンは以降マスクのまま保持される。制約式はαt + K·βt + γt = 1（Kは非マスクトークン数）。

【逆プロセスの近似】
エンコーダ・デコーダTransformerがx0の分布をプロンプトy条件付きで近似する。エンコーダはCLIPテキストエンコーダ（凍結）、デコーダTransformerはxtに対してグローバル自己注意を適用し、ベクトル埋め込みのカテゴリカル分布の対数確率を1回のフォワードパスで出力する。

【ARモデルとの比較】
自己回帰（AR）モデルと比較して、VQ-Diffusionは3つの問題点を改善している：(1)解像度増加に伴う線形的な推論速度低下、(2)誤差累積、(3)ラスタースキャン順序による方向バイアス。ARモデルが各ピクセルを逐次予測するのに対し、VQ-Diffusionはデコーダが全潜在トークンにグローバル注意を与えた上で一括予測する。

【連続拡散モデルとの比較】
連続拡散（DDPMなど）ではガウスノイズを加算し、U-Netでノイズを予測するのに対し、離散拡散ではノイズ予測の明確なアナログが存在しないため、x0分布を直接予測する方式が採用されている。離散拡散の先行研究としては、二項分布（Sohl-Dickstein 2015）、多項分布（Argmax Flows）、構造化ノイズ（D3PM）などが存在する。

【実装】
Hugging Faceのdiffusersライブラリに統合されており、VQDiffusionPipelineとして数行のコードで利用可能。モデルはmicrosoft/vq-diffusion-ithqとして公開、FP16対応あり。

## アイデア

- 離散潜在空間での拡散は「マスクトークン」という吸収状態を持つ有向遷移として定式化でき、連続ガウス拡散とは異なる数理構造（カテゴリカル分布上のマルコフ連鎖）を持つ点が興味深い
- 1回のフォワードパスで全トークンの事後分布を予測するため、ARモデルの逐次生成に比べて推論時の誤差累積が構造的に抑制される設計になっている
- テキスト条件付けにCLIPエンコーダを凍結したまま使用し、拡散デコーダのみを学習する構成は、事前学習済み表現の効率的な活用パターンとして参考になる

## 関連記事

- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1265 Würstchen：42倍圧縮による高速・低コスト画像生成拡散モデルの紹介
- /deep_1538 Japanese Stable Diffusion: 日本語特化テキスト-画像生成モデル
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[VQ-Diffusion：離散潜在空間における条件付き拡散モデル](https://huggingface.co/blog/vq-diffusion)
