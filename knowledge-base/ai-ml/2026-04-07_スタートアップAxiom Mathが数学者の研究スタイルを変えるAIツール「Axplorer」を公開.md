---
title: "スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-07
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン発見, AlphaEvolve, DARPA-expMath, オープンソース]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-07T12:24:36.892210"
---

## 要約

Palo Alto拠点のスタートアップAxiom Mathが、数学者向けのAIパターン発見ツール「Axplorer」を無償公開した。同ツールは、MetaのFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上でしか動作しなかった前身ツールをMac Pro単体で実行可能にした点が最大の特徴。

PatternBoostはグラフ理論の未解決問題「Turán四サイクル問題」を解くために使用された実績を持つ。この問題は、多数の点を結ぶ線を描く際に4点を一巡するループを作らずに最大限の辺を引く方法を求めるものであり、SNS・サプライチェーン・検索エンジンランキングの分析に応用されるグラフ理論の重要な問題。PatternBoostによる解法では数万台のマシンを3週間稼働させたのに対し、Axplorerは同じ結果を2.5時間で再現した。さらにAxiom Mathは他の2つのグラフ理論の主要問題でも最良既知結果に並ぶか上回る結果を得たと主張している。

Axplorerのアルゴリズムの基本は反復的なパターン探索だ。ユーザーが例示を与えると、ツールが類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックする、というサイクルを繰り返す。これはGoogle DeepMindのAlphaEvolveと類似した発想（LLMが候補を生成し最良のものを選んで改善を繰り返す）だが、AlphaEvolveは大規模GPUクラスタを要し一般公開されていない点が異なる。

CEOのCarina Hong（数学者出身）は、LLMベースのアプローチとの差別化を強調する。GPT-5などのLLMは既存データの派生解を生成するのには優れているが、「誰も思いついたことのない新しい洞察」を要する難問には不向きだとChartonは述べる。Axplorerはパターン発見を通じた新しい数学的着想の創出を目的としており、神経ネットワークの自前学習も不要な設計になっている。

コードはオープンソースとしてGitHubで公開済み。米国防高等研究計画局（DARPA）の「expMath（Exponentiating Mathematics）」イニシアティブとも方向性を一致させている。一方、シドニー大学のGgeordie Williamson（PatternBoostの共同研究者）は改良効果への期待を示しつつ、「多くのAIツールが数学者に売り込まれている中で、さらに一つ増えることの意義はまだ不明」と慎重な見方も示している。

## アイデア

- 反復的パターン探索（例示→生成→選択→フィードバック）というヒューマン・イン・ザ・ループ型の探索ループは、LLMのような文脈再利用型とは異なる「新規性創出」のアーキテクチャとして注目に値する
- スーパーコンピュータ3週間分の計算をMac Pro単体で2.5時間に圧縮できた効率化は、アルゴリズム設計の改善によるものであり、ハードウェアスケールに依存しないAI手法の実用化指針として参考になる
- AlphaEvolveとPatternBoost/Axplorerの比較から、「クローズドで高性能」vs「オープンで民主化」という二極化がAI研究ツール市場でも顕在化しており、アクセシビリティが実用普及の鍵になることが示唆される

## Yujiの取り組みへの示唆

直接的な監査・GRC領域との関連は薄いが、Axplorerの「人間が選択し、AIがパターンを拡張する」反復ループ設計は、監査エージェントにおけるReActパターン（観察→推論→行動）との構造的類似性がある。監査手続きの中でリスクパターンや異常取引パターンを発見する際に、同様のヒューマン・イン・ザ・ループ型パターン増幅アーキテクチャをLangGraphで実装するヒントになり得る。また、GRPO/RLAIFによる報酬設計において「選択された良いパターンを正例として強化学習する」という観点からも参考になる。

## 原文リンク

[スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
