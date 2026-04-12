---
title: "スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-10
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, DARPA-expMath, オープンソース]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
related: [203, 1121, 1305, 1190, 948]
processed_at: "2026-04-10T21:19:44.473105"
---

## 要約

カリフォルニア州パロアルトを拠点とするAxiom Mathは、数学者向けのAIツール「Axplorer」を無償公開した。同ツールはMeta在籍時にFrançois Chartonが2024年に開発した「PatternBoost」を再設計したもので、スーパーコンピュータ上で動作していたPatternBoostをMac Pro単体で実行可能にした点が最大の特徴。PatternBoostはグラフ理論の未解決問題「Turán四閉路問題」の解決に使用されたが、当時はMetaの数千〜数万台規模のマシンを3週間稼働させるという「恥ずかしいほどのブルートフォース」手法だった。Axplorerはその同等の結果をわずか2.5時間で再現したとChartonは述べている。

Axplorerの基本的な仕組みは反復的なパターン探索である。ユーザーが具体的な数学的オブジェクトの例を入力すると、ツールが類似例を生成し、ユーザーが興味深いものを選択してフィードバックする。このサイクルを繰り返すことで、これまで発見されていなかった数学的パターンを発掘していく。Google DeepMindのAlphaEvolveと概念的に類似しており、AlphaEvolveもLLMで候補解を生成し最良のものを保持・改善するアプローチを取るが、AlphaEvolveは大規模GPUクラスター上で動作し一般公開されていない。AxplorerはオープンソースでGitHubから取得可能。

Axiom MathのCEOでありматематик（数学者）でもあるCarina Hongは、既存のAIツールが「解の発見」に偏っていると指摘する。数学は本来探索的・実験的な営みであり、Axplorerはその探索プロセス自体を支援することを目指す。独自のニューラルネットワーク訓練を不要とし、ステップバイステップのガイドで操作できる設計は、数学者の心理的障壁を下げることを意図している。

Axiom MathはAxplorerを使って、Turán問題以外にも2つのグラフ理論の難問で最良既知結果に匹敵または改善する成果を上げたと主張している。米国防高等研究計画局（DARPA）の「expMath（Exponentiating Mathematics）」イニシアティブの文脈とも合致する。一方、共同研究者であるシドニー大学のGeordie Williamsonは「多くの企業がツールを売り込む奇妙な時代」と述べ、改良の有意性は今後の実証次第と慎重な姿勢を示した。LLMによるアプローチについてChartonは、「LLMは既存の蓄積から派生するものには非常に優れているが保守的であり、前例のない洞察が必要な問題には不向き」と明確に否定的評価を示している。

## アイデア

- 反復的フィードバックループによるパターン探索という設計思想は、人間の直感（どのパターンが興味深いか）とAIの生成能力を組み合わせた協調型探索として、強化学習的なアイデアを数学研究に応用したもの
- スーパーコンピュータ3週間→Mac Pro単体2.5時間という効率化は、アルゴリズム設計の改善によるもので、計算リソースの民主化という観点から研究アクセスの平等化を示す好例
- LLMは「既存知識の補間」には強いが「前例のない洞察」には弱いというChartonの指摘は、LLMの本質的限界を端的に表しており、探索的AIシステム設計における特化型アーキテクチャの必要性を示唆する
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者の研究スタイルを変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
