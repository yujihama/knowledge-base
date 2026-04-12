---
title: "コミュニティで共同構築するデータセット：ArgillaとHugging Face Spacesを活用した集合知によるデータ収集"
url: "https://huggingface.co/blog/community-datasets"
date: 2026-04-09
tags: [Argilla, HuggingFace, データセット構築, 選好データ, アノテーション, RLHF, コミュニティ]
category: "ai-ml"
memo: "[HF Blog] Data is better together: Enabling communities to collectively build better datasets together using Argilla and Hugging Face Spaces"
processed_at: "2026-04-09T12:23:24.685543"
---

## 要約

2024年3月、ArgillとHugging Faceは「Data is Better Together」という実験的取り組みを発表した。これはコミュニティが集合的に選好データセットを構築するプロジェクトであり、数日間で350名のコントリビューターが参加し、11,000件以上のプロンプト評価が収集された。その結果、10,000件のプロンプトとユーザー評価からなる「10k_prompts_ranked」データセットが公開された。

技術的な仕組みとして、ArgillaはLLMや特化型モデル向けのオープンソースアノテーションツールであり、Hugging Face SpacesはMLデモ・アプリのホスティングプラットフォームである。今回の核心となる新機能は、Hugging FaceアカウントによるArgilla認証の統合であり、これによりユーザーは数秒でアノテーションタスクへの貢献を開始できるようになった。従来の集合的データ構築の障壁だったセットアップの複雑さが大幅に解消された。

背景として、多言語・多ドメイン・多タスクにわたる高品質データセットの不足が依然としてML開発の課題であることが指摘されている。Hugging Face Hub上では既に数千のモデル・データセット・デモが共有されているが、データ構築への参加にはMLや程的スキルが必要とされてきた。このイニシアチブはその壁を除去し、非エンジニアも含む幅広いコミュニティがAI開発に貢献できる仕組みを目指す。

具体的な支援内容として、初期コホートに参加するコミュニティには、Hugging Faceによる無料の永続ストレージとCPU Spacesの提供、ArgillとHugging Faceによる広報支援、専用コミュニティチャンネルへの招待が含まれる。対象プロジェクトは主にテキストベースのデータセットであり、現在十分なデータが存在しない言語・ドメイン・タスクに焦点を当てたものが優先される。参加希望者はHugging Face Discordの「#data-is-better-together」チャンネルを通じて応募できる。

## アイデア

- HFアカウント認証によるArgilla統合により、アノテーション参加のフリクションをほぼゼロにした設計は、大規模な人間フィードバック収集の実用的モデルとして注目に値する
- MLスキル不要でAI開発に貢献できる仕組みはドメイン専門家（監査・法務・医療等）から高品質な専門知識ラベルを収集する際に応用可能
- 350名・11,000件を数日で収集した実績は、コミュニティ駆動の選好データ収集がRLHF/RLAIFのスケールアップに現実的な選択肢であることを示す
## 関連記事

- /deep_906 Argilla 2.4: コード不要でHugging Face Hub上のファインチューニング・評価データセットを構築
- /deep_1391 中国語話者向けHugging Faceブログ開設：中国AIコミュニティとの協働促進
- /deep_835 Synthetic Data Generator：自然言語でデータセットを構築するノーコードツール
- /deep_1213 Prodigy-HFの紹介：Hugging Faceとの直接統合
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム

## 原文リンク

[コミュニティで共同構築するデータセット：ArgillaとHugging Face Spacesを活用した集合知によるデータ収集](https://huggingface.co/blog/community-datasets)
