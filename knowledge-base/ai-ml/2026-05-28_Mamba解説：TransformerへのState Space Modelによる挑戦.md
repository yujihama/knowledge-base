---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-28
tags: [Mamba, State Space Model, SSM, Selective SSM, HiPPO, 離散化, ZOH, 線形スケーリング, 長コンテキスト, Transformer代替]
category: "ai-ml"
related: [222, 2480, 2510, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-28T09:26:20.851309"
---

## 要約

MambaはAlbert GuとTri Daoが開発した、Transformerの代替となるState Space Model（SSM）ベースのシーケンスモデルである。Transformerの中核問題はAttentionの二乗計算量（O(n²)）とKVキャッシュのO(n)メモリ消費にあり、コンテキスト長が伸びるほど速度・メモリ両面でボトルネックが生じる。Mambaはこの「二乗ボトルネック」を除去し、系列長に対して線形スケーリングを実現しながら、100万トークン規模のコンテキストでも性能が向上することを示した。推論速度はTransformerの最大5倍速い。

技術的な核心はSSMの状態方程式にある。連続時間モデルとして h'(t) = Ah(t) + Bx(t)、出力として y(t) = Ch(t) + Dx(t) で表される。状態hは「過去の圧縮」であり、入力x と行列A・B・C・D により次状態と出力が決まる。これをZero-Order Hold（ZOH）離散化により差分方程式へ変換し、実際のトークン系列処理に適用する。離散化後の行列はÂ・B̂と表記される。

Mambaの革新点は「選択的SSM（Selective SSM）」にある。従来のSSMは線形時不変（LTI）システムであり、入力に依存せず固定の行列A・B・Cを使うため、情報を選択的に保持・無視することができなかった。Mambaでは行列B・C・Δ（タイムステップ）を入力xの関数とすることで、内容依存の状態更新を可能にした。これによりInduction HeadやAssociative Recall（名前と職業のペア記憶）のような、Transformerが得意とするタスクをSSMで初めて解けるようにした。

実装上の課題として、入力依存パラメータによりHiPPO初期化などの最適化手法が使えなくなる問題がある。この課題をFlash-SSD（ハードウェア対応パラレルスキャン）で解決し、GPU上で実用的な速度を達成している。並列スキャンはパラレルプレフィックス和アルゴリズムを用い、見かけ上は再帰処理を並列化する。

Mamba-3Bは同サイズのTransformerと同等以上、かつ2倍サイズのTransformerに匹敵するプレトレーニング性能を示した（The Pile評価）。一方で欠点も存在する：（1）induction headなどのアルゴリズム的タスクでは依然Transformerに劣る場合がある、（2）モデルのInterpretabilityが難しく、Attentionパターンのような可視化ができない、（3）Transformerエコシステム（FlashAttention, vLLM等）の恩恵を受けにくい。監査エージェント開発への示唆として、長大な監査証跡ログや規制文書を扱う場面でMambaの線形コンテキストスケーリングは直接的に有効である。ただし説明責任（Explainability）要件の高い監査領域ではInterpretabilityの低さが懸念される。

## アイデア

- 選択的SSM（Selective SSM）により、入力内容に応じて状態を動的に保持・破棄できる点が従来LTI-SSMとの決定的違いであり、これがInduction HeadsやAssociative Recallを可能にした
- 訓練時は並列スキャン（パラレルプレフィックス和）、推論時は再帰計算という二重モードの実装により、TransformerのKVキャッシュ問題を根本的に回避しつつGPU効率を確保している
- 状態hを「過去の圧縮」と捉えるフレームワークは、エージェントの長期記憶設計（隠れ状態としての世界モデル）に応用できる概念的フレームワークを提供している

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **RNN / 再帰ニューラルネット** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **HiPPO初期化** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
