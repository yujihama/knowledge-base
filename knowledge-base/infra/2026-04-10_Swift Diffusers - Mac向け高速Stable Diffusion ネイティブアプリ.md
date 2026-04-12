---
title: "Swift Diffusers - Mac向け高速Stable Diffusion ネイティブアプリ"
url: "https://huggingface.co/blog/fast-mac-diffusers"
date: 2026-04-10
tags: [Core ML, Stable Diffusion, Apple Silicon, Neural Engine, Swift, 画像生成, ローカル推論]
category: "infra"
memo: "[HF Blog] Swift 🧨Diffusers - Fast Stable Diffusion for Mac"
related: [1493, 992, 1181, 1211, 1489]
processed_at: "2026-04-10T12:36:56.104779"
---

## 要約

HuggingFaceが2023年2月にリリースしたMac向けネイティブ画像生成アプリ「Diffusers for Mac」のバージョン1.1に関するブログ記事。PythonのDiffusersライブラリのMac対応版として位置づけられ、PyTorchモデルではなくAppleのCore MLフォーマットに変換されたモデルを使用することが最大の特徴。Core MLはCPU・GPU・Neural Engine（ANE）を同時に活用でき、Core MLフレームワークが自動的に最適なデバイス割り当てを行う。PyTorchのmpsデバイスはNeural Engineを使用できないため、Core ML採用による性能優位性がある。

ベンチマーク結果によると、Stable Diffusion 1.5をM1 8GBで実行した場合、GPU使用時は32.9秒、ANE使用時は18.8秒。M1 Max 64GBではGPU使用時9秒、ANE使用時20.4秒と逆転現象が起きており、これはM1 MaxがGPUコアを32基（標準M1の4倍）持つのに対しNeural Engineのコア数は同じ16基であることに起因する。一方、標準M1チップ搭載のMac MiniではANEがGPUの約2倍高速という結果が出ている。GPU＋ANEの併用は、それぞれ単独使用の最良値を超えないことも確認された。バージョン1.1では実行環境のハードウェア構成に基づき最適アクセラレータを自動選択する機能が追加された。

アプリはSwift・SwiftUIで実装されておりオープンソース（MITライセンス相当）。ローカル実行のためプロンプトや生成画像は外部に送信されないプライバシー保護が保証される。UIにはguidance scale設定、シード再利用ショートカット、モデルダウンロードインジケーター、安全チェッカーの無効化オプションが追加された。将来的にはHubからのDreambooth・ファインチューニング済みモデルへのアクセス機能、iOS/iPadOS版のリリースが計画されている。

## アイデア

- CPU・GPU・Neural Engineをフレームワーク側が自動分割して並列実行するCore MLのアーキテクチャは、ヘテロジニアスコンピューティングの実用例として興味深い
- 同一チップファミリーでもGPUコア数の差（M1: 8コア vs M1 Max: 32コア）がANE/GPU最適戦略の分岐点になるという実測データは、ハードウェア選定の指標として有用
- PyTorchモデルをCore ML形式に変換してデプロイするパイプラインは、エッジデバイス向けモデル配布の汎用パターンとして参照できる

## 関連記事

- /deep_1493 Apple SiliconでCore MLを使ってStable Diffusionを動かす
- /deep_992 WWDC 24: Core MLでMistral 7Bをオンデバイス実行する
- /deep_1181 SegMoE: Segmindによる拡散モデルのMixture of Experts フレームワーク
- /deep_1211 LCM LoRAによるSDXLの4ステップ高速推論
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較

## 原文リンク

[Swift Diffusers - Mac向け高速Stable Diffusion ネイティブアプリ](https://huggingface.co/blog/fast-mac-diffusers)
