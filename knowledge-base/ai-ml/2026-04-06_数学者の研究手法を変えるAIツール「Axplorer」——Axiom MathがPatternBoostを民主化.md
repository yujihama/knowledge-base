---
title: "数学者の研究手法を変えるAIツール「Axplorer」——Axiom MathがPatternBoostを民主化"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-06
tags: [PatternBoost, Axplorer, AlphaEvolve, グラフ理論, パターン発見, 数学AI, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-06T21:08:10.409772"
---

## 要約

Axiom Math（パロアルト拠点のスタートアップ）が、数学者向けAIツール「Axplorer」を無償公開した。Axplorerは、Meta在籍時にFrançois Chartonが共同開発した「PatternBoost」を大幅に改良したもので、スーパーコンピュータ不要でMac Pro1台上で動作する。

PatternBoostはTurán四サイクル問題（グラフ理論における未解決問題の一つ。点の集合に対し、4点を結ぶ閉路を形成せずに最大何本の辺を引けるか）の解法発見に使われたが、当時はMetaの数万台規模の計算クラスタで3週間かけて実行する必要があった。Axplorerは同じTurán問題の結果を2.5時間で再現したと報告されており、効率・速度ともに大幅に向上している。AxplorerのコードはGitHubでオープンソース公開されている。

Axplorerの動作原理はPatternBoostと同様で、ユーザーが例示を与えると、ツールが類似パターンを自動生成する。ユーザーが興味深いものを選択してフィードバックすると、さらに類似パターンを生成する反復プロセスを繰り返す。これはGoogle DeepMindのAlphaEvolveが採用する「LLMで候補を生成→優良解を選択→改善を繰り返す」進化的アプローチと概念的に近い。

ChartonはLLMによる数学研究（GPT-5を使ったErdős問題の解法発見等）に懐疑的で、「LLMは既存情報の派生には優れるが、誰も持ったことのない新しい洞察が必要な問題には向かない」と指摘する。Axplorerは既存データからの推論ではなく、パターン探索による新規発見を志向する点が差別化要素である。

Axiom MathはAxplorerを使い、グラフ理論の別の2問題でも既知の最良結果に並ぶか上回る結果を得たと主張している。米国防高等研究計画局（DARPA）の「expMath」イニシアチブの一環とも位置付けられており、AI活用による数学研究加速という国家的文脈も持つ。

シドニー大学のGgeordie WilliamsonはPatternBoostの共同研究者だが、Axplorerの改良点が理論上は適用範囲を広げると認めつつ、「その改善がどれほど重要かはまだわからない」と慎重な評価を示している。また「今は多くの企業がツールを売り込んでいる時期であり、数学者は可能性の多さに圧倒されている」とも述べており、ツールの乱立という課題も浮き彫りになっている。

## アイデア

- 「例を与える→類似生成→選別→再入力」という反復的パターン探索ループは、人間の直感とAIの計算力を組み合わせたヒューマンインザループ型探索の好例であり、エージェント設計における人間フィードバック活用（RLAIF的発想）と構造的に類似する
- スーパーコンピュータ3週間→Mac Pro 2.5時間という効率化は、アルゴリズムの改良によって計算資源のボトルネックを解消できることを示しており、ローカルLLMインフラ設計における「計算効率 vs. 規模」のトレードオフを考える上で参考になる
- LLMは「既存データの派生」には強いが「誰も見たことのない洞察」には弱いというChartonの指摘は、監査領域での異常検知や新規リスク発見においてもLLM単体への過信を戒める重要な視点を提供する
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[数学者の研究手法を変えるAIツール「Axplorer」——Axiom MathがPatternBoostを民主化](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
