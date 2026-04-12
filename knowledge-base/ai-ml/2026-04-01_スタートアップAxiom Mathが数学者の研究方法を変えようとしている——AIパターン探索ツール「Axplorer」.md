---
title: "スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-01
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, 進化的探索, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-01T09:12:54.818049"
---

## 要約

Axiom Math（カリフォルニア州パロアルト）は、数学者向けの無料AIツール「Axplorer」を公開した。これはMetaでFrançois Chartonが2024年に共同開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上で動作していたPatternBoostをMac Pro単体で動作するよう効率化している。

PatternBoostは既にグラフ理論の難問「Turán四サイクル問題」を解くために使われた実績がある。この問題は、多数の点が描かれた面において、4点のループを作らずにできるだけ多くの線を引くという組み合わせ最適化問題で、ソーシャルメディア・サプライチェーン・検索エンジンランキングなどの複雑ネットワーク解析に関連する。PatternBoostによる解法ではMetaの数万台のマシンを用いて3週間を要したが、Axplorerは同一問題を2.5時間で再現している。

Axplorerの基本的な動作原理は反復的パターン生成である。ユーザーが例を与えると、ツールは類似するパターンを多数生成し、ユーザーが興味深いものを選択してフィードバックすることで、探索を収束させていく。これはGoogle DeepMindのAlphaEvolveと類似したアプローチ（進化的サンプリング＋LLMによる改善提案）だが、AlphaEvolveが大規模GPUクラスタ必須かつクローズドであるのに対し、AxplorerはオープンソースでGitHub公開されており、単一マシンで動作する点が異なる。

ChartonはLLMによる数学への応用（GPT-5を用いたErdős問題の解決など）に対し批判的で、「LLMは既存データの派生物は得意だが保守的であり、新しいアイデアや未発見のパターンには不向き」と主張する。Axplorerの設計思想はLLMではなく、探索的パターン生成に特化した点にある。

DARPAは2025年に「expMath（Exponentiating Mathematics）」イニシアティブを立ち上げ、AIツールの数学研究への統合を促進しており、Axiom MathはこのエコシステムへのOSSコントリビューターとして位置づけている。シドニー大学のGeodie Williamsonは改良点の理論的可能性を認めつつも、「実際にどの程度有効かは使ってみないと分からない」と慎重な見方を示している。

## アイデア

- 反復的パターン選択（ユーザーが興味深いパターンを選んでフィードバック→次世代生成）という人間-AI協調ループが、LLMの「保守性」を補完する探索手法として機能している点
- スーパーコンピュータ依存だったPatternBoostを単一Mac Proで動作させ、かつ同問題を3週間→2.5時間に短縮した効率化の実現——アーキテクチャレベルでの計算効率改善が小規模インフラでの研究民主化を可能にしている
- AlphaEvolve（クローズド・大規模GPU必須）に対しオープンソース・シングルマシン動作で対抗するという戦略——ツールの「アクセシビリティ」がAI研究エコシステムにおける差別化軸になりうる

## Yujiの取り組みへの示唆

監査エージェント開発における仮説探索フェーズで、Axplorerのような反復的パターン生成アプローチを参考にできる。例えば、不正パターンや異常取引の「未知のパターン」を探索する際に、LLMの保守性（既存データへの依存）を補う探索ループ設計のアイデアとして有用。また、AlphaEvolve型の進化的サンプリングをLangGraphのサイクル構造に組み込み、LLM-as-judgeで有望な仮説を選別する設計パターンへの示唆が得られる。

## 原文リンク

[スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
