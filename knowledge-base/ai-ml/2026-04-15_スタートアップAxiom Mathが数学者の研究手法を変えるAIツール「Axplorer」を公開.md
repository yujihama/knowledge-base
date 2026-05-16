---
title: "スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-15
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン発見, AlphaEvolve, Turán問題, オープンソース, DARPA expMath]
category: "ai-ml"
related: [203, 1711, 1121, 1305, 1190]
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-15T12:33:17.135411"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学者向けのAIツール「Axplorer」を無償公開した。Axplorerは、Meta在籍時にFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、PatternBoostがスーパーコンピューター上で動作していたのに対し、AxplorerはMac Pro1台で動作する。

PatternBoostはグラフ理論の難問「Turán四サイクル問題」を解くために使用された実績を持つ。この問題は、点の集合の間に線をできるだけ多く引きながら、4点が一周するループを作らないという最適化問題で、ソーシャルメディアや供給網、検索エンジンのネットワーク分析に応用される重要な問題である。PatternBoostはMetaの数千〜数万台のマシンで3週間かけて解いたが、Axplorerは同じ結果を2.5時間で達成したという。さらにAxiom Mathは、Axplorerを用いてグラフ理論の別の2つの重要問題でも最良既知結果に並ぶか上回る成果を出したと主張している。

Axplorerの基本的なアルゴリズムはPatternBoostと同様で、ユーザーがサンプルを与えると類似パターンを生成し、興味深いものを選んでフィードバックすることでさらに改良されたパターンを生成するという反復プロセスを取る。Google DeepMindのAlphaEvolveも同様のアプローチ（LLMで解候補を生成し最良のものを保持・改善）を採用しているが、AlphaEvolveは大規模GPUクラスターが必要でアクセスが限定的である点が異なる。AxplorerはオープンソースでGitHubで公開されており、学生や研究者が自分のマシンで利用できる点が差別化要素となっている。

Axiom Math CEOのCarina Hongは数学者自身であり、ツールの設計思想として「数学者に独自のニューラルネットワーク訓練を求めない」「ステップバイステップのガイドでウォークスルーできる」ことを重視している。一方、シドニー大学の数学者Geordie Williamsonは「PatternBoostは良いアイデアだが万能薬ではない」と評しており、Axplorerの改善が実際にどの程度の意義を持つかは今後の実証次第と述べている。

LLMによる数学アプローチとの比較として、Chartonは「LLMはすでに存在するものの派生には優れているが保守的であり、誰も持ったことのない洞察が必要な問題には限界がある」と主張。Axplorerのパターン発見型アプローチはこの限界を補完するものと位置づけられている。米国DARPAも数学へのAI活用を推進する「expMath」イニシアチブを設立しており、Axiom MathはこのトレンドのプレイヤーとしてD自らを位置づけている。監査エージェント開発への示唆として、パターン発見型の反復的フィードバックループは、監査における異常検知や規則の例外ケース発見にも転用可能なアーキテクチャである。

## アイデア

- PatternBoostのパターン生成→選択→フィードバックのループは強化学習的な反復改善と類似しており、ヒューリスティック探索をLLMなしで実現する点が興味深い
- スーパーコンピューター3週間の計算をMac Pro2.5時間に圧縮した効率化は、アルゴリズムの根本的な改善（ブルートフォースから知識誘導探索への転換）を示唆する
- 「LLMは既存データの派生には強いが新規洞察に弱い」というChartonの批判は、LLMと非LLM型探索エンジンの役割分担を考える上で重要な視点を提供する

## 前提知識

- **PatternBoost** → /deep_175 スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」
- **グラフ理論** → /deep_175 スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」
- **AlphaEvolve** → /deep_175 スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」
- **Turán問題** → /deep_210 数学者のための進化的パターン探索AI「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの新ツール
- **組合せ最適化** → /deep_238 オフライン決定トランスフォーマーによる神経組合せ最適化：巡回セールスマン問題でヒューリスティックを超える

## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1711 ~Don't~ Repeat Yourself：HuggingFace Transformersライブラリの設計哲学
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表

## 原文リンク

[スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
