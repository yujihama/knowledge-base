---
title: "スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開"
url: "https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/"
date: 2026-04-09
tags: [PatternBoost, Axplorer, グラフ理論, 数学AI, パターン探索, AlphaEvolve, オープンソース, DARPA-expMath]
category: "ai-ml"
memo: "[MIT Technology Review AI] This startup wants to change how mathematicians do math"
processed_at: "2026-04-09T12:02:07.500695"
---

## 要約

カリフォルニア州パロアルトを拠点とするスタートアップAxiom Mathが、数学者向けの無償AIツール「Axplorer」を公開した。同ツールはMeta在籍時にFrançois Chartonが2024年に共同開発した「PatternBoost」を再設計したものであり、スーパーコンピュータが必要だったPatternBoostに対し、AxplorerはMac Pro単体で動作する。

PatternBoostはグラフ理論の難問「Turán四サイクル問題」の解法発見に用いられた実績がある。AxplorerはPatternBoostと同じ結果を約2.5時間で再現したのに対し、PatternBoostは数千〜数万台のマシンを使って3週間を要した。Axiom MathはAxplorerを用いてグラフ理論の他の2つの難問でも最良の既知結果に匹敵または改善する成果を上げたと発表している。

Axplorerの仕組みはパターン生成の反復的ループに基づく。ユーザーがサンプルを与えると、ツールが類似パターンを生成し、ユーザーが有望なものを選択してフィードバックすると、さらに改善された候補を生成するという流れを繰り返す。これはGoogle DeepMindのAlphaEvolveと類似したアーキテクチャであるが、AlphaEvolveが大規模GPUクラスタを必要とし外部アクセスが制限されているのに対し、AxplorerはオープンソースとしてGitHub上で公開されており、誰でもインストールして利用可能な点が異なる。

ChartonはLLMによる数学問題の解法発見（GPT-5を用いたErdős問題の解法等）に対して懐疑的であり、「LLMは既存データの派生には優れるが保守的であり、真に新しいアイデアは生み出せない」と主張する。PatternBoostおよびAxplorerの設計思想は既存の解法ではなく、誰も発見したことのない新しいパターンの探索にある。

シドニー大学のGgeordie WilliamsonはPatternBoostの共同研究者であるが、Axplorerの改善点が理論上は適用範囲を広げるものの「実際の重要性は今後検証が必要」とコメントしている。またWilliamsonは「多くの企業から数学者向けツールが次々と提供されており数学者は選択肢の多さに圧倒されている」とも述べ、新ツールの実際のインパクトについて慎重な見方を示している。

米国DARPA（国防高等研究計画局）は「expMath（Exponentiating Mathematics）」という新イニシアティブを立ち上げ、数学者によるAIツールの開発・利用を促進している。Axiom MathはこのDARPAの取り組みの一環として位置づけており、数学の突破口がコンピュータサイエンスや次世代AI・暗号セキュリティに波及効果をもたらすという考えに基づいて活動している。

## アイデア

- 人間が選択・フィードバックを行いながらAIがパターンを反復生成する「進化的探索ループ」は、LLMの保守性を補い未知の構造を発見するための設計思想として注目に値する
- スーパーコンピュータ規模の計算（3週間・数万台）をMac Pro単体・2.5時間に圧縮した効率化は、モデルアーキテクチャとサーチ戦略の最適化による成果であり、ローカルLLM推論の可能性を示す
- 「解法を見つける」だけでなく「誰も気づいていないパターンを探索する」という問題設定の違いが、LLMベースのアプローチとの本質的な差異を生んでおり、探索と活用（exploration vs. exploitation）のバランス設計が重要
## 関連記事

- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ
- /deep_1121 StarCoder2とThe Stack v2：次世代オープンコードLLMの公開
- /deep_1305 Hugging Faceにおけるオープンソーステキスト生成・LLMエコシステム
- /deep_1190 Hugging FaceとGoogleがオープンAI協力のための戦略的パートナーシップを発表
- /deep_948 Hugging FaceがTruffleHogと提携し、シークレットスキャン機能をプラットフォームに統合

## 原文リンク

[スタートアップAxiom Mathが数学者の研究手法を変えるAIツール「Axplorer」を公開](https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/)
