---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-16
tags: [LLM, 自動運転, Transformer, Vision Transformer, End-to-End学習, Perception, Planning, GPT-4 Vision, HiLM-D, PromptTrack]
category: "ai-ml"
related: [216, 4906, 2975, 1855, 105]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-16T21:23:03.688445"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転に応用する研究動向を解説した2024年3月の解説記事である。自動運転の従来アーキテクチャは「モジュラー型」（Perception・Localization・Planning・Controlの4モジュール分離）と「End-to-End学習」（単一ニューラルネットワークで操舵・加速を直接予測）に大別されるが、いずれも完全自動運転を実現できていない。そこへLLMを第三の解法として位置づけ、その可能性を検討する。LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoder構造のTransformerモデル、次単語予測（Next-Word Prediction）の3要素を説明する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータ等に変換（Vision Transformerが担当）し、Transformerはトークン列を処理するため入力の種類に依存しない構造を維持できる。研究が活発な適用領域は4つ：（1）Perception（画像から物体・車線等を検出・追跡。GPT-4 Vision、HiLM-D、MTD-GPT、PromptTrackなどのモデルが対応）、（2）Planning（鳥瞰図や知覚出力から「車線変更すべきか」等の行動を記述。DriveGPT4などが対象）、（3）Generation（Diffusionモデルによる訓練データやシナリオの自動生成）、（4）Q&A（シナリオに基づく対話インターフェース）。LLMの強みとして挙げられるのは、膨大なテキストコーパスから学習した「常識的推論能力」であり、エッジケースへの対応においてルールベースシステムより柔軟に振る舞える可能性がある。一方、課題はリアルタイム処理の遅延（LLMの推論速度は走行制御に求められるミリ秒単位の応答に不向き）、センサーデータのトークン化における情報損失、および安全性の保証（ハルシネーションが致命的事故につながるリスク）である。記事はLLMを自動運転の「銀の弾丸」とは見なさず、既存モジュールとの組み合わせにより特定サブタスク（特にPlanningとQ&A）で補完的役割を果たす可能性を示す。監査エージェント開発への示唆として、LLMをEnd-to-Endで意思決定に使うのではなく、知覚・計画・制御を分離し各段階でLLMを補助的に組み込むモジュラー設計の有効性は、LangGraphベースの監査エージェント設計にも応用可能である。特にPlanningノードにLLMを用いて「次に何を検査すべきか」を推論させる構成は直接的な類推として参考になる。

## アイデア

- LLMの「常識推論」をPlanningモジュールに限定適用することで、End-to-Endのブラックボックス問題を回避しつつ柔軟な意思決定を実現できる設計思想は、監査エージェントのReActループ設計に直接転用可能
- Vision TransformerによるLiDAR・RADAR点群のトークン化は、テキスト以外のマルチモーダルデータをLLMパイプラインに統合する汎用的手法であり、監査ログや数値データのトークン化にも応用できる
- GPT-4 Visionを用いた物体検出（PromptTrackのID付きトラッキング含む）は、LLMが従来の特化型モデル（DETR等）と組み合わせることで実用的な検出精度を達成できることを示しており、専用モデルとLLMのハイブリッド設計の有効性を示す

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **LiDAR点群** (TODO: 読むべき)

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_4906 連載｜生成AIの数理 第1回「次の言葉」を予測せよ ——n-gramからアテンションまで，必然の連鎖——
- /deep_2975 正規化フリーTransformerの初期化時における劣臨界信号伝播
- /deep_1855 機械学習をコードとして扱う時代の到来
- /deep_105 TransformerでAttention Residualsを観察する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
