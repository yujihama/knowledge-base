---
title: "正規化フリーTransformerの初期化時における劣臨界信号伝播"
url: "https://tldr.takara.ai/p/2604.11890"
date: 2026-04-26
tags: [Transformer, signal propagation, APJN, LayerNorm, Dynamic Tanh, DyT, Derf, criticality, initialization, gradient flow, Vision Transformer]
category: "ai-ml"
related: [1855, 694, 2622, 2948, 1467]
memo: "[HF Daily Papers] Subcritical Signal Propagation at Initialization in Normalization-Free Transformers"
processed_at: "2026-04-26T12:02:48.713368"
---

## 要約

本論文は、Transformerにおける初期化時の信号伝播を、平均偏ヤコビアンノルム（APJN: Averaged Partial Jacobian Norm）という指標を用いて理論的に分析した研究である。APJNは層をまたいだ勾配増幅の尺度であり、深いネットワークにおける学習安定性の代理指標として機能する。

従来のAPJN解析を拡張し、双方向アテンション（bidirectional attention）と置換対称な入力トークン配置を持つTransformerに適用可能な再帰関係（recurrence relations）を導出した。これにより、活性化統計とAPJNが層を越えてどのように伝播するかを定式化している。

理論の主要な予測として、アーキテクチャの違いによりAPJNの漸近挙動が大きく異なることが示された。具体的には、pre-LayerNorm構成（LayerNormを残差ブロック前に配置する一般的な設計）ではAPJNがべき乗則（power-law）的に成長し、残差ネットワークで知られる臨界（critical）挙動を示す。一方、LayerNormをelement-wiseなtanh型非線形関数で置き換えたアーキテクチャでは、APJNが引き延ばされた指数関数（stretched-exponential）的に成長し、これは劣臨界（subcritical）状態を意味する。劣臨界状態では深い層への信号伝播が減衰するため、学習が不安定になりやすい。

応用として、近年提案されたDynamic Tanh（DyT）およびDynamic erf（Derf）という正規化フリーTransformerに本理論を適用した。これらのアーキテクチャでは、LayerNormの代替としてDyTやDerfを用いることでバッチ正規化なしの学習を目指しているが、理論分析によりこれらが劣臨界挙動を示すことが明確化された。これが、DyTおよびDerf Transformerが初期化や最適化の設定に対して感度が高く、安定した学習のために慎重なチューニングを必要とする理由を説明している。

実験的には、深いVision Transformer（ViT）において実測したAPJNと理論予測が一致することを確認しており、理論の実用的妥当性を示している。

監査エージェント開発への示唆としては直接的な関連は薄いが、大規模LLMのファインチューニングや独自アーキテクチャ設計時に、正規化層の有無や置換が学習安定性に与える影響を定量的に評価する枠組みとして参照できる。特にLoRAやQLoRAを用いた学習で不安定性が生じる場合、LayerNormの配置を見直す理論的根拠になり得る。

## アイデア

- LayerNormをtanh型関数で置き換えると劣臨界状態になるという理論的説明は、正規化フリーアーキテクチャが『なぜ』難しいかを初めて定量的に説明しており、DyT系の研究への重要なカウンターポイントになる
- APJNという単一のスカラー指標で深いTransformerの学習安定性を初期化前に予測できる枠組みは、大規模モデルのアーキテクチャ探索（NAS）における安価な事前フィルタリング手法として応用可能
- 残差ネットワークで知られる臨界性（criticality）の概念がTransformerにも成立することの理論的証明は、両アーキテクチャを統一的に捉える信号伝播理論の基盤となる

## 前提知識

- **Transformer（アテンション機構）** (TODO: 読むべき)
- **LayerNorm** (TODO: 読むべき)
- **勾配消失・爆発** (TODO: 読むべき)
- **ヤコビアン行列** (TODO: 読むべき)
- **残差ネットワーク（ResNet）** (TODO: 読むべき)

## 関連記事

- /deep_1855 機械学習をコードとして扱う時代の到来
- /deep_694 QUEST: クエリ変調球面アテンションによるロバストなアテンション定式化
- /deep_2622 Car-GPT：LLMは自動運転を実現できるか？
- /deep_2948 Car-GPT：LLMは自動運転を実現できるか？
- /deep_1467 Car-GPT: LLMは自動運転を実現できるか？

## 原文リンク

[正規化フリーTransformerの初期化時における劣臨界信号伝播](https://tldr.takara.ai/p/2604.11890)
