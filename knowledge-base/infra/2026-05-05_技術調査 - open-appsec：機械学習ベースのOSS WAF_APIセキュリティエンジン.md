---
title: "技術調査 - open-appsec：機械学習ベースのOSS WAF/APIセキュリティエンジン"
url: "https://zenn.dev/suwash/articles/open-appsec_20260427"
date: 2026-05-05
tags: [WAF, open-appsec, 機械学習, Kubernetes, NGINX, OWASP, ゼロデイ防御, APIセキュリティ, OSS, Check Point]
category: "infra"
related: [1754, 2550, 396, 1335, 568]
memo: "[Zenn 機械学習] 技術調査 - open-appsec"
processed_at: "2026-05-05T12:08:29.614594"
---

## 要約

open-appsecはCheck Point Software Technologiesが開発・公開する機械学習ベースのOSS Web Application Firewall（WAF）およびAPIセキュリティエンジン。Apache 2.0ライセンスで提供されるコアエンジンを持ち、NGINX・Kong・APISIX・Envoy・Istioといった主要リバースプロキシや APIゲートウェイにアタッチメントとして統合できる。Linux・Docker・Kubernetes環境に対応し、シグネチャや手動ルール不要でOWASP Top 10およびゼロデイ攻撃を防御する。

ML検出エンジンは2段階構成を採る。Phase 1のSupervised Modelは数百万件の攻撃・正常リクエストをCloud側でオフライン学習した汎用脅威検出モデルで、Fog SaaS（downloads.openappsec.io）から自動配信される。Phase 2のUnsupervised Model（Adaptive Learning）は保護対象環境内でリアルタイムに構築され、URLパス・ヘッダー・パラメーター分布などの特徴量から環境固有の正常パターンを学習する。SmartSyncサービスが複数エージェント間の学習データを集約し、SmartSync-Tuningが継続的なチューニング提案を生成する。両モデルの統合判定結果はeventConfidence（Low/Medium/High/Very High）として出力される。

提供形態は3種類。Local Managed（AGENT_TOKEN不要、オフライン運用可、Apache 2.0無料）、Centrally Managed（my.openappsec.ioのSaaS管理、無料利用可・Premium Edition月額$79〜）、商用CloudGuard WAF。エージェントバイナリ（cp-nano-agent）は共通OSS。AGENT_TOKENの有無で動作モードが切り替わる設計のため、Local ManagedからCentrally Managedへの段階移行が容易。

アーキテクチャはAttachment Module（HTTPデータ抽出）→ cp-nano-agent（Orchestrator・HTTP Transaction Handler・WAF2 Engine・Deep Parser・Watchdog）の構成。NGINX-Agent間はIPC共有メモリ（Docker環境では--ipc=hostオプション）で通信し、OrchestratorはFog SaaSとOAuth 2.0・256bitキー認証・JWTでTLS接続する。

ModSecurity（2024年7月EOL）・Coraza・NGINX App Protectとの比較では、open-appsecのみがシグネチャ不要の2モデルML検出とゼロデイ先制防御を提供。Log4Shell・Spring4Shell・Text4Shellをシグネチャなしで事前ブロックした実績を持つ。True Positive Rateは99.368%（Defaultプロファイル、open-appsec公開レポート）。IPSは2,800以上のWeb CVEをカバーし、OpenAPIスキーマバリデーション・アンチボット・ファイルセキュリティ・CrowdSec連携も内蔵する。

監査エージェント開発への示唆：WAFのML判定ログ（eventConfidence、攻撃クラス、URL等）をLangGraphベースの監査エージェントのデータソースとして活用することで、セキュリティインシデントの自動証跡収集・リスク分類パイプラインを構築できる。Local Managedのオフライン運用能力は機密性の高い内部監査環境への導入適性が高い。

## アイデア

- Supervised+Unsupervisedの2段階MLパイプラインにより、グローバル脅威知識とローカル環境固有の正常パターンを組み合わせた判定が可能で、シグネチャ更新サイクルを排除している点
- AGENT_TOKENの有無だけでLocal/Centrally Managedを切り替える設計により、オフライン環境で検証後にそのままSaaS管理へ段階移行できるアーキテクチャ上の柔軟性
- SmartSyncによるエージェント間学習データ集約が、分散Kubernetesクラスター全体での適応学習精度向上を実現している点（単一エージェントより多様なトラフィックパターンを学習できる）

## 前提知識

- **WAF（Web Application Firewall）** (TODO: 読むべき)
- **教師あり/教師なし学習** (TODO: 読むべき)
- **OWASP Top 10** (TODO: 読むべき)
- **Kubernetes CRD** (TODO: 読むべき)
- **リバースプロキシ** (TODO: 読むべき)

## 関連記事

- /deep_1754 🤗 AIリサーチ・レジデンシープログラムの発表
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_396 機械学習モデル構築：PythonフレームワークとBigQuery MLの違いと使い分け
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_568 天文学から占星術へ：機械学習による星座ベース性格予測の幻想を検証する

## 原文リンク

[技術調査 - open-appsec：機械学習ベースのOSS WAF/APIセキュリティエンジン](https://zenn.dev/suwash/articles/open-appsec_20260427)
