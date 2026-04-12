---
title: "数学者のやり方を変えようとするスタートアップ：Axiom MathのAxplorerとは"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-08
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-08T09:21:58.347027"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学者向けの無償AIツール「Axplorer」を公開した。Axplorerは、2024年にMetaのFrançois Chartonが共同開発した「PatternBoost」を再設計したもので、PatternBoostがスーパーコンピュータ上で動作していたのに対し、AxplorerはMac Pro単体で動く。PatternBoostはグラフ理論の難問「Turán四サイクル問題」を解くために使われたが、当時Chartonは数万台のマシンを3週間動かすという「恥ずかしいほどのブルートフォース」を要した。AxplorerはTurán問題の同等結果をわずか2.5時間で達成しており、効率が大幅に向上している。Axiom Mathはさらに、グラフ理論の別の2つの重要問題でも既知の最良結果に並ぶか上回る成果を出したと述べている。

Axplorerの仕組みはPatternBoostと同様のループ型パターン探索に基づく。ユーザーが例を与えると、ツールが類似パターンを生成し、ユーザーが興味深いものを選んでフィードバックすると、さらに類似したパターンが生成される。この反復プロセスにより、これまで誰も気づかなかったパターンの発見を支援する。Google DeepMindのAlphaEvolveも同様にLLMを用いて新しい解を生成し最良のものを保持するアーキテクチャを持つが、大規模なGPUクラスター上でのみ動作し、外部研究者はDeepMindのスタッフを通じて問題を入力させる必要がある閉じたシステムである。これに対しAxplorerはコードをオープンソースでGitHub公開しており、一般の学生・研究者が利用できる点が差別化要因となっている。

DARPAは「expMath（Exponentiating Mathematics）」という新イニシアチブを設立し、数学者にAIツールの開発・活用を促している。Axiom MathはこのDARPA主導の動きの一部と位置づけている。ChartonはLLMによる数学への取り組みについて「LLMは既存のものの派生には非常に優れているが、保守的で新しいアイデアを生み出せない」と批判的な見方を示す。Sydney大学のGeodie Williamsonは改良点に期待しつつも「効果の大きさは実際に見てみないとわからない」と慎重な見解を示しており、「数学者はホワイトボードを捨てるべきではない」と述べている。

## アイデア

- 人間のフィードバックループを組み込んだパターン生成（例を選択→再生成）という手法は、RLHFやRLAIFと構造的に類似しており、数学的発見以外のドメインにも転用可能な学習ループの設計として参考になる
- AlphaEvolveとの対比が鮮明：同様のアーキテクチャでも、クローズドなGPUクラスター依存 vs オープンソース・単一Mac Proという展開戦略の違いが、研究者コミュニティへの普及速度に直結する
- 「LLMは保守的：既存データの派生に強いが新規インサイトは出しにくい」という制約に対し、パターンブーストのような非LLMの組み合わせで補完するハイブリッドアプローチが有効という示唆

## Yujiの取り組みへの示唆

監査エージェント開発において、Axplorerの「例を与えてパターンを生成→人間が選択→再生成」というループ構造はRLAIFや人間フィードバックを活用したエージェント改善サイクルと本質的に同じ設計思想であり、LangGraphでの監査ワークフロー最適化に応用できる可能性がある。また「LLMは既存データの派生に強いが新規パターン発見には限界がある」という観察は、監査における異常検知や不正パターン発見においてLLM単体に頼らずハイブリッドアプローチを設計する際の根拠として活用できる。

## 原文リンク

[数学者のやり方を変えようとするスタートアップ：Axiom MathのAxplorerとは](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
