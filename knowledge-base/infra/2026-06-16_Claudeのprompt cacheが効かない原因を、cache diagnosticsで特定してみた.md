---
title: "Claudeのprompt cacheが効かない原因を、cache diagnosticsで特定してみた"
url: "https://zenn.dev/mochitec_tech/articles/cff58bf183c643"
date: 2026-06-16
tags: [prompt caching, cache diagnostics, Claude API, Anthropic, Observability, コスト最適化, beta機能]
category: "infra"
related: [2293, 4816, 6753, 3240, 2960]
memo: "[Zenn LLM] Claudeのprompt cacheが効かない原因を、cache diagnosticsで特定してみた"
processed_at: "2026-06-16T09:03:32.459304"
---

## 要約

Anthropicが2026年5月13日にbeta公開したcache diagnostics機能を最小構成で検証した記事。prompt cachingはプロンプトの先頭がバイト単位で完全一致する場合のみ有効で、これまでキャッシュミスの原因はcache_read_input_tokensがゼロになることしか観測できず、原因特定は勘に頼るしかなかった。cache diagnosticsはbetaヘッダー「anthropic-beta: cache-diagnosis-2026-04-07」を付けることで利用可能になり、リクエストごとに軽量なフィンガープリント（ハッシュとトークン数推定値）を保存する。次のリクエストでprevious_message_idとして前回のレスポンスidを渡すと、APIが新旧フィンガープリントを比較し最初の分岐点をdiagnosticsオブジェクトで返す。生のプロンプトは保存しないためZDR適格。返却されるcache_miss_reason.typeは6種類：model_changed（別モデルに切り替わった）、system_changed（systemプロンプトが変化）、tools_changed（toolsの追加・並べ替え・非決定的シリアライズ）、messages_changed（過去メッセージの編集・切り詰め）、previous_message_not_found（フィンガープリントが存在しない）、unavailable（比較不能）。実験ではclaude-opus-4-8でターン1に約6,275トークンのキャッシュを書き込み、ターン2でcache_read_input_tokens=6,275のヒットを確認。意図的にsystemプロンプト末尾にtimestampを差し込んだターン3ではcache_read_input_tokens=0となり、diagnosticsがsystem_changedを返した。cache_missed_input_tokensは6,610で、分岐以降のprefixが丸ごと無効になった規模感を示す（課金数値ではなくバイト長由来の概算）。diagnosticsは「リクエストが変わったか」、usageは「キャッシュがヒットしたか」の2軸で読むのが基本で、両方nullかつcache_read高ければ正常、*_changedかつread低ければ自分のバグ、nullかつread低ければTTL切れの可能性と切り分けられる。注意点として、tool_choice/thinking/context_managementなどのパラメータ差分があるとunavailableになる、フィンガープリントの保持期間は短くバッチでの時間空きに弱い、などがある。現在Bedrock/Vertexでは未対応。監査エージェント開発においてキャッシュ前提のコスト設計を行う際、デプロイ前にcache_miss_reasonを確認することで、キャッシュ崩れの原因をコード変更と紐づけて検出できる。

## アイデア

- フィンガープリントに生プロンプトを保存せずハッシュのみを持つ設計により、ZDR（Zero Data Retention）適格を維持しながらデバッグ情報を提供する点が実用的
- cache_miss_reasonが最初の分岐点のみを返す仕様により、前から順に修正するという明確な修正戦略が導ける（後段の分岐は隠れるため）
- diagnostics（リクエスト変化の有無）とusage.cache_read_input_tokens（ヒットの有無）を2軸で組み合わせることで、「自分のバグ」と「TTL切れ」を切り分けられる診断マトリクスが監査ログ分析の手法として応用できる

## 前提知識

- **prompt caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- **Claude API** → /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- **multi-turn conversation** → /deep_1462 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **cache_control ephemeral** (TODO: 読むべき)
- **beta header** (TODO: 読むべき)

## 関連記事

- /deep_2293 【2026年】Claude APIを最安で使う方法：サブスク不要で40%以上節約
- /deep_4816 マルチモデルルーティング入門：GPT・Claude・Geminiを使い分ける実装パターン
- /deep_6753 RAGのコスト問題を1/15に削る ― 「毎回検索しない」4層アーキテクチャの設計
- /deep_3240 Opus 4.7 に移行するなら 
- /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）

## 原文リンク

[Claudeのprompt cacheが効かない原因を、cache diagnosticsで特定してみた](https://zenn.dev/mochitec_tech/articles/cff58bf183c643)
