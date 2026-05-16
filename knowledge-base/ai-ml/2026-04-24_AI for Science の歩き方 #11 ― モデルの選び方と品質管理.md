---
title: "AI for Science の歩き方 #11 ― モデルの選び方と品質管理"
url: "https://zenn.dev/aws_japan/articles/ai4s-11-model-2026"
date: 2026-04-24
tags: [Amazon Bedrock, モデル選定, 再現性, temperature, Guardrails, オープンウェイトモデル, RLHF, LLM, DeepSeek R1, Claude Sonnet 4.6]
category: "ai-ml"
related: [111, 2700, 1595, 1560, 991]
memo: "[Zenn LLM] AI for Science の歩き方 #11 ― モデルの選び方と品質管理"
processed_at: "2026-04-24T12:54:10.701750"
---

## 要約

研究用途における AI モデルの選定基準と出力品質管理の実践的ガイドライン。ベンチマーク順位ではなく「妥当性・信頼性・再現性・追試可能性」の4軸（Stoltz et al. 2026）で選ぶべきとし、7ステップの選定フローを提示する。Step1でデータ機密性を確認（Amazon Bedrock はデータを学習に使用しないポリシー）、Step2で再現性確保のため temperature・top_p・モデルバージョンを固定する（Jarrett et al. 2025 は temperature 0.0→1.0 で GPT-4o の診断精度が 100%→89.4% に低下し、ユニーク診断数が 483% 増加することを実証）。Step3で東京リージョン（ap-northeast-1）や日本国内クロスリージョン推論の活用を検討、Step4で研究タイプ別コストを見積もり、Step5でタスク別モデルを選択（日本語タスクは Claude Sonnet 4.6、数学・推論は DeepSeek R1、低コストは Llama 4 Maverick 17B）。Step6で Amazon Bedrock の Compare モードで複数モデルを同一プロンプトで比較、Step7で Converse API によりモデル ID 変更だけで切り替え可能にしてベンダーロックインを回避する。商用モデルとオープンウェイトモデルの比較では、Stanford HAI AI Index 2025 によると特定ベンチマーク上の性能差は 2025年2月時点で 1.70% まで縮小。再現性が重要な研究ではオープンウェイトモデルのバージョン固定が有利。出力品質管理として Amazon Bedrock Guardrails を紹介し、日本語対応機能（PII マスキング・話題制限・有害コンテンツフィルタ）と英語のみ対応機能（Contextual Grounding Check・Automated Reasoning Checks）を区別して説明。運用上の注意として、確証バイアス対策（反論・批判視点のプロンプト活用、Jhaveri et al. 2026 で効果実証）、AI への認知的依存回避、モデルの安全性制約による過剰拒否（Kirk et al. 2023 が RLHF による出力多様性低下を実証、Cui et al. 2024 はモデルごとの過剰拒否率が 5%未満〜40%超と差大）への対応を列挙する。監査エージェント開発への示唆として、temperature・モデルバージョンの記録と固定は LLM-as-judge の再現性確保に直結し、Guardrails の PII マスキングは被監査企業の機密情報処理に応用可能。

## アイデア

- temperature が 0.0→1.0 で診断精度 100%→89.4%、ユニーク診断数 483% 増という定量データは、LLM-as-judge のスコア安定性議論に直接使える根拠
- 商用モデルとオープンウェイトモデルの性能差が 1.70% まで縮小（Stanford HAI 2025）という事実は、再現性・機密性要件があるならオープンウェイト選択のコスト正当化に使える
- Amazon Bedrock Guardrails の日本語対応範囲（PII マスキング・話題制限・有害フィルタは○、ワードフィルタ・根拠チェックは×）を把握することで、日本語監査エージェントのガードレール設計の現実的な制約を事前に把握できる

## 前提知識

- **temperature / top_p** (TODO: 読むべき)
- **RLHF** → /deep_37 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **オープンウェイトモデル** → /deep_711 AI政策 @🤗: ホワイトハウスAIアクションプランRFIへの回答
- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓

## 関連記事

- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_2700 動的個人嗜好への対応：ペアファインチューニングによる矛盾する人間的価値観の解決
- /deep_1595 ウェルビーイングに根ざしたAIの肯定的ビジョンが必要だ
- /deep_1560 あなたがAIに疲れる理由は、あなたが「翻訳」を押しつけられているからだ
- /deep_991 Llama 3.1 リリース — 405B・70B・8Bの多言語対応・128Kコンテキスト版

## 原文リンク

[AI for Science の歩き方 #11 ― モデルの選び方と品質管理](https://zenn.dev/aws_japan/articles/ai4s-11-model-2026)
