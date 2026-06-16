---
title: "障害対応コパイロットを作った話——Google Chat Bot の設計意思決定録"
url: "https://zenn.dev/interpark/articles/incident-copilot-design-decisions"
date: 2026-06-16
tags: [Google Chat Bot, Gemini, Vertex AI, Lambda, DynamoDB, Bedrock, Titan Embeddings, コサイン類似度, API Gateway, Lambda Authorizer, SumoLogic, 障害対応, コパイロット, サーバーレス]
category: "agent-arch"
related: [2208, 6851, 5906, 7517, 2]
memo: "[Zenn LLM] 障害対応コパイロットを作った話"
processed_at: "2026-06-16T09:07:32.494431"
---

## 要約

DeloitteではなくInterpark社内向けに、AWS上でGoogle Chat Botとして動く「障害対応コパイロット」を2ヶ月でMVPから認証強化版まで構築した事例。システム構成はLambda + DynamoDBのサーバーレス構成で、SumoLogicやCloudWatchのアラートをトリガーにGemini（Vertex AI）でログ解析を行い、結果を当番者へのメンション付きでGoogle Chatに投稿する。主な機能は①アラート自動解析（原因切り分けと対応要否判定）、②Titan Embeddingsを用いた過去インシデントのベクトル類似検索、③スラッシュコマンドによる定型操作、④対話Q&A。

設計上の重要判断は4点。第一にLLM選定：当初BedrockのClaudeを使用していたが、コストと推論の「考える量」の制御自由度からVertex AIのGeminiへ移行。Geminiは「調査経路が尽きると早めに撤退する」傾向があるため、代替調査経路を明示するプロンプトチューニングで対処。Embeddings（Titan）は移行コスト対効果が低いためBedrock据え置きとし、解析とベクトル化でベンダーを分ける構成を採用。第二にベクトル検索の実装：専用ベクトルDBは導入せず、DynamoDBにEmbeddingをJSON文字列で保存し全件cosine類似度計算。インシデント件数が少ない段階では専用サービスの運用コストより全件スキャンのほうが総合的に安いという判断。第三に認証設計：Phase 1〜2では無認証のLambda Function URLに直結していたが、LLM呼び出しが課金と直結するため「課金を膨らませる攻撃の入口」になりうるとして、Phase 3でAPI Gateway HTTP API＋Lambda Authorizerに刷新。Google Chat経路はJWT検証、SumoLogic経路はX-Webhook-TokenヘッダをSSM SecureStringと照合する方式を採用し、経路ごとに認証方式を変えた。さらにルート別スロットリングで課金の青天井を防止。旧Function URLの削除を切替手順に明示的に含めた点がポイント。第四に「自動化ではなくコパイロット」という設計思想：最終判断と実作業は人間に残し、LLMはあくまで叩き台と下書きを提供する役割に限定。この線引きがすべての設計判断の土台となっている。監査エージェント開発への示唆として、反復的な手順業務へのLLM適用、サーバーレスアーキテクチャによる低運用コスト化、Webhook認証設計（JWT vs 共有シークレット）のパターンは直接転用可能。

## アイデア

- LLMベンダー移行時にEmbeddingsとChat LLMを別々に判断する「部分移行」戦略——全部一度に動かさないことで移行リスクを分散できる
- 専用ベクトルDBを使わずDynamoDB全件スキャンで類似検索——件数規模に応じた技術選定の具体例として、過剰なインフラ投資を避ける判断基準を示す
- 無認証Webhook＝LLM課金攻撃の入口という脅威モデリング——送信元ごとに認証方式を最適化（JWT vs 共有シークレット）しスロットリングで課金上限を設ける設計

## 前提知識

- **Webhook認証** (TODO: 読むべき)
- **Embedding / ベクトル類似検索** (TODO: 読むべき)
- **Lambda + API Gateway** (TODO: 読むべき)
- **Gemini / Vertex AI** (TODO: 読むべき)
- **サーバーレスアーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_2208 スクショ→AI分析アプリの全体設計：iOS MVVM + AWSサーバーレスで恋愛分析AIアプリを作る
- /deep_6851 ナイーブじゃないベイズ判定器を使った文章分類
- /deep_5906 Kagentでコンテキストエンジニアリングを導入してみた — トークン消費を16万→8万に削減
- /deep_7517 Gemini APIのPrompt Cachingで会話履歴を効率的に管理する（Go言語編）
- /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 原文リンク

[障害対応コパイロットを作った話——Google Chat Bot の設計意思決定録](https://zenn.dev/interpark/articles/incident-copilot-design-decisions)
