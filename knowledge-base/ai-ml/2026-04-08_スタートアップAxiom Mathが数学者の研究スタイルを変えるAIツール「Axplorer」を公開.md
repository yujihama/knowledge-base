---
title: "スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-08
tags: [PatternBoost, Axplorer, graph-theory, AlphaEvolve, evolutionary-search, open-source, DARPA-expMath, combinatorics]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
related: [159, 615, 347, 1519, 836]
processed_at: "2026-04-08T21:19:15.929251"
---

## 要約

Palo Alto拠点のスタートアップAxiom Mathが、数学者向けAIツール「Axplorer」を無償公開した。同ツールはMeta在籍時にFrançois Chartonが共同開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上で動作していた前身とは異なり、Mac Pro単体で動作する。

PatternBoostはグラフ理論の難問「Turán四サイクル問題」を解くために使われた実績を持つ。同問題は、点の集合において4点を結ぶループを作らずにできるだけ多くの辺を引く方法を求めるもので、ソーシャルメディアのネットワーク解析やサプライチェーン、検索エンジンランキングに応用される。Charton氏はMeta時代に数万台のマシンを3週間動かして解を得たが、Axplorerは同じTurán問題の結果をわずか2.5時間で再現したという。

Axplorerの動作原理はPatternBoostと同様で、ユーザーが数学的な例を与えると類似パターンを生成し、ユーザーが興味深いものを選択してフィードバックすることで探索を繰り返す進化的アプローチを採る。これはGoogle DeepMindのAlphaEvolveがLLMを使って解候補を生成・改善し続ける手法と類似した思想を持つ。AlphaEvolveが大規模GPUクラスタを必要とし外部から利用申請が必要なのに対し、AxplorerはオープンソースでコードがGitHubで公開されており、誰でも導入できる点が差別化要素。

Charton氏はGPT-5などのLLMを使った最近の数学的成果に対して批判的で、「LLMは既存の知識の派生として機能するが、真に新しい洞察を生む能力は限定的」と指摘する。一方でAxplorerは、これまで誰も気づいていないパターンの発見を支援し、新たな数学的分野の開拓につながる可能性を目指す。Axiom Mathはすでに他の2つのグラフ理論の難問でも既知の最良結果に並ぶか超える成果を出したと主張している。

シドニー大学のGeodie Williamson氏はPatternBoostの共同研究者で、Axplorerへの改良点が理論上は適用範囲を拡大するとしつつ、実際の有効性は「今後見極めが必要」とコメント。また数学者がAIツールの洪水に圧倒されている現状も指摘しており、ホワイトボードを使った古典的アプローチの価値も忘れるべきでないと述べる。

米国防高等研究計画局（DARPA）は「expMath（Exponentiating Mathematics）」イニシアチブを立ち上げ、数学分野でのAI活用を推進しており、Axiom MathはこのエコシステムのプレイヤーとしてAI数学ツールの民主化を目指す。

## アイデア

- 進化的フィードバックループによるパターン探索：ユーザーが「面白い」と感じたサンプルを選択して再入力する人間参加型の探索ループは、RLHF的な選好学習と構造的に類似しており、数学以外のドメイン（例：監査ルール生成）にも転用できる可能性がある
- LLMの保守性とパターン探索エンジンの補完関係：LLMは既存データに基づく派生生成に強い一方、PatternBoost/Axplorerのような進化的探索は未踏の解空間を開拓できる。両者を組み合わせたハイブリッドアーキテクチャが有効な問題クラスが存在する
- スーパーコンピュータ→単一Mac Proへの効率化：3週間×数万台→2.5時間×1台という劇的な計算効率の改善は、アルゴリズム設計（探索空間の刈り込み、表現の工夫）によるものであり、ハードウェアスケールアウトに依存しないAI実用化の好例
## 関連記事

- /deep_159 野生動物をどこでも識別：SpeciesNetによる野生生物モニタリング
- /deep_615 OneComp: 生成AIモデル圧縮のワンライン革命
- /deep_347 OmniWeaving: 自由形式の構成と推論を用いた統合動画生成モデル
- /deep_1519 MolmoWeb: オープンなビジュアルWebエージェントとオープンデータ
- /deep_836 LeMaterial: 材料科学研究を加速するオープンソースイニシアチブ

## 原文リンク

[スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
