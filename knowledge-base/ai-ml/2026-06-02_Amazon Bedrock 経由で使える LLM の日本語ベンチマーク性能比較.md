---
title: "Amazon Bedrock 経由で使える LLM の日本語ベンチマーク性能比較"
url: "https://zenn.dev/aws_japan/articles/2026-06-01-bedrock-japanese-eval"
date: 2026-06-02
tags: [llm-jp-eval, Amazon Bedrock, 日本語ベンチマーク, LLM評価, Converse API, MMLU, GSM8K, Qwen3, Claude, コストパフォーマンス]
category: "ai-ml"
related: [3820, 1068, 4944, 4815, 7074]
memo: "[Zenn LLM] Amazon Bedrock 経由で使える LLM の日本語ベンチマーク性能"
processed_at: "2026-06-02T21:05:43.032554"
---

## 要約

Amazon Bedrock 経由で利用できる複数の LLM を対象に、llm-jp-eval という日本語ベンチマークツールを用いて日本語性能を体系的に評価した結果をまとめた記事。llm-jp は国立情報学研究所（NII）が主導する日本発の LLM 開発プロジェクトであり、llm-jp-eval はそのプロジェクトが提供する多タスク評価フレームワーク。評価は bedrock-runtime エンドポイントの Converse API を通じて実施し、temperature=0、reasoning パラメータ最小値という条件で統一。コストは us-east-1/us-west-2 の標準 on-demand 単価を使用。評価タスクは NLI（自然言語推論：jnli, jsem）、QA（質問応答：jemhopqa, niilc）、RC（読解：jsquad）、CR（常識推論：jcommonsenseqa）、HE-JA（日本語試験：jmmlu）、HE-EN（英語試験：mmlu_en）、MR（数学推論：gsm8k, mgsm）、MT（機械翻訳：alt-j-to-e）の 8 カテゴリ。SUM（要約：xlsum_ja）は今回の集計から除外。結果として Claude 系モデルは高性能だがコストも高く、コストパフォーマンス面では gpt-oss 120B、Qwen3-Next 80B、Nemotron Super 3 120B などが安価で良好なスコアを示した。最新モデルが必ずしも最高スコアを記録するわけではなく、性能は飽和傾向にある。誤答事例の分析では、データセット自体に問題のある事例（「一週間は何曜日から始まる？」の正解が「万人が認める答えはない」など）や、exact_match 評価の限界（意味的に正しいが文字列一致しない「シベリア気団」→「シベリア」問題）が浮き彫りになった。最新 LLM はデータセット自体の誤りを検出できる水準に達しており、accuracy 指標だけでは実力の正確な把握が難しい状況となっている。監査エージェント開発への示唆として、日本語での自然言語推論・読解・多段階推論タスクにおけるモデル選定の際に、コストと性能のトレードオフを定量的に把握するための参照データとして活用できる。特に内部監査文書の要約や QA システム構築において、Claude 以外の安価なモデルでも特定タスクでは十分な性能が期待できることが示された。

## アイデア

- exact_match 評価の限界：意味的に正しい回答でも文字列一致しなければ不正解とされる問題が多数存在し、最新 LLM の実力をベンチマーク数値だけでは正確に測れない状況になっている
- 最新・高コストモデルが必ずしも最高スコアを出さない性能飽和現象：gpt-oss 120B や Qwen3-Next 80B などオープンウェイトモデルが安価で競合水準の性能を発揮しており、コスト最適化の余地が大きい
- データセット品質問題の顕在化：最新 LLM がベンチマークデータの誤り（例：「一週間の始まり曜日」問題）を検出できる水準に達しており、ベンチマーク自体の信頼性評価が今後の課題となっている

## 前提知識

- **llm-jp-eval** → /deep_902 日本語LLMオープンリーダーボードの公開
- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **Converse API** (TODO: 読むべき)
- **MMLU** → /deep_273 ペルソナ・プロンプト「〇〇の専門家です」は精度を下げる――USC研究がMMILUで71.6%→68.0%の低下を確認
- **exact_match評価** (TODO: 読むべき)

## 関連記事

- /deep_3820 知ったかぶりのGPTか、すぐ意見を変えるClaudeか？「修復」がLLMのマルチターン対話の不安定性を明らかにする
- /deep_1068 構造化生成によるプロンプト一貫性の改善
- /deep_4944 大規模言語モデルにおける言語横断的応答一貫性：ILRに基づくClaudeの6言語評価
- /deep_4815 フリーミアムAIアプリのマネタイズ設計 ― Qwen3 80B無料×Claude Sonnet有料の二層構造と損益分岐の数学
- /deep_7074 Opus 4.8 はコスパが良い？——Opus 4.7 と QCD で比較した（オトナの自由研究 #20）

## 原文リンク

[Amazon Bedrock 経由で使える LLM の日本語ベンチマーク性能比較](https://zenn.dev/aws_japan/articles/2026-06-01-bedrock-japanese-eval)
