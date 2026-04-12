---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-07
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長コンテキスト, 選択機構, S6, Zero-Order Hold, 並列スキャン, LLM]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [222, 833, 216, 105, 199]
processed_at: "2026-04-07T21:50:23.755941"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアーキテクチャ的限界を克服することを目的としている。Transformerの中核問題はAttention機構のO(n²)時間計算量にあり、シーケンス長が増加するほど推論速度が低下し、KVキャッシュによるO(n)メモリ消費も問題となる。Mambaはこの「二次ボトルネック」を排除し、Transformerと同等の性能を維持しながら最大100万トークンの長コンテキストを線形スケーリングで処理できる。推論速度はTransformerの最大5倍とされる。

Mambaの数学的基盤は制御理論に由来する。連続時間微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) で表される線形SSMを離散化（Zero-Order Hold法）し、行列 A、B、C の各要素を入力xに依存して動的に変化させる「選択機構（Selective SSM / S6）」を導入した点がMambaの核心的な革新である。従来のSSM（S4等）では行列パラメータが入力非依存で固定されており、関連性の低いトークンも均等に記憶してしまう問題があった。Mambaは入力に応じてどの情報を記憶・忘却するかを制御できるため、LSTMのゲート機構に近い表現力を持ちながら並列学習が可能となっている。

ハードウェア面では、GPUのHBMとSRAM間のメモリ帯域幅ボトルネックを回避するために、FlashAttentionと類似した「カーネルフュージョン」と「並列スキャン」を組み合わせたHardware-Aware Algorithmを実装している。学習時は畳み込みとして並列処理し、推論時は逐次的なリカレント演算として実行するデュアルモードが特徴的である。

Mamba-3BはThe Pileベンチマークにおいて同規模のTransformerを上回り、2倍規模のTransformerと同等の性能を示した。音声・ゲノム解析など他モダリティでも有効性が確認されている。一方で、Mambaは状態を固定サイズの隠れ状態に圧縮するため、Transformerのような明示的なコンテキスト参照（全トークンへのアテンション）はできない。これは「記憶の非可逆的圧縮」という根本的トレードオフを意味し、特定タスクでのIn-Context Learningや解釈可能性の観点での課題となりうる。

## アイデア

- 入力依存の選択機構（Selective SSM）により、従来SSMの「全情報を均等記憶」という制約を突破した点。どの情報を隠れ状態に書き込み・忘却するかを動的制御できるのはLSTMゲートとAttentionの中間的な表現力を実現している
- 学習時は畳み込み（並列化可能）、推論時はリカレント演算（定数時間）という二重表現を利用するデュアルモード実装。同一モデルが学習効率と推論効率の両方を最適化できるアーキテクチャ設計として応用範囲が広い
- 隠れ状態は「過去の圧縮」であり、Transformerのように任意の過去トークンを直接参照できない。このトレードオフは解釈可能性（Interpretability）において重要で、モデルが何を「覚えていて何を忘れたか」を追跡する新たな手法が必要になる
## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
