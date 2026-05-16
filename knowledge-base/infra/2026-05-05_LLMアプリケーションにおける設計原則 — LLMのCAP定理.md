---
title: "LLMアプリケーションにおける設計原則 — LLMのCAP定理"
url: "https://zenn.dev/hsaki/articles/llm-cap-theorem"
date: 2026-05-05
tags: [LLM設計原則, CAP定理, TPM/RPM, Provisioned Throughput, AI Gateway, SLO/SLA, BYOC, レートリミット, フォールバック, キャパシティ管理]
category: "infra"
related: [2592, 3091, 2951, 1427]
memo: "[Zenn LLM] LLMアプリケーションにおける設計Principal - LLMのCAP定理"
processed_at: "2026-05-05T12:04:40.178226"
---

## 要約

分散システムのCAP定理（Consistency・Availability・Partition tolerance）と構造的に同型なトレードオフがLLMアプリケーション設計にも存在するという主張。著者はC=Consistency（利用モデルの一貫性）・A=Availability（TPM/RPMクオータ内での応答継続）・P=Price（利用コスト）の3軸を提案し、3つを同時に満たす設計は不可能と論じる。

**CA選択（Pを捨てる）**: 単一モデルに絞りAmazon BedrockのReserved Tier・Azure OpenAIのPTU・Vertex AIのProvisioned Throughputなどでスループットを予約。閑散時の無駄コストとトークン単価の割高感が生じる。

**CP選択（Aを捨てる）**: 高品質モデルを従量課金で使い続けるが、規模拡大後にTPM/RPM超過で429エラーが頻発しレイテンシ悪化・リトライ増大を招く。

**AP選択（Cを捨てる）**: Azure API ManagementのAI GatewayやCloudflare AI GatewayのFallback機能で複数モデルを切り替えて可用性を確保するが、モデル間で出力品質が不均一になり、複数モデルの同時チューニング・メンテナンスコストが増加する。

可用性管理については、LLMプロバイダーがTPM/RPMという**速度指標**でSLOを定義するのに対し、エンドユーザーは**リクエスト成功率・稼働率（数指標）**を期待するという根本的な齟齬を指摘。トラフィックが特定時間帯に集中する場合、速度指標→数指標への変換過程でSLI数値が大幅に下落する（例：144,000リクエストを1分に集中させるとSuccess Rate≈0.7%）。

この問題への対応策として：①AI機能と非AI機能でSLO/SLAを分離する、②サービスTierごとに異なるSLAを設ける、③BYOC（Bring Your Own Credential）やOAuth2でLLMクオータ管理をユーザー側に委譲する、④429発生時はリトライ・バックオフ・リクエストキューイングで吸収しつつ202非同期返却でユーザー期待値をコントロールする、といったアーキテクチャパターンを提案。監査エージェント開発への示唆としては、エージェントが高頻度でLLMを呼ぶ構成ではCP戦略から始め、スループット上限に近づいたらAP（マルチモデルフォールバック）への移行を検討する設計判断フレームワークとして活用できる。ビジネスサイドも含めた意思決定者全員がこのトレードオフを腹落ちした上でプロダクト優先度を決める必要があると強調している。

## アイデア

- 分散システムのCAP定理をLLM設計に転用し、Partition toleranceをPriceに置き換えることでC/A/Pトレードオフとして再定式化した点が新鮮で、設計議論の共通言語として使いやすい
- LLMプロバイダーの速度指標SLI（TPM/RPM）とエンドユーザーが期待する数指標SLI（成功率・稼働率）の構造的ミスマッチを定量例（Success Rate 0.7%）で示した点が実務的に重要
- BYOC（Bring Your Own Credential）でLLMクオータ管理責任をユーザーに委譲するというアーキテクチャパターンは、ITリテラシーが高い開発者向けツール（Claude Code等）では有効な可用性管理手法

## 前提知識

- **CAP定理** (TODO: 読むべき)
- **TPM/RPM** (TODO: 読むべき)
- **SLO/SLI** (TODO: 読むべき)
- **Provisioned Throughput** (TODO: 読むべき)
- **429 Too Many Requests** (TODO: 読むべき)

## 関連記事

- /deep_2592 LiteLLM 入門 ── 複数 LLM を統一インターフェースで扱う AI Gateway
- /deep_3091 LiteLLM vs OpenRouter vs Portkey: LLMゲートウェイ完全比較【2026年版】
- /deep_2951 CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計
- /deep_1427 Claude Code CLIをGLM/MiniMaxで代替した話（コスト大幅削減の実測）

## 原文リンク

[LLMアプリケーションにおける設計原則 — LLMのCAP定理](https://zenn.dev/hsaki/articles/llm-cap-theorem)
