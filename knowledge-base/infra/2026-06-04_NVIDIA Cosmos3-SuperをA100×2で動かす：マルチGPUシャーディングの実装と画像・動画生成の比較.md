---
title: "NVIDIA Cosmos3-SuperをA100×2で動かす：マルチGPUシャーディングの実装と画像・動画生成の比較"
url: "https://zenn.dev/ollo/articles/6490f9cbe5494a"
date: 2026-06-04
tags: [Cosmos3-Super, Mixture-of-Transformers, Diffusion Transformer, マルチGPUシャーディング, Text-to-Image, Image-to-Video, A100, diffusers, device_map, BF16]
category: "infra"
related: [1572, 1302, 1495, 1275, 1306]
memo: "[Zenn LLM] NVIDIA Cosmos3-SuperをA100で動かす / 画像・動画生成をGeminiと比較"
processed_at: "2026-06-04T09:16:12.938694"
---

## 要約

2026年5月末にリリースされたNVIDIA Cosmos3-Superは、Mixture-of-Transformers（MoT）とDiffusion Transformerを組み合わせた約65Bパラメータの生成基盤モデルで、Text-to-Image（T2I）とImage-to-Video（I2V）の2タスクに対応する。BF16での重みが約130GB（T2I: 132GB、I2V: 131GB）あるため、A100-80GB×1枚には搭載不可で、本記事では2枚（合計160GB）へのシャーディング手法を詳述している。

マルチGPUロードで試みた「device_map='balanced'」はコンポーネント単位の配置しかできず、124GBの単一transformerがCPUにオフロードされ40秒/ステップという実用不可な速度となった。「device_map='auto'」での自動分割は、embed_tokens/proj_in/time_embedderなどの前処理モジュールがcuda:0とcuda:1に分散してデバイス不一致エラーを引き起こした。

最終的に有効だったのは手動device_mapで、前後処理モジュール（embed_tokens, proj_in, proj_out, time_embedder, norm, lm_head等）をすべてcuda:0に集約し、64ブロックのうち中央34ブロックのみをcuda:1に配置する方法。これによりcuda:0≒63GB、cuda:1≒67GBでCPUオフロードなしの安定動作を実現した。VAE・vision_encoder・sound_tokenizerはlatentと同一デバイス（cuda:0）に揃える必要もある。

生成パラメータはT2Iが1024×1024・50ステップ・guidance_scale=4.0、I2Vが480p（480×832）・189フレーム（約8秒@24fps）・50ステップ・guidance_scale=6.0。速度はT2Iが約43秒/枚（1.18 it/s）、I2Vが約16分/本（18.9 s/it＋VAEデコード）。

製造業（CNCマシニングセンタ、アーク溶接ロボット）をテーマとした生成物をNano Banana Pro（静止画）とVeo 3.1（動画）と比較した結果、Cosmos3-Superはローカル動作モデルでありながら商用クラウドモデルと同水準のクオリティを達成している。株式会社Olloは異常検知・マニュアル自動作成AIを開発しており、このモデルのファインチューニングによる自社プロダクト精度向上を目指す。

監査エージェント開発への直接的示唆は少ないが、大規模マルチモーダルモデルの手動シャーディング手法は、同様の65B超モデルをオンプレミスGPUクラスタで運用する際に汎用的に応用できる実装パターンである。

## アイデア

- device_map='auto'/'balanced'が65B超モデルでは機能しない理由が具体的に示されており、前後処理モジュールの同一デバイス集約という手動シャーディングのパターンは他の大規模モデル運用にも応用可能
- MoT（Mixture-of-Transformers）＋Diffusion Transformerという組み合わせにより、テキスト・画像・動画・音声を単一バックボーンで扱いながら複数タスク派生モデルを提供するアーキテクチャ設計が、フィジカルAI向け基盤モデルとしてどのような優位性を持つか
- 製造業特化のユースケース（CNC加工・溶接ロボット）でVeo 3.1と同水準の結果をローカルで達成できることは、工場現場のセキュリティ要件（データ外部送信不可）に応えるオンプレ生成AIの実用可能性を示している

## 前提知識

- **Diffusion Transformer** → /deep_712 NVIDIAのGTC 2025発表：Physical AI開発者向け新オープンモデルとデータセット
- **Mixture-of-Transformers (MoT)** (TODO: 読むべき)
- **device_map / モデルシャーディング** (TODO: 読むべき)
- **BF16 量子化** (TODO: 読むべき)
- **diffusers ライブラリ** (TODO: 読むべき)

## 関連記事

- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1495 VQ-Diffusion：離散潜在空間における条件付き拡散モデル
- /deep_1275 PyTorch FSDPを使ったLlama 2 70Bのファインチューニング
- /deep_1306 Intel CPU上でのStable Diffusionモデルのファインチューニング

## 原文リンク

[NVIDIA Cosmos3-SuperをA100×2で動かす：マルチGPUシャーディングの実装と画像・動画生成の比較](https://zenn.dev/ollo/articles/6490f9cbe5494a)
