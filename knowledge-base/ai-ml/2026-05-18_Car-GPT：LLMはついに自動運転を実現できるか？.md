---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-18
tags: [LLM, 自動運転, Transformer, Vision-Language Model, End-to-End学習, Perception, Planning, LanguageMPC, PromptTrack]
category: "ai-ml"
related: [216, 4906, 105, 1638, 672]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-18T21:10:19.493603"
---

## 要約

自動運転の従来アーキテクチャは、Perception（環境認識）、Localization（自己位置推定）、Planning（経路計画）、Control（制御命令生成）の4モジュールに分割するモジュラーアプローチが主流だった。2010年代後半からEnd-to-Endニューラルネットワークによるアプローチが注目されたが、ブラックボックス問題が残存している。本記事は、LLM（大規模言語モデル）をこれらのモジュールに適用する可能性を解説する。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoderまたは純Decoderで構成されるTransformerアーキテクチャ（Multi-head Attention、Layer Normalizationを含む）、次単語予測タスクを説明する。自動運転への適用では、入力を画像・LiDAR点群・RADARデータに、出力を運転タスク（レーン変更等）に置き換えることで、同一Transformerアーキテクチャを流用できる。

Perceptionへの応用例として、GPT-4 VisionによるBounding Box生成、HiLM-DやMTD-GPTによるビデオ対応検出、PromptTrack（DETRとLLMを組み合わせ、各オブジェクトにユニークIDを付与するトラッキング）が挙げられる。

Planningへの応用では、LanguageMPC（LLMがコスト関数を生成し、MPCが最適軌道を計算する）、DriveVLM（Vision-Language Modelを用いた鳥瞰図からの意思決定）、DiMA（Diffusionモデルによるシナリオ生成でトレーニングデータを拡充）などが研究されている。

Q&Aインターフェースとして、ドライバーがシナリオについて質問できるチャットUIの実現可能性も示されている。

LLMの自動運転への統合における主な課題は、(1) リアルタイム推論の計算コスト（現状のLLMは低レイテンシ要件を満たさない）、(2) センサーデータ（LiDAR等）のトークン化効率、(3) ハルシネーションによる誤判断リスク、の3点である。現時点ではLLMは既存モジュールの完全代替ではなく、高次の推論・説明生成・エッジケース対応において補完的な役割を担うと位置づけられる。監査エージェント開発への示唆として、LLMをEnd-to-Endで意思決定に用いるのではなく、LanguageMPCのようにLLMが目的関数や評価基準を生成し、最適化ソルバーが実行する「LLM-as-Planner」パターンは、監査判断プロセスの透明性確保に応用可能。

## アイデア

- LanguageMPCパターン：LLMがコスト関数を生成しMPC（モデル予測制御）が最適化を担う分業構造は、監査エージェントでLLMが評価基準を動的生成しソルバーが判断する設計に転用できる
- PromptTrackのようにオブジェクトにユニークIDを付与し追跡するアプローチは、監査証跡において特定リスク項目を跨がって追跡するエンティティ管理に応用できる
- DiMAのようなDiffusionモデルによる合成シナリオ生成でトレーニングデータを拡充する手法は、監査エージェントのエッジケース（不正パターン等）のデータ不足問題に対応可能

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **MPC（モデル予測制御）** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusionモデル** → /deep_3423 LLMs+：今AIで重要な10のこと

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_4906 連載｜生成AIの数理 第1回「次の言葉」を予測せよ ——n-gramからアテンションまで，必然の連鎖——
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_1638 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- /deep_672 Mambaの解説：Transformerに挑む状態空間モデル

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
