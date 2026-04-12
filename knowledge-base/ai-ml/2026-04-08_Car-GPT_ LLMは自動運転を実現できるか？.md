---
title: "Car-GPT: LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-04-08
tags: [自動運転, LLM, Transformer, Vision-Language Model, Perception, Planning, End-to-End学習, PromptTrack, HiLM-D, GPT-4V]
category: "ai-ml"
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-04-08T21:48:59.110652"
---

## 要約

本記事はThe Gradient掲載の解説記事（2024年3月）で、LLM（大規模言語モデル）が自動運転の4つの柱（Perception・Localization・Planning・Control）にどう応用できるかを論じる。

従来の自動運転アーキテクチャは「モジュラー型」（Perception→Localization→Planning→Controlを独立したモジュールで構成）と、近年台頭した「End-to-End学習」（単一のニューラルネットワークがステアリングや加速を直接予測）の2系統がある。後者はブラックボックス問題を抱える。そこに第三の道としてLLMの活用が模索されている。

LLMの基礎として、テキストをトークン（数値列）に変換するTokenization、Encoder-Decoder構造のTransformerアーキテクチャ（Multi-head Attention、Layer Normalizationなど）、そして次単語予測によるデコードの仕組みを解説する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADAR点群・アルゴリズム出力（レーン線、物体等）に置き換え、出力を運転タスク（車線変更指示など）にすることで既存のTransformerをほぼそのまま活用できる。

2023年の主要研究領域は以下の4つ：
1. **Perception**：GPT-4 Vision、HiLM-D、MTD-GPTが画像から物体・レーン等を検出・追跡。PromptTrackはDETRとLLMを組み合わせ、物体にユニークIDを付与する4D Perception的アプローチを実現。
2. **Planning**：Vision-Language ModelをPlanning層に統合し、鳥瞰図や知覚出力から「直進」「譲る」等の高レベル判断を生成。
3. **Generation**：Diffusionモデルを活用した学習用合成データ・シナリオ生成。
4. **Q&A**：チャットインターフェースを通じてシナリオへの質問応答を行う。

記事はLLMが自動運転の「予期せぬ解決策」（ペニシリン的発見の比喩）になりうると主張するが、実用化には計算コスト・リアルタイム性・安全性の課題が残る。モジュラー型からEnd-to-Endへ、さらにLLMベースの統合アーキテクチャへという流れは、特定ドメインへのLLM適用の汎用的なパターンとして注目される。

## アイデア

- モジュラー型→End-to-End→LLM統合という自動運転アーキテクチャの進化パターンは、監査エージェント設計における「ルールベース→ML→LLMエージェント」という移行と構造的に類似しており、アーキテクチャ選択の思考フレームとして参照できる
- PromptTrackのようにDETRなどの既存検出器とLLMを組み合わせてIDトラッキングを実現するアプローチは、専門ツール（既存の監査ロジック）とLLMを組み合わせるハイブリッドエージェント設計の具体例として示唆的
- 入力をトークン化すれば画像・LiDAR・センサーデータ等あらゆるモダリティをTransformerに入力できるという発想は、監査における財務データ・テキスト・ログ等の異種データをエージェントに統合するマルチモーダルRAG設計に応用できる

## Yujiの取り組みへの示唆

自動運転でのLLM活用アーキテクチャ（知覚→計画→制御の各モジュールをLLMで代替・補完）は、監査エージェントにおける「データ収集→リスク評価→判断→レポート生成」のパイプライン設計と構造的に対応する。特にLLMをPlanningレイヤーに組み込み高レベル判断を生成するアプローチは、LangGraphで構築中の監査エージェントのReActループにおけるルーティングや判断生成に転用できる。ただし自動運転特有の安全要件やリアルタイム性の議論が中心であり、監査ドメイン固有の示唆（説明可能性・証跡管理等）は少ないため、アーキテクチャパターンの参考として位置づけるのが適切。

## 原文リンク

[Car-GPT: LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
