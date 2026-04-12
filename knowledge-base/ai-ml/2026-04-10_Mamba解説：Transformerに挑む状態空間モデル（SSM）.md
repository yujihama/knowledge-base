---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-10
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, 選択的SSM, 並列スキャン, ZOH離散化, シーケンスモデル]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-10T12:50:57.248436"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンションメカニズムが持つO(n²)の計算複雑性問題を解決することを目的としている。Transformerでは全トークン間のペアワイズ通信によりKVキャッシュがO(n)メモリを消費し、長文脈での推論が困難になるが、MambaはSSMを用いて状態を圧縮することでこの制約を回避する。

技術的核心は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を離散化したものであり、Zero-Order Hold（ZOH）手法で差分方程式に変換する。パラメータA, B, C, Δが入力xに依存して動的に変化する点が従来のSSM（S4等）との最大の差異で、これを「選択的状態空間モデル」と呼ぶ。

計算効率化のため、並列スキャンアルゴリズムとFlashAttentionに類似したカーネルフュージョンを組み合わせたHardware-Aware Selective Scanを実装し、Transformerと比較して推論速度が最大5倍向上。学習時はO(n log n)、推論時はO(1)（固定サイズの隠れ状態を再帰的に更新）という特性を持つ。

Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pileベンチマークで達成。言語・音声・ゲノミクスなど複数モダリティでState-of-the-Artを記録し、100万トークン長のシーケンスまでスケーリング性能が改善する。

一方で制約も存在する。固定サイズの隠れ状態に情報を圧縮するため、Transformerのような正確なルックバック（例：文脈内に特定の文字列が出現するかを判定するInduction Headsタスク）が苦手。Transformerが「無損失な過去の記憶」を持つのに対し、Mambaは「損失を伴う圧縮」を行う。この特性はコード補完や長文書検索など正確な参照が必要なタスクではTransformerに劣る可能性を示す。

解釈可能性の観点では、アテンションヘッドに相当する明示的な構造がないため、機械的解釈可能性（Mechanistic Interpretability）の適用が困難。AI安全性研究においても、現在の手法の多くがTransformerの構造を前提としているため、Mambaへの転用には新たな研究が必要となる。

## アイデア

- 選択的SSMの核心：パラメータB, C, Δが入力依存で動的変化することで、どの情報を状態に「記憶」しどの情報を「無視」するかをモデルが学習できる点。固定パラメータのSSMでは入力に関わらず同じ状態遷移をするため表現力が低かった
- 推論時O(1)の再帰という性質：KVキャッシュが不要で固定メモリで動作するため、長文脈でのバッチ推論やエッジデプロイに対して根本的なアーキテクチャ上の優位性がある
- 「損失圧縮」vs「無損失記憶」のトレードオフ：Mambaの隠れ状態は過去の情報を圧縮して保持するため、長期依存関係の保持と正確な参照のどちらを重視するかによってTransformerとMambaの使い分けが生じる設計上の問題
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
