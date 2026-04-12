---
title: "Sempre HealthがExpert Acceleration Programを活用してMLロードマップを加速した事例"
url: "https://huggingface.co/blog/sempre-health-eap-case-study"
date: 2026-04-12
tags: [NLP, テキスト分類, Hugging Face, Expert Acceleration Program, ヘルスケアAI, 本番NLPパイプライン, ルールベース→ML移行]
category: "ai-ml"
memo: "[HF Blog] How Sempre Health is leveraging the Expert Acceleration Program to accelerate their ML roadmap"
related: [1310, 107, 88, 1661, 902]
processed_at: "2026-04-12T09:13:30.768470"
---

## 要約

Sempre Healthは、SMS経由で患者の服薬アドヒアランスと処方薬の費用負担を改善するヘルスケアスタートアップ。同社は1日数千件の患者からの受信SMSを処理しており、その多くは「処方箋の再注文リクエスト」「サンクスメッセージ」など定型的な応答が可能なものであった。

従来はルールベースのシステムで受信メッセージの約80%を捕捉していたが、残り20%の改善には統計的機械学習アプローチが必要と判断。Hugging Faceのライブラリ群と言語モデルを活用したNLPパイプラインの構築を検討し始めた。

CTOのSwaraj BanerjeeとMLエンジニアのLarry ZhangはNLP・MLのバックグラウンドを持つものの、ユースケース固有の問題定式化、最適なモデルアーキテクチャ選定、トレーニングデータのラベリング手法について不確実性があった。そこでHugging FaceのExpert Acceleration Program（EAP）を活用。EAPチームは以下の点で貢献した：(1) 代表性・正確性の高いラベル取得戦略のアドバイス、(2) ユースケースに最適なモデルと手法への即時誘導による調査工数の大幅削減。

本番NLPパイプラインのデプロイ後、受信メッセージの約20%が自動処理されるようになり、以前はpatient operationsチームのチケットとなっていた低付加価値業務が削減された。これにより業務スケーラビリティとチームワークフローに大きなインパクトをもたらした。

監査エージェント開発への示唆：小規模チームがドメイン特化NLPパイプラインを短期間で本番投入した本事例は、社内ナレッジや監査調書の自動分類・応答システムに直接応用可能。特に「問題の正確な定式化」と「適切なモデル選定」に専門知識を集中投入することで開発期間を大幅短縮できる点は、監査エージェント設計においても重要な示唆となる。

## アイデア

- ルールベース80%捕捉からML統計アプローチへの移行により、残余20%の自動化を達成した段階的アーキテクチャ設計の考え方
- ドメイン専門家（医療SMS）とMLエキスパートの協業により、ラベリング戦略と問題定式化の質を高め、少人数チームでも短期本番化を実現した外部加速モデル
- 「自動応答可能なメッセージの識別」という分類タスクに絞ることで、複雑な生成AIを使わずHugging Face既存モデルのファインチューニングで十分なROIを得られることの実証

## 前提知識

- **テキスト分類** → [ヴォイニッチ写本は何語か？ — 5つのテキストとの統計比較で600年の謎を分類する](../ai-ml/2026-03-29_ヴォイニッチ写本は何語か？ — 5つのテキストとの統計比較で600年の謎を分類する.md)
- **NLPファインチューニング** (TODO: 読むべき)
- **Hugging Face Transformers** → [Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する](../ai-ml/2026-04-11_Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する.md)
- **ラベリング戦略** (TODO: 読むべき)
- **ルールベースシステム** (TODO: 読むべき)

## 関連記事

- [複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー](../infra/2026-04-10_複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー.md)
- [ヴォイニッチ写本は何語か？ — 5つのテキストとの統計比較で600年の謎を分類する](../ai-ml/2026-03-29_ヴォイニッチ写本は何語か？ — 5つのテキストとの統計比較で600年の謎を分類する.md)
- [研究者向けMCP：AIを研究ツールに接続する方法](../agent-arch/2026-04-06_研究者向けMCP：AIを研究ツールに接続する方法.md)
- [機械学習ディレクターの洞察 第3回：金融業界編](../audit-ai/2026-04-12_機械学習ディレクターの洞察 第3回：金融業界編.md)
- [日本語LLMオープンリーダーボードの公開](../ai-ml/2026-04-08_日本語LLMオープンリーダーボードの公開.md)

## 原文リンク

[Sempre HealthがExpert Acceleration Programを活用してMLロードマップを加速した事例](https://huggingface.co/blog/sempre-health-eap-case-study)
