---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-08
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形計算量, 選択的SSM, S6, HiPPO, parallel-scan, 長文脈処理]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-08T21:48:24.513638"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量（O(n²)）ボトルネックを線形計算量（O(n)）で解消する。Mamba-3Bは同サイズのTransformerを上回り、2倍のサイズのTransformerに匹敵する性能を示しつつ、推論速度はTransformerの最大5倍に達する。

【SSMの数理的構造】Mambaの中核はControl Theory由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される状態空間モデル。これをZero-Order Hold（ZOH）法で離散化し、実装可能な差分方程式 h_t = Āh_{t-1} + B̄x_t に変換する。行列A, B, Cは入力xに依存しない固定パラメータではなく、選択的SSM（S6）においては入力に応じて動的に変化する（input-dependent）設計となっている。これが従来の線形時不変SSMやHiPPO理論を拡張したMambaの本質的な革新点。

【計算効率の実現方法】畳み込み表現とリカレント表現の双方で計算可能であり、並列スキャン（parallel scan）・カーネルフュージョン・再計算（recomputation）を組み合わせたHardware-Aware Algorithmにより、HBM（高帯域幅メモリ）へのアクセスを最小化。FlashAttentionと同様の発想でGPU I/Oを最適化し、高速化を実現している。

【Transformerとの比較】Transformerのアテンション機構はトークン間通信をKVキャッシュ経由で全トークン参照（O(n)空間・O(n²)時間）するのに対し、MambaのSSMは固定サイズの隠れ状態hで過去情報を圧縮して保持する（リカレント型）。長文脈（100万トークン規模）での運用が現実的となる一方、アテンションが持つ「過去の全トークンへの直接アクセス」はなく、情報は有損失圧縮される。解釈可能性の観点では、どの情報が隠れ状態に保持されるかを特定するのがTransformerより困難という課題もある。

【応用領域】言語モデリングのほか、音声・ゲノム解析等のシーケンスデータに対してstate-of-the-artを達成。長文脈推論・リアルタイム処理が求められるエッジデプロイや、長期記憶が必要なチャットボット等に特に優位性を発揮する。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能するリカレント設計は、監査エージェントにおける長期セッション管理（複数の監査手続きにわたる文脈保持）への応用可能性がある
- 入力依存の行列B, Cにより「どの情報を記憶・忘却するか」を動的に制御する選択的SSMは、ReActエージェントのワーキングメモリ設計に対する新たな設計原理を示唆している
- 並列スキャンとカーネルフュージョンによるHardware-Aware Algorithmは、FlashAttentionと同様の思想でGPU効率を最大化しており、ローカルLLMインフラ（RTX 3090等）での低レイテンシ推論に直結する実装知識として価値がある

## Yujiの取り組みへの示唆

監査エージェントでは長い監査証跡や複数期間にわたる財務データを扱うため、Transformerの二次計算量ボトルネックは実用上の制約になりうる。MambaのSSMベース設計は、LangGraphの各ノードが保持するエージェント状態（state）の概念とも対応しており、長文脈エージェントの基盤モデル選定において有力な選択肢となる。また、ローカルLLMインフラ（RTX 3090予定）でのデプロイ時に、同等性能でメモリ効率・推論速度が優れるMambaベースモデルは実用的な選択肢であり、Ollama等でのサービング設計にも参考になる。

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性](https://thegradient.pub/mamba-explained/)
