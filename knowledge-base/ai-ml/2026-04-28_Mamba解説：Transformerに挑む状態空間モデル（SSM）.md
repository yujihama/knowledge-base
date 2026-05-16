---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-28
tags: [Mamba, SSM, State Space Model, Transformer代替, Selection Mechanism, Hardware-Aware Scan, 線形計算量, 長文脈]
category: "ai-ml"
related: [2480, 2510, 3105, 222, 833]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-28T12:15:22.440292"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerではすべてのトークンが過去の全トークンを参照するKVキャッシュ機構のため、学習時にO(n²)の計算量、推論時にO(n)の時間とO(n)のメモリが必要となる。Mambaはこれをゼロオーダーホールド（ZOH）離散化を用いたSSMに置き換えることで、系列長に対して線形（O(n)）の計算量を実現している。

SSMの基本方程式は連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、「状態 h」が過去の情報を圧縮して保持するマルコフ的な構造をとる。これを離散化すると漸化式 h_t = Ā h_{t-1} + B̄ x_t となり、RNNに類似した再帰的な推論が可能になる一方、学習時は畳み込みカーネルとして並列処理もできる（双対性）。

SSMの古典的な問題として「選択性の欠如」がある。従来のSSMでは行列A・B・CがInput非依存の定数であるため、どのトークン情報を保持・破棄すべきかを文脈に応じて制御できなかった。MambaはこれをSelection Mechanismで解決し、B・C・Δ（タイムステップ）をInput依存にすることで、重要な情報を状態に保持し不要な情報を忘却する選択的フィルタリングを実現する。

ハードウェア最適化としてHardware-Aware Selective Scanを採用し、中間状態をGPUのSRAM上で処理することでHBMへのメモリ転送を削減、FlashAttentionと同様のカーネル融合アプローチをとる。Mambaブロックはアテンション+MLPのTransformerブロックと同等の役割を果たし、SSMが系列間の「通信」、MLPスタイルの射影が「計算」を担う。

Mamba-3Bは同サイズのTransformerと同等かそれ以上、かつ2倍サイズのTransformerに匹敵する性能を言語・音声・ゲノムの各モダリティで示した。推論速度はTransformer比最大5倍高速で、100万トークンの超長文脈においてもスケールする。

ただし課題もある。In-Context Learningにおいてはアテンション機構を持たないため苦手な傾向があり、「状態」の有限圧縮により特定情報の正確な想起が難しい場合がある。また解釈可能性（Interpretability）の観点では、Transformerのアテンションヘッドが持つ「サーキット」的な分析手法がSSMには直接適用できず、新たな解釈フレームワークの開発が必要とされる。監査エージェント開発への示唆としては、長い監査ログや規制文書（100万トークン規模）を低メモリ・低レイテンシで処理する基盤モデルとして、Mambaアーキテクチャが有力な選択肢となりうる。

## アイデア

- SSMの学習時は畳み込み、推論時は再帰（RNN的）として動作できる双対性が、並列学習と低レイテンシ推論を両立させる鍵であり、アーキテクチャ設計の柔軟性として参考になる
- Selection MechanismでΔ（タイムステップ幅）をInput依存にすることが、事実上「このトークンをどれだけ重視するか」の制御になっており、Attentionとは異なる形の選択性実現のアイデアが興味深い
- 解釈可能性の問題：TransformerのAttention weightやサーキット分析がそのまま使えないため、SSMの内部状態 h をどう可視化・分析するかという新たな研究課題が生まれており、LLM-as-judgeや監査ログ分析ツールの設計に影響しうる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN** → /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **畳み込みニューラルネット** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
