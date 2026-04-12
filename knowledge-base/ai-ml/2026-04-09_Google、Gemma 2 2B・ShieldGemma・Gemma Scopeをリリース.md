---
title: "Google、Gemma 2 2B・ShieldGemma・Gemma Scopeをリリース"
url: "https://huggingface.co/blog/gemma-july-update"
date: 2026-04-09
tags: [Gemma2, ShieldGemma, GemmaScope, SparseAutoencoder, SpeculativeDecoding, SafetyClassifier, MechanisticInterpretability, GGUF, llama.cpp]
category: "ai-ml"
memo: "[HF Blog] Google releases Gemma 2 2B, ShieldGemma and Gemma Scope"
processed_at: "2026-04-09T09:05:06.078362"
---

## 要約

Googleは2024年7月31日、Gemma 2ファミリーの新モデル群を公開した。

**Gemma 2 2B**は2.6Bパラメータのコンパクトモデルで、既存の9B・27Bに続く小型版。スライディングアテンションとlogit soft-cappingを採用し、bfloat16推論を推奨。HuggingFace Transformers、llama.cpp（GGUFフォーマット）から利用可能。Open LLM Leaderboard v2ではIFEval 56.7（同サイズ帯最高）、MMLU-Pro 17.2を記録し、知識タスクと指示追従で同サイズのPhi-2（15.5平均）やQwen2-1.5B-Instruct（13.9平均）を上回る平均スコア17.0を達成。

特筆すべき用途として**Assisted Generation（Speculative Decoding）**がある。Gemma 2 2Bをアシスタントモデルとして27Bモデルと組み合わせることで、品質を維持しながら最大3倍の生成高速化が可能。LLMはトークンを生成するよりも確認する方が高速である性質を利用し、小モデルが候補シーケンスを生成→大モデルが検証・採用するパイプラインを構成する。アシスタントモデルは対象LLMの1/10〜1/100のパラメータ規模が推奨。

**ShieldGemma**はGemma 2ベースの安全性分類器シリーズ。開発者がアプリケーションの入力・出力をフィルタリングするために設計されており、2B・9B・27Bの3サイズが提供される。「dangerous content」「hate speech」「sexually explicit」「harassment」の4カテゴリを分類し、Yes/Noの確率スコアで出力。JBB-Behaviors・OpenAI Policy等のベンチマークで既存の安全分類器を上回る性能を示す。

**Gemma Scope**はGemma 2 2Bおよび9Bに対する包括的なSparse Autoencoder（SAE）スイート。モデルの内部表現を解釈するための機械的解釈可能性（Mechanistic Interpretability）ツールであり、各レイヤーの残差ストリーム・アテンション出力・MLP出力をカバー。latent数は1Kから1Mまで複数サイズが提供され、JumpReLU SAEアーキテクチャを採用。Neuronpediaと連携しインタラクティブな探索が可能。

## アイデア

- Speculative Decodingによる大型モデルの推論高速化：2.6Bモデルを27Bのアシスタントとして使うことで品質ゼロ損失で3倍高速化できる設計は、エージェントループの低レイテンシ化に直接応用可能
- ShieldGemmaによる入出力フィルタリング：分類器を推論パイプラインの前後に挟む設計パターンは、LLM-as-judgeの安全ガードレールとして実装しやすい軽量な選択肢
- Gemma ScopeのSAEによるモデル内部の解釈：JumpReLU SAEで残差ストリームをスパース特徴に分解するアプローチは、LLMの判断根拠を人間が検証する機械的解釈可能性研究の実用的な基盤となる
## 関連記事

- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- /deep_400 GGMLとllama.cppがHugging Faceに参加——ローカルAIの長期的発展を支える体制へ
- /deep_1146 1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった

## 原文リンク

[Google、Gemma 2 2B・ShieldGemma・Gemma Scopeをリリース](https://huggingface.co/blog/gemma-july-update)
