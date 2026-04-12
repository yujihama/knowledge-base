---
title: "スタートアップAxiom Mathが数学者のための AI ツール「Axplorer」を公開——パターン探索で未解決問題に挑む"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-08
tags: [PatternBoost, Axplorer, グラフ理論, 数学AI, パターン探索, AlphaEvolve, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-08T21:40:58.985517"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathが、数学者向けAIツール「Axplorer」を無償公開した。同ツールはMeta在籍時にFrançois Chartonが開発した「PatternBoost」を再設計したもので、スーパーコンピュータを必要としていた前身ツールとは異なり、Mac Pro単体で動作する。

PatternBoostはグラフ理論の未解決問題「Turán四サイクル問題」を解くために活用され、数万台のマシンで3週間実行した。Axplorerは同じTurán問題を2.5時間で同等の結果に達したと報告されており、効率が大幅に改善されている。コードはオープンソースとしてGitHubで公開されている。

Axplorerの動作原理はPatternBoostを踏襲する反復的パターン探索である。ユーザーが初期サンプルを与えると、ツールはそれに類似した例を生成する。ユーザーが興味深いものを選択してフィードバックすると、ツールはさらに類似例を生成するというループを繰り返す。この手法はGoogle DeepMindのAlphaEvolveに近い発想で、優れた候補を保持しながらLLMに改善を求める進化的アプローチとも共通する。

ChartonはChatGPTなどのLLMが最近の数学的成果（Erdős問題群の解決など）をもたらしたことに懐疑的で、「誰も取り組んでいなかっただけの問題を解いても大した意味はない」と述べる。Axplorerが狙うのは有名数学者たちが長年研究してきた難問であり、Axiom Mathはすでにグラフ理論の2問題でも既知の最良結果に並ぶか上回る成果を出したとしている。

CEOのCarina Hongは、数学はただ解を求めるだけでなく探索的・実験的な活動だと強調する。AlphaEvolveは閉鎖環境でDeepMindのスタッフ経由でしかアクセスできないのに対し、Axplorerは誰でもローカルにインストールして使える点を差別化要因とする。ただし、シドニー大学のGeodie Williamsonは「数学者は今や多数のAIツールを提案されており、改善効果の実際の大きさはこれから見極める必要がある」と慎重な見方を示す。

米国防高等研究計画局（DARPA）は「expMath（Exponentiating Mathematics）」イニシアチブを立ち上げ、数学とAIの融合を推進しており、Axiom MathはこのトレンドにAlignした取り組みと位置付けられる。数学の新発見はコンピュータサイエンス・次世代AI・暗号技術に波及効果をもたらすと期待される。

## アイデア

- 人間のフィードバックループと機械生成を組み合わせた反復的パターン探索は、RLAIF的な発想（人間選好 → 再生成 → 絞り込み）と構造的に近く、強化学習の探索フェーズに応用できる可能性がある
- Axplorerの『初期例を与えて類似例を生成し選別するループ』は、LangGraphのサイクルグラフとして実装しやすい構造であり、エージェントの仮説生成・評価・絞り込みフローのプロトタイプとして参考になる
- 既知ベストを保持しながら反復改善するAlphaEvolve/Axplorer型の進化的探索は、監査ルール生成・異常パターン発見など正解ラベルが存在しないドメインへの適用可能性を示唆している

## Yujiの取り組みへの示唆

Axplorerの反復的パターン探索（サンプル生成→人間選別→再生成）は、GRPOやRLAIFで人間フィードバックを活用するアプローチと構造的に類似しており、監査エージェントにおける異常パターンの仮説生成ループ設計の参考になる。LangGraphでノードを『生成』『評価』『絞り込み』に分けたサイクルグラフを組めば、同様の探索ダイナミクスを監査ドメインに応用できる。ただし数学ドメイン固有の内容が中心であり、直接的な実装示唆よりもアーキテクチャパターンの参考として捉えるのが適切。

## 原文リンク

[スタートアップAxiom Mathが数学者のための AI ツール「Axplorer」を公開——パターン探索で未解決問題に挑む](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
