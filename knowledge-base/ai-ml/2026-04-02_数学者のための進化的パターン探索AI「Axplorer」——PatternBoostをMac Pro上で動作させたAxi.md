---
title: "数学者のための進化的パターン探索AI「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの新ツール"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-02
tags: [PatternBoost, Axplorer, グラフ理論, 進化的探索, AlphaEvolve, 数学AI, オープンソース, Turán問題]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
related: [203, 1121, 1305, 1190, 948]
processed_at: "2026-04-02T12:09:04.746273"
---

## 要約

Axiom Math（カリフォルニア州パロアルト）が、数学研究向けのAIツール「Axplorer」を無償公開した。Axplorerは、MetaのFrançois Chartonが2024年に共同開発した「PatternBoost」を刷新したもので、スーパーコンピュータ上でしか動作しなかった前身に対し、Mac Pro（単一マシン）上で動作する点が最大の特徴。

PatternBoostはグラフ理論の未解決問題「Turán四サイクル問題」の突破に使われた実績を持つ。Turán問題とは、平面上の点集合に対し、4点が一巡するループを作らずに最大限の辺を引く方法を求める問題で、社会ネットワーク・サプライチェーン・検索エンジンランキングのグラフ解析に応用される重要な問題。PatternBoostはMetaの数万台のマシンで3週間かけてこれを解いたが、AxplorerはMetaのパフォーマンスに匹敵する結果を2.5時間で再現したという。さらにAxplorer導入により、他の2つのグラフ理論上の重要問題についても既知の最良結果と同等か改善する結果を出したとAxiom Mathは主張する。

Axplorerの動作原理はPatternBoostと同様の進化的アプローチ：ユーザーが問題の例を与えると、ツールがそれに似た候補を生成し、ユーザーが有望なものを選択してフィードバックするサイクルを繰り返す。これはGoogle DeepMindのAlphaEvolve（LLMを使い最良の候補を保持・改良するシステム）と類似した思想だが、AlphaEvolveが大規模GPUクラスタ上のクローズドシステムであるのに対し、Axplorerはオープンソースで一般公開されている。

ChartonはLLMによる数学問題解決に懐疑的で、「LLMは既存のデータの派生的な答えは得意だが、誰も持ったことのない洞察は生み出せない」と指摘する。Axplorerの狙いは、LLMでは届かない「新たなパターンの発見」にあり、ゼロから新しい数学的概念を開拓する探索的・実験的な用途を想定。CEOのCarina Hong（数学者出身）は、数学者が独自のニューラルネットを訓練する必要がない設計を意識しており、ステップバイステップのガイドで学生・研究者が反例や解候補を素早く生成できるようにしている。

シドニー大学のGgeordie Williamsonは、PatternBoostからの技術的改善点は理論上は広い問題に適用可能とする一方、「実際の有意性はまだ見えない」と慎重な評価。米DARPA発の「expMath」イニシアティブ（AI数学ツール開発奨励）との連携もAxiomは意識している。コードはGitHubで公開済み。

## アイデア

- ユーザーが候補を選択してフィードバックするヒューマン・イン・ザ・ループの進化的探索ループ——監査ルール候補の生成・絞り込みプロセスに応用できる設計思想
- LLMは既存の解の派生には強いが「誰も気づいていないパターンの発見」には限界があるという指摘——RAGベースの監査エージェントで同様の限界を認識し、探索型アプローチで補完する余地がある
- スーパーコンピュータ依存のツールを単一ローカルマシンで再現可能にした効率化（3週間→2.5時間）——大規模インフラなしにRTX 3090等でローカルLLM推論を行う方向性と同じく、民主化の観点で重要なエンジニアリング指標
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[数学者のための進化的パターン探索AI「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの新ツール](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
