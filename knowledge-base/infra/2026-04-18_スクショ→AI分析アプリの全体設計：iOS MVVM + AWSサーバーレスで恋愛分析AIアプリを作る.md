---
title: "スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る"
url: "https://zenn.dev/m_naoki_m/articles/3bf9daeb7a882d"
date: 2026-04-18
tags: [iOS, SwiftUI, MVVM, AWS, Bedrock, Lambda, Cognito, DynamoDB, OCR, Qwen3, Claude Sonnet, Swift Concurrency, actor, フリーミアム, サーバーレス, CDK, StoreKit2, プロンプトインジェクション対策]
category: "infra"
related: [826, 1737, 1660, 1735, 1562]
memo: "[Zenn LLM] スクショ→AI分析アプリの全体設計 ― iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る"
processed_at: "2026-04-18T12:13:26.129024"
---

## 要約

チャット画面のスクリーンショットをiPhone上でOCR処理し、クラウドLLMが心理分析・返信候補を生成するiOSアプリ「Relora」の全体設計を解説した記事。iOSクライアントはSwiftUI + SwiftData + MVVM + Swift Concurrencyで構成し、クラウド側はAWS CDK（TypeScript）でAPI Gateway + Lambda + Bedrock + Cognito + DynamoDBをコード管理する完全サーバーレス構成を採用。

最大の設計判断はプライバシー最優先のハイブリッドアーキテクチャ：スクリーンショットの画像データはApple Vision frameworkでデバイス上のみOCR処理し、抽出後の構造化テキストのみをAPIに送信する。これにより画像がクラウドに渡らない構造を実現している。

iOSクライアントでは@Observableマクロ（iOS 17+）を使ってAnalysisServiceをシングルトン管理し、State enumで「idle/analyzing/completed/failed」の状態機械を表現。ImageAnalysisService（OCR）とCloudAnalysisService（認証・API）はactorとして分離し、並行処理のレース条件を防ぐ。分析は「ローカルOCR→クラウドLLM→JSONパース」の3段パイプラインで、各工程の所要時間をSwiftDataに記録して運用時のボトルネック特定に活用。

LLMモデルは2層戦略：無料ユーザーにはAmazon BedrockのQwen3 Next 80B（us-east-1リージョン）、有料ユーザーにはClaude Sonnet 4.6（global inference profile）を割り当てるフリーミアム設計。コスト最適化とサービス品質を両立している。

セキュリティは多層防御設計：JWT認証（Cognito）→入力バリデーション→プロンプトインジェクション検出→Bedrock Guardrails→JSON抽出の順で処理。Cognitoはselfsignup無効化してLambda経由のみサインアップを許可し、1IPあたりのレート制限も実装。StoreKit 2のJWS検証をサーバー側で行い、DynamoDBのアトミックカウンターで使用量を制限する課金ロジックも含む。

インフラはLambda + DynamoDB PAY_PER_REQUESTに全振りし、トラフィックゼロなら料金ゼロ・突然10倍でも自動スケールの個人開発スケールに最適な構成。9言語対応でグローバルにデイワンリリースした。監査エージェント開発への示唆として、「ローカル処理でデータを秘匿しクラウドLLMで推論する」パターンと「actorによる並行性制御」「3段パイプラインの各工程計測」は、機密データを扱う監査AIシステムのアーキテクチャ設計に直接応用可能。

## アイデア

- 画像をクラウドに送らずデバイス上OCRで構造化テキストのみAPIに送信するプライバシー設計：監査AIでも機密文書を端末処理してLLMに要約のみ送るアーキテクチャとして転用可能
- 無料層にQwen3 80B・有料層にClaude Sonnet 4.6を割り当てる2層LLMモデル戦略：コストとサービス品質のトレードオフを料金プランに反映する設計パターン
- actorによる直列実行強制で並行OCR処理のメモリクラッシュとトークン更新のレース条件を同時解決：Swift Concurrencyの適切な粒度分割が運用安定性に直結することを実証

## 前提知識

- **Swift Concurrency** (TODO: 読むべき)
- **MVVM** (TODO: 読むべき)
- **AWS Bedrock** (TODO: 読むべき)
- **Cognito JWT** (TODO: 読むべき)
- **Apple Vision OCR** (TODO: 読むべき)

## 関連記事

- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_1737 難問を「選択肢」に変える：RLVRの探索限界を突破するCog-DRIFT
- /deep_1660 大規模言語モデルは基礎的なアルゴリズムを再発明できるか？
- /deep_1735 分散AIプラットフォームChutesとBittensorで始めるDePIN推論基盤
- /deep_1562 不完全なベリファイアでも十分：ノイズのある報酬による学習（RLVR）

## 原文リンク

[スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る](https://zenn.dev/m_naoki_m/articles/3bf9daeb7a882d)
