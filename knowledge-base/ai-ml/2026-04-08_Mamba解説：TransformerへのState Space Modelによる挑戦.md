---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-08
tags: [Mamba, SSM, State Space Model, Transformer, 線形スケーリング, Selective State Space, ZOH離散化, 長コンテキスト, RNN, Parallel Scan]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [222, 201, 199, 833, 255]
processed_at: "2026-04-08T21:00:39.423791"
---

## 要約

MambaはGu・Dao両氏が開発したState Space Model（SSM）ベースのアーキテクチャで、Transformerの二次計算量ボトルネックを線形スケーリングで解決する。Transformerの注意機構はトークン間のpairwise通信のためにO(n²)の学習計算量とO(n)のKVキャッシュメモリを要するが、Mambaはこれを連続時間微分方程式h'(t)=Ah(t)+Bx(t)とy(t)=Ch(t)+Dx(t)で表される状態空間モデルに置き換える。この「隠れ状態h」が過去の情報を圧縮・保持し、新しい入力xとの組み合わせで次の出力yを予測する。連続時間式はZero-Order Hold（ZOH）離散化により差分方程式h_{t+1}=Āh_t+B̄x_tへ変換され、実際のシーケンス処理に適用される。Mambaの最大の革新は「Selective State Space」、すなわち入力依存の選択的ゲーティングにあり、A・B・Cパラメータをスカラー選択機構Δで動的に調整することで、関連情報のみを状態に保持する能力を持つ。従来SSMの線形時間不変（LTI）の制約を超え、コンテンツに応じた状態更新が可能になった。実装上はParallel Associative Scanを活用して訓練時の並列計算を実現し、推論時はRNNのような逐次処理で定常メモリを維持する。ベンチマーク結果では、Mamba-3BはThe Pile上で同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵するperplexityを達成。推論速度はTransformerと比較して最大5倍高速。コンテキスト長100万トークンまでスケール可能であることも実証されている。一方で限界も存在する。Selective Stateは固定サイズであるため、理論上は過去の無限の情報を保持できず、Transformerの完全なattentionが持つ「完璧な記憶」とのトレードオフがある。また、Mamba内部の隠れ状態の解釈性はTransformerのAttention Weightと比較して困難であり、Mechanistic Interpretabilityの観点では研究途上である。マルチモーダル応用（言語・音声・ゲノム）での有効性も示されており、長文書処理やリアルタイムシーケンス処理を必要とするドメインで注目されている。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能する設計思想は、監査エージェントが長大な監査証跡を扱う際のメモリ効率設計に直接応用できる概念
- 入力依存の選択的ゲーティング（Selective SSM）は、どの情報を記憶・忘却するかを動的に決定するメカニズムで、人間の認知の「注意の選択性」を数学的に模倣している
- 訓練時はConvolution（並列）・推論時はRNN（逐次）という二重性により、同一モデルで学習効率と推論効率を両立させる設計は、Transformerには存在しない独自のトレードオフ解決策
## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
