---
title: "Gemma 4の4種類のモデルを整理：Dense・MoE・PLEアーキテクチャの違い"
url: "https://zenn.dev/tasshi441/articles/8a80daffac2556"
date: 2026-05-28
tags: [Gemma4, MoE, PLE, ローカルLLM, オープンウェイト, Instruction-Tuning, エッジデバイス, vLLM]
category: "ai-ml"
related: [6668, 859, 2056, 5266, 1420]
memo: "[Zenn LLM] Gemma 4が4種類もあって混乱したので整理してみた！"
processed_at: "2026-05-28T21:03:45.494939"
---

## 要約

GoogleがGoogle 2026年4月にリリースしたオープンウェイトLLM「Gemma 4」には、アーキテクチャと用途が異なる4つのモデルが存在する。

**Gemma 4 31B**はDenseアーキテクチャ（標準的なTransformer）で、全31Bパラメータを毎トークン使用する。8bit量子化時で31GBのVRAM/RAMが必要で、リクエスト数が少なく出力品質が重要な用途向け。

**Gemma 4 26B A4B**（Active 4B）はMoE（Mixture of Experts）アーキテクチャで、128個のエキスパートのうち毎トークン8個のみをアクティブにする。総重みは26B（26GB必要）だが、推論時は実質4B相当の計算量で動作するため、26B級の品質を4B級の速度で実現する。セルフホストでAPIライクな用途に最適。

**Gemma 4 E4B**（Effective 4B）はPLE（Per-Layer Embeddings）アーキテクチャを採用。総パラメータは8Bだが、各レイヤーに専用のエンベディングテーブルを持たせ必要な値をlookupするだけにすることで実行時の計算負荷を4B相当に抑える。モデルサイズが8Bと軽量なためスマートフォン（iPhone 17 Proで動作確認済み）でも高速動作する。ファインチューニングによるタスク特化が期待される。

**Gemma 4 E2B**（Effective 2B）も同じPLEアーキテクチャで、総パラメータ約5B・実行時2B。Raspberry Piなどエッジデバイス向けで、ネットワーク制約環境やレイテンシ最優先のユースケースに特化。

各モデル名の末尾に「it」（Instruction-Tuned）が付くバリアントも存在し、事前学習のみのベースモデルと区別される。実用では「it」サフィックス付きを使えばよい。

MoEとPLEはどちらも「実行時アクティブパラメータを削減する」点で共通するが、仕組みが異なる。MoEは複数エキスパートの選択的活用、PLEはレイヤー固有エンベディングによる計算量圧縮である。監査エージェント開発への示唆としては、Gemma 4 E4Bをタスク特化型にファインチューニングすることで、高速・低コストかつ本番環境に耐えうる推論エンジンを構築できる可能性がある。単一責任原則でエージェントを分割し、各タスクに特化した小型モデルを割り当てるアーキテクチャと相性が良い。

## アイデア

- PLE（Per-Layer Embeddings）はMoEとは異なるアプローチで実行時計算量を削減する手法で、エッジデバイスへの展開を念頭に設計されている点が独自
- Gemma 4 E4Bをタスクごとにファインチューニングしてエージェントのサブタスク担当モデルとして使う構成は、低VRAMでの本番運用を現実的にする
- 「モデル総パラメータ数」と「実行時アクティブパラメータ数」を区別して命名するGemma 4の命名規則（A4B, E4B）は、モデル選定時のVRAM見積もりと推論速度を正確に把握するための実用的なフレームワークになっている

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **Instruction Tuning** → /deep_2008 舗装状態評価に特化したVision-Language基盤モデル：PaveGPTとPaveInstructデータセット
- **量子化（Quantization）** (TODO: 読むべき)
- **ファインチューニング** → /deep_530 AIモデルカスタマイズへの移行はアーキテクチャ上の必須事項

## 関連記事

- /deep_6668 M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査
- /deep_859 Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル
- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較
- /deep_5266 13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証

## 原文リンク

[Gemma 4の4種類のモデルを整理：Dense・MoE・PLEアーキテクチャの違い](https://zenn.dev/tasshi441/articles/8a80daffac2556)
