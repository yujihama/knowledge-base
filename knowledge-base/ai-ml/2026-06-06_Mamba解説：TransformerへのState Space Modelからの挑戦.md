---
title: "Mamba解説：TransformerへのState Space Modelからの挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-06
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈処理, 線形スケーリング, 選択的状態空間, ZOH離散化, LLM]
category: "ai-ml"
related: [3105, 7117, 833, 216, 2480]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-06T21:33:57.281314"
---

## 要約

MambaはGu・Daoによって開発されたState Space Model（SSM）ベースの言語モデルアーキテクチャで、Transformerが抱える二次計算量の問題を根本的に解決することを目指している。Transformerは全トークン間のAttentionを計算するため訓練時にO(n²)の時間複雑度、推論時にO(n)のKVキャッシュ空間を必要とし、長文脈（100万トークン規模）では現実的に機能しない。Mambaはこの「二次ボトルネック」を取り除き、系列長に対して線形スケーリングを実現する。

Mambaの核心はSSMの数式にある。連続時間の状態空間方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を離散化（Zero-Order Hold法）し、h_{t+1} = Āh_t + B̄x_t、y_t = Ch_t + Dx_t として実装する。ここで隠れ状態hは「過去の圧縮」であり、Transformerのように全過去トークンを明示的に参照する必要がない。これによりRNNと同様の逐次推論が可能となる。

従来のSSM（S4等）が固定パラメータA・B・Cを使用するのに対し、Mambaの最大の革新は「選択的状態空間モデル」と呼ばれる入力依存パラメータ化にある。B・C・Δを入力x_tの関数とすることで、どの情報を状態に保持し何を無視するかをモデルが動的に制御できる。これはAttentionの「動的コンテキスト依存フィルタリング」に相当する能力をRNN的な計算コストで実現する。

訓練時は畳み込み（FFT活用）で並列化し、推論時はRNNモードで逐次処理する二重実装により、訓練効率と推論速度の両立を図る。さらにFlashAttentionに着想を得たハードウェア対応アルゴリズムとカーネルフュージョンにより、A100 GPU上でTransformerより最大5倍高速な推論を実現している。Mamba-3Bモデルはthe Pile評価において同規模Transformerを上回り、2倍規模のTransformerに匹敵する性能を示す。

MambaブロックはTransformerブロックと同様にスタック構造を取り、Attention（通信）をSSMに置き換えMLP（計算）を保持する。解釈可能性・AIセーフティの観点では、RNN的な圧縮された隠れ状態が内部表現の解析を困難にする可能性がある一方、選択機構の分析が新たな解釈手法を要求する。監査エージェント開発への示唆としては、長文書（監査報告書・規制文書）を100万トークン規模で処理する際のバックボーンアーキテクチャ選択肢として、Mambaは計算コスト削減の有力候補となる。

## アイデア

- 訓練時は畳み込み（並列）・推論時はRNN（逐次）という二重モードの実装により、TransformerのO(n²)訓練コストとRNNの逐次推論速度の両方を同時に達成している点が構造的に独創的
- B・C・Δを入力依存にする「選択機構」がSSMの本質的弱点（固定フィルタ）を克服し、Attention的な動的文脈選択をO(n)コストで近似する発想は、エージェントの長期記憶設計にも応用可能
- 隠れ状態hを「過去の圧縮」と定式化する点はマルコフ決定過程の状態定義と一致しており、強化学習ベースのエージェント（ReAct等）の状態表現設計と概念的に接続できる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **State Space Model（S4）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析

## 原文リンク

[Mamba解説：TransformerへのState Space Modelからの挑戦](https://thegradient.pub/mamba-explained/)
