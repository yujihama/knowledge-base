---
title: "スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」をリリース"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-09
tags: [PatternBoost, Axplorer, 数学AI, グラフ理論, パターン発見, AlphaEvolve, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-09T21:29:42.537676"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学的パターンを発見することで長年の未解決問題の突破口を開くAIツール「Axplorer」を無償公開した。Axplorerは、Meta在籍時にFrançois Chartonが2024年に共同開発した「PatternBoost」を再設計したものであり、スーパーコンピュータが必要だったPatternBoostとは異なり、Mac Pro単体で動作する。PatternBoostはグラフ理論の難問「Turán四サイクル問題」を解くのに使用されたが、その際はMetaの数千〜数万台のマシンを3週間稼働させるという大規模な計算が必要だった。Axplorerはこれと同等の結果を2.5時間で達成したとされ、効率性の大幅な改善を実現している。AxplorerはPatternBoostと同様に、ユーザーが例を与えると類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックするというループを繰り返す設計になっている。これはGoogle DeepMindのAlphaEvolveと類似したコンセプトであるが、AlphaEvolveは大規模GPUクラスタを必要とし、一般研究者はDeepMindのスタッフを通じてしかアクセスできないのに対し、AxplorerはオープンソースとしてGitHubで公開されており、誰でも自身のマシンで利用できる。Axiom MathはAxplorerを用いてグラフ理論の2つの重要問題においても最良の既知結果に匹敵または上回る成果を得たと報告している。Chartonは、LLMは既存のデータを組み合わせることには長けているが本質的に保守的であり、誰も考えたことのない新しい洞察（パターン発見）には不向きであると指摘し、Axplorerが解決を目指すのはまさにその領域だと述べた。米国国防高等研究計画局（DARPA）は「expMath（Exponentiating Mathematics）」というイニシアティブを立ち上げ、数学者によるAIツールの開発・活用を促進しており、Axiom MathはこのムーブメントとAIによる数学的探索の民主化を目指している。コードはオープンソースで、学生や研究者がサンプル解や反例の生成に活用し、数学的発見を加速させることを想定している。

## アイデア

- ユーザーが例を提示→モデルが類似パターンを生成→ユーザーが選択→再入力というインタラクティブなループ設計は、人間の直感とAIの探索能力を組み合わせたヒューマン・イン・ザ・ループ最適化の応用例として注目に値する
- スーパーコンピュータ3週間相当の計算をMac Pro 2.5時間に圧縮した効率化は、アルゴリズムの改良だけでなく問題表現の工夫（グラフ構造のエンコーディング等）が鍵である可能性が高く、小規模計算資源でのAI研究の可能性を示す
- LLMの「保守性」（既存データの組み合わせに留まる）を明示的に批判し、パターン探索型AIで補完するというアーキテクチャ的分業の考え方は、AI研究ツール設計における重要な視点を提供する

## Yujiの取り組みへの示唆

監査エージェント開発において、未知のリスクパターンや不正スキームの発見はLLMだけでは難しい課題であり、AxplorerのようなパターンブースティングアプローチをRAGや異常検知モジュールに組み込む設計の参考になる。特に「既存事例の組み合わせに留まるLLMの限界を人間の選択ループで補う」設計思想は、LangGraphによるReActエージェントのツール設計やRLAIF/GRPOでの報酬設計に応用できる可能性がある。

## 原文リンク

[スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」をリリース](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
