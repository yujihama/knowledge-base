---
title: "源内（デジタル庁ガバメントAI）OSS版を技術解剖 — AWS/Azure/GCP 3クラウド対応の行政RAG基盤"
url: "https://zenn.dev/trailfusionai/articles/ai-news-20260427162443-52dc0e"
date: 2026-05-09
tags: [RAG, 行政AI, AWS Bedrock, Vertex AI, OSS, CDK, OpenSearch, LLMセルフデプロイ, e-Gov]
category: "infra"
related: [856, 192, 435, 1116, 2794]
memo: "[Zenn LLM] 源内（デジタル庁ガバメントAI）OSS版を技術解剖 — AWS/Azure/GCP 3クラウド対応の行政RAG基盤"
processed_at: "2026-05-09T12:49:46.241366"
---

## 要約

デジタル庁が2026年4月24日に政府職員向け生成AI基盤「源内（Genai）」をOSS公開した。GitHubにはTypeScript製フロントエンド「genai-web」（359⭐）とPython製バックエンド「genai-ai-api」（220⭐）の2リポジトリが存在し、いずれもMIT License + CC BY 4.0で商用利用可能。2026年度中に18万人規模の実証が予定されている。

技術的には3つの問題を3クラウドで分担解決する構成が特徴的。①行政実務RAG（AWS）：Bedrock（amazon.titan-embed-text-v2:0でベクトル化、claude-sonnet-4-6で回答生成）+ OpenSearch Serverless + Lambda + CDKのサーバーレス構成で行政文書の高速検索を実現。②LLMセルフデプロイ（Azure）：Azure OpenAIではなく任意のOSS LLM（Llama-3系、Qwen2系）を自前エンドポイントで立て、機密データを外部LLMに送らない設計。OpenAI互換API（/v1/chat/completions）経由で呼び出す。③法制度AI（GCP）：e-Gov APIから法令データを定期取り込みし、Vertex AIで回答。プロンプトで「引用なしで答えてはいけない」と明示的に制約することでハルシネーションを抑制する設計。

WebUI（genai-web）はTypeScript + Lambda + CDKで構成され、チャット・履歴・利用統計・Cognito認証を含む。現時点の制約としてはSlack/Teams連携未提供、SAML/OIDC拡張は自前実装が必要、グラフRAGやマルチホップRAGは未実装、改ざん耐性ログは要追加実装など。

他国の行政AI OSS（米国GSAのOpenActはAWSのみ・法令RAGなし、シンガポールGovTech PairはAzureのみ・法令RAGなし）と比較して、3クラウド対応と法令RAG内蔵が突出した特徴。

監査エージェント開発への示唆として、行政実務RAGのアーキテクチャ（Bedrock + OpenSearch Serverless + Lambda）はそのまま監査証跡の検索基盤に転用できる。また法制度AIのプロンプト設計（引用強制）は監査基準条文への準拠回答生成に応用可能。CloudWatch/Stackdriverによる監査ログも標準搭載されており、GRC観点でのリファレンス実装として参照価値が高い。

## アイデア

- 3クラウドを機能別に分担する設計（AWS=RAG、Azure=プライベートLLM、GCP=法令特化）は、ベンダーロックインを避けつつ各クラウドの強みを活かすリファレンスアーキテクチャとして再利用性が高い
- 法制度AIで「引用なしで答えてはいけない」をプロンプトレベルで強制する手法は、監査基準・法令根拠の明示が必須な業務AIへそのまま適用できるハルシネーション抑制パターン
- MIT + CC BY 4.0の二重ライセンスにより、コードは商用改変自由・文書は著作権表示で利用可能という行政OSSとして現実的な公開形態を採用しており、自治体提案・民間SaaS組み込みの法的障壁を除去している

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **AWS Bedrock** → /deep_3509 Strands Agents SDK入門：3行で始めるAIエージェント開発と他フレームワーク比較
- **Vertex AI** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **CDK** → /deep_2208 スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る
- **OpenSearch Serverless** (TODO: 読むべき)

## 関連記事

- /deep_856 Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで
- /deep_192 Googleスポンサーによるアフリカ全土「データサイエンス for Health アイデアソン」イノベーション報告
- /deep_435 Applied Engineerとは？SE・SAとの違いと求人800%増の背景【2026年版】
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針

## 原文リンク

[源内（デジタル庁ガバメントAI）OSS版を技術解剖 — AWS/Azure/GCP 3クラウド対応の行政RAG基盤](https://zenn.dev/trailfusionai/articles/ai-news-20260427162443-52dc0e)
