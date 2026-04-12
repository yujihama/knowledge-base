---
title: "スタートアップAxiom Mathが数学者向けAIツール「Axplorer」を公開——PatternBoostをMac Proで動作可能に"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-07
tags: [PatternBoost, Axplorer, graph-theory, mathematical-discovery, AlphaEvolve, open-source, pattern-generation, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-07T21:06:39.444822"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathは、数学的パターン探索に特化したAIツール「Axplorer」を無料・オープンソースで公開した。同ツールはMeta在籍時にFrançois Chartonが開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上での動作を単一のMac Proで置き換えることに成功している。

PatternBoostはグラフ理論の難問「Turán four-cycles問題」を解くために使われた実績があり、Axplorerは同問題で同等の結果を2.5時間で再現した（PatternBoostでは数万台のマシンを3週間稼働）。Axiom Mathはさらにグラフ理論の他の2つの未解決問題でも既知の最良結果に並ぶか上回る成果を得たと主張する。

Axplorerの仕組みは反復的なパターン生成と選択に基づく。ユーザーが数学的な例を入力すると、ツールが類似のパターンを生成する。ユーザーが興味深いものを選んでフィードバックすると、次世代のパターンが生成される——これをGoogle DeepMindのAlphaEvolveと同様のアプローチと位置づけているが、AlphaEvolveは大規模GPUクラスタを必要とする非公開ツールであるのに対し、AxplorerはMac Proで動作するオープンソース実装という差別化を図っている。

CEOのCarina Hong（数学者）は、LLMが既存の解法を流用するのには長けているが、誰も持っていない洞察を必要とする問題には不向きだという点を強調する。Axplorerは新パターンの発見に特化しており、LLMベースのチャットボットアプローチとは設計思想が異なる。

米国DARPA（国防高等研究計画局）も「expMath（Exponentiating Mathematics）」イニシアチブを通じてAI活用の数学研究を推進しており、Axiom MathはそのエコシステムのプレイヤーとしてAIと数学者の協働モデルを提唱している。シドニー大学の数学者Geordie Williamsonは改善点に期待しつつも「多数のツールが溢れる時代において、追加のツールのインパクトは未知数」と慎重な見方を示している。

## アイデア

- 反復的パターン選択ループ（例を入力→類似パターン生成→ユーザーが選択→再入力）は、強化学習のヒューマンフィードバック（RLHF）と構造的に類似しており、数学的探索をRLAIFフレームワークで捉え直せる可能性がある
- スーパーコンピュータ3週間の計算をMac Proで2.5時間に圧縮した効率化は、アルゴリズム設計の改善によるものであり、単なるハードウェアスケールアップとは異なるアプローチとして注目に値する
- LLMは「既存データの微分（derivative）」に強いが、未探索の領域では限界があるというChartonの指摘は、LLM-as-judgeや自律エージェントの適用範囲を設計する上での重要な制約条件を示している

## Yujiの取り組みへの示唆

監査エージェント開発において「既存の監査手続きのパターンから新たな異常パターンや不正シグナルを帰納的に発見する」という問題設定はAxplorerの探索ループと構造的に対応する。PatternBoostの「例→類似生成→選択→再入力」のサイクルは、LangGraphでの状態遷移設計やRLAIFによる報酬モデル構築にそのまま応用できる枠組みであり、人間の監査専門家がパターンを評価・フィードバックするヒューマン・イン・ザ・ループ設計の参考事例になる。

## 原文リンク

[スタートアップAxiom Mathが数学者向けAIツール「Axplorer」を公開——PatternBoostをMac Proで動作可能に](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
