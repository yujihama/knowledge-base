---
title: "OmniWeaving: 自由形式の構成と推論を用いた統合動画生成モデル"
url: "https://tldr.takara.ai/p/2603.24458"
date: 2026-04-06
tags: [video-generation, multimodal, unified-model, reasoning, open-source, benchmark, pretraining]
category: "ai-ml"
memo: "[HF Daily Papers] OmniWeaving: Towards Unified Video Generation with Free-form Composition and Reasoning"
processed_at: "2026-04-06T21:00:59.029624"
---

## 要約

OmniWeavingは、テキスト・複数画像・動画を入力として統合的に扱える動画生成モデルで、オープンソースの統合動画生成モデルとして初めてSoTA性能を達成した研究。既存のオープンソース動画生成モデルはタスクが断片化しており、単一フレームワーク内で多様なタスクを統合できる研究は少なかった。Seedance-2.0などのプロプライエタリシステムと比較してオープンソース勢の大幅な遅れを埋めることが目的とされている。

アーキテクチャ上の特徴として、テキスト・マルチ画像・動画がインターリーブされた（交互配置された）入力を時間軸方向にバインドする機能を持つ。これにより、複数の異なるモダリティ入力を一貫した動画として生成できる。また、複雑なユーザー意図を推論する「reasoning-informed」なエージェント的能力を備えており、単純な条件付き生成を超えたインテリジェントな動画制作が可能となる設計になっている。

学習面では、多様な構成シナリオおよび推論補強シナリオを含む大規模事前学習データセットを活用しており、自由形式の構成（free-form composition）と推論（reasoning）能力を同時に獲得させる戦略が取られている。

評価面では、IntelligentVBenchという新たなベンチマークを導入しており、これは次世代の統合動画生成を包括的に評価するために設計された初のベンチマークとされている。IntelligentVBenchを用いた実験において、OmniWeavingはオープンソース統合モデルの中でSoTA性能を示した。コードおよびモデルは近日中に公開予定で、プロジェクトページ（https://omniweaving.github.io）が公開されている。著者はZhao Zhong, Kaihang Pan, Qi Tianら14名。

## アイデア

- インターリーブされたテキスト・画像・動画入力を時間軸でバインドする設計は、マルチモーダルエージェントが動的なコンテキストを扱う際のアーキテクチャ参考になる
- ユーザー意図の推論をエージェント的に行う『reasoning-informed』アプローチは、曖昧な指示を解釈して適切なアクションを実行するエージェント設計と概念的に共通する
- IntelligentVBenchのような能力別包括ベンチマーク設計の思想は、監査エージェントの評価フレームワーク設計（タスク種別ごとの能力評価）に応用できる

## Yujiの取り組みへの示唆

動画生成モデル自体は監査業務と直接関係しないが、複雑なユーザー意図をエージェントが推論しながら実行するという設計思想はLangGraphベースの監査エージェント開発に示唆がある。特にIntelligentVBenchのように『統合能力を包括的に評価するベンチマーク設計』の考え方は、監査エージェントのLLM-as-judge評価フレームワーク構築時に参考になる。

## 原文リンク

[OmniWeaving: 自由形式の構成と推論を用いた統合動画生成モデル](https://tldr.takara.ai/p/2603.24458)
