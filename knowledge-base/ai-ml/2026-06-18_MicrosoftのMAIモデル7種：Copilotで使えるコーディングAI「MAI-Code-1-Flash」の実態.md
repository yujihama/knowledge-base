---
title: "MicrosoftのMAIモデル7種：Copilotで使えるコーディングAI「MAI-Code-1-Flash」の実態"
url: "https://zenn.dev/okssusucha/articles/20260618-microsoft-mai-models-2026"
date: 2026-06-18
tags: [MAI-Code-1-Flash, MAI-Thinking-1, MoE, GitHub Copilot, SWE-Bench, Microsoft AI, コーディングモデル, 蒸留なし学習]
category: "ai-ml"
related: [8550, 7411, 5469, 1964, 7831]
memo: "[Zenn LLM] Microsoftの自社モデルMAI 7種、Copilotで使えるコーディングAIの中身"
processed_at: "2026-06-18T21:15:18.563603"
---

## 要約

Microsoft Build 2026（2026年6月初頭）でMicrosoft AI部門が7つのMAIモデルを一斉発表した。モダリティ別の内訳は、推論（MAI-Thinking-1）、コーディング（MAI-Code-1-Flash）、画像生成（MAI-Image-2.5）、文字起こし（MAI-Transcribe-1.5、43言語対応）、音声合成（MAI-Voice-2）およびそれぞれのFlash派生版。

即座に使えるのはMAI-Code-1-Flashで、活性パラメータ50億の軽量コーディングモデルとしてVS CodeのGitHub Copilot個人ユーザー向けにロールアウト済み。モデルピッカーで明示選択可能なほか、Copilotのauto pickerの候補にも組み込まれている。ベンチマーク比較のターゲットはAnthropic Claude Haiku 4.5で、SWE-Bench Pro（実際のGitHub issueにパッチを当てるベンチマーク）でMAI-Code-1-Flashが51.2%、Haiku 4.5が35.2%と15ポイント以上の差。さらにSWE-Bench Verifiedでは最大60%少ないトークンで問題を解けるとMicrosoftは主張しており、エージェントを対話的に回す用途ではレイテンシとコスト両面で効いてくる。

フラッグシップ推論モデルMAI-Thinking-1は「活性パラメータ35B、総パラメータ約1兆」のMixture of Experts（MoE）構成。発表直後にSimon Willison氏が「35BモデルなのにSonnet 4.6より好まれる」と評したが、これは活性パラメータと総パラメータの混同による誤読であり、後に訂正された。実態は規模相応の大型モデルで、AIME 2025で97.0%、AIME 2026で94.5%、SWE-Bench ProでClaude Opus 4.6と互角、1,276タスクの人間ブラインド評価ではClaude Sonnet 4.6より好まれたとされる。コンテキスト長は256kトークン（約600ページ相当）。現時点ではMicrosoft Foundryのプライベートプレビューのみ。

Microsoftは「第三者モデルからの蒸留なし、クリーンでトレーサブルなエンタープライズグレードデータでゼロから学習」と強調するが、Simon Willison氏は初報後に「適切にライセンスされたデータ」という説明は額面どおりに受け取れないと記事を訂正。データ来歴の主張は現時点で検証が追いついていない。ベンチマーク数値や提供形態は確認できる事実だが、「クリーンなデータ・蒸留なし」の主張には留保が必要。

構造的な意義として、これまでOpenAIの最大顧客かつ最大出資者だったMicrosoftが、フロンティア級の推論モデルを自社開発したことでOpenAI依存から自立しようとしている点が大きい。監査エージェント開発への示唆としては、SWE-Bench Proのスコアが高くトークン消費が少ないMAI-Code-1-Flashは、コード生成・パッチ検証を繰り返すエージェントループのコスト最適化に有効な選択肢となりうる。マルチプロバイダ前提のエージェント設計においては、モデルの選択肢がさらに広がった。

## アイデア

- MoEの活性パラメータ（35B）と総パラメータ（1兆）の混同問題：各社でパラメータ表記が揺れており、ベンチマーク比較時にモデル規模を誤読するリスクが実際に起きた事例として参考になる
- SWE-Bench Proで60%少ないトークンで同等以上の精度を達成する設計：トークン効率はエージェントループのコスト・レイテンシに直結するため、小型モデル選定の指標としてスコアだけでなくトークン消費量も重要な評価軸になる
- 「蒸留なし・クリーンデータ」の主張とその検証困難性：学習データの来歴主張はエンタープライズ導入の法的リスクと直結するが、外部検証が追いつかない現状はモデル選定時のデューデリジェンス上の盲点になりうる

## 前提知識

- **Mixture of Experts (MoE)** → /deep_150 TransformersライブラリにおけるMixture of Experts (MoE)の実装と最適化
- **SWE-Bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **知識蒸留 (Distillation)** (TODO: 読むべき)
- **GitHub Copilot** → /deep_1739 8リポジトリに同じ変更を並列展開したら、Copilotレビューのばらつきがシグナルになった話
- **活性パラメータ vs 総パラメータ** (TODO: 読むべき)

## 関連記事

- /deep_8550 思考をオフにできないOSSコーディングモデル Kimi K2.7 Code
- /deep_7411 中国のAIモデルを実用目線で整理する（2026年6月）
- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド
- /deep_1964 GLM-5.1徹底レビュー：200Kトークンコンテキストと8時間自律実行が拓くコード生成の新地平
- /deep_7831 Copilot CLI モデル別コスパ比較 (2026年6月版) — SWE-bench × Pareto frontier

## 原文リンク

[MicrosoftのMAIモデル7種：Copilotで使えるコーディングAI「MAI-Code-1-Flash」の実態](https://zenn.dev/okssusucha/articles/20260618-microsoft-mai-models-2026)
