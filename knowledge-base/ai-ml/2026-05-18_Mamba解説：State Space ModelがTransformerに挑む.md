---
title: "Mamba解説：State Space ModelがTransformerに挑む"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-18
tags: [Mamba, SSM, State Space Model, Selective SSM, S6, Transformer, 線形スケーリング, 長文脈, parallel scan, 離散化]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-18T09:20:54.262027"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つO(n²)の計算量ボトルネックを解消することを目的としている。Transformerはトークン間の全対全通信（KVキャッシュ）により、長いシーケンスになるほど推論が遅くなり、メモリ消費も増大する。Mambaはこれに対し、制御理論に由来する状態空間モデルをアテンションの代替として採用し、O(n)の線形スケーリングを実現する。

SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される。隠れ状態h(t)が「過去の圧縮」として機能し、新しい観測x(t)と組み合わせることで出力y(t)を予測する。実装上は離散化（Zero-Order Hold法）によりこれを差分方程式に変換し、コンピュータ上で扱えるようにする。

Mambaの最大の革新は「選択的状態空間モデル（Selective SSM / S6）」である。従来のSSM（例：S4）では行列A, B, Cが入力に依存しない固定値だったため、関連情報と無関係な情報を選別できなかった。MambaではB, C, ∆（タイムステップサイズ）を入力x_tの関数とすることで、コンテキストに応じて「何を記憶し何を忘れるか」を動的に制御できる。これはTransformerのQKV行列が入力依存であることと類似した設計思想を持つ。

ハードウェア最適化の観点では、S6は並行スキャン（parallel scan）によりGPU上でCUDA並列計算を活用しつつ、FlashAttentionと同様に中間結果をHBMではなくSRAM（shared memory）上で管理することで高速化を実現している。推論速度はTransformerの最大5倍、メモリ使用量も大幅に削減される。

Mamba-3Bモデルは同サイズのTransformerと同等以上の性能を示し、The Pileベンチマークでは2倍サイズのTransformerに匹敵するとされる。言語・音声・ゲノム解析など複数モダリティでSoTAを達成している。100万トークン規模のコンテキストも現実的に扱える点が大きな差別化要素となる。

解釈可能性・AIセーフティの観点では、Mambaの隠れ状態は固定サイズであり、Transformerのアテンションパターンに相当するような内部状態の可視化・解析が難しく、これが今後の課題とされる。監査エージェント開発への示唆としては、長大なログやドキュメントシーケンスを扱うタスクにおいてMambaベースのアーキテクチャが有効な選択肢となり得る点、また線形メモリ消費の特性からエッジ・オンプレミス環境でのLLM推論コスト削減にも応用できる点が挙げられる。

## アイデア

- 隠れ状態を「過去の圧縮」と位置づけることで、固定サイズメモリによる無限長コンテキストの近似を実現している点——これはLSTMとTransformerの中間的な設計思想であり、RNN系モデルの再評価につながる
- B, C, ∆を入力依存にする『選択的』機構がMamba最大の革新であり、「コンテキストに応じて忘却率を変える動的ゲーティング」として捉えると、LSTM/GRUのゲート機構をより洗練させたものとも解釈できる
- 並行スキャン（parallel scan）によりRNN的な逐次依存構造をGPU並列計算で処理する手法は、SSMを実用的なLLMバックボーンにする上での核心的エンジニアリングであり、同様のアプローチが他の逐次モデルにも応用可能

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **離散化（Zero-Order Hold）** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：State Space ModelがTransformerに挑む](https://thegradient.pub/mamba-explained/)
