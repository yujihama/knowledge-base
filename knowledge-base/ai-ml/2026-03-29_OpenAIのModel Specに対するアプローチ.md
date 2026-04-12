---
title: "OpenAIのModel Specに対するアプローチ"
url: "https://openai.com/index/our-approach-to-the-model-spec"
date: 2026-03-29
tags: [ModelSpec, RLHF, RLAIF, alignment, AI-safety, operator-user, value-alignment, Constitutional-AI]
category: "ai-ml"
memo: "[OpenAI Blog] Inside our approach to the Model Spec"
processed_at: "2026-03-29T22:47:48.330050"
---

## 要約

OpenAIのModel Spec（モデル仕様書）は、ChatGPTをはじめとするOpenAIのAIモデルが「どのように振る舞うべきか」を定めた公式ガイドラインである。本ページはそのアプローチを解説している。

Model Specの核心は、AIモデルが従うべき優先順位の階層構造にある。優先度の高い順に「Broadly safe（広義の安全性）」「Broadly ethical（倫理的行動）」「Adherent to OpenAI's principles（OpenAIの原則への準拠）」「Genuinely helpful（真の有用性）」の4層で構成される。

「Broadly safe」は、現在のAI開発段階において人間による監督・制御を支持することを意味する。モデルが誤った価値観を持つ可能性を考慮し、人間がAIの行動を修正・訂正できる体制を維持することを最優先とする。これはモデルが自律的に判断して人間の制御を迂回することを明示的に禁じている。

「Genuinely helpful」については、過度に慎重な拒否（over-refusal）を避けることを強調している。「賢い友人」のメタファーを用い、法律家・医師・金融アドバイザー等の専門家が知人に対して率直に情報提供するように、ユーザーに実質的な価値を届けることを目指す。

Operator（API利用者・企業）とUser（エンドユーザー）の権限分離も重要な概念である。OperatorはSystem Promptを通じてモデルの挙動をカスタマイズでき、UserはOperatorが許可した範囲内でさらに調整できる。モデルはこの権限階層を遵守する。

RLHF（人間フィードバック強化学習）やRLAIF（AI フィードバック強化学習）との関係では、Model Specがアノテーターや評価AIへの指示書として機能し、トレーニングデータの品質基準を定める。これにより、モデルの価値観をスケーラブルに形成する仕組みとなっている。

また「Default behaviors」と「Non-default behaviors」の概念を導入し、文脈に応じた柔軟な振る舞いを可能にしながら、コアとなる安全制約（hardcoded behaviors）は変更不可として固定している。

## アイデア

- 優先順位階層（Safe > Ethical > Principled > Helpful）は監査AIの判断ロジック設計に直接応用可能：エージェントが競合する指示を受けた際の優先度解決フレームワークとして実装できる
- Operator/Userの権限分離モデルは、マルチテナント型監査エージェントのアクセス制御設計に転用できる：監査法人レベル・チームレベル・担当者レベルで許可スコープを階層化する
- 「過度な拒否を避ける」原則は、LLM-as-judgeの評価基準設計に示唆を与える：False Negativeコスト（有用な回答の不当な拒絶）をFalse Positiveと同等に評価する必要性

## Yujiの取り組みへの示唆

Model Specの優先順位階層構造（Safe > Ethical > Helpful）は、Yujiが開発中の監査エージェントにおける判断ロジックの設計パターンとして直接参照できる。LangGraphのノード間で競合する指示が発生した際の解決優先度をModel Specと同様の階層で定義することで、エージェントの予測可能性と監査適合性を両立できる。またRLAIFによる価値アライメント手法は、監査判断の品質評価モデル（LLM-as-judge）のトレーニング設計に応用可能であり、GRPO/RLAIFの研究との接続点として重要。

## 原文リンク

[OpenAIのModel Specに対するアプローチ](https://openai.com/index/our-approach-to-the-model-spec)
