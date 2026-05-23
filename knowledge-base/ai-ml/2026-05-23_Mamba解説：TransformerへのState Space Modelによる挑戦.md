---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-23
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, HiPPO, S6, 선택적注意機構, 線形スケーリング, シーケンスモデル]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-23T21:10:46.293565"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを克服することを目的とする。Transformerは全トークン間のAttention計算によりO(n²)の時間計算量とO(n)のKVキャッシュメモリを必要とするため、長文脈（例：100万トークン）では実用的でない。Mambaはこの問題を制御理論由来のSSMで代替する。

SSMの基本式は h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) という連続時間微分方程式で表され、隠れ状態hが過去の情報を圧縮して保持する。連続時間を離散化するためにZero-Order Hold（ZOH）法を用い、バッチ学習時はコンボリューション演算で並列化、推論時はRNN的な逐次処理で動作する。これによりトレーニング効率と推論効率を両立している。

Mambaの核心的な革新はS6（Selective State Space）機構にある。従来のSSM（S4等）は行列A, B, Cが入力に依存しない線形時不変（LTI）システムだったため、選択的な情報フィルタリングができなかった。MambaではB, Cおよびタイムステップ幅Δを入力xの関数として学習させることで、どの情報を隠れ状態に残すか・捨てるかを動的に制御できるようにした。これはTransformerのAttentionが各トークンペアの関連性を動的に計算するメカニズムと概念的に対応する。

ハードウェア実装では、HiPPO行列による初期化でA行列の構造を制約し、Δのスキャン演算をGPUのSRAM上でフュージョンすることで、理論上は遅くなるはずの選択的SSMを高速化するHardware-Aware Algorithmを実現した。

ベンチマークでは、Mamba-3BがThe Pile上でTransformer同サイズを上回り、2倍サイズのTransformerに匹敵する性能を示した。推論速度はTransformerの最大5倍速い。一方で、Mambaは固定サイズの隠れ状態に情報を圧縮するため、in-context learningや逆順情報取得（「5トークン前の単語は？」等）が苦手という弱点も指摘されている。解釈可能性の観点では、Transformerと異なり特定トークンへの注意可視化が困難で、メカニスティック解釈手法の再設計が必要になる。監査エージェントへの応用としては、長大な監査ログや契約書の全文処理において、Transformerのメモリ制約を回避できる点が重要な示唆となる。

## アイデア

- 隠れ状態hが過去の全トークンの圧縮表現として機能するため、理論上は無限の文脈長を有限メモリで扱えるが、その圧縮による情報損失が逆順アクセスや正確なin-context retrievalの弱点につながる点は、RAGシステム設計のトレードオフと同質の問題
- B, C, Δを入力依存にする「選択性」の導入が鍵で、これにより定数係数の線形RNNからTransformerのAttentionに近い表現力を得ながら、計算量はO(n)のまま維持するという設計上の妙がある
- Train時はConvolution、Inference時はRNNとして動作するデュアルモード設計は、エージェントのバッチ学習と逐次推論を同一アーキテクチャで効率化できる可能性を示しており、監査エージェントのリアルタイム判断処理に応用できる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model (S4)** (TODO: 読むべき)
- **畳み込み演算** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
