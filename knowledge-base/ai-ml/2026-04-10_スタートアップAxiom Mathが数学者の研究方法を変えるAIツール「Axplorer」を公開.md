---
title: "スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-10
tags: [PatternBoost, Axplorer, グラフ理論, 数学AI, AlphaEvolve, DARPA-expMath, パターン探索, オープンソース]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
related: [203, 1121, 1305, 1190, 948]
processed_at: "2026-04-10T09:24:16.900651"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathが、数学者向けの無料AIツール「Axplorer」を公開した。このツールはMeta在籍時にFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピュータが必要だったPatternBoostと異なり、Mac Pro1台で動作する。

PatternBoostはグラフ理論の難問「Turán四サイクル問題」を解くために使われたツールで、Meta在籍時のChartonは数千〜数万台のマシンを3週間稼働させることで解を導いた。Axplorerはこれと同等の結果を2.5時間で出せるとされ、効率性と速度において大幅な改善が実現されている。さらにAxiom Mathは、Axplorerを用いてグラフ理論の他の2つの重要問題においても既知の最良結果に匹敵または上回る成果を得たと発表している。

Axplorerの仕組みはPatternBoostの反復的パターン探索に基づく。ユーザーが例を与えると、ツールが類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックする。これをループすることで、従来誰も気づかなかったパターンを発見していく手法だ。Google DeepMindのAlphaEvolveも同様にLLMで新解を探索するが、AlphaEvolveはクローズドで大規模GPUクラスタが必要であり、DeepMindのスタッフに依頼しなければ使えない。Axplorerはオープンソース（GitHub公開）でMac Pro1台で使える点が差別化ポイントである。

Axiom MathのCEO Carina Hongは、LLMベースのアプローチ（GPT-5等で未解決問題を解く最近の潮流）に対し、Chartonは批判的な見方を示している。LLMは既存データの「保守的な」再利用には優れるが、誰も持ったことのない新たな洞察が必要な問題には限界があると指摘する。Axplorerはそうした新発見のための探索的・実験的ツールと位置付けられている。

米国DARPAも「expMath（Exponentiating Mathematics）」という新イニシアチブを立ち上げ、数学者がAIツールを開発・活用するよう奨励しており、Axiom MathはこのエコシステムにおけるキープレイヤーとしてPoジションを取ろうとしている。

シドニー大学の数学者Geordie Williamsonは、PatternBoostの共同研究者でありAxplorerの改善点に注目しているが、「別のツールが加わることの影響は不透明」とも述べており、数学コミュニティが多数のAIツールに圧倒されているという現状も浮き彫りになっている。

## アイデア

- 反復的パターン探索（ユーザーが選択→フィードバック→再生成）という人間-AIループ設計が、LLMの保守的な解生成の限界を補う構造として興味深い
- スーパーコンピュータ3週間分の計算をMac Pro1台・2.5時間に圧縮できたという効率化は、アルゴリズム設計とモデル最適化の組み合わせによるものであり、ローカルLLM推論の可能性を示す事例
- 「既存問題の解法」ではなく「新たなパターンの発見」にフォーカスするという設計思想は、AI活用の目的論（exploitationではなくexploration）として応用範囲が広い
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
