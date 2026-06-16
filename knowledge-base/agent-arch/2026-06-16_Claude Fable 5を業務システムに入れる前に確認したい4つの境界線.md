---
title: "Claude Fable 5を業務システムに入れる前に確認したい4つの境界線"
url: "https://zenn.dev/yushiyamamoto/articles/claude-fable-5-production-boundaries"
date: 2026-06-16
tags: [Claude Fable 5, Anthropic, LLM API, fallback設計, データ保持, モデルルーティング, Amazon Bedrock, stop_reason, Mythosクラス, 業務システム統合]
category: "agent-arch"
related: [2293, 8059, 3504, 7297, 8066]
memo: "[Zenn LLM] Claude Fable 5を業務システムに入れる前に確認したい4つの境界線"
processed_at: "2026-06-16T09:06:57.617323"
---

## 要約

2026年6月9日に公開されたClaude Fable 5（Mythosクラス）を業務システムへ統合する際に先に決めるべき4つの運用境界線を整理した実務ガイド。モデルIDは`claude-fable-5`、context window 1Mトークン、最大出力128kトークン、adaptive thinkingが常時ONで、手動のextended thinking budgetやassistant prefillは非対応という仕様を前提とする。

**境界線1：拒否とフォールバック**。Fable 5にはサイバーセキュリティ・生物/化学・推論蒸留を検知する新分類器が搭載されており、拒否時はHTTPエラーではなくHTTP 200で`stop_reason: "refusal"`として返る。`stop_details.category`には`cyber`/`bio`/`reasoning_extraction`が入る。フォールバックはClaude API、Amazon Bedrock、Vertex AIで実装方式が異なり、requested_model、served_model、stop_reason、fallback_model、billable_pathをログに記録することが最低要件。公式はフォールバック非発生率95%超と述べるが、正当な業務用途でも誤検知が起きると明言しており、「必ず答える」前提を捨てた設計が必要。

**境界線2：料金とアクセス**。API従量課金はinput $10/MTok、output $50/MTokで6月9日から利用可能。Pro/Max/Team等のサブスクは6月22日まで追加費用なし、6月23日以降は使用クレジットが必要となりプランから一時除外される。評価は6/22までに完了し、代表ワークロードでOpus 4.8と比較してから本採用の是非を判断すべきとしている。input 200k＋output 20kで約$3/回、100回/月で$300/月という試算例を示す。

**境界線3：30日データ保持**。Mythosクラスは全トラフィックで30日保持が必須となり、ゼロデータ保持（ZDR）の対象外。Amazon Bedrockでも`provider data share`の有効化が必要。顧客契約やプライバシーポリシーで「プロンプトは保持されない」と説明している案件にはFable 5を使わないルーティングが必要。この判断は技術側だけで完結せず法務・契約担当との確認が必須。

**境界線4：モデルルーティング設計**。大規模コード移行・長時間agenticタスクにはFable 5、通常の設計相談・コードレビューはOpus 4.8/Sonnet 4.6、高頻度分類・短文生成はSonnet/Haikuという役割分担が推奨される。ZDR要件あり・機密データ・セキュリティ/生物系ドメインへの直送は避ける。監査エージェント開発においては、拒否とフォールバックの観測ログ設計をプロンプト改善より先に実装すべき点と、30日保持が監査データの取り扱いルールと矛盾しないかの事前確認が特に重要な示唆となる。

## アイデア

- 拒否がHTTP 200で返る設計（stop_reason: refusal）は通常の例外ハンドラでは拾えず、パイプライン全体でrefusalを正常系として扱うアーキテクチャが必要という点が実装上の盲点になりやすい
- モデルティアごとにデータ保持ポリシーが異なる（Fable 5は30日必須・ZDR不可）という制約が、モデル選択を技術的判断ではなく契約・コンプライアンス判断に引き上げるという構造的変化
- 6/22〜6/23の料金体系切り替えという時間的境界を評価ウィンドウとして活用し、本番採用判断を期限駆動で行う戦略的アプローチ

## 前提知識

- **Claude Messages API** (TODO: 読むべき)
- **stop_reason / stop_details** (TODO: 読むべき)
- **Zero Data Retention (ZDR)** (TODO: 読むべき)
- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **LLMフォールバック設計** (TODO: 読むべき)

## 関連記事

- /deep_2293 【2026年】Claude APIを最安で使う方法：サブスク不要で40%以上節約
- /deep_8059 「有意差なし ≠ 差なし」をClaude Fable 5は理解しているか――設計書レビューで見えたOpus 4.8との差
- /deep_3504 harness engineering を5層で整理する — Pythonで1から書いて見えたこと
- /deep_7297 LLM APIのコストをどう下げるか — 用途別の使い分けと4つの節約術
- /deep_8066 Claude Fable 5レビュー：Opusの2倍の価格に見合う価値はあるか

## 原文リンク

[Claude Fable 5を業務システムに入れる前に確認したい4つの境界線](https://zenn.dev/yushiyamamoto/articles/claude-fable-5-production-boundaries)
