---
title: "H CompanyのHolo2-235B-A22BモデルがUIローカリゼーションでSOTAを達成"
url: "https://huggingface.co/blog/Hcompany/introducing-holo2-235b-a22b"
date: 2026-04-02
tags: [GUI-grounding, UI-localization, agentic-localization, ScreenSpot-Pro, MoE, computer-use, SkyPilot, multi-step-agent]
category: "agent-arch"
memo: "[HF Blog] H Company's new Holo2 model takes the lead in UI Localization"
processed_at: "2026-04-02T09:08:45.647926"
---

## 要約

H Companyは2026年2月3日、UIローカリゼーション特化モデル「Holo2-235B-A22B Preview」を公開した。本モデルはGUIグラウンディングベンチマーク「ScreenSpot-Pro」で78.5%、「OSWorld G」で79.0%を達成し、いずれも新たなState-of-the-Art（SOTA）を記録した。

モデルの主要技術は「Agentic Localization（エージェント的局在化）」である。4K高解像度インターフェースでは小さなUI要素を正確に特定することが難しく、従来の単一推論アプローチでは精度に限界があった。Agentic Localizationでは予測を反復的に精錬するアプローチを採用し、シングルステップで70.6%だったScreenSpot-Proの精度が、3ステップのエージェントモードで78.5%まで向上する。この反復的改善により、全Holo2モデルサイズで10〜20%の相対的精度向上を実現している。

モデルサイズは235Bパラメータ（アクティブ22B）のMoE（Mixture of Experts）構成であり、Hugging Faceで研究用途向けに公開されている。トレーニングインフラにはSkyPilotを採用しており、複数クラウドプロバイダーにまたがるKubernetes（k8s）ワークロードを統一インターフェースで管理することで、インフラ管理の複雑さを抽象化し、研究者がモデル開発に集中できる環境を構築している。

なお、同社は本記事公開の約2ヶ月後の2026年4月1日に後継モデル「Holo3」を発表しており、コンピュータ操作エージェント分野での継続的な開発が確認できる。

## アイデア

- 反復的予測精錬（Agentic Localization）により単一推論比で10〜20%精度向上。エージェントが自己評価・修正ループを持つ設計が精度に直結している
- 235B総パラメータ中アクティブ22BのMoE構成で大規模モデルの推論効率を維持しながら高精度を実現している点が設計上の注目点
- SkyPilotによるマルチクラウド・k8s抽象化が大規模トレーニングのボトルネックを解消しており、インフラ依存を減らした研究サイクル短縮の実例
## 関連記事

- /deep_645 Holo3：コンピュータ使用の最前線を突破する自律エージェントモデル
- /deep_32 モデルからエージェントへ：Responses APIへのコンピュータ環境の統合
- /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- /deep_641 トレーニング不要なエキスパート言語モデルの動的アップサイクリング
- /deep_827 smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ

## 原文リンク

[H CompanyのHolo2-235B-A22BモデルがUIローカリゼーションでSOTAを達成](https://huggingface.co/blog/Hcompany/introducing-holo2-235b-a22b)
