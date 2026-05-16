---
title: "Windows上でDevinが動作するようになっていた、そして広がる可能性"
url: "https://zenn.dev/smasato/articles/77b42be3c85f7c"
date: 2026-05-10
tags: [Devin, Windows, ブループリント, 宣言的構成, マルチプラットフォーム, GitHub Actions, Cognition]
category: "infra"
related: [3648, 4035, 4328, 3001, 2367]
memo: "[Zenn LLM] Windows上でDevinが動作するようになっていた、そして広がる可能性"
processed_at: "2026-05-10T09:34:18.729691"
---

## 要約

CognitionのAIソフトウェアエンジニアDevinが、従来のLinux（Ubuntu）専用環境からWindowsをサポートするようになった。現時点では限定提供（要問い合わせ）だが、公式ドキュメントに「Windows サポート」ページが追加され、.NETやVisual Studio / C++プロジェクト向けのブループリント例も公開されている。

Windowsサポートの実現は、DevinのブループリントによるCI設定の宣言的構成（`.devin/blueprints/`配下のYAML定義）を基盤としている。`runs-on: windows`を指定するだけでWindows環境を対象にでき、`runs-on: [default, windows]`と書けばLinux/Windowsの共通ブループリントを定義できる。LinuxとWindowsでホームディレクトリ（`/home/ubuntu` vs `/c/Users/Administrator`）やパッケージマネージャー（`apt-get` vs `choco`/`winget`）が異なるが、bashはどちらでも利用可能。差分の吸収にはGitHub Actionsのアクション（例：`github.com/actions/setup-node@v4`）を`uses:`キーで呼び出せる仕組みが既に組み込まれており、これがマルチプラットフォーム対応の布石になっていたと著者は考察する。

宣言的構成が導入された本質的な意義として、従来の対話的スナップショット方式では秘伝のタレ化・OSアップグレード困難という問題があったが、宣言的構成ではスナップショットをゼロからビルドするため、Cognition側が既存スナップショットを気にせずOSやインフラを変更できるようになった点が挙げられる。ユーザー側はEnterprise/組織/リポジトリ単位でブループリントを定義し、基盤層の変更はCognitionが管理するという二層構造が実現した。

今後の展望として、著者はmacOSサポートの追加、およびLinux限定のComputer Use機能のWindows/macOS対応を予測する。GitHub Actionsエコシステムとの統合により、ユーザーが最小限の定義でマルチプラットフォーム対応ワークフローを構築できる方向性は、監査エージェント等の業務AIシステムをWindows環境（Active Directory連携・.NETスタック等）で動作させる可能性を広げるものとして注目に値する。

## アイデア

- GitHub Actionsの`runs-on`構文をそのままAIエージェントのブループリントに転用する設計は、既存CI/CDエコシステムとの統合を最小学習コストで実現する合理的なアーキテクチャ判断
- スナップショットの秘伝のタレ化問題を宣言的構成（毎日ゼロビルド）で解決するアプローチは、監査エージェントシステムの環境再現性・監査証跡の観点でも応用できる設計原則
- ユーザー層（ブループリント定義）とプラットフォーム層（OS管理）を分離する二層アーキテクチャにより、Cognitionがユーザー影響ゼロでインフラを刷新できる構造は、マルチテナントAIサービス設計のモデルケース

## 前提知識

- **Devin Blueprint** (TODO: 読むべき)
- **宣言的構成** (TODO: 読むべき)
- **GitHub Actions runs-on** (TODO: 読むべき)
- **Chocolatey/winget** (TODO: 読むべき)
- **Computer Use** → /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則

## 関連記事

- /deep_3648 機械学習論文を毎日自動収集してAIで日本語解説するサイトを作った（MLinfo）
- /deep_4035 GitHub Copilotで既存ソフトウェアを改修するためのコンテキスト設計
- /deep_4328 Devin 2.2とDeNA全社2,000名導入 — 自律型AIエンジニアの実用フェーズ
- /deep_3001 AIコーディングツールを乗り換えまくっていたら、エージェント経済の入口にいた
- /deep_2367 AIエージェント3体にAI業界を毎朝分析させて55日が経った：軍事インテリジェンス手法をLLMに載せた自動分析システム

## 原文リンク

[Windows上でDevinが動作するようになっていた、そして広がる可能性](https://zenn.dev/smasato/articles/77b42be3c85f7c)
