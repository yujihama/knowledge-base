---
title: "SegMoE: Segmindによる拡散モデルのMixture of Experts フレームワーク"
url: "https://huggingface.co/blog/segmoe"
date: 2026-04-09
tags: [MoE, Stable Diffusion, SDXL, 画像生成, モデルマージ, diffusers, sparse-MoE, mergekit]
category: "ai-ml"
memo: "[HF Blog] SegMoE: Segmind Mixture of Diffusion Experts"
processed_at: "2026-04-09T21:03:06.079579"
---

## 要約

SegMoEは、Stable Diffusion系の画像生成モデルに対してMixture of Experts（MoE）アーキテクチャを適用するフレームワーク。Mixtral 8x7bと同様の設計思想で、複数の事前学習済みモデルをエキスパートとして組み合わせ、Feed-Forward層・Attention層・またはその両方をスパースなMoE層に置き換える。ルーターネットワークがトークンごとに最適なエキスパートを選択して処理する仕組み。

リリースされたモデルは3種類：SegMoE-2x1（2エキスパート・1つを使用）、SegMoE-4x2（4エキスパート・2つを使用）、SegMoE SD 4x2（Stable Diffusion 1.5ベースの4エキスパート）。SegMoE-4x2は24GBのVRAM（半精度）を必要とする。

独自MoEモデルの作成はconfig.yamlを定義してCLIコマンド`segmoe config.yaml segmoe_v0`を実行するだけで完了。設定ではベースモデル・エキスパート数・使用レイヤー種別（ff/attn/all）・トークンあたりエキスパート数を指定し、各エキスパートにはゲート重み計算用のポジティブ/ネガティブプロンプトを付与する。Hugging FaceモデルとCivitAIモデルの両方をエキスパートとして利用可能。

Hugging Face Diffusersエコシステムに完全統合されており、`segmoe`パッケージ経由でSegMoEPipelineを使ってSDXL同等の推論APIで利用可能。コードの類似性から設計思想はmergekit（LLM向けモデルマージライブラリ）を参考にしている。

比較実験では「three green glass bottles」「panda bear with aviator glasses」等のプロンプトに対してベースモデル（RealVisXL_V3.0）よりプロンプト理解精度が向上することを確認。デメリットとして、エキスパート数増加による推論速度低下と高VRAM要求（複数GPU環境向き）が挙げられる。Apache 2.0ライセンスで公開。

## アイデア

- ゲート重み計算にポジティブ/ネガティブプロンプトを使う設計は、各エキスパートの得意ドメインを自然言語で定義できる点が実用的。LLMのMoEとは異なりプロンプト意味空間でルーティングを学習させる手法
- Feed-Forward層・Attention層・全層の3モードでMoE化する粒度を選べる設計は、モデル容量と推論コストのトレードオフを細かく制御できる
- 複数の特化済みモデルを追加学習なしに組み合わせてアンサンブル効果を得る手法は、ドメイン特化エキスパートを事後的に統合するアーキテクチャパターンとして汎用性がある

## Yujiの取り組みへの示唆

監査エージェント開発への直接的な関連は薄いが、「複数の特化エキスパートをルーターで動的に切り替える」というMoEの設計思想はLangGraphのマルチエージェント構成と概念的に類似している。各エージェントをドメイン特化エキスパートとして定義し、入力の性質に応じてルーティングするアーキテクチャ設計の参考になる可能性がある。また、プロンプトベースでゲート重みを定義する手法は、LLM-as-judgeでエージェントの専門性を言語的に指定するアプローチへの示唆を含む。

## 原文リンク

[SegMoE: Segmindによる拡散モデルのMixture of Experts フレームワーク](https://huggingface.co/blog/segmoe)
