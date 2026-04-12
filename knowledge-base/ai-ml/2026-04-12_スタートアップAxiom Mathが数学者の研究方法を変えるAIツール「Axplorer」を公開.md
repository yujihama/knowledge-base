---
title: "スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-12
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, 組み合わせ最適化, オープンソース]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-12T09:20:03.778589"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学者向けの無料AIツール「Axplorer」をリリースした。このツールはMeta在籍時にFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピューター上で動作していたPatternBoostに対し、AxplorerはMac Pro単体で動作する点が大きな特徴である。

PatternBoostはグラフ理論の未解決問題「Turán四サイクル問題」を解くために使用された実績を持つ。この問題は、多数の頂点間にできるだけ多くの辺を引きつつ、4頂点を結ぶ閉路（四サイクル）を作らないようにする組み合わせ最適化問題で、ソーシャルネットワーク・サプライチェーン・検索エンジンのランキング分析など複雑なネットワーク解析に応用される重要な問題である。PatternBoostはMetaの数万台規模のマシンで3週間かけて解いたが、Axplorerは同等の結果を2.5時間で達成したとChartonは述べている。さらにAxiom MathはAxplorerを用いてグラフ理論の他の2つの著名問題でも最良既知結果に並ぶか改善する成果を得たと主張している。

AxplorerのコアアルゴリズムはPatternBoostと同様の反復的パターン探索方式を採用する。ユーザーが問題例を与えると、ツールが類似する例を複数生成し、ユーザーが興味深いものを選択してフィードバックする。ツールはそれを元にさらに生成を繰り返す、という進化的探索ループを構成する。これはGoogle DeepMindのAlphaEvolveがLLMを用いて新規解を生成し最良候補を保持して改善を繰り返すアプローチと概念的に類似している。

AxplorerとAlphaEvolveの大きな違いはアクセス性にある。AlphaEvolveは大規模GPUクラスターを必要とし、DeepMindのスタッフを介さなければ利用できないクローズドなシステムである。一方AxplorerはオープンソースでGitHub上で公開されており、自分のマシンにインストールすれば誰でも利用可能だ。

ChartonはLLMによる数学の解法発見に対して懐疑的な立場を示している。「LLMは既存のデータから派生するものには極めて優れているが、保守的であり既存のものを再利用しようとする」とし、誰も考えたことのない新しいアイデアや洞察が必要な大問題には不向きだと指摘する。Axplorerが狙うのはまさにそのような「新しいパターンの発見」を通じた数学的探索の支援である。

シドニー大学の数学者Geordie Williamsonは「PatternBoostは素晴らしいアイデアだが万能薬ではない」と述べ、ホワイトボードを使う地道なアプローチも忘れてはならないと警告している。また、現時点でAxplorerに加えられた改良が実際にどの程度の効果を持つかは「今後次第」としている。米国防高等研究計画局（DARPA）も「expMath」イニシアチブでAI数学ツールの開発を奨励しており、Axiom Mathはこのエコシステムにおけるオープンなプレーヤーとして位置づけられる。

## アイデア

- LLMは既存データからの派生問題に強いが、PatternBoost/Axplorerのような進化的パターン探索は「誰も見たことのない新パターン」の発見に特化しており、LLMとは補完的なアプローチである
- スーパーコンピューター3週間相当の計算をMac Pro単体で2.5時間に圧縮したアーキテクチャ改善は、エージェント開発における計算効率最適化の参考になる
- ユーザーが面白い候補を選んでフィードバックするループ構造は、LLM-as-judgeや強化学習のReward Modelingと類似した人間フィードバック活用の設計パターンであり、監査エージェントにおける人間-AI協調インターフェース設計に応用できる

## 前提知識

- **PatternBoost** → [スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」](../ai-ml/2026-04-01_スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」.md)
- **AlphaEvolve** → [スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」](../ai-ml/2026-04-01_スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」.md)
- **グラフ理論** → [スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」](../ai-ml/2026-04-01_スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」.md)
- **進化的アルゴリズム** → [MolEvolve: 解釈可能な分子最適化のためのLLM誘導型進化探索](../ai-ml/2026-03-31_MolEvolve_ 解釈可能な分子最適化のためのLLM誘導型進化探索.md)
- **LLM評価限界** (TODO: 読むべき)

## 関連記事

- [疎学習による分枝戦略の改善で混合整数計画ソルバーを高速化](../ai-ml/2026-04-08_疎学習による分枝戦略の改善で混合整数計画ソルバーを高速化.md)
- [グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ](../ai-ml/2026-04-02_グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ.md)
- [StarCoder2とThe Stack v2：次世代オープンコードLLMの公開](../ai-ml/2026-04-09_StarCoder2とThe Stack v2：次世代オープンコードLLMの公開.md)
- [Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム](../ai-ml/2026-04-10_Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム.md)
- [Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表](../infra/2026-04-09_Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表.md)

## 原文リンク

[スタートアップAxiom Mathが数学者の研究方法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
