---
title: "LLMの出力を簡単に評価できるPythonライブラリ「llm-evaluation-toolkit」を作りました"
url: "https://zenn.dev/swoswoyuu1156/articles/7a1208cd31e84a"
date: 2026-06-13
tags: [LLM-as-a-Judge, BLEU, ROUGE, SemanticSimilarity, 評価指標, Pythonライブラリ, OpenAI, Anthropic]
category: "ai-ml"
related: [2278, 4816, 4849, 41, 4885]
memo: "[Zenn LLM] LLMの出力を簡単に評価できるPythonライブラリを作りました"
processed_at: "2026-06-13T09:04:36.970274"
---

## 要約

llm-evaluation-toolkitは、APIベースのLLM出力を複数指標で評価するための軽量Pythonライブラリ。lm-eval-harnessやHugging Face evaluateといった既存ツールが研究用途に特化し、APIベースLLMへの適用が煩雑である課題に対し、シンプルなインターフェースで4種類の評価指標を統一的に提供する。

対応指標は以下の4つ。①BLEU（Bilingual Evaluation Understudy）：1〜4-gramのフレーズ一致率を測定し、機械翻訳・固定フォーマット生成に適する。言い換えには弱い。②ROUGE（ROUGE-1/2/L）：単語・2-gram・最長共通部分列の一致を測定し、要約タスクに適する。③セマンティック類似度：sentence-transformersでテキストをベクトル化しコサイン類似度を算出。BLEUやROUGEが捉えられない同義語・言い換えを考慮できる（例："The cat is on the mat"と"A feline rests upon the rug"はBLEU低・セマンティック高）。④LLM-as-a-Judge：GPT-4o-miniなど別のLLMが審判として採点。正解テキスト不要で、創作文・コード説明・複雑なQ&Aなど正解定義が困難なタスクに有効。temperature=0.0で採点再現性を確保。

設計上の特徴として、全指標がcompute(predictions, references)という同一インターフェースを持ち、指標の追加・切り替え時に呼び出しコードを変更不要。sentence-transformers（数百MB）はオプション依存として分離し、pip install llm-evaluation-toolkit[semantic]でのみインストール。OpenAIとAnthropicはBaseProviderという抽象クラスで統一し、プロバイダ切り替えがコード変更なしに可能。BaseEvaluatorを使えば複数指標を一括実行できる。

監査エージェント開発への示唆：LLM-as-a-Judgeは正解ラベルなしでエージェントの回答品質を定量評価できるため、監査エージェントのアウトプット品質管理（リスク判定の妥当性確認、調書文章の品質スコアリング）に直接応用可能。BLEU/ROUGEはテンプレート準拠の定型文生成（監査意見文など）の評価に使える。統一APIにより、GPT-4oとClaude 3.5 Sonnetのような複数モデルを同一パイプラインで比較評価するベンチマーク構築が容易になる。

## アイデア

- LLM-as-a-Judgeをtemperature=0.0で実行することで採点の再現性を確保している点は、監査エージェントの品質管理パイプラインに組み込む際の重要な設計パターン
- sentence-transformersをオプション依存に切り出すことで軽量版と全機能版を使い分ける設計は、本番環境とCI環境でのデプロイサイズ最適化の手法として参考になる
- BaseProviderの抽象クラスによりOpenAI/Anthropicを同一コードで切り替えられる設計は、モデル比較ベンチマーク自動化の基盤として応用できる

## 前提知識

- **BLEU/ROUGE** (TODO: 読むべき)
- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **コサイン類似度** → /deep_6842 R.E.V.I.S. #3「器を分け、裏方を統べる」── SwiftローカルLLMアプリv0.0.4の設計思想
- **sentence-transformers** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **APIベースLLM** (TODO: 読むべき)

## 関連記事

- /deep_2278 仕事とAIの関係を実際に解明できる唯一のデータとは何か
- /deep_4816 マルチモデルルーティング入門：GPT・Claude・Geminiを使い分ける実装パターン
- /deep_4849 マスク対アルトマン裁判第1週：マスク、騙されたと主張・AIによる人類滅亡を警告・xAIがOpenAIモデルを蒸留していることを認める
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_4885 ハイプと利益の間に欠けているステップ：AIの「フェーズ2問題」

## 原文リンク

[LLMの出力を簡単に評価できるPythonライブラリ「llm-evaluation-toolkit」を作りました](https://zenn.dev/swoswoyuu1156/articles/7a1208cd31e84a)
