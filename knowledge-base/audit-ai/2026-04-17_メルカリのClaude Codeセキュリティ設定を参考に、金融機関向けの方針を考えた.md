---
title: "メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた"
url: "https://zenn.dev/nekoai_lab/articles/fe200eacaf70ae"
date: 2026-04-17
tags: [Claude Code, Amazon Bedrock, FISC, MDM, managed-settings.json, CloudTrail, S3 Object Lock, WORM, PrivateLink, AIガバナンス, 金融規制, MCP, IAM最小権限, SIEM]
category: "audit-ai"
related: [430, 13, 51, 2059, 9]
memo: "[Zenn LLM] メルカリの Claude Code セキュリティ設定を参考に、金融機関向けの方針を考えた"
processed_at: "2026-04-17T12:30:16.148398"
---

## 要約

本記事は、メルカリAI Security Teamが公表した「Claude Codeセキュリティ設定の組織配布戦略」を出発点に、日本の金融機関固有の要件（FISC安全対策基準・データ越境・監査証跡・AIガバナンス）を満たすための追加対策を個人が体系的に整理したものである。

メルカリの構成はMDM（Jamf/Kandji/Intune）でmanaged-settings.jsonを全端末に強制配布し、bypassPermissionsDisabled: trueで--dangerously-skip-permissionsを封じ、.env・SSHキー等へのReadとcurl/wget/rm -rfをdenyリストに明記する。エンジニア/非エンジニアをTier別プロファイルで分離し、非エンジニアにはdisableUserConfig: trueも付与する。これにより端末・設定層の統制はほぼ完結する。

一方、金融機関には以下4つの不足がある。①データ越境：Claude Codeのデフォルト接続先は米国Anthropicサーバーであり、顧客情報や与信ロジックを含むコードを処理すると個人情報保護法の第三国提供に該当しうる。②FISC対応：Anthropicを外部委託先として評価するにはSOC 2 Type II報告書のNDA取得から始まる実務的ハードルが高い。③監査証跡：AIへの入出力を7年間WORM保存し当局検査で提示できる必要がある。④AIガバナンス：金融庁AIディスカッションペーパー（2025年3月）への対応として経営レベルの統制が求められる。

これら①〜③をまとめて解決する手段がAmazon Bedrock東京リージョン（ap-northeast-1）経由の接続である。MDMのenvセクションでANTHROPIC_BASE_URLをBedrock Runtime エンドポイントに固定し、CLAUDE_CODE_USE_BEDROCK=1を設定することでAnthropicへの直接接続をManaged設定レベルで禁止できる。Bedrockを採用すると、処理が日本リージョン内で完結しデータ越境が消え、外部委託先評価対象がFISC対応済みのAWSになり、CloudTrailが全API呼び出しを自動記録する。S3 Object LockをCOMPLIANCEモード・7年保持で設定することで改ざん防止要件も充足する。IAM権限はbedrock:InvokeModelとbedrock:InvokeModelWithResponseStreamのみに絞り、S3/RDS/SecretsManagerへのアクセスをClaudeの実行コンテキストから完全に排除する。

みずほフィナンシャルグループはAWS Summit Japan 2025でこの構成の採用を公表しており、PrivateLinkによる閉域接続でパブリックインターネットを経由しない構成を実現している。

監査・ガバナンス層では、CloudTrailログをKinesis Data Firehose経由でSplunkやMicrosoft SentinelなどのSIEMにリアルタイム転送し、事後参照だけでは満たせない監査証跡要件に対応する。AIガバナンス委員会はCISOを委員長とし、CTO・コンプライアンス部長・法務部長を委員として設置し年次レビューと重大インシデントの報告ラインを規定する。CI/CDへのClaude Code組み込み時は-pフラグ利用のリスクが高まるため、CI用IAMロールの完全分離と.claude/settings.jsonのPR変更に2名以上のApproval必須（情報セキュリティ部門をRequired Reviewer）を義務付ける。

監査エージェント開発への示唆として、本構成はLangGraph等のエージェントがAWS上でClaudeを呼び出す際にも直接適用できる。BedrockのCloudTrail統合をエージェントの操作ログと突合することで、エージェント行動の完全な監査証跡を金融規制水準で実現できる点が重要である。

## アイデア

- ANTHROPIC_BASE_URLをMDMのManaged設定（ユーザー変更不可）レベルでBedrock東京リージョンに固定することで、端末設定層とインフラ層を単一の配布ファイルで同時に制御できる設計が巧み
- S3 Object LockのCOMPLIANCEモード（管理者でも削除不可）とGOVERNANCEモード（管理者は削除可）の使い分けを金融機関要件から明示している点が実務的に有用
- 外部委託先評価の対象をAnthropicではなくAWS（FISC対応済み）にスライドさせることで、SOC 2 Type II取得交渉を省略できるという契約構造の逆転発想

## 前提知識

- **Amazon Bedrock** → /deep_2060 「この文書たちをAIに学ばせたい」に1日で応えた話 ── Amazon Bedrock Knowledge Basesで作る社内RAG
- **MDM / managed-settings.json** (TODO: 読むべき)
- **CloudTrail / S3 Object Lock** (TODO: 読むべき)
- **FISC安全対策基準** (TODO: 読むべき)
- **MCP (Model Context Protocol)** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装
- /deep_51 SaaSを個人開発して運営しているが、本当に「SaaS is Dead」を感じ始めている
- /deep_2059 LLMを使って開発するなら、可観測性を最初から考えておくべきだった
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装

## 原文リンク

[メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた](https://zenn.dev/nekoai_lab/articles/fe200eacaf70ae)
