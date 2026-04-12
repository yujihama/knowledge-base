---
title: "Nyströmformer: Nyström法による線形時間・メモリでのSelf-Attention近似"
url: "https://huggingface.co/blog/nystromformer"
date: 2026-04-11
tags: [Nyströmformer, efficient-attention, linear-attention, Transformer, 行列近似, Nyström法, 長文処理, HuggingFace]
category: "ai-ml"
memo: "[HF Blog] Nyströmformer: Approximating self-attention in linear time and memory via the Nyström method"
related: [1494, 1185, 1572, 1529, 1449]
processed_at: "2026-04-11T21:27:23.563760"
---

## 要約

Transformerのself-attentionはシーケンス長nに対してO(n²)の計算量・メモリを要するため、長文処理がボトルネックとなる。Nyströmformerはこの問題を行列近似の古典的手法「Nyström法」を応用することでO(n)に削減する手法。

【Nyström法の基本原理】行列P（n×n）を全計算せず、m行・m列をサンプリングして4つの部分行列（A_P: m×m、B_P: m×(n-m)、F_P: (n-m)×m、C_P: (n-m)×(n-m)）に分解。未知のC_PをC_P ≈ F_P × A_P⁺ × B_P（A_P⁺はMoore-Penrose疑似逆行列）で推定し、P全体をP̂ = [A_P; F_P] × A_P⁺ × [A_P, B_P]の積として表現する。

【Self-Attentionへの適用上の問題点】Softmax行列Sに直接Nyström法を適用しようとすると、1列をサンプリングするためにその行全体が必要（Softmaxの分母計算のため）となり、直接適用は不可能。

【解決策：ランドマーク選択】クエリQとキーKから「ランドマーク（Nyströmポイント）」Q̃とK̃を構築し、以下の3つの行列を定義する：
- F̃ = softmax(QK̃ᵀ/√d)（n×m）
- Ã = softmax(Q̃K̃ᵀ/√d)⁺（m×m）
- B̃ = softmax(Q̃Kᵀ/√d)（m×n）

Softmax行列の近似はŜ = F̃ÃB̃となり、これにV（値行列）を乗じてAttention出力を得る。このアプローチではQKᵀ（n×n行列）の計算を完全に回避できるため、O(n²)の計算を不要にする。

【ランドマークの構築方法】m行をランダムサンプリングする代わりに「セグメント平均」を使用。n個のトークンをm個のセグメントに分割し、各セグメントの平均ベクトルを計算。実験によればm=32またはm=64個のランドマークで、n=4096〜8192の長シーケンスにおいても標準Self-Attentionや他の効率的Attentionと競合する性能を達成。

【実装詳細】HuggingFaceの実装では、Q・Kをreshapeしてdim=-2方向でmeanを取ることでQ̃・K̃を生成。疑似逆行列の計算にはiterative methodsが使用される。また、値に対して1D depthwise convolutionのスキップ接続が追加されている。

NyströmformerはLong Range Arena等のベンチマークでBigBird、Longformer等と競合する性能を示しており、NLPとCVの両タスクで有効性を確認。

## アイデア

- Softmax行列に直接Nyström法を適用できないという制約を、クエリ・キー空間でのランドマーク選択という迂回路で解決する発想が巧妙。行列近似の数学的枠組みをニューラルネット設計に接続している
- セグメント平均によるランドマーク構築は、ランダムサンプリングより安定した近似を提供し、わずかm=32〜64点で長シーケンス（n=4096）を扱える点が実用的
- 3行列の積Ŝ = F̃ÃB̃という分解は、疑似逆行列Ãをボトルネックとして全体の情報を圧縮・展開するオートエンコーダ的な構造とも解釈でき、情報圧縮の観点からも面白い
## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_1185 HuggingFaceで始めるPatch Time Series Transformer（PatchTST）
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Nyströmformer: Nyström法による線形時間・メモリでのSelf-Attention近似](https://huggingface.co/blog/nystromformer)
