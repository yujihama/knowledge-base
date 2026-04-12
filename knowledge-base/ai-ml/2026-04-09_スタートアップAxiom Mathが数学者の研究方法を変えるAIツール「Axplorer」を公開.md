---
title: "スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-09
tags: [PatternBoost, Axplorer, グラフ理論, 数学的発見, パターン探索, AlphaEvolve, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
related: [203, 1121, 1305, 1190, 948]
processed_at: "2026-04-09T21:12:33.998678"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathが、数学者向けのAIツール「Axplorer」を無償公開した。同ツールは、MetaでFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピュータを必要とした前身と異なり、Mac Pro単体で動作する。

PatternBoostはグラフ理論の未解決問題「Turán四サイクル問題」を解くのに使われたが、Metaの数千台のマシンで3週間実行する必要があった。Axplorerは同じ問題を2.5時間で解き、単一マシン上で動作する点が大きな改善点である。アーキテクチャの核心は「パターンブースティング」という手法で、ユーザーが例を与えると類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックすることで反復的に探索を深める。これはGoogle DeepMindのAlphaEvolveと類似したアプローチ（最良の提案を保持しLLMに改善を依頼する）だが、閉鎖的なAlphaEvolveと異なりオープンソース（GitHub公開）で、誰でも利用可能である。

Axiom Math CEOのCarina Hongは数学者自身であり、ツールの設計思想として「数学者に独自のニューラルネットワーク訓練を求めない」ことを重視している。Axplorerはステップバイステップのガイド付きで、学生や研究者が反例や解の候補を生成できる。同社はTurán問題に加え、グラフ理論の他の2つの重要問題で既存の最良結果に匹敵または改善する成果を出したと主張している。

LLMベースのアプローチ（GPT-5等を使ったErdős問題の解法）に対してChartonは懐疑的で、「LLMは既存データの派生物には強いが保守的であり、新たな洞察を必要とする問題には限界がある」と指摘する。Axplorerはこの限界を補う「新パターンの発見」に特化している。米国DARPAも「expMath（Exponentiating Mathematics）」イニシアチブを通じ数学へのAI活用を推進しており、Axiom Mathはこの潮流の一端を担う。シドニー大学のGgeordie Williamsonは改善点を評価しつつも「多くの企業がツールを提供しており数学者は飽和状態」と慎重な見方を示している。

## アイデア

- 「パターンブースティング」という人間参加型の反復探索ループ：ユーザーが面白いパターンを選択→モデルが類似パターンを生成→を繰り返すことで、純粋なLLMでは到達できない新規パターンを発見できる設計思想
- スーパーコンピュータ依存（数千台・3週間）からMac Pro単体・2.5時間への効率化：計算効率の改善がツールの民主化に直結する好例で、アルゴリズムの質がスケールを代替できることを示す
- LLMの「保守性」問題：LLMは学習データの分布内では強力だが、前人未踏の洞察を要する問題では限界がある。この補完としてパターン進化型探索（AlphaEvolve、PatternBoost系）が有効という示唆
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
