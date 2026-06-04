---
title: "Jetson AGX Orin(32GB) + Xavier(32GB) を繋いで、32GB超えのLLMをllama.cppで動かした話"
url: "https://zenn.dev/nooop/articles/785b7c511f991b"
date: 2026-06-04
tags: [llama.cpp, RPC分散推論, Jetson AGX Orin, Jetson AGX Xavier, MoE, Qwen3, ローカルLLM, CUDA, エッジAI]
category: "infra"
related: [6918, 2862, 2292, 5839, 6360]
memo: "[Zenn LLM] Jetson AGX Orin(32GB) + Xavier(32GB) を繋いで、32GB超えのLLMをllama.cppで動かした話"
processed_at: "2026-06-04T09:17:21.454376"
---

## 要約

Jetson AGX Orin（32GB, JetPack 6.2, CUDA 12.6, SM87 Ampere）とJetson AGX Xavier（32GB, JetPack 5.1.4, CUDA 11.4, SM72 Volta）の2台を有線LANで直結し、llama.cppのRPC分散推論機能を使って合計約60GBのメモリ空間でLLMを動作させた実験報告。

XavierはWiFiを持たないため、OrinをWiFiルーター兼ゲートウェイとして構成（iptables NATマスカレード＋IPフォワーディング）し、固定IP（Orin: 192.168.100.1、Xavier: 192.168.100.2）で接続した。

ビルドの最大の課題は2台でOSとCUDAバージョンが異なる点で、共通バイナリは利用不可。それぞれ`-DCMAKE_CUDA_ARCHITECTURES=72`（Xavier）と`=87`（Orin）を指定して個別ビルドした。分散推論のキーオプションは`-DLLAMA_RPC=ON`で、これによりrpc-serverとllama-cliのRPCクライアント機能が有効化される。

最初に試したQwen2.5 72B（Dense版, Q4_K_M, 約44GB）では生成速度2.5 t/sにとどまった。Denseモデルは全パラメータを毎回使用するため推論コストが高く、RPC経由のネットワーク帯域（1Gbps）と相まって低速になった。

次にMoE（Mixture of Experts）モデルであるQwen3-30B-A3B（総パラメータ30B、アクティブ3B）をBF16からQ8_0に量子化（約31GB）して試したところ、生成速度14.8 t/sを達成。Dense版比で約6倍の改善。MoEは推論時に一部のエキスパートのみ活性化するため、パラメータ数の割に計算量が少なく、エッジデバイスとの相性が良い。起動時にRPC経由でモデル転送が発生するため約15分を要した。

vllmはXavierのCUDA 11.4環境でビルドエラーとなり利用不可だったが、llama.cppは古いCUDAバージョンでも動作する点が強み。複数のRPCサーバーをチェーン接続することで更に大きいモデルへの拡張も可能な構成となっている。監査エージェント開発においてはオンプレミス多ノード推論構成の参考事例として有用であり、機密データをクラウド送信せずにローカルでLLMを動作させるアーキテクチャの実証例となる。

## アイデア

- OSとCUDAバージョンが異なる異種デバイス間でもllama.cppのRPCを使えば分散推論が可能で、SM番号を個別指定してビルドすれば統合メモリプールとして扱える
- DenseモデルよりMoEモデルの方がエッジデバイスのRPC分散環境に適しており、アクティブパラメータ比（3B/30B=10%）が低いほど帯域・計算の制約を回避しやすい
- RPCサーバーをチェーン接続すれば3台以上への拡張も可能で、廃棄予定の旧世代Jetsonをメモリ拡張ノードとして再活用できるコスト効率の高い構成

## 前提知識

- **llama.cpp RPC** (TODO: 読むべき)
- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)
- **CUDA SM アーキテクチャ** (TODO: 読むべき)
- **iptables NAT** (TODO: 読むべき)

## 関連記事

- /deep_6918 Jetson AGX XavierでQwen3.6-35B（MoE）をllama.cppで動かす
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_2292 8Bモデルが1GBに収まる1ビットLLM「Bonsai」を動かしてみた
- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略

## 原文リンク

[Jetson AGX Orin(32GB) + Xavier(32GB) を繋いで、32GB超えのLLMをllama.cppで動かした話](https://zenn.dev/nooop/articles/785b7c511f991b)
