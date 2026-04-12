---
title: "Apple SiliconでCore MLを使ってStable Diffusionを動かす"
url: "https://huggingface.co/blog/diffusers-coreml"
date: 2026-04-10
tags: [Core ML, Stable Diffusion, Apple Silicon, Neural Engine, Diffusers, ローカルLLM, M1, Swift]
category: "infra"
memo: "[HF Blog] Using Stable Diffusion with Core ML on Apple Silicon"
related: [1444, 992, 1181, 1211, 1306]
processed_at: "2026-04-10T21:12:44.991832"
---

## 要約

AppleエンジニアがHugging Face Diffusersをベースに、Stable DiffusionモデルをCore ML形式へ変換・推論するスクリプトを公開した。対応モデルはSD v1.4、v1.5、v2 base、v2.1 baseで、変換済みウェイトがHugging Face Hubに公開されている。Core MLはCPU・GPU・Apple Neural Engine（NE）の全コンピュートユニットをサポートし、モデルの異なる部分を異なるハードウェアで実行することで性能を最大化できる。注目点はアテンション実装の2バリアント：'original'（CPU/GPUのみ対応）と'split_einsum'（全コンピュートユニット対応、Appleが導入）で、デバイスによってどちらが高速かは異なるため実測推奨。M1 Max（32 GPU cores、64GB）搭載MacBook Proでは、originalアテンション＋全コンピュートユニット＋macOS Ventura 13.1 Beta 4の組み合わせでSD v1.4による画像生成が18秒を達成。macOS Ventura 13.1未満では黒画像や著しい速度低下が発生するため注意が必要。モデル形式は用途別に分かれており、Pythonでの推論には'packages'形式、Swiftコードには事前コンパイル済みの'mlmodelc'形式（'compiled'）を使用する。Pythonでは`huggingface_hub`の`snapshot_download`でモデルをダウンロードし、Apple提供の`python_coreml_stable_diffusion.pipeline`スクリプトで推論を実行。`--compute-unit`オプションでALL/CPU_AND_GPU/CPU_ONLY/CPU_AND_NEを選択できる。Swift推論ではコンパイル済みモデルを用いるためモデルロード時の起動が高速。Dreambooth・Textual Inversion・ファインチューニングで作成したカスタムモデルも、Apple提供の変換スクリプトを使えばCore ML形式へ変換可能。後続としてMac App StoreアプリとSwiftソースコードも公開されており、ネイティブアプリとしてStable Diffusionをローカル実行できる環境が整備されている。

## アイデア

- CPU・GPU・Neural Engineをモデルの部位ごとに使い分ける'mixed compute unit'戦略は、異種ハードウェア構成での推論最適化の好例
- originalとsplit_einsumの2アテンション実装をバリアントとして並存させる設計は、ハードウェア依存の性能差をユーザー実測で解決するプラグマティックなアプローチ
- Pythonパッケージ（推論用）とコンパイル済みmlmodelc（Swift/アプリ用）を分けて配布することで、研究者とアプリ開発者の両ユースケースを単一リポジトリでカバーしている
## 関連記事

- /deep_1444 Swift Diffusers - Mac向け高速Stable Diffusion ネイティブアプリ
- /deep_992 WWDC 24: Core MLでMistral 7Bをオンデバイス実行する
- /deep_1181 SegMoE: Segmindによる拡散モデルのMixture of Experts フレームワーク
- /deep_1211 LCM LoRAによるSDXLの4ステップ高速推論
- /deep_1306 Intel CPU上でのStable Diffusionモデルのファインチューニング

## 原文リンク

[Apple SiliconでCore MLを使ってStable Diffusionを動かす](https://huggingface.co/blog/diffusers-coreml)
