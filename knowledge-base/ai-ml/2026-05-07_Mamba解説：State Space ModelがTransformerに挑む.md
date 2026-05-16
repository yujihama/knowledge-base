---
title: "Mamba解説：State Space ModelがTransformerに挑む"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-07
tags: [Mamba, SSM, State Space Model, Transformer, 線形スケーリング, 選択機構, Selective SSM, 長文コンテキスト, LTI, Parallel Scan]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-07T09:22:53.254640"
---

## 要約

MambaはGu and Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算量の問題を解決する。Transformerのアテンション機構はすべてのトークン間のペア通信を行うため、学習時のforward passがO(n²)、推論時の各トークン生成がO(n)の時間計算量を持つ。さらにKVキャッシュによりO(n)の空間計算量も必要で、長文コンテキスト（例：100万トークン）では現実的に動作しない。Mambaはこの「二次ボトルネック」を除去し、シーケンス長に対して線形スケーリングを実現する。

Mambaの中核はSSMであり、制御理論に基づく連続時間微分方程式h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)を離散化（Zero-Order Hold法）して実装する。状態hは過去の情報の圧縮であり、マルコフ決定過程として定式化される。古典的なSSMはA, B, C行列が入力に依存しない時不変（Linear Time Invariant）であったが、これは「選択的」な情報フィルタリングができないという限界があった。

Mambaの最大の革新は「選択機構（Selective State Space）」の導入で、入力xに基づいてB, C, Δパラメータを動的に変化させる。これにより、モデルは関連情報を状態に取り込み、無関連情報を無視する能力を持つ。たとえば「The cat sat on the mat. It was a...'」でItが何を指すかを判断する際、catという情報を選択的に保持できる。

ハードウェア効率のため「Parallel Scan」アルゴリズムを採用し、GPU上でのカーネルフュージョンにより計算を高速化。Training時は並列処理（畳み込みモード）、Inference時はRNNスタイルの逐次処理を切り替えることで、TransformerのFlashAttentionに相当する最適化を実現する。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能を示す。推論速度はTransformerの最大5倍速く、コンテキスト長が増えても推論速度が低下しない。言語・音声・ゲノミクスなど複数モダリティでstate-of-the-art性能を達成。

解釈可能性の観点では、Mambaの固定サイズ状態が「情報の圧縮点」であることから、Transformerのアテンション分析とは異なるアプローチが必要。AI安全性の文脈では、過去の圧縮方法が信頼性・バイアスに影響する可能性がある。監査AIへの応用としては、監査ログや契約書など長大なドキュメントの処理においてTransformerより効率的な処理が期待できる。

## アイデア

- 選択機構（Selective State Space）により、入力依存でB/C/Δを動的変化させる点が古典的LTI-SSMとの本質的差異で、これによりRNNの高速性とTransformerの表現力を両立する
- Training時は並列畳み込み・Inference時はRNN逐次処理というデュアルモード動作により、同一モデルで学習効率と推論効率を同時に最適化できるアーキテクチャ設計が巧妙
- 固定サイズ状態による過去情報の圧縮は、Transformerの「全履歴参照」に対するトレードオフであり、何を覚え何を忘れるかの選択メカニズムがモデルの品質を左右する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **制御理論・微分方程式** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：State Space ModelがTransformerに挑む](https://thegradient.pub/mamba-explained/)
