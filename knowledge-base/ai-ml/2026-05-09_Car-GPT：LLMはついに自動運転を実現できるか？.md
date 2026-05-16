---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-09
tags: [LLM, 自動運転, Transformer, Vision Transformer, Perception, Planning, End-to-End学習, PromptTrack, GPT-4V]
category: "ai-ml"
related: [216, 2975, 1855, 105, 694]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-09T09:30:51.952476"
---

## 要約

本記事は、大規模言語モデル（LLM）が自動運転の4大モジュール（Perception・Localization・Planning・Control）に与える可能性を解説した入門的技術論考である。

自動運転の歴史的アプローチとして、2010年代に主流だった「モジュール型」（各機能を独立したモジュールに分割）と、それに代わる「End-to-End学習」（単一ニューラルネットワークで操舵・加速を直接予測するが、ブラックボックス問題を孕む）が紹介される。

LLMの基礎として、トークン化（テキストを数値IDに変換）・Transformerアーキテクチャ（エンコーダ・デコーダ構造、Multi-Head Attention）・次単語予測タスクが概説される。自動運転への適用では、画像・LiDAR点群・RADARデータもトークン化可能（Vision Transformerの応用）であり、Transformerコアは入力種別に依存しないため流用できる。

研究が活発な4領域が示される：
1. **Perception**：GPT-4 Visionによる物体検出・説明、HiLM-D・MTD-GPTによるマルチタスク検出、PromptTrack（DETRとLLMを組み合わせたオブジェクト追跡・ID付与）。
2. **Planning**：LLMがbird-eye-viewや知覚出力から「車線変更すべき」等の行動計画を生成。
3. **生成**：拡散モデルを用いたトレーニングデータ・代替シナリオの自動生成。
4. **Q&A**：シナリオに基づく対話インターフェース。

LLMの強みとして、自然言語による説明可能性（ブラックボックス問題の緩和）、Few-shot学習による少データ適応、コモンセンス推論の内包が挙げられる。一方、リアルタイム推論の計算コスト、センサーデータとのモダリティ統合の難しさ、安全クリティカル環境での信頼性確保が課題として残る。

監査エージェント開発への示唆：LLMをブラックボックスなEnd-to-Endモデルの説明層として外付けする設計思想は、監査AIにおいても「判断根拠の言語化」モジュールとして応用可能。PromptTrackのようにIDを付与してオブジェクトを追跡する手法は、監査ログ上のエンティティ追跡（取引・仕訳の同一性管理）への転用が考えられる。

## アイデア

- LiDAR点群・RADARデータもトークン化してTransformerに入力できるという発想は、監査ログや構造化データをLLMに食わせる際のモダリティ統合問題と同型であり、エンコード設計の参考になる
- PromptTrackのようにオブジェクトに一意IDを付与して追跡する手法は、監査エージェントが複数ステップにわたって同一エンティティ（取引・仕訳・承認者）を追跡するトレーサビリティ管理に直接応用できる
- ブラックボックスなEnd-to-Endモデルに対してLLMを「説明層」として外付けする設計は、既存の数値モデルや判定ルールに説明可能性を後付けする監査AI設計パターンとして有望

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **LiDAR点群** (TODO: 読むべき)

## 関連記事

- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_2975 正規化フリーTransformerの初期化時における劣臨界信号伝播
- /deep_1855 機械学習をコードとして扱う時代の到来
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_694 QUEST: クエリ変調球面アテンションによるロバストなアテンション定式化

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
