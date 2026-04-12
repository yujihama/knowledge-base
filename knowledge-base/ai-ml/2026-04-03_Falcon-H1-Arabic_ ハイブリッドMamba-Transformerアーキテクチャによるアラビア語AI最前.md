---
title: "Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線"
url: "https://huggingface.co/blog/tiiuae/falcon-h1-arabic"
date: 2026-04-03
tags: [Mamba, SSM, ハイブリッドアーキテクチャ, Arabic-NLP, 長コンテキスト, DPO, SFT, Falcon-H1, vLLM, 多言語LLM]
category: "ai-ml"
memo: "[HF Blog] Introducing Falcon-H1-Arabic: Pushing the Boundaries of Arabic Language AI with Hybrid Architecture"
processed_at: "2026-04-03T09:09:40.459851"
---

## 要約

UAE のTII（Technology Innovation Institute）が、アラビア語特化の大規模言語モデルファミリー「Falcon-H1-Arabic」を発表した。3B・7B・34Bの3サイズで構成され、Open Arabic LLM Leaderboard（OALL）において同規模モデルをすべてのスケールで上回るSOTA性能を達成している。

最大の技術的特徴は、State Space Model（Mamba）とTransformerアテンションを各ブロック内で並列実行するハイブリッドアーキテクチャ「Falcon-H1」の採用にある。両コンポーネントの出力を連結した後に出力プロジェクションを行う設計により、Mambaの線形時間スケーラビリティと、アテンションの精密な長距離依存モデリングを両立させている。アラビア語の豊かな形態論・語順の柔軟性に対してこの構造が有効に機能するとされる。

コンテキスト長は前モデル「Falcon-Arabic」の32Kトークンから大幅拡張され、3Bモデルで128K、7B・34Bモデルでは256K（約20万語）を実現した。法律文書・医療記録・学術論文など数百ページ規模の文書処理が可能となり、「lost in the middle」問題への対策もポストトレーニングで明示的に施されている。

事前学習データは約3000億トークンで構成され、アラビア語・英語・多言語コンテンツをほぼ均等に混合。データパイプラインはアラビア語の正書法・形態論・ダイアクリティクス・統語パターンに特化した多段階品質フィルタリングを実施し、エジプト方言・レバント方言・湾岸方言・マグレブ方言など方言多様性も拡充している。

ポストトレーニングはSFT（Supervised Fine-Tuning）とDPO（Direct Preference Optimization）の2段階で構成。SFTでは高品質アラビア語指示データ・長コンテキスト例・構造化推論タスクを使用し、DPOでは長コンテキスト推論と汎用言語能力のバランスを最適化している。壊滅的忘却を防ぐためのカリキュラム管理も明示的に実施されている。

ベンチマークではOALLに加え、STEM関連の3LMベンチマーク、コーディング・数学タスクでも評価されており、各スケールで競合モデルを上回る結果を示している。推論バックエンドにvLLMを使用することで、Accelerate比で大幅な高速化も達成している。

## アイデア

- MambaとTransformerを並列実行して出力を連結するハイブリッドブロック設計は、長文書処理エージェントのバックボーンとして線形スケーラビリティと精度を同時に確保できる可能性がある
- 「lost in the middle」問題をアーキテクチャではなくポストトレーニングで明示的に対処している点は、長文書監査レポート処理エージェントの設計において参考になる実用的アプローチである
- SFT→DPOの2段階アライメントで長コンテキスト推論能力と汎用能力のトレードオフを制御する手法は、特定ドメイン（監査・法務）への特化モデル開発における忘却問題への対処として応用可能

## Yujiの取り組みへの示唆

256Kトークンの長コンテキスト処理能力と「lost in the middle」対策の具体的手法は、数百ページに及ぶ監査調書・内部統制文書を扱うRAGエージェント設計に直接応用できる。また、SFT＋DPOによる長コンテキスト推論と汎用能力のバランス制御の手法は、LangGraphベースの監査エージェントをドメイン特化チューニングする際の壊滅的忘却回避策として参考になる。Mambaハイブリッドアーキテクチャの線形スケーラビリティは、高QPS・低レイテンシが求められる監査エージェントのバックボーン選定において検討価値がある。

## 原文リンク

[Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線](https://huggingface.co/blog/tiiuae/falcon-h1-arabic)
