---
title: "信頼は持ち運べる：AIエージェントのツール選択にPortableなトラストインフラを"
url: "https://zenn.dev/xkumakichi/articles/e93a438265a682"
date: 2026-04-28
tags: [XAIP, trust-infrastructure, W3C-DID, MCP, tool-selection, Bayesian-scoring, Ed25519, provider-neutral, behavior-derived]
category: "agent-arch"
related: [430, 2550, 2688, 88, 1784]
memo: "[Zenn LLM] 信頼は持ち運べる"
processed_at: "2026-04-28T12:39:45.369762"
---

## 要約

AIエージェントがツールを選択する際、現状は「モデルの学習データに名前があるか」「プラットフォームが表示すると決めたもの」に依存しており、ランタイムの信頼シグナルが存在しない。昨日どのツールが成功したか、古いデータを返していないか、deprecateされていないかを知らないまま選択している。これはツール選択の問題ではなく、信頼データの問題だと筆者は指摘する。

信頼データの出所は3種類ある。①自己申告（READMEへの記述）、②プラットフォームキュレーション（おすすめリスト）、③振る舞い由来（behavior-derived、過去の実行結果を署名・集約）。ゲーミングやドリフト・上流ポリシー変更に耐性があるのは③のみだが、実装コストが最も高い。

単一レジストリ上にトラストスコアを構築すると、そのレジストリ自体が暗黙のトラストレイヤーとなり、可視性ルールの変更がスコア対象空間を変えてしまう。これは特定コミュニティへの批判ではなく、「上流の可視性判断が下流の信頼シグナルへ流れ込む階層構造」全般に当てはまる構造的問題だ。

これを解決するXAIPプロトコルは4つの設計原則を持つ。①Ed25519署名付きレシート（agentDid, callerDid, taskHash, resultHash, success, latencyMs, timestampを含み、呼び出し側もco-signするため自己水増し不可）、②W3C DID（did:key/did:web/did:xrpl）によるプラットフォーム非依存ID、③bayesianScore × callerDiversity × coSignFactorによるBayesianスコアリング（DID方式ごとに異なるpriorで安価なIDが信頼を無料取得できない設計）、④MCP・LangChain.js・OpenAI tool callingが同一フォーマットのレシートを出力するprovider-neutralな発行源。

稼働中のリファレンスデプロイでは、ツールサーバー10台を対象に2,100枚以上の署名付きレシートを収集済み。CIによる毎日の自動収集で毎実行ごとに新しいcaller鍵を生成しcaller diversityを担保している。Trust APIへのPOSTリクエストでリアルタイムのツール選択推薦と反実仮想（信頼データなしランダム選択シミュレーション）が得られる。

監査エージェント開発への示唆：エージェントのツール選択根拠を「持ち運び可能で監査可能な形」で記録するというアプローチは、内部監査領域での説明責任要件と直接対応する。将来の規制要件（「このエージェントのツール選択根拠は何か」）に対し、署名付きレシートによるトレーサブルな回答が用意できる。次版v0.5ではclass-aware risk evaluation（外部台帳アンカー型settlementツールとadvisoryツールを異なる信頼シグナルで評価）を扱う予定。

## アイデア

- callerDiversityをスコアの一次シグナルとして組み込み、単一エージェントによる自己水増しを構造的に排除している点（co-signと組み合わせてゲーミング耐性を実現）
- LangChain・OpenAI・MCPが同一バイト互換レシートを出力する設計により、フレームワーク横断で単一トラストグラフを形成できる点（観測サイロの解消）
- 反実仮想（counterfactual）レスポンスを信頼APIに組み込み、信頼データの有無による選択差分を定量化できる点（信頼インフラの価値を測定可能にする）

## 前提知識

- **W3C DID** (TODO: 読むべき)
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Ed25519署名** (TODO: 読むべき)
- **Bayesian推定** (TODO: 読むべき)
- **tool calling** → /deep_946 HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[信頼は持ち運べる：AIエージェントのツール選択にPortableなトラストインフラを](https://zenn.dev/xkumakichi/articles/e93a438265a682)
