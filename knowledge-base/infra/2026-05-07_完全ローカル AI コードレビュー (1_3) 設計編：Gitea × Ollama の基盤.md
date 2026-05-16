---
title: "完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤"
url: "https://zenn.dev/motowo/articles/local-ai-code-review-design"
date: 2026-05-07
tags: [Gitea, Ollama, Gemma4, ローカルLLM, コードレビュー, CI/CD, act_runner, 閉域網, 最小権限, ISMAP]
category: "infra"
related: [2257, 2691, 2105, 3903, 2056]
memo: "[Zenn LLM] 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤"
processed_at: "2026-05-07T09:40:24.115355"
---

## 要約

クラウド AI が利用できない閉域網・オンプレ環境向けに、Gitea v1.25 + Gitea Actions + act_runner v0.3 + Ollama v0.20（Gemma 4 E4B モデル）を組み合わせた完全ローカル AI コードレビューシステムの設計を解説した記事。全通信が 127.0.0.1 または host.docker.internal に閉じており、外部への通信が一切発生しないアーキテクチャが特徴。

クラウド AI を使えない根拠として、SaaS 受託開発における顧客 NDA・金融分野の FISC 安全対策基準・医療情報の 3 省 2 ガイドライン・公共調達の ISMAP・製造防衛分野の営業秘密保護を具体的に列挙。OWASP LLM Top 10 2025 の LLM02（Sensitive Information Disclosure）や経済産業省・総務省の AI 事業者ガイドライン第 1.0 版（2024）も根拠として参照されており、「漠然とした不安」ではなく法令・契約に基づく設計判断として位置づけている。

アクセス制御は「bot アカウント → PAT → Secret → act_runner → workflow」の 5 階層構造で最小権限を実現。PAT は Gitea v1.23 以降の granular scope で read:repository + write:issue のみに絞り、Secrets はリポジトリ単位で管理。act_runner は scope=instance で運用負荷を最小化しつつ、悪意あるワークフロー対策は Part3 に委ねる設計。

信頼境界設計では、Gitea・Ollama を 127.0.0.1 のみに bind する Ingress 制限と、Docker コンテナからの Egress（外向き通信）を --internal オプションや macOS の pf ルールで遮断する手法を区別して説明。Docker Desktop for Mac の仕様で localhost がコンテナ自身を指す点など、実装時のハマりポイントも設計段階で整理している。

Part2 では ai-review.yml と ai_review.py の実装・Mac+Docker 特有のトラブルシューティング、Part3 では PAT ローテーション・スパイク対応・複数リポジトリ横展開を扱う予定。監査エージェント開発への示唆としては、閉域網での LLM 活用における 5 階層スコープ設計・Ingress/Egress 分離の信頼境界設計・ISMAP や AI 事業者ガイドライン準拠のアーキテクチャ決定プロセスが、内部監査システムのセキュリティ設計に直接適用可能。

## アイデア

- 全通信を 127.0.0.1 に閉じるためのアーキテクチャ設計として、Ingress（受信制限）と Egress（送信制限）を明示的に分離して設計する手法は、閉域網での LLM 運用全般に適用できるセキュリティパターン
- 「bot アカウント → PAT → Secret → Runner → workflow」の 5 階層スコープ設計は、LLM エージェントに与える権限を段階的に絞り込む最小権限原則の具体的実装例として汎用性が高い
- FISC・ISMAP・OWASP LLM Top 10・AI 事業者ガイドラインを業界断面ごとに対応付けた禁止根拠の整理は、AI 導入可否を法令・契約ベースで判断するための実用的なフレームワーク

## 前提知識

- **Gitea Actions** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Docker Desktop** (TODO: 読むべき)
- **最小権限原則** (TODO: 読むべき)
- **OWASP LLM Top 10** → /deep_2543 【実装】あなたのAIアシスタント、一文でハイジャックされてます——PythonでPrompt Injection検出ゲートを作る

## 関連記事

- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成
- /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた
- /deep_2056 Gemma 4 思考モード検証：26B vs E4B — ローカルLLMでのオイラー数問題を題材にした精度・速度比較

## 原文リンク

[完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤](https://zenn.dev/motowo/articles/local-ai-code-review-design)
