---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-07
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形複雑度, 選択的状態空間, S4, Zero-Order Hold, 長文脈処理, 並列スキャン]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-07T09:38:55.602089"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算コストの問題を線形複雑度で解決する。Transformerはトークン間の通信にアテンションを使うため、学習時はO(n²)、推論時はO(n)の時間計算量となり、KVキャッシュのO(n)メモリも必要とする。Mambaはこれをコントロール理論由来のSSMで置き換え、推論時はO(1)のメモリと時間で動作する。

Mambaの中核はh'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)という連続時間微分方程式で、入力x、隠れ状態h、出力yの関係を定義する。実装上はZero-Order Hold（ZOH）離散化によりΔ（タイムステップ）を介して差分方程式に変換する。Mamba-3Bは同サイズのTransformerと同等、かつ2倍サイズのTransformerに匹敵するThe Pile上の性能を示し、推論速度はTransformerの最大5倍とされる。

従来のSSM（S4等）との最大の違いは「選択的状態空間（Selective SSM / S6）」の導入にある。S4まではA・B・Cが入力に依存しない固定パラメータだったため、各トークンに等しく注意を払う「情報圧縮の均等性」という問題があった。MambaではB・C・Δを入力依存（input-dependent）にすることで、重要なトークンは長く記憶し、無関係なトークンは忘れる選択的フィルタリングが可能になる。これはRNNにおける「ゲーティング」に相当する機能をSSMに組み込んだ形だ。

ハードウェア面ではParallel Associative Scan（並列スキャン）を活用して学習を高速化し、FlashAttentionに類比されるカーネル融合（kernel fusion）でGPUのHBM-SRAM間のメモリ転送を最小化する。これによりSSMが本来持つ逐次依存性に起因する学習の遅さを克服している。

アーキテクチャ的にはMambaブロック1つに2系統の射影があり、一方はSSMに通し、もう一方はSiLU活性化を通じたゲートとして機能する。またMambaはアテンションを完全に除去しているため、in-context learningや複雑なコピータスクで弱さが指摘されており、MambaByte、Vision Mamba、Jamba（Mamba+Transformer混合）など後続研究での補完が続いている。

解釈可能性・安全性の観点では、RNN的な内部表現を持つMambaはTransformerより解析が難しく、回路的解釈（mechanistic interpretability）の手法がそのまま適用できない課題がある。監査エージェント開発への示唆としては、長大な監査ログや規制文書など超長文脈（100万トークン超）の効率的処理が必要なシナリオで、Transformerベースより低レイテンシ・低メモリのバックボーンとして有望であり、エッジデプロイや低コスト推論基盤の選択肢となり得る。

## アイデア

- B・C・Δを入力依存にする「選択的SSM」の設計思想は、RNNのLSTMゲートに相当する機能をSSMに持ち込んだ統一的解釈で、どのトークンを圧縮し何を捨てるかをモデル自身が学習する点が面白い
- 推論時はRNN的なO(1)状態更新、学習時はCNN的な並列スキャンで計算するという二重の計算グラフを持つ点で、訓練と推論で全く異なる計算パスを使う珍しいアーキテクチャ設計になっている
- Transformerのアテンションが「無制限の完全記憶」であるのに対し、MambaのSSMは「有限サイズの圧縮記憶」であるため、情報を選択的に捨てる能力がモデルのパフォーマンスに直結するという構造的なトレードオフが、解釈可能性研究の新たな問いを生んでいる

## 前提知識

- **Transformer・アテンション機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
