---
title: "外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline"
url: "https://tldr.takara.ai/p/2604.00784"
date: 2026-04-08
tags: [VLM, surgical-video, multimodal, fine-tuning, dataset, spatial-temporal, in-context-learning, video-understanding]
category: "ai-ml"
memo: "[HF Daily Papers] An Approach to Enriching Surgical Video Datasets for Fine-Grained Spatial-Temporal Understanding of Vision-Language Models"
related: [1608, 975, 650, 522, 71]
processed_at: "2026-04-08T12:22:30.466541"
---

## 要約

外科手術動画の理解は、コンピュータ支援手術（Computer-Assisted Surgery）の発展に不可欠な要素であるが、既存の外科向けビジョン言語（VLM）データセットは、複雑に絡み合った空間的・時間的ダイナミクスを十分に捉えられていないという課題があった。本研究では、この課題に対処するため「SurgSTU-Pipeline」と呼ばれる決定論的なデータセット生成パイプラインを提案している。

従来、外科動画データセットの大規模構築には2つの障壁があった。①専門家による手動アノテーションの高コスト、②大規模言語モデル（LLM）を利用した自動生成におけるエラー発生リスク、である。SurgSTU-Pipelineはこれを「時間的連続性フィルタリング（temporal continuity filtering）」と「空間的連続性フィルタリング（spatial continuity filtering）」という2段階のフィルタリング機構を組み込むことで、信頼性の高い決定論的生成を実現している。

このパイプラインを公開済みの外科手術データセットに適用した結果、「SurgSTU dataset」が構築された。このデータセットは7,515件の動画クリップに対して、15万件（150k）の細粒度な空間・時間 Q&Aサンプルを付与したものである。

評価実験の結果、以下の知見が得られた。①最新の汎用 VLM（GPT-4V 系等）はゼロショット設定において外科動画の時空間理解で苦戦する。②In-context learning（文脈内学習）を活用することで、これら汎用モデルの空間・時間的能力は改善可能。③SurgSTUの訓練データでファインチューニングしたVLMは、すべての空間・時間タスクにおいて最高性能を達成し、データセットの有効性が実証された。コードは今後公開予定。

## アイデア

- 決定論的パイプラインによる大規模QAデータセット生成という手法は、ドメイン特化VLMのファインチューニング用データを低コストで構築する汎用的なアプローチとして参考になる
- 時間的・空間的連続性フィルタリングという2段階フィルタで生成品質を担保する設計は、LLMによる自動生成の誤り混入問題への実践的な解答であり、他ドメインへの転用可能性が高い
- 汎用VLMがゼロショットで専門ドメイン（手術動画）に適用困難な一方、In-context learningで改善できるという知見は、少数サンプルでのドメイン適応戦略を検討する際に有用

## 関連記事

- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_522 TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク
- /deep_71 Sensible Agent: プロアクティブARエージェントとの非侵襲的インタラクションフレームワーク

## 原文リンク

[外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline](https://tldr.takara.ai/p/2604.00784)
