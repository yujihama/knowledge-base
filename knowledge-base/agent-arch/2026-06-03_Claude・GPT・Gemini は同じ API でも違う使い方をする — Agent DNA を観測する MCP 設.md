---
title: "Claude・GPT・Gemini は同じ API でも違う使い方をする — Agent DNA を観測する MCP 設計"
url: "https://zenn.dev/kanseilink/articles/kanseilink-agent-dna-overview-20260512"
date: 2026-06-03
tags: [MCP, Agent DNA, LLM比較, Claude, GPT, Gemini, SQLite, model_name正規化, 可観測性, マルチエージェント]
category: "agent-arch"
related: [5165, 3000, 5464, 68, 2550]
memo: "[Zenn LLM] Claude・GPT・Gemini は同じ API でも違う使い方をする — Agent DNA を観測する MCP 設計"
processed_at: "2026-06-03T09:07:47.066555"
---

## 要約

KanseiLink は MCP（Model Context Protocol）サーバーとして 150 以上のサービスを束ねるインテリジェンス層を運用している。その実運用の中で、同一 API を Claude・GPT・Gemini にそれぞれ叩かせると、成功率・リトライ挙動・エラー対応・サービス選択順位に明確な差異が生じることが判明した。この LLM 固有の行動パターンを社内では「Agent DNA」と呼んでいる。

具体的な差異として観測された傾向は以下の通り。(1) エラー対応: 4xx エラーに対してリトライを継続する族と、即座に別 API へ切り替える族がある。(2) 検索クエリの語彙: 日本語で丁寧文を投げる族とキーワードのみを投げる族がある。(3) ワークアラウンド戦略: `auth_expired` エラーに対し、トークン更新を試みる族と別エンドポイント探索を行う族がある。

これらの差異を事後に分析可能にするため、呼び出し元の LLM 名を正規化する仕組みを実装した。生の `model_name`（例: `claude-sonnet-4-20250514` や `anthropic/claude-4-sonnet`）は表記が揺れるため、TypeScript で `normalizeModelName()` 関数を実装し、日付サフィックス（`-20250514` 形式）とプロバイダプレフィックス（`anthropic/`, `openai/` 等）を別々に除去したうえでエイリアスマップに照合する。さらに `inferAgentType()` でモデル名から `claude`/`gpt`/`gemini`/`other` の4族に分類する。

ストレージには SQLite を採用し、`outcomes` テーブルに正規化後の `model_name` と `agent_type` を別カラムとして両方保存する設計とした。`agent_type` にインデックスを張ることで族ごとの集計を効率化し、`model_name` でモデル世代（例: Claude 3.5 と Sonnet 4）を区別した分析も可能にしている。

設計上の教訓として、(1) `agent_type` カラムは最初からスキーマに含めること（後付けでは過去ログが NULL になる）、(2) 正規化マップはコードに散らさずデータとして管理すること（モデルは毎月増える）、(3) 集計は族ごと（`GROUP BY agent_type`）と全体の両方を取ること（平均だけでは差分が消える）の3点が挙げられている。

この観測基盤の上に、MCP ツール `agent_voice` として 11 軸の構造化インタビューを用意し、エージェントから直接フィードバックを収集する仕組みも実装している。SaaS が「エージェント向け API」を設計する際に特定 LLM の DNA に最適化されると他の LLM で詰まる現象が生じるため、最初から多様な DNA を前提とした設計が必要とされる。監査エージェント開発においても、複数 LLM を組み合わせるマルチエージェント構成では各モデルの行動差異を可観測にしておくことが品質管理上重要な示唆となる。

## アイデア

- LLM ごとの行動差異（エラーリトライ戦略・クエリ語彙・ワークアラウンド選択）を「Agent DNA」として体系的に観測・分類する概念は、マルチ LLM システムの品質管理フレームワークとして応用可能
- model_name の正規化において日付サフィックスとプロバイダプレフィックスを別々に除去する順序依存の処理設計は、モデル識別子の標準化問題として汎用的に参照できる実装パターン
- エージェントから直接フィードバックを収集する `agent_voice` ツール（11 軸構造化インタビュー）は LLM-as-judge の発展形として、API 設計の改善ループを自動化する手法として興味深い

## 前提知識

- **Model Context Protocol (MCP)** (TODO: 読むべき)
- **LLM API呼び出し** (TODO: 読むべき)
- **SQLite** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **TypeScript** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説
- **マルチエージェント設計** → /deep_5319 マルチエージェント設計の7原則：Factory「Missions」が16日間自律稼働を実現

## 関連記事

- /deep_5165 RFPを貼るだけでAWSアーキテクチャ設計書が出てくるSaaSを個人開発した
- /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較
- /deep_5464 MCP・A2A・Function Calling：3つを混同していませんか？【Google Cloud ADK視点で整理】
- /deep_68 Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで

## 原文リンク

[Claude・GPT・Gemini は同じ API でも違う使い方をする — Agent DNA を観測する MCP 設計](https://zenn.dev/kanseilink/articles/kanseilink-agent-dna-overview-20260512)
