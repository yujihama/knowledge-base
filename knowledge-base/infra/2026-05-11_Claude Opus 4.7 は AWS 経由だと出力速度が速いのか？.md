---
title: "Claude Opus 4.7 は AWS 経由だと出力速度が速いのか？"
url: "https://zenn.dev/aws_japan/articles/2026-05-08-opus4-7-speed"
date: 2026-05-11
tags: [Claude Opus 4.7, Amazon Bedrock, Artificial Analysis, LLM benchmark, throughput, API provider, Adaptive Reasoning]
category: "infra"
related: [5025, 2140, 4815, 2060, 2548]
memo: "[Zenn LLM] Claude Opus 4.7 は AWS 経由だと出力速度が速いのか？"
processed_at: "2026-05-11T12:13:45.725125"
---

## 要約

Artificial Analysis（artificialanalysis.ai）のベンチマークデータを用いて、Claude Opus 4.7 の出力速度をAPIプロバイダ別に比較した記事。結論として、AWS（Amazon Bedrock）経由での利用は他プロバイダと比較して出力速度（トークン/秒）が明確に高いことが確認された。

計測方法は、1k/10kトークンの入力を1日8回、100kトークン入力を週1回テストし、過去72時間の中央値（P50）を用いる。テストサーバーはGoogle Cloud の us-central1-a ゾーンに配置され、各実行では固有のプロンプトを生成して使用する。出力速度は「（総トークン数 − 最初のチャンクトークン数）÷（最終チャンク受信時刻 − 最初のチャンク受信時刻）」として定義される。

比較結果のポイントは2点ある。第一に、出力速度（スループット）においてはAWSが他プロバイダより明確に優位であった。第二に、エンドツーエンドレスポンス時間（入力処理時間 ＋ Reasoningトークン数 ÷ Reasoning出力速度 ＋ 500 ÷ 回答出力速度）ではプロバイダ間の明確な差は観測されなかった。この差異は、トークン数が大きい場合に顕著に現れ、500トークン程度の短い生成では差が出にくい性質によるものと解釈される。

また、同一のClaude Opus 4.6では同様のプロバイダ間差異は見られず、Opus 4.7 固有の特性である点も強調されている。OpenRouterにもパフォーマンスモニタリングが存在するが、多様な本番トラフィックから算出されており、条件統一や系統的なトークン長別実験は行われていないため、Artificial Analysisとの比較には注意が必要。

Opus 4.7 はリリースから1ヶ月未満であり、今後のモデル・インフラ最適化によって結果が変化する可能性があることが明記されている。監査エージェント開発への示唆としては、長い推論チェーンや大量トークン出力を伴うReActエージェントをAmazon Bedrock経由で運用することで、スループット面での恩恵を受けられる可能性がある。

## アイデア

- 同一モデルでもAPIプロバイダによってスループットが有意に異なり、長文生成タスクではその差が顕著になる点は、エージェント設計時のインフラ選定基準として実用的
- エンドツーエンドレスポンス時間ではプロバイダ差が出にくい一方、純粋な出力速度では差が出るという非対称性は、Reasoningトークン生成フェーズがボトルネックになっている可能性を示唆する
- Opus 4.6 では同差異が見られないことから、Adaptive Reasoning（extended thinking）モードの実装・最適化がプロバイダ毎のスループット差に影響している可能性がある

## 前提知識

- **Claude Opus 4.7** → /deep_2548 LLM開発者のための「Claude Opus 4.7」アーキテクチャ再考：モデルの進化が変えるRAGとMemoryの境界線
- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **Adaptive Reasoning** (TODO: 読むべき)
- **LLM throughput** (TODO: 読むべき)
- **Time to First Token** (TODO: 読むべき)

## 関連記事

- /deep_5025 私がOpus 4.7を「アホになった」とあまり感じなかった理由：要件定義書駆動の実装フロー
- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた
- /deep_4815 フリーミアムAIアプリのマネタイズ設計 ― Qwen3 80B無料×Claude Sonnet有料の二層構造と損益分岐の数学
- /deep_2060 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG
- /deep_2548 LLM開発者のための「Claude Opus 4.7」アーキテクチャ再考：モデルの進化が変えるRAGとMemoryの境界線

## 原文リンク

[Claude Opus 4.7 は AWS 経由だと出力速度が速いのか？](https://zenn.dev/aws_japan/articles/2026-05-08-opus4-7-speed)
