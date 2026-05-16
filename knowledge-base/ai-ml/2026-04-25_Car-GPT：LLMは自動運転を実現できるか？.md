---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-25
tags: [LLM, 自動運転, End-to-End学習, Transformer, Perception, Planning, GPT-Driver, PromptTrack, BEV, Vision Transformer]
category: "ai-ml"
related: [216, 1855, 105, 694, 1638]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-25T12:45:21.647520"
---

## 要約

本記事は、The Gradientに掲載された2024年3月の解説記事で、LLM（大規模言語モデル）を自動運転車に適用する研究動向を概観する。自動運転の従来アーキテクチャは「モジュール型」（知覚・自己位置推定・計画・制御の4段階を個別モジュールで処理）だったが、2010年代後半からEnd-to-End学習（単一ニューラルネットで入力から操舵・加速を直接出力）が注目されてきた。そこにLLMという第三の選択肢が浮上している。LLMの基礎として、テキストをトークン（数値）に変換するTokenization、Encoder-Decoderまたはデコーダ単体で構成されるTransformerアーキテクチャ、そして次トークン予測による出力生成の仕組みを説明する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータに、出力を運転タスク（車線変更等）に置き換えるだけで同じTransformerブロックが機能する。研究が活発な4領域として、①Perception（環境記述）、②Planning（行動決定）、③データ生成（拡散モデルによる訓練データ合成）、④Q&A（シナリオへの質問応答）が挙げられる。具体的モデルとして、HiLM-D・MTD-GPTが画像から物体検出、PromptTrackがDETRとLLMを組み合わせてオブジェクトIDを継続追跡、BEV（鳥瞰図）ベースのPlanning研究ではGPT-Driver（GPT-4をプランナーとして使用）などが登場している。課題としては、LLMのトークン予測が確率的であり安全クリティカルなリアルタイム制御に求められる決定論的出力や低レイテンシとの相性が悪い点、センサーデータのトークン化コスト、学習データの不足などが指摘される。記事はペニシリン発見のアナロジーで「意外なブレークスルー」としてLLMを位置づけるが、技術的成熟度はまだ研究段階であり、商用自動運転への統合には多くのギャップが残るとまとめている。監査エージェント開発への示唆としては、LLMをコントローラとして使いつつ決定論的な安全制約を外部から課す「ハイブリッド設計」パターンが、監査ワークフローにおける判断の再現性確保にも応用可能。

## アイデア

- LLMのトークン予測は確率的であるため、安全クリティカルな制御系では決定論的出力を保証する外部制約レイヤーが必須という設計上の矛盾が、監査エージェントの判断担保にも同様に存在する
- GPT-Driverのように既存の強力な汎用LLM（GPT-4）をドメイン特化のプランナーとして転用するアプローチは、大量のドメインデータ収集コストを削減できる可能性がある
- PromptTrackのようにDETR等の専門モジュールとLLMを組み合わせる「ハイブリッドアーキテクチャ」は、完全End-to-Endと純粋モジュール型の中間として実用性が高く、エージェント設計全般に示唆がある

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **BEV（鳥瞰図表現）** (TODO: 読むべき)
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_1855 機械学習をコードとして扱う時代の到来
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_694 QUEST: クエリ変調球面アテンションによるロバストなアテンション定式化
- /deep_1638 Mamba解説：Transformerに挑む状態空間モデル（SSM）

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
