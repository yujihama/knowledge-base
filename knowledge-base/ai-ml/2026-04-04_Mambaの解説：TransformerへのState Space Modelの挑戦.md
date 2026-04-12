---
title: "Mambaの解説：TransformerへのState Space Modelの挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-04
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, 選択的状態空間, Zero-Order Hold, Parallel Scan, LTI, Gu-Dao]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-04T09:00:42.812679"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのボトルネックを克服することを目的としている。Transformerの根本的な問題は、Attention機構のO(n²)時間計算量と、KVキャッシュのO(n)空間計算量にある。これにより、コンテキスト長が増加するにつれてレイテンシが二次関数的に悪化し、長文脈処理（100万トークン規模）が現実的ではなくなる。

Mambaはこの問題をSSMで代替することで解決する。SSMの核心は、連続時間微分方程式 h'(t) = Ah(t) + Bx(t) と出力方程式 y(t) = Ch(t) + Dx(t) で表される状態遷移モデルであり、過去の全トークンを参照する代わりに、固定サイズの隠れ状態hに情報を圧縮する。この「状態は過去の圧縮」という設計思想により、推論時はO(1)空間・O(n)時間を実現する。

離散化にはZero-Order Hold（ZOH）手法を採用し、連続時間モデルをΔパラメータを用いた離散差分方程式に変換する。このΔはサンプリング間隔を制御し、学習可能パラメータとして扱われる。

従来のSSM（S4等）との最大の違いは「選択性（Selectivity）」にある。従来のSSMではA・B・Cが入力に依存しない時不変（LTI）パラメータだったが、Mambaではこれらを入力xの関数として動的に変化させる。これにより「どの情報を状態に残すか」を入力に応じて適応的に制御できる。一方で、この入力依存性によりS4で可能だった畳み込み表現による並列学習が使えなくなる問題が生じる。

MambaはこれをHardware-Aware Parallel Scan（並列スキャン）とFlashAttention類似のカーネルフュージョンで解決し、GPU上での高速学習を実現した。Mamba-3Bモデルは同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能をThe Pile等のベンチマークで示し、推論速度はTransformerの最大5倍とされる。

ただし課題も存在する。Mambaのリカレント構造は固定サイズの状態に情報を圧縮するため、Transformerの「完全な文脈への無損失アクセス」と比較して情報損失のリスクがある。また、Transformerで発達したInterpretability手法（Attention Head分析等）がMambaには直接適用できず、解釈可能性の研究は未発達である。現時点ではTransformerほどの大規模スケーリング実績もない。

## アイデア

- 固定サイズの隠れ状態に過去を圧縮するリカレント構造は、監査ログのストリーム処理（無制限長の取引履歴を固定メモリで処理）に直接応用できる設計パターン
- 「選択性」（どの入力情報を状態に保持するかを動的決定）はAgentのメモリ管理問題と同型であり、LangGraphのState設計における不要情報の自動フィルタリングに示唆を与える
- Transformerの二次計算量ボトルネックをSSMで回避するアーキテクチャ選択は、長大な監査証跡ドキュメントを扱うRAGパイプラインのエンコーダ選択に影響する実用的知見

## Yujiの取り組みへの示唆

監査エージェントは長大な監査証跡・契約書・規制文書を扱うため、100万トークン規模のコンテキストを線形コストで処理できるMambaのアーキテクチャは直接的な応用候補となる。LangGraphのStateノードにおける情報保持戦略（何を残し何を捨てるか）はMambaの選択性メカニズムと概念的に対応しており、エージェントメモリ設計の参考になる。また、ローカルLLMインフラ（RTX 3090）での長文脈推論においてTransformer比最大5倍の速度向上は実運用上の意義が大きく、Ollamaでの展開モデル選定時にMambaベースモデルを検討する価値がある。

## 原文リンク

[Mambaの解説：TransformerへのState Space Modelの挑戦](https://thegradient.pub/mamba-explained/)
