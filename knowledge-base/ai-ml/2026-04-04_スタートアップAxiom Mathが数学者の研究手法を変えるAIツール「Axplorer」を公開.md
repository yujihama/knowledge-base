---
title: "スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-04
tags: [PatternBoost, Axplorer, グラフ理論, パターン探索, AlphaEvolve, 数学AI, オープンソース, 進化的アルゴリズム]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-04T12:08:07.073594"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathが、数学者向けAIツール「Axplorer」を無償公開した。Axplorerは、MetaのFrançois Charton（現Axiom Mathリサーチサイエンティスト）が2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上で動作していたPatternBoostと異なり、Mac Pro1台で実行できる。

PatternBoostはグラフ理論の難問「Turán four-cycles問題」を解くために使われた実績がある。この問題は、複数の点に対して4点が一周でつながるループ（四辺形）を作らずに可能な限り多くの線を引く方法を求めるもので、SNSネットワークやサプライチェーンの解析に用いられるグラフ理論の重要課題。PatternBoostではMetaの数千〜数万台のマシンを使い3週間かかったが、AxplorerはMac Pro1台でわずか2.5時間で同等の結果を再現した。さらにAxiom Mathは他の2つのグラフ理論の難問でも既知の最良結果を一致または改善したと述べている。

Axplorerの仕組みはPatternBoostと同様の反復的パターン探索に基づく。ユーザーが例を与えると、ツールが類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックすることでさらに洗練されたパターンを生成する、進化的な探索ループを採用している。これはGoogle DeepMindのAlphaEvolveが「LLMに解を提案させ、良い提案を残して改良を繰り返す」アプローチと概念的に近い。

AxplorerのコードはオープンソースとしてGitHubで公開されており、ニューラルネットワークの独自学習を不要とし、ステップバイステップで使用できる設計により、数学者や学生が容易に利用できることを目指す。CEOのCarina Hong（数学者出身）は、既存問題の解法発見だけでなく、誰も気づいていなかったパターンの発見を通じて数学探索を加速させることを狙いとして強調する。

DARPAも「expMath（Exponentiating Mathematics）」イニシアチブを通じてAI数学ツールの普及を後押ししており、Axiom Mathはこのエコシステムにおけるオープンなツールプロバイダーとして位置づける。シドニー大学のGgeordie Williamsonは「PatternBoostは優れたアイデアだが万能ではない」とコメントし、ホワイトボードなど伝統的な手法の重要性も指摘している。

## アイデア

- 進化的パターン探索（ユーザーが選択→フィードバック→生成を繰り返す）は、LLMのように学習済みパターンに依存せず、既存解のない問題領域でも機能する点で、探索型エージェントの設計参考になる
- スーパーコンピュータ依存（PatternBoost：3週間・数万台）からMac Pro1台・2.5時間への大幅な効率化は、アルゴリズム改善によるオープンソース化の典型例であり、企業クローズドツール（AlphaEvolve等）に対するアクセシビリティの観点で重要
- 「LLMは既存データの派生に強いが、全く新しいアイデアが必要な問題には弱い」というChartonの指摘は、LLM単独エージェントの限界と、探索的な外部ツール（シミュレータ・検証器）との組み合わせの必要性を示唆する

## Yujiの取り組みへの示唆

直接的な監査領域との関連は薄いが、「LLMは保守的で既存解の派生に強いが新規パターン発見には弱い」という知見は、監査エージェント設計においてLLMだけに頼らず探索的サブエージェントを組み合わせるアーキテクチャの根拠として参照できる。また、Axplorerの反復フィードバック型パターン探索は、LangGraphでの人間参加型（HITL）ループ設計や、RLAIFにおける報酬シグナル設計の発想と構造的に類似しており、エージェントのループ設計を考える際の参考になる。

## 原文リンク

[スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
