---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-02
tags: [Mamba, SSM, State Space Model, Transformer, selective-SSM, HiPPO, parallel-scan, long-context, sequence-model]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [199, 222, 833, 289, 255]
processed_at: "2026-04-02T21:08:53.710810"
---

## 要約

MambaはAlbert GuとTri Daoが開発した新しいシーケンスモデルアーキテクチャで、State Space Model（SSM）をベースとしている。Transformerの最大の弱点である注意機構の計算量O(n²)問題（二次ボトルネック）を、線形計算量O(n)で代替することを目的としている。

TransformerはKVキャッシュに全トークンの情報を保持するため、コンテキスト長が伸びるほどメモリ使用量と推論レイテンシが増大する。Mambaは連続時間の微分方程式 h'(t) = Ah(t) + Bx(t) をベースとし、これをZero-Order Hold（ZOH）法で離散化することで、シーケンスを固定サイズの隠れ状態hに圧縮する。この隠れ状態が「過去の圧縮表現」として機能し、全過去トークンを参照せずとも予測が可能になる。

Mambaの最大の革新はSelective State Spaceで、入力xに応じてパラメータB・C・Δを動的に変化させる「選択的」メカニズムにある。従来のS4等の線形時間不変（LTI）SSMは固定パラメータのため情報の選別ができなかったが、Mambaは入力依存的にパラメータを変化させることでコンテンツに応じたフィルタリングを実現している。

実装上の課題として、入力依存パラメータによりHiPPO行列など畳み込み表現が使えなくなるため、並列スキャンアルゴリズムとHardware-Aware（フラッシュ注意に類似したカーネルフュージョン）を組み合わせて高速化している。これにより推論時はTransformer比最大5倍の速度を達成し、100万トークン超のシーケンスにもスケールする。

性能面ではMamba-3Bモデルが同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。言語・音声・ゲノミクス等のモダリティでSOTA達成。

ただし弱点もある。Mambaの隠れ状態は固定サイズのため情報損失が避けられず、Transformerのようなインコンテキスト学習（ICL）が苦手な傾向がある。「Hungry Hungry Hippos」実験では、特定トークンを長距離検索するタスクでTransformerより劣る結果も報告されている。また解釈可能性の観点では、隠れ状態がブラックボックスであり、Transformer的なAttentionパターン分析が適用できない。

## アイデア

- 選択的SSMの「入力依存パラメータ」の考え方は、エージェントが過去の観察をどの粒度で記憶・忘却するかの設計に応用できる。固定サイズ隠れ状態への圧縮は、長期記憶と短期記憶のトレードオフそのもの。
- Transformerの二次ボトルネック回避はRAGアーキテクチャの設計思想と対照的：RAGは外部検索で文脈を補うが、Mambaは状態圧縮で内部的に対処する。長文書処理が必要なユースケースでは両者の組み合わせが有望。
- ZOHによる連続→離散の変換は制御理論由来で、LLM以外のリアルタイム時系列処理（監査ログの異常検知など）への応用可能性を示唆している。
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_289 DeepPolisherによる高精度ゲノムポリッシング：ゲノム研究の基盤強化
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
