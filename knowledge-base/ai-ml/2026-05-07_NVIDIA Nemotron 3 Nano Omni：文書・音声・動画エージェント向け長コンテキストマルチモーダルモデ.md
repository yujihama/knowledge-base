---
title: "NVIDIA Nemotron 3 Nano Omni：文書・音声・動画エージェント向け長コンテキストマルチモーダルモデル"
url: "https://huggingface.co/blog/nvidia/nemotron-3-nano-omni-multimodal-intelligence"
date: 2026-05-07
tags: [Nemotron, マルチモーダルLLM, Mamba-SSM, MoE, 長コンテキスト, ASR, 動画理解, GUIエージェント, NVIDIA]
category: "ai-ml"
related: [2558, 346, 171, 714, 3482]
memo: "[HF Blog] Introducing NVIDIA Nemotron 3 Nano Omni: Long-Context Multimodal Intelligence for Documents, Audio and Video Agents"
processed_at: "2026-05-07T12:02:44.146857"
---

## 要約

NVIDIAが2026年4月28日に公開したNemotron 3 Nano Omniは、テキスト・画像・動画・音声を統合処理するオムニモーダル理解モデルで、パラメータ数は30B（Mixture-of-Expertsにより実効3B）。バックボーンはNemotron 3 Nano 30B-A3Bで、Mamba SSM層23個・MoE層23個（128エキスパート、top-6ルーティング）・グループクエリアテンション層6個を組み合わせたハイブリッドアーキテクチャを採用。視覚エンコーダにC-RADIOv4-H、音声エンコーダにParakeet-TDT-0.6B-v2を搭載し、それぞれ軽量プロジェクタ経由でLLMバックボーンに接続する。

文書理解では、従来のタイリング戦略を廃止し、ネイティブアスペクト比でのダイナミック解像度処理を導入。画像あたり1,024〜13,312ビジュアルパッチ（正方形換算で512×512〜1,840×1,840相当）を使用でき、100ページ超の長大文書を処理可能。MMlongbench-Docで57.5点（Qwen3-Omni 30B-A3Bの49.5を上回る）、OCRBenchV2-Enで65.8点を記録。

動画処理では、Conv3D Tubelet Embeddingにより連続2フレームを1トークンに統合してビジョントークン数を半減。推論時にはEVS（Efficient Video Sampling）で冗長な動画トークンをビジョンエンコーダ後に削減。Video-MMEで72.2点、WorldSenseで55.4点、DailyOmniで74.1点を達成。

音声面では、Parakeet-TDT-0.6B-v2が多様なアクセント・背景雑音下の長時間音声を処理。VoiceBenchで89.4点、HF Open ASR WERで5.95（Qwen3-Omniの6.55より低誤り率）。

エージェント用途として、GUIスクリーンショット解釈・UI状態監視・ワークフロー自動化を対象としたコンピュータユース機能を訓練済み。ScreenSpot-Proで57.8点、OSWorldで47.4点（従来版Nemotron Nano V2 VLの11.0から大幅向上）。

訓練レシピは多段階マルチモーダルアライメント→コンテキスト拡張→選好最適化→マルチモーダル強化学習の順で構成。効率面では同等インタラクティビティを持つ他のオムニモデルと比較して、マルチ文書用途で7.4倍、動画用途で9.2倍のシステムスループットを達成。BF16・FP8・NVFP4の3種類のチェックポイントをHuggingFaceで公開。

監査エージェント開発への示唆：100ページ超の契約書・コンプライアンス文書・財務報告書の解析に適したアーキテクチャであり、OCR精度とレイアウト理解を両立している点が内部監査ワークフローへの組み込みに有効。OSWorldスコア47.4はGUIエージェントとしての実用水準を示しており、監査証跡収集の自動化シナリオにも応用できる。

## アイデア

- Mamba SSM・MoE・グループクエリアテンションを1モデル内で組み合わせるハイブリッドアーキテクチャが、長コンテキストの効率と推論品質を同時に確保する設計として参考になる
- Conv3D Tubelet EmbeddingとEVSを組み合わせることでビジョントークン数を大幅削減しつつ動画品質を維持する手法は、トークン予算管理が重要なエージェントパイプラインに応用できる
- 多段階訓練（アライメント→コンテキスト拡張→選好最適化→マルチモーダルRL）の順序設計が、音声・動画などの新モダリティ追加時のファインチューニング戦略として参考になる

## 前提知識

- **Mixture-of-Experts** → /deep_134 大規模視覚言語モデルの継続的アンラーニング：概念分解による忘却対象の特定と拒否応答生成
- **Mamba SSM** (TODO: 読むべき)
- **Vision-Language Model** → /deep_498 Vision-Language Modelの埋め込み空間における意味的階層の説明・検証・アラインメント
- **Multimodal Alignment** (TODO: 読むべき)
- **RLHF/選好最適化** (TODO: 読むべき)

## 関連記事

- /deep_2558 オンデバイスストリーミングASRの限界に挑む：低レイテンシ推論向け高精度コンパクト英語モデル
- /deep_346 NVIDIAが600万件の多言語推論データセットを公開
- /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開
- /deep_714 Gemma 3：Googleの新マルチモーダル・多言語・長コンテキスト対応オープンLLM
- /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 原文リンク

[NVIDIA Nemotron 3 Nano Omni：文書・音声・動画エージェント向け長コンテキストマルチモーダルモデル](https://huggingface.co/blog/nvidia/nemotron-3-nano-omni-multimodal-intelligence)
