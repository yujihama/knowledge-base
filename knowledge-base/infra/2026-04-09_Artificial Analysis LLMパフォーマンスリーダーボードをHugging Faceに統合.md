---
title: "Artificial Analysis LLMパフォーマンスリーダーボードをHugging Faceに統合"
url: "https://huggingface.co/blog/leaderboard-artificial-analysis"
date: 2026-04-09
tags: [LLMリーダーボード, APIベンチマーク, スループット, TTFT, コスト最適化, Hugging Face, Artificial Analysis]
category: "infra"
memo: "[HF Blog] Bringing the Artificial Analysis LLM Performance Leaderboard to Hugging Face"
processed_at: "2026-04-09T09:49:06.338830"
---

## 要約

Artificial AnalysisがHugging Faceと連携し、100以上のサーバーレスLLM APIエンドポイントを対象とした品質・価格・速度の総合評価リーダーボードを公開した。LLMを用いたアプリケーション開発において、モデルの精度だけでなくスループット（tokens/s）やTTFT（Time to First Token）がシステム全体の性能を左右するという問題意識が背景にある。

計測指標は以下の5つ：(1) 品質インデックス（MMLU、MT-Bench、HumanEval、Chatbot Arenaに基づく複合スコア）、(2) コンテキストウィンドウサイズ、(3) 価格（入力/出力トークン単価および入力3:出力1の比率でブレンドした単一指標）、(4) スループット（過去14日間の中央値・P5/P25/P75/P95）、(5) レイテンシ（TTFT、同様の統計値）。各エンドポイントは1日8回テストされ、プロンプト長（約100/1k/10kトークン）と並列クエリ数（1/10）の6通りのワークロードで評価される。

2024年5月時点のハイライトとして、Claude 3 OpusとLlama 3 8Bの間に300倍以上（2桁以上のオーダー）の価格差が存在する。Llama 3リリース後48時間以内に7プロバイダーがAPIを提供開始するなど、オープンモデルへの需要の高さと競争激化が示されている。モデルセグメント別には、高品質・高価格帯（GPT-4 Turbo、Claude 3 Opus）、中間帯（Llama 3 70B、Mixtral 8x22B、Command R+、Gemini 1.5 Pro、DBRX）、高速・低価格帯（Llama 3 8B、Claude 3 Haiku、Mixtral 8x7B）に分類される。

実用上の重要な示唆として、大型モデル1回の呼び出しより、小型・高速モデルによる並列多数呼び出し＋大型モデルによる統合というパターンが、コスト・品質両面で優れる場合があることが示されている。具体例として、GPT-4 Turboで少数記事を処理するより、Llama 3 8Bで数十ページを並列処理しGPT-4 Turboで統合する方が、10倍のトークン消費でも低コストかつ高品質になりうると説明されている。

## アイデア

- 品質・価格・速度を単一プラットフォームで比較することで、モデル選定の意思決定を定量化できる点（特にP5/P95の分布情報は本番運用のSLA設計に直結する）
- 入力3:出力1比率でのブレンド価格という標準化手法により、異なるプロバイダー間の実質コストを単一指標で比較可能にしている点
- 小型モデルの並列活用＋大型モデルによる統合というアーキテクチャパターンが、単純なモデルスケールアップより優れる場合があるという実証的な示唆
## 関連記事

- /deep_1021 Text Generation Inference（TGI）ベンチマークツールの使い方と活用指針
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話

## 原文リンク

[Artificial Analysis LLMパフォーマンスリーダーボードをHugging Faceに統合](https://huggingface.co/blog/leaderboard-artificial-analysis)
