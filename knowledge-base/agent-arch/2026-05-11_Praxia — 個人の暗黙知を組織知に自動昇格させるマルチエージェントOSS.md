---
title: "Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS"
url: "https://zenn.dev/gen99/articles/88a84eddc21ce5"
date: 2026-05-11
tags: [マルチエージェント, 暗黙知, 組織知, メモリ循環, RAG, RBAC, SSO, LTM, OSS, LangGraph, MCP, Ollama, KMS, 監査ログ, AutonomousAgent]
category: "agent-arch"
related: [4177, 4520, 2404, 858, 2255]
memo: "[Zenn LLM] 🪡Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSSを作った"
processed_at: "2026-05-11T12:12:16.414159"
---

## 要約

PraxiaはApache 2.0で公開されたマルチエージェント・オーケストレーターOSSで、「ベテランの効くプロンプトが個人の引き出しに留まる」問題を解決するために設計された。コアの差別化は「個人→組織メモリ自動循環機構」で、ユーザが普通に使うだけで明示的なsave操作なしに個人メモリ(Layer 1)が蓄積され、Sleep-time Consolidationが「頻度/成果連動/LLM自己評価」の3経路並走で共有メモリ(Layer 3)→Markdown凍結層(Layer 4)→Graph層(Layer 5)へと自動昇格させる。アーキテクチャは5層スタック+Skillsレジストリで構成される。業務フロー特化スキルとして投資・営業・設計・購買・特許・法務の6領域を標準同梱し、LTMバックエンドはjson/mem0/langmem/letta/zep/hindsightの6種に対応。LLMはClaude/ChatGPT/Gemini/Qwen他100+モデルをサポートし、Gemma+Ollamaでの完全オンプレ運用も同一コードで実現できる。エンタープライズ向け機能としてOIDC SSO(Google/Microsoft/Okta/GitHub/Keycloak)・4ロールRBAC・監査ログ・ACLをすべてOSSに内包しており、paywall不要で利用できる点が商用エージェント基盤との大きな差異。ユーザ委譲OAuthでBox/SharePoint等の連携先ACLをユーザ単位で適用し、サービスアカウント経由のデータ漏洩リスクを排除する。KMS暗号化はAWS/Azure/GCP/Vault/localの5アダプタに対応したAES-GCM envelope encryptionで実装。自律エージェント(AutonomousAgent)はLLM駆動のツール使用ループで個人メモリ・組織メモリ・スキル・コネクタを自発的に活用し、全ツール呼出しはaudit logに記録される。期待効果として、法務レビューは60-90分→10-15分、営業商談準備は6h→1h、設計レビュー負荷は16h/週→4h/週などの定量値が提示されている。監査エージェント開発への示唆として、SSO+RBAC+監査ログのOSS内包設計・read_onlyメモリモードによる機微情報の足跡レス運用・ACLポリシーのGlobベース管理は、内部監査領域のLangGraphエージェント設計において参照価値が高い。また3経路昇格判定（頻度/成果/LLM自己評価）はLLM-as-judgeによる品質評価ループの実装パターンとして応用できる。

## アイデア

- Sleep-time Consolidationによる3経路並走昇格（頻度/成果連動/LLM自己評価）で、ユーザの明示的操作なしにドメイン特化の試行錯誤を組織知化する設計は、エージェントの自己改善ループとして参考になる
- ユーザ委譲OAuthで連携先(Box/SharePoint等)のACLをユーザ単位に適用し、サービスアカウントに起因するデータ越境を構造的に防ぐアーキテクチャは、エンタープライズRAGの権限制御モデルとして実用的
- read_onlyメモリモードとACLロックをadminが強制できる設計により、出願前特許情報など機微情報を扱う業務でメモリへの足跡を残さず運用できる点は、内部監査・コンプライアンス領域のエージェント設計に直接応用可能

## 前提知識

- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LTM (Long-Term Memory)** (TODO: 読むべき)
- **RBAC/OIDC SSO** (TODO: 読むべき)
- **ReAct/ToolUse Loop** (TODO: 読むべき)

## 関連記事

- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する

## 原文リンク

[Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS](https://zenn.dev/gen99/articles/88a84eddc21ce5)
