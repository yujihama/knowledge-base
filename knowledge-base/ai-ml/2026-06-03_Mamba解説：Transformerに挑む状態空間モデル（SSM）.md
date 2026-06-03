---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-03
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 選択的SSM, 並列スキャン, 線形スケーリング, 長コンテキスト]
category: "ai-ml"
related: [2510, 222, 2480, 1837, 3105]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-03T09:24:21.535318"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttentionメカニズムが抱える二次計算量（O(n²)）のボトルネックを解消することを目的としている。

Transformerの問題点として、Attentionでは全トークン間のペアワイズ通信を行うため訓練時にO(n²)の時間計算量が発生し、KVキャッシュもO(n)のメモリを消費する。コンテキスト長が伸びるにつれて速度低下とOOMエラーのリスクが増大する。FlashAttentionやSliding Window Attentionなどの緩和策はあるが、百万トークン超の超長コンテキストには根本的な代替手法が必要とされる。

MambaのSSMは制御理論に基づく連続時間微分方程式（h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)）を離散化して実装する。状態hは「過去の圧縮」であり、新しい観測xと組み合わせることで次の出力yを決定する。離散化にはZero-Order Hold（ZOH）を使用し、実際のシーケンス処理に対応させる。

SSMの重要な特性として、訓練時は畳み込み（convolution）として並列計算でき効率的であり、推論時はリカレント（RNN的）な形式で逐次処理できる二面性がある。これにより訓練効率と推論時のO(1)メモリ効率を両立する。

Mambaの核心的イノベーションは「選択的状態空間モデル（Selective SSM / S6）」である。従来のSSMはパラメータA、B、Cが入力に依存しない線形時不変（LTI）であり、入力を選択的に無視できないという欠点があった。MambaではB、C、ステップサイズΔを入力xの関数とし、どの情報を状態に取り込み何を忘れるかを動的に制御できる。これによりInduction HeadのようなContext-dependentなタスクにも対応可能となった。

実装面ではハードウェアを意識した「並列スキャン」アルゴリズムとHBMとSRAM間のデータ転送を最適化するFlash Mamba（カーネルフュージョン）を採用し、Transformerより最大5倍高速な推論を実現する。

性能面ではMamba-3Bが同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する事前学習・下流タスク評価結果を示している。言語・音声・ゲノミクスなど複数モダリティでSOTAを達成した。

ただし欠点もあり、Retrievalタスク（特定トークンの正確な再現）やIn-context Learningの一部タスクではTransformerに劣る傾向がある。これは固定サイズの状態hへの情報圧縮に起因し、解釈可能性研究においてもKVキャッシュのような明示的なアテンションパターンがないため分析が難しい。監査エージェント開発への示唆として、長期ログ・監査証跡の処理においてMambaの線形スケーリング特性は大規模監査データの逐次処理に有効だが、特定エビデンスの正確な参照が求められる場面ではTransformerとのハイブリッド構成（Jamba等）が現実的な選択肢となる。

## アイデア

- SSMは訓練時はConvolution、推論時はRNNとして動作する二面性を持ち、同一モデルで訓練効率と推論メモリ効率を両立できる設計が巧妙
- 「選択的」SSMによりB・C・Δを入力依存にすることで、固定フィルタの限界（入力無視不可）を克服し、コンテキスト依存の情報選択をO(n)で実現した点
- 状態hを「過去の圧縮」と定義することで固定サイズメモリへの凝縮が可能になるが、これはRetrievalタスクの弱点とも表裏一体であり、RNNと同様のトレードオフが依然として存在する

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **畳み込みニューラルネット（CNN）** (TODO: 読むべき)
- **制御理論・状態空間表現** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
