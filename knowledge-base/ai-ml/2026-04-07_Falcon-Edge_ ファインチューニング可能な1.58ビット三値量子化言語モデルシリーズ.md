---
title: "Falcon-Edge: ファインチューニング可能な1.58ビット三値量子化言語モデルシリーズ"
url: "https://huggingface.co/blog/tiiuae/falcon-edge"
date: 2026-04-07
tags: [BitNet, 量子化LLM, 1bit-LLM, Falcon, エッジAI, SFT, TII-UAE, onebitllms, ternary-weights, モデル圧縮]
category: "ai-ml"
memo: "[HF Blog] Falcon-Edge: A series of powerful, universal, fine-tunable 1.58bit language models."
processed_at: "2026-04-07T21:35:24.378457"
---

## 要約

TII UAE（Technology Innovation Institute）が開発したFalcon-Edgeは、BitNetアーキテクチャをベースとした三値重み（{-1, 0, 1}）の言語モデルシリーズ。1Bおよび3Bパラメータの2サイズで提供され、それぞれベースモデルとインストラクションチューニング済みモデルが存在する。学習データは約1.5兆トークン（1.5 Tera Tokens）の内部データミックスを使用し、WSD学習率スケジューラで事前学習を実施。

最大の技術的特徴は「シングルトレーニングプロセスから複数形式を同時生成する新しい事前学習パラダイム」にある。一回の学習で、① bfloat16の通常モデル、② ネイティブBitNetモデル、③ ファインチューニング用の事前量子化済みBitNetモデル、の3種類を出力する。これはBitNet線形層における活性化量子化（int8スケールを用いた近似）の性質を利用した手法であり、事後量子化なしに重みスケールを注入することで非BitNetバージョンを近似できることを実験的に確認している。

Hugging Face Leaderboard v2のベンチマークにおいて、同規模の他モデルと同等以上の性能を示し、MicrosoftのBitNetモデルとの比較でも競争力のある結果を得た。

従来のBitNetリリースは量子化済みの推論専用モデルのみを公開していたが、Falcon-Edgeは事前量子化済み重み（`revision="prequantized"`）を公開することでファインチューニングを可能にした。`nn.Linear`層を`BitnetLinear`に置き換えることで継続事前学習やSFTが実行可能。

また、`onebitllms`という軽量Pythonパッケージを新たに提供し、TRL（SFTTrainer）等の既存ファインチューニングツールとの統合を容易にしている。モデルの読み込みはHugging Face transformersの`from_pretrained`に`revision`引数を指定するだけで対応可能。エッジデバイスへの展開を想定した「matmul-free」設計により、メモリ効率と推論速度の大幅な改善を実現している。

## アイデア

- 単一学習プロセスからbfloat16・ネイティブBitNet・事前量子化済みの3形式を同時生成するパラダイムは、量子化モデルの研究コストを大幅に削減する可能性がある
- 事前量子化済み重みの公開によりBitNetモデルのファインチューニングエコシステムが形成され始めており、特定ドメイン向け超軽量モデルの民主化が進む
- 1.58ビット三値重みによる「matmul-free」設計は、GPU非搭載のエッジデバイス（Raspberry Pi等）でのLLM実行を現実的にする技術的マイルストーンとなりうる
## 関連記事

- /deep_1249 スマホより小さい。1ビットLLMが「AIをどこでも動かす」時代を本当に変えるかもしれない話
- /deep_1147 Bonsaiが見せた1ビットの夢──PrismML 1-bit LLMが専用ハードウェアにもたらす構造的断絶
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_1528 補償ベースLLM量子化における残差誤差の再考
- /deep_154 ロボティクスAIを組み込みプラットフォームへ展開：データセット収録・VLAファインチューニング・オンデバイス最適化

## 原文リンク

[Falcon-Edge: ファインチューニング可能な1.58ビット三値量子化言語モデルシリーズ](https://huggingface.co/blog/tiiuae/falcon-edge)
