---
title: "スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-11
tags: [PatternBoost, Axplorer, グラフ理論, 数学的パターン探索, AlphaEvolve, DARPA-expMath, オープンソース, 記号的AI]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-11T21:36:32.904332"
---

## 要約

カリフォルニア州パロアルトのスタートアップAxiom Mathが、数学者向けのオープンソースAIツール「Axplorer」を無料公開した。同ツールは、MetaのFrançois Chartonが2024年に開発した「PatternBoost」を基にしたリデザインで、スーパーコンピュータ上で動作していたPatternBoostをMac Pro一台で動作可能にした点が大きな進化である。

PatternBoostはグラフ理論における未解決問題「Turán四サイクル問題」を解くために使用されたツールで、当時は数千〜数万台のマシンで3週間かけて計算した。Axplorerはその同じ結果を2.5時間で再現したとChartonは述べており、効率性の大幅な向上が確認されている。また、Axiom MathはAxplorerを用いてグラフ理論の他2つの著名問題でも最良既知結果に匹敵または改善したとしている。

Axplorerの基本的な仕組みはパターン探索のループである。ユーザーが例を与えると、ツールが類似パターンを生成する。ユーザーは興味深いものを選択して再入力し、さらに類似パターンを生成するというサイクルを繰り返す。この手法はGoogle DeepMindのAlphaEvolveと類似しており、AlphaEvolveがLLMを使って新解法を提案し最良案を保持・改善するのと同様の反復的アプローチを取る。

ChartonはLLMによる数学的発見に懐疑的で、「LLMは既存のものの派生には優れているが、保守的であり真に新しいアイデアを生み出しにくい」と指摘する。Axplorerは既知のパターンに依存せず、人類がまだ気づいていないパターンを探索することに特化している。

米国防高等研究計画局（DARPA）は「expMath（Exponentiating Mathematics）」という新イニシアチブを立ち上げ、数学者のAIツール活用を促進しており、Axiom MathはこのエコシステムへPy貢献することを意図している。

コードはGitHub上でオープンソースとして公開されており、学生や研究者が問題のサンプル解や反例生成に使えることを香港出身のCEO Carina Hongは期待している。シドニー大学のGeordie Williamsonは「PatternBoostは優れたアイデアだが万能ではない」と評しつつ、新たな改善による適用範囲の拡大には注目している。

## アイデア

- 人間がフィードバックループでパターンを選別し、AIが生成を繰り返す「インタラクティブ進化的探索」はRLHF/RLAIFの数学版として解釈できる
- スーパーコンピュータ依存だったPatternBoostをMac Pro一台・2.5時間で再現できたアーキテクチャ改善は、推論時計算効率化の実践例として注目に値する
- LLMが「既存データの派生」に強く「真の新規発見」に弱いという指摘は、エージェント設計でLLMを探索エンジンとして使う際の根本的制約を示唆する
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
