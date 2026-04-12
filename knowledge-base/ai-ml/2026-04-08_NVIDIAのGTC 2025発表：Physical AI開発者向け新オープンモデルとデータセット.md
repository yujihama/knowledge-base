---
title: "NVIDIAのGTC 2025発表：Physical AI開発者向け新オープンモデルとデータセット"
url: "https://huggingface.co/blog/nvidia-physical-ai"
date: 2026-04-08
tags: [Physical AI, World Foundation Model, Cosmos Transfer, Isaac GR00T N1, ControlNet, Diffusion Transformer, Vision-Language Model, ヒューマノイドロボット, 合成データ生成, LeRobot]
category: "ai-ml"
memo: "[HF Blog] NVIDIA's GTC 2025 Announcement for Physical AI Developers: New Open Models and Datasets"
processed_at: "2026-04-08T09:16:00.851638"
---

## 要約

NVIDIAはGTC 2025カンファレンスにて、Physical AI（物理世界で動作するAI）開発を加速する3つのオープンソースリリースを発表した。

**1. Cosmos Transfer（世界基盤モデル）**
70億パラメータのWorld Foundation Model（WFM）で、複数の制御入力（マルチコントロール）を受け付け、高忠実度の仮想世界シーンを生成する。入力タイプは3Dバウンディングボックスマップ、軌跡マップ、深度マップ、セグメンテーションマップなど多様。仕組みとして、センサーモダリティごとに個別のControlNetを訓練し、推論時に各制御ブランチの信号をAdaptive Spatiotemporal Control Mapで乗算・加算してTransformerブロックに注入する。出力は構造・外観を維持しつつ天候・環境を変化させたフォトリアルな動画シーケンスで、NVIDIA Omniverseと組み合わせてロボティクス・自動運転車向けの合成データ生成に活用可能。

**2. Physical AI Dataset（オープンデータセット）**
Hugging Face上で公開された商用グレードのデータセット。総量15TB、32万件以上のロボティクス訓練用トラジェクトリ、最大1,000件のUniversal Scene Description（OpenUSD）アセット（SimReadyコレクション含む）で構成。Cosmos Predictなどの基盤モデルのポストトレーニング用途に設計されており、LeRobotフォーマットと互換性を持つPyTorchスクリプトも提供。

**3. NVIDIA Isaac GR00T N1（ヒューマノイドロボット基盤モデル）**
Hugging Faceで公開された2Bパラメータのモデル（NVIDIA Isaac GR00T-N1-2B）で、汎用ヒューマノイドロボット推論・スキルのための世界初のオープン基盤モデルと位置づけられる。言語と画像のマルチモーダル入力を受け付け、Fourier GR-1や1X Neoなど複数のヒューマノイット機体に単一の重みセットで対応するクロスエンボディメントモデル。

アーキテクチャは人間の認知に着想を得たデュアルシステム構造：
- **System 2（VLM）**：NVIDIA-Eagle＋SmolLM-1.7Bベースで環境理解・言語指示の解釈・行動計画を担う「熟慮的思考」システム
- **System 1（Diffusion Transformer）**：System 2の計画を連続的なロボット動作に変換する「直感的行動」システム

訓練データは実キャプチャデータ、Isaac GR00T Blueprintによる合成データ、インターネット規模の動画データの組み合わせ。把持・両腕協調・物体受け渡しなど複雑なマルチステップタスクに対応し、マテリアルハンドリング・包装・検査用途に適する。

## アイデア

- デュアルシステム（System 1＝Diffusion Transformer による行動生成、System 2＝VLMによる計画立案）の分離アーキテクチャは、監査エージェントにおける「推論エージェント（LangGraph）」と「実行アクション（ツール呼び出し）」の役割分離設計に直接応用できる思想的フレームワーク
- Cosmos Transferの『センサーモダリティごとにControlNetを独立訓練し推論時に信号を合成する』手法は、複数の非同期データソース（財務データ・監査ログ・テキスト証跡）を統合するマルチモーダルRAGパイプラインの設計に示唆を与える
- 15TB・32万トラジェクトリという大規模ポストトレーニング用データセットをHugging Faceで公開した点は、Domain-specific LLMのファインチューニングにおけるデータ品質・規模感の基準として参考になる
## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1500 自宅でヒューマノイドロボットを訓練するギグワーカーたち
- /deep_1585 ヒューマノイドロボットをホームトレーニングするギグワーカーたち
- /deep_1123 ヒューマノイドロボットをギグワーカーが自宅で訓練する新たなデータ収集エコノミー
- /deep_1183 オープンLLMによるConstitutional AI（憲法的AI）の実装

## 原文リンク

[NVIDIAのGTC 2025発表：Physical AI開発者向け新オープンモデルとデータセット](https://huggingface.co/blog/nvidia-physical-ai)
