---
title: "スタートアップAxisom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-09
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, DARPA-expMath, オープンソース, LLM限界]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-09T09:29:58.914510"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学の未解決問題に取り組む研究者向けAIツール「Axplorer」を無償公開した。Axplorerは、Meta在籍時にFrançois Charton氏が共同開発した「PatternBoost」を再設計したもので、PatternBoostがスーパーコンピュータ上で動作していたのに対し、AxplorerはMac Pro単体で動作する。

PatternBoostはグラフ理論の難問「Turán四サイクル問題」の解法発見に使われた。同問題はグラフ上のノード間に可能な限り多くのエッジを引きつつ、4ノードからなるループを生成しないための構造を求めるもので、ソーシャルメディアや供給チェーン、検索エンジンランキング等の複雑ネットワーク解析に応用される。PatternBoostは数万台のマシンを3週間稼働させてこの結果を得たが、Axplorerは同等の結果を2.5時間で達成した。さらにAxiom Mathは、グラフ理論の他の2つの重要問題においても最良既知結果に匹敵または上回る成果を得たと述べている。

Axplorerの仕組みはPatternBoostと同様の反復的パターン探索アプローチを採用する。ユーザーが数学的オブジェクトの例を与えると、ツールが類似するオブジェクトを生成し、ユーザーが興味深いものを選択してフィードバックする。このサイクルを繰り返すことで新たな数学的パターンを発見する。LLMが既存データに基づく「保守的」な解を生成するのに対し、PatternBoost/Axplorerは誰も気づいていなかったパターンを探索する点で異なるアプローチをとる。コードはオープンソースとしてGitHub上で公開されており、サンプル解や反例の生成を通じて学生・研究者の数学的発見を加速することを目指す。

Charton氏はGPT-5等のLLMを用いたErdős問題の解法発見について、「見落とされていた問題の中から解けるものを見つけるだけ」と批判的に評価し、Axplorerは著名な数学者が長年取り組んできた「真に難しい問題」を対象とすると強調する。GoogleDeepMindのAlphaEvolveも同様に進化的アプローチで新解法を発見しているが、大規模GPUクラスタが必要で一般研究者がアクセスできない。Axplorerはその民主化版として位置づけられる。米国DARPAも「expMath（Exponentiating Mathematics）」イニシアティブで数学AIツールの開発・普及を推進しており、Axiom MathはこのエコシステムとしてのAIツール提供者として自社を位置づける。シドニー大学のGeodie Williamson氏はAxplorerの改善点を評価しつつも「実際の効果は未知数」と慎重な姿勢を示している。

## アイデア

- LLMの「保守性」（既存データの再利用傾向）を補完する反復的パターン探索アプローチ：ユーザーが面白い例を選択しフィードバックするヒューマン・イン・ザ・ループ設計が、探索空間の効率的な絞り込みを実現している
- スーパーコンピュータ依存（数万台×3週間）からMac Pro単体×2.5時間への効率化：アルゴリズムの改良により計算資源要件を数桁削減し、ツールの民主化を実現した点が注目に値する
- 「解を見つける」AIと「パターンを発見する」AIの役割分担：LLMが既知手法の組み合わせに強い一方、PatternBoost系ツールは前人未踏のパターン発見に特化するという機能的棲み分けの概念

## Yujiの取り組みへの示唆

直接的な監査AIへの応用は薄いが、反復的パターン探索（人間が選択→AIが生成→人間が評価）のループ構造は、LangGraphを用いた監査エージェントにおけるReActサイクルやLLM-as-judgeの設計思想と共鳴する。特に「LLMは保守的で既存データの派生物を生成する」という指摘は、監査エージェントが新規リスクパターンを発見する際にLLM単体に依存することの限界を示唆しており、ルールベースの探索と組み合わせたハイブリッドアーキテクチャの必要性を再確認させる。

## 原文リンク

[スタートアップAxisom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
