---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-15
tags: [Mamba, SSM, 状態空間モデル, 選択的SSM, S6, 線形スケーリング, 長コンテキスト, 離散化, ZOH, 並列スキャン]
category: "ai-ml"
related: [2510, 222, 2480, 1837, 3105]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-15T09:20:23.495638"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttentionが持つ二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時O(n²)の計算量とO(n)のKVキャッシュメモリが必要だが、MambaはSSMを用いてこれを線形スケーリングに抑える。

SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される。ここでhは隠れ状態（過去の圧縮表現）、xは入力、yは出力。実装では離散化（Zero-Order Hold法）を適用し、差分方程式 h_t = Āh_{t-1} + B̄x_t、y_t = Ch_t に変換する。

Mambaの最大の革新点は「選択的SSM（S6）」で、パラメータB・C・Δをトークンごとに入力依存で変化させる点にある。従来のS4ではA・B・C・Δが時間不変（LTIシステム）だったため、各トークンを等しく扱うしかなかった。選択的メカニズムにより、関連性の高い情報は長く保持し、無関係な情報は忘却するという動的なフィルタリングが可能になる。

アーキテクチャ的には、TransformerブロックのAttentionをMambaブロック（SSM）に置き換えた構成で、Mambaブロックは拡張線形層→1D畳み込み→SiLU活性化→SSM→ゲーティングの流れを持つ。計算上の工夫として、並列スキャン（並列プレフィックス和）を使い学習時にO(n log n)で実行し、推論時はRNNスタイルで逐次実行してO(1)メモリで処理する。さらにHardware-Aware Algorithmによりフラッシュメモリ（HBM）とSRAM間のデータ転送を最適化している。

Mamba-3Bモデルは同規模Transformerを上回り、2倍規模のTransformerと同等性能をThe Pile上で達成。推論速度はTransformerの最大5倍。ただし、Transformerの数百億〜数千億パラメータ規模と比較するとまだ小規模であり、実世界の大規模検証はこれから。

解釈可能性・安全性の観点では、InductionHeadsのようなTransformerで発見されたサーキット相当の概念がMambaに存在するか未解明。また線形再帰の性質上、「どの過去情報を保持しているか」の分析手法がAttentionの重み可視化とは根本的に異なる。監査AIへの示唆として、長文書（契約書・監査調書等）を低コストで処理できる可能性があるが、現時点で大規模な実績は限定的。

## アイデア

- 隠れ状態を『過去の圧縮』と位置づける設計思想：RNNとTransformerの中間として、固定サイズの隠れ状態で無限長の過去を近似するトレードオフが、どのタスクで破綻するかを実験的に検証できる
- 入力依存パラメータ（選択的SSM）によるソフトな記憶管理：B・C・Δを動的に変化させることで「何を忘れるか」を学習させるアプローチは、RAGのチャンク戦略とは対照的なエンドツーエンド記憶圧縮の可能性を示す
- 並列スキャンによる学習高速化と推論時RNNの二面性：同一モデルを学習時はO(n log n)並列、推論時はO(1)メモリで動かせる設計は、エッジデバイスや長期会話エージェントへの展開で実用的優位性を持つ

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN** → /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
