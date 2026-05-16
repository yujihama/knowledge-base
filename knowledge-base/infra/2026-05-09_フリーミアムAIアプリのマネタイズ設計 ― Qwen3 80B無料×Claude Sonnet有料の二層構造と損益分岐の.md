---
title: "フリーミアムAIアプリのマネタイズ設計 ― Qwen3 80B無料×Claude Sonnet有料の二層構造と損益分岐の数学"
url: "https://zenn.dev/m_naoki_m/articles/f116e6bc20331d"
date: 2026-05-09
tags: [フリーミアム, マネタイズ, Amazon Bedrock, Qwen3, Claude Sonnet, DynamoDB, StoreKit 2, レート制限, JWS検証, 個人開発]
category: "infra"
related: [2208, 4036, 3098, 4038, 826]
memo: "[Zenn LLM] フリーミアムAIアプリのマネタイズ設計 ― 80B無料 × Sonnet有料の二層と損益分岐の数学"
processed_at: "2026-05-09T21:34:14.489306"
---

## 要約

個人開発の恋愛メッセージ分析アプリ「Relora」を題材に、AIアプリのフリーミアム設計の経済的成立条件と実装を解説した記事。

核心は「無料ユーザーに劣化版ではなく実用版を提供する」設計原則。Amazon Bedrock の Converse API を使い、無料層に Qwen3 Next 80B（input $0.15/output $1.20 per 1M tokens）、有料層に Claude Sonnet 4.6（input $3.00/output $15.00）を割り当てる。1回の分析コストは入力1,800tok・出力450tokで計算すると、Qwen3が約0.12円、Sonnetが約1.8円（1USD=150円換算）で、コスト比は約1:15。

損益分岐の試算では、全員Sonnet運用（シナリオA）だと無料ユーザー1万人で月LLMコスト18万円かかり、月額¥980プランで有料ユーザー270人が損益分岐点。一方、Qwen3を無料層に使う二層設計（シナリオB）では同トラフィックのLLMコストが月12,000円（1/15）となり、有料15人で無料コストを相殺できる。課金転換率2%=DAU1万で200人の有料ユーザーがいればシナリオBは黒字、シナリオAは赤字という構造の違いが生まれる。

レート制限はDynamoDBの条件付き更新でアトミックに実装。ConditionExpressionで「上限未満ならインクリメント、超えたら ConditionalCheckFailedException」を1ステップ処理し、Lambda同時実行でも競合によるカウント超過が発生しない。

課金検証はStoreKit 2のjwsRepresentationをApple Root CA G3まで遡ってサーバー側で検証し、DynamoDBのSUBSCRIPTIONレコードでplan状態を管理。クライアントが送るtier=premiumは一切信頼せず、/v1/analyzeハンドラ冒頭でDBからplan確定後、freeプランからSonnetを呼ぶリクエストは403で拒否する。

Sonnet上限到達時はサーバーが429を返し、クライアントがQwen3で自動フォールバックする設計で「使えない」体験をゼロにする。不正アカウント大量作成にはIPベースで1日100アカウント上限を同じDynamoDBアトミック更新で対応。

DAUスケール試算ではDAU1万でQwen3 LLMコスト月3.6万円、インフラ込みで月5万円程度。API GatewayのグローバルスロットリングはDAU5,000超でボトルネックになる見込み。監査エージェント開発への示唆としては、DynamoDBの条件付き更新パターンは監査ログの重複防止やアトミックな状態遷移管理に転用可能。また、「サーバーが最終決定権を持つ」設計原則は、エージェントの権限判定をクライアント側に委ねないゼロトラスト的アーキテクチャ設計に直結する。

## アイデア

- モデル二層設計でコストを1/15に圧縮し、課金転換率2%という同一KPIが黒字・赤字を分ける構造的な設計差異を数学的に示した点
- DynamoDBのConditionExpressionによるアトミックレート制限で、分散環境でもスレッドセーフなカウント上限をサーバーレスコードなしで実現する実装パターン
- Sonnet上限到達時にクライアントが自動フォールバックする設計により「使えない」体験を排除しつつ、サーバー側はシンプルに429を返すだけにするUX設計とバックエンド分離の考え方

## 前提知識

- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **StoreKit 2** (TODO: 読むべき)
- **DynamoDB 条件付き更新** (TODO: 読むべき)
- **JWS検証** (TODO: 読むべき)
- **フリーミアム設計** (TODO: 読むべき)

## 関連記事

- /deep_2208 スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る
- /deep_4036 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第4回) ── 「きみ」を消したら、品質も消えた話
- /deep_3098 LLMプロンプトにエビデンスベースの心理学を組み込む ― 恋愛分析AIの設計
- /deep_4038 AIに毎週自分を評価させてみた──Claude Sonnetによる個人アセスメントの実践
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する

## 原文リンク

[フリーミアムAIアプリのマネタイズ設計 ― Qwen3 80B無料×Claude Sonnet有料の二層構造と損益分岐の数学](https://zenn.dev/m_naoki_m/articles/f116e6bc20331d)
