---
title: "NVIDIA Cosmos Reason 2：フィジカルAI向け高度推論VLMの最新版"
url: "https://huggingface.co/blog/nvidia/nvidia-cosmos-reason-2-brings-advanced-reasoning"
date: 2026-04-03
tags: [VLM, Physical-AI, NVIDIA-Cosmos, VLA, Robotics, Spatio-temporal-reasoning, OCR, Fine-tuning, Open-model]
category: "ai-ml"
memo: "[HF Blog] NVIDIA Cosmos Reason 2 Brings Advanced Reasoning To Physical AI"
processed_at: "2026-04-03T09:09:07.096601"
---

## 要約

NVIDIAは2026年1月5日、物理世界で動作するロボットやAIエージェント向けの推論型ビジョン言語モデル（VLM）「Cosmos Reason 2」をオープンモデルとして公開した。2Bと8Bの2種類のパラメータサイズを提供し、エッジからクラウドまで柔軟なデプロイに対応する。

前バージョン（Cosmos Reason 1）から主要な改善点は以下の通り。コンテキスト長が16Kトークンから256Kトークンへと16倍に拡張された。空間理解能力として2D/3D点位置特定、バウンディングボックス座標、軌跡データ、OCRサポートが新たに追加された。Physical AI BenchおよびPhysical Reasoningリーダーボードで1位を獲得し、視覚的理解のオープンモデル中でトップの精度を示している。

主要ユースケースは3つ。第1にビデオ分析AIエージェント：大量の映像データから洞察を抽出する用途で、SalesforceはCobaltロボットの映像をAgentforceとVSSブループリントを組み合わせて職場安全・コンプライアンス分析に活用している。第2にデータアノテーションと批評：UberはCosmos Reason 2を自動運転車（AV）の訓練データ向けキャプション生成に試験採用しており、Cosmos Reason 2-8Bをファインチューニングした結果、BLEUスコアが10.6%（0.113→0.125）、MCQ型VQAが0.67ポイント（80.18%→80.85%）、LingoQAが13.8%（63.2%→77.0%）改善された。第3にロボット計画・推論：ロボットグリッパーが実行すべきステップとJSON形式の軌跡座標を出力するVLA（Vision Language Action）モデルとして機能する。EncordはCosmos Reason 2をデータエージェントライブラリとAIデータプラットフォームにネイティブ統合している。

Cosmos Familyの他モデルとして、未来状態を映像として予測するCosmos Predict 2.5（2Bと14B）、シミュレーション映像をリアル環境へ変換するCosmos Transfer 2.5、ヒューマノイドロボット向け全身制御VLAのNVIDIA GR00T N1.6も同時に展開されている。Hugging Faceよりモデルをダウンロードでき、AWS・GCP・Azureでの提供も予定されている。

## アイデア

- 256Kトークンの長コンテキストにより、長尺ビデオの時系列推論が可能になった点：監視映像や業務プロセス動画全体を一括処理するエージェントへの応用可能性がある
- JSON形式で軌跡座標とステップを出力する設計：構造化出力をPydanticモデルと組み合わせることで、VLMの出力を下流エージェントが直接消費できるパイプラインが構築しやすくなる
- Uberのファインチューニング事例（LingoQA +13.8%）が示すように、汎用VLMをドメイン特化データで微調整することで垂直領域の精度を大幅改善できる：ドメイン適応の費用対効果を数値で示した具体例として参考になる
## 関連記事

- /deep_819 外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline
- /deep_986 ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介
- /deep_305 オープンモデルでOCRパイプラインを強化する：VLMベースドキュメントAIの実践ガイド
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_127 VLAモデルのための実用的なワールドモデルベース強化学習フレームワーク（VLA-MBPO）

## 原文リンク

[NVIDIA Cosmos Reason 2：フィジカルAI向け高度推論VLMの最新版](https://huggingface.co/blog/nvidia/nvidia-cosmos-reason-2-brings-advanced-reasoning)
