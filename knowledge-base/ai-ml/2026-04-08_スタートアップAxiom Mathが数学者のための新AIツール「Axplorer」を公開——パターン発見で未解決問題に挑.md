---
title: "スタートアップAxiom Mathが数学者のための新AIツール「Axplorer」を公開——パターン発見で未解決問題に挑む"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-08
tags: [PatternBoost, Axplorer, グラフ理論, パターン発見, AlphaEvolve, 数学AI, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-08T12:34:29.271862"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学者向けの無料AIツール「Axplorer」をリリースした。これはMeta在籍時にFrançois Chartonらが開発した「PatternBoost」をベースに再設計したもので、スーパーコンピュータ上で動作していたPatternBoostとは異なり、Mac Pro単体で実行可能な点が大きな特徴である。

Axplorerの基本的な仕組みはパターン発見の反復ループだ。ユーザーが数学的な例を与えると、ツールが類似する例を複数生成する。ユーザーは興味深いものを選択してフィードバックし、ツールはさらにそれに似た例を生成する——このサイクルを繰り返すことで、従来の手法では見つけられなかったパターンの発見を支援する。この設計思想はGoogle DeepMindのAlphaEvolveに近いが、AlphaEvolveが大規模なGPUクラスタを必要とし一般研究者には開放されていないのに対し、Axplorerはオープンソース（GitHub公開）で個人のマシンで動作する点で差別化している。

PatternBoostがグラフ理論の難問「Turán four-cycles問題」を解くのに数万台のマシンで3週間かかったのに対し、Axplorerは同結果を1台のマシンで2.5時間で再現したとChartonは述べている。さらにAxiom Mathは他の2つのグラフ理論の重要問題でも最良既知結果に並ぶか上回る成果を出したと主張している。

ChartonはGPT-5などLLMを用いて解かれた最近の未解決問題の成果に否定的だ。「LLMは既存の知識の派生が得意だが保守的で、誰も持ったことのない新たな洞察は生み出せない」とし、自身は長年著名な数学者が研究してきた「難しい問題」を標的にしていると語る。

CEOのCarina Hong（数学者出身）は、既存のAIツールが数学者に独自のニューラルネットワーク学習を求めることが普及の障壁になっていると指摘し、Axplorerはステップバイステップのガイド付きUIで誰でも使えるよう設計されていると強調する。米国防高等研究計画局（DARPA）の「expMath」イニシアチブの一環ともみなされており、次世代AI開発やインターネットセキュリティ向上に寄与する新数学の発見を目指している。

シドニー大学のGgeordie Williamsonは理論的改善は認めつつも「実際の効果はまだわからない」と慎重な見方を示し、「数学者は今やツールの洪水に圧倒されている」とも述べた。

## アイデア

- 「人間が選択→AIが生成→人間が絞り込む」反復ループによるパターン探索は、仮説生成エージェントの設計に転用可能——監査における異常パターン発見プロセスに応用できる
- LLMは既存知識の補間は得意だが「誰も思ったことのない洞察」には限界があるという指摘は、LLM単体依存のエージェント設計の弱点を端的に示しており、symbolic/evolutionary手法との組み合わせの重要性を示唆する
- スーパーコンピュータ規模の計算（数万台×3週間）を単一Mac Proで2.5時間に圧縮したアーキテクチャ効率化は、ローカルLLMインフラ設計における計算効率とスケールのトレードオフ議論に参考になる
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者のための新AIツール「Axplorer」を公開——パターン発見で未解決問題に挑む](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
