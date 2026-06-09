---
title: "LLMの出力にどのデータが寄与したかが分かる？ TDA（Training Data Attribution）の基礎"
url: "https://zenn.dev/fleure/articles/data_attribution_foundation"
date: 2026-06-09
tags: [TDA, Training Data Attribution, 影響関数, Influence Function, gradient-based, representation-based, AirRep, TRAK, LoGra, LLM解釈性]
category: "ai-ml"
related: [1411, 2132, 7367, 209, 1323]
memo: "[Zenn LLM] LLMの出力にどのデータが寄与したかが分かる？ TDAの基礎の基礎"
processed_at: "2026-06-09T09:06:14.499138"
---

## 要約

TDA（Training Data Attribution）は、LLMが特定の出力を生成した際に、どの学習データがその出力に寄与したかを特定する手法群の総称。法律・医療など根拠の明示が求められるドメインで特に重要性が高い。

手法は大きく2系統に分類される。①representation-based手法は「出力と表現が近い学習データほど影響度が高い」という仮定に基づき、TF-IDF・n-gram・テキスト埋め込み・モデルの隠れ状態などで類似度を計算する。計算効率が高く大規模モデルにも適用しやすいが、選択する表現空間に結果が依存する欠点がある。近年のAirRep（NeurIPS 2025 Spotlight）は、Attribution専用に表現ベクトルを学習し直すことでこの欠点に対処し、複数データのグループ単位の影響も捉えられるようにした。

②gradient-based手法は損失関数の勾配情報を使い、特定学習データを除外した場合の損失変化を閉形式（再学習不要）で評価する影響関数（Influence Function）を中心概念とする。基礎論文はKoh & Liang（ICML 2017）で、数式は I = -(1/n)∇L(z',θ̂)ᵀ H⁻¹ ∇L(zᵢ,θ̂) と表される。ヘッセ行列の逆行列計算がボトルネックとなるため、TRAK（ICML 2023）やLoGra（NeurIPS 2025）などの近似手法が継続的に開発されている。

周辺領域として、RAG評価に直結するContext Attribution（ContextCite, NeurIPS 2024）や、出力が事前学習由来かコンテキスト由来かを判別するKnowledge Source Attributionも存在する。監査エージェント開発への示唆として、LLMの判断根拠をトレーニングデータレベルで追跡できるTDAは、監査証跡の透明性確保や誤出力の原因分析に直接応用可能であり、特にFine Tuning済みモデルで特定ドメインデータの影響度を定量化する用途が考えられる。

## アイデア

- 影響関数を使えばLLMを再学習せずに特定学習データの寄与度を閉形式で計算できる点が、大規模モデルの解釈性研究において実用上の鍵となっている
- AirRepのようにAttribution専用に表現空間を学習し直すアプローチは、RAGの検索品質評価とTDAの境界を曖昧にし、検索・帰属を統合したフレームワークへの発展可能性がある
- Context AttributionとKnowledge Source Attributionの組み合わせにより、LLMの出力が「いつ学習した知識」と「今回与えたコンテキスト」のどちらに依存しているかを定量化できれば、RAGシステムの信頼性評価が根本的に変わる

## 前提知識

- **Influence Function** (TODO: 読むべき)
- **ヘッセ行列** → /deep_7529 平坦性と汎化：同次斉次ニューラルネットワークによるマルチインデックスモデルの学習
- **損失関数・勾配** (TODO: 読むべき)
- **Fine Tuning** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_1411 形状・対称性・構造：機械学習研究における数学の役割の変遷
- /deep_2132 形状・対称性・構造：機械学習研究における数学の役割の変遷
- /deep_7367 形状・対称性・構造：機械学習研究における数学の役割の変容
- /deep_209 形状・対称性・構造：機械学習研究における数学の役割の変化
- /deep_1323 形状・対称性・構造：機械学習研究における数学の役割の変化

## 原文リンク

[LLMの出力にどのデータが寄与したかが分かる？ TDA（Training Data Attribution）の基礎](https://zenn.dev/fleure/articles/data_attribution_foundation)
