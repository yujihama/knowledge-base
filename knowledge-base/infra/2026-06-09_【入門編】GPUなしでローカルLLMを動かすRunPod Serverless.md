---
title: "【入門編】GPUなしでローカルLLMを動かすRunPod Serverless"
url: "https://zenn.dev/fkky/articles/41b86131fd14ec"
date: 2026-06-09
tags: [RunPod, Serverless, GPU, Hugging Face, LLM推論, Docker, Model Cache, API]
category: "infra"
related: [3650, 7407, 2815, 1883, 3513]
memo: "[Zenn LLM] 【入門編】GPUなしでローカルLLMを動かすRunPod Serverless"
processed_at: "2026-06-09T09:08:27.554271"
---

## 要約

RunPod Serverlessは、必要なときだけGPUインスタンスを起動するAWSラムダ型のGPUクラウドサービスで、個人が低コストでLLM推論・動画生成を実行できる環境を提供する。常時起動型の「Pod」と対比して、Serverlessはリクエスト受信時にワーカーを自動起動し、処理完了後に自動停止する仕組みを取る。A100クラスのGPUでも1秒あたり約0.1円前後のコストで、動画生成（Wan2.2使用時）は1本3円以下での実行が可能。

最大の特徴はModel Cacheと呼ばれる機能で、Hugging Faceのリポジトリパス（例: Qwen/Qwen2.5-7B-Instruct）を指定すると、ワーカー課金時間外にモデルを自動ダウンロード・キャッシュする。これによりDockerイメージへのモデル焼き込みや、ダウンロード待機時間への課金が不要になる。

デプロイ方法は2種類あり、（1）GitHubリポジトリを直接連携してDockerfileからビルドする方法と、（2）ビルド済みイメージを直接指定する方法がある。前者はリモートプッシュ時に自動ビルドが走り、起動中のワーカーが新イメージへ順次切り替わる仕組みのため、手軽さで推奨されている。

API仕様は非同期実行（/run）と同期実行（/runsync）の2モードを持ち、/runはジョブIDを即座に返してステータスをポーリングする設計。ジョブ結果は完了後30分間のみ取得可能。リクエストはinputキーを最上位に持つJSONが基本形で、inputの内容はワーカーのハンドラ実装に依存する。ステータスはIN_QUEUE/IN_PROGRESS/COMPLETED/FAILED/CANCELLED/TIMED_OUTの6種類。

推奨設定として、Active Workers（常時課金ワーカー）は0、Idle Timeoutは最小値の1秒に設定することでコストを最小化できる。初回チャージ最低額は$10で無料枠はないが、招待リンク経由で$5クレジットが双方に付与される。監査エージェント開発への応用としては、ローカル環境にGPUを持たない状態でも推論APIを従量制で利用できるため、LLM-as-judgeの評価サービスやエージェント内の補助推論エンジンをコスト効率よく試せる点が有用。

## アイデア

- Model Cache機能によりモデルダウンロード時間を課金対象外にする設計は、コールドスタート問題をコスト面から巧みに回避している
- Active Workers=0・Idle Timeout=1秒の設定でほぼ完全な従量課金を実現し、個人利用での固定費をゼロに近づけられる
- GitHubリポジトリ連携による自動ビルド・ローリングアップデートの仕組みは、推論ロジックのCI/CDパイプラインとして機能し、モデル切り替えを宣言的に管理できる

## 前提知識

- **Serverless アーキテクチャ** (TODO: 読むべき)
- **Docker コンテナ** (TODO: 読むべき)
- **Hugging Face モデルハブ** (TODO: 読むべき)
- **REST API / curl** (TODO: 読むべき)
- **GPU クラウド** (TODO: 読むべき)

## 関連記事

- /deep_3650 GPUクラウドRunpodを利用するときのTips
- /deep_7407 米国で広がる「個人向けGPU従量課金レンタル」市場の全体像と、日本展開の可能性【2026年版】
- /deep_2815 Ubuntu Server に Docker と GPU ドライバをインストールする
- /deep_1883 Google Cloud上でサーバーレスTransformersパイプラインを構築した記録
- /deep_3513 EC2でLLM推論のコールドスタートをどこまで短縮できるか検証してみた

## 原文リンク

[【入門編】GPUなしでローカルLLMを動かすRunPod Serverless](https://zenn.dev/fkky/articles/41b86131fd14ec)
