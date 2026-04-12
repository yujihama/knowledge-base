---
title: "GraphcoreとHugging FaceがIPU対応Transformerモデル群を大幅拡充"
url: "https://huggingface.co/blog/graphcore-update"
date: 2026-04-12
tags: [Hugging Face Optimum, IPU, Graphcore, Transformer, ViT, BERT, T5, BART, Wav2Vec2, HuBERT, Bow IPU, Poplar SDK]
category: "infra"
memo: "[HF Blog] Graphcore and Hugging Face Launch New Lineup of IPU-Ready Transformers"
processed_at: "2026-04-12T09:11:42.557300"
---

## 要約

GraphcoreとHugging Faceは、オープンソースのパフォーマンス最適化ライブラリ「Hugging Face Optimum」において、IPU（Intelligence Processing Unit）対応モデルを10種類に拡充した（2022年5月）。当初はBERTのみだったが、NLP・音声・画像認識の3モダリティにわたる以下のモデルが追加された。

【NLP】GPT-2（自己回帰型テキスト生成）、RoBERTa（MLM事前学習）、DeBERTa（分離注意機構＋強化マスクデコーダによるBERT改良版）、BART（双方向エンコーダ＋自己回帰デコーダのseq2seqモデル）、LXMERT（視覚・言語クロスモーダルエンコーダ）、T5（テキストtoテキスト統一フレームワーク）。【画像】ViT（Vision Transformer、画像をパッチ分割してTransformerで処理）。【音声】HuBERT（自己教師あり音声認識、Librispeech 960hベンチマークでwav2vec 2.0同等以上）、Wav2Vec2（対照学習による自己教師あり音声表現学習）。

各モデルにはIPU設定ファイルと事前学習済み重みが同梱され、コード変更なしで利用可能。Graphcoreの新ハードウェア「Bow IPU」（WoW 3D積層技術採用、最大350テラFLOPS、前世代比40%性能向上・16%省電力化）への移行も既存コードのまま対応できる。ソフトウェア面ではPoplar SDK 2.5がリリースされ、PyTorchやTensorFlowとの統合が強化された。

Hugging Face Hubの数千のデータセットにも同時アクセス可能であり、ファインチューニングのエンドツーエンドワークフローをIPU上で低コードで実現できる点が実用上の最大の価値。サイバーセキュリティ、音声通話自動化、創薬、翻訳など多様な産業応用が想定される。監査エージェント開発への示唆としては、BARTやT5のような汎用seq2seqモデルをIPU上で効率的にファインチューニングすることで、監査レポート要約・異常検知テキスト分類などのタスクを低レイテンシで処理するパイプライン構築の参考になる。

## アイデア

- WoW（Wafer-on-Wafer）3D積層技術によりチップ面積を増やさずに350テラFLOPSを達成しており、GPU以外のAIアクセラレータのアーキテクチャ多様化の具体例として注目に値する
- Optimumの設計思想（IPU設定ファイルをモデルに同梱）により、ハードウェア最適化の知識がなくてもスペシャリストが作成した設定を再利用できる「最適化の民主化」モデルは、エージェントシステムのツール設計にも応用できる
- LXMERTのようなクロスモーダルアーキテクチャ（テキスト・画像・物体関係の3エンコーダ統合）は、監査文書とスキャン画像を同時処理するマルチモーダル監査エージェントの将来的な基盤技術となり得る

## 前提知識

- **Transformer** → [LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する](../ai-ml/2026-03-29_LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する.md)
- **BERT** → [DariMis: YouTubeにおけるダリ語偽情報検出のためのハーム認識モデリング](../ai-ml/2026-03-30_DariMis_ YouTubeにおけるダリ語偽情報検出のためのハーム認識モデリング.md)
- **自己教師あり学習** → [LeWorldModel入門: 15Mパラメータで実現するJEPAベースWorld Model](../ai-ml/2026-04-03_LeWorldModel入門_ 15Mパラメータで実現するJEPAベースWorld Model.md)
- **seq2seq** → [【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜](../ai-ml/2026-04-02_【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えた.md)
- **IPU / AIアクセラレータ** (TODO: 読むべき)

## 関連記事

- [ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド](../ai-ml/2026-04-11_ビジョントランスフォーマー（ViT）をHugging Face Optimum Graphcoreで活用する詳細ガイド.md)
- [高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較](../infra/2026-04-10_高速トレーニングと推論_ Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較.md)
- [TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化](../infra/2026-04-07_TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化.md)
- [AWS Inferentia2でHugging Face Transformersを高速化する](../infra/2026-04-10_AWS Inferentia2でHugging Face Transformersを高速化する.md)
- [🤗 TransformersによるProbabilistic時系列予測](../ai-ml/2026-04-10_🤗 TransformersによるProbabilistic時系列予測.md)

## 原文リンク

[GraphcoreとHugging FaceがIPU対応Transformerモデル群を大幅拡充](https://huggingface.co/blog/graphcore-update)
