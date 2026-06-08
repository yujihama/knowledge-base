---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-08
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長コンテキスト, 選択的SSM, HiPPO, 線形RNN, S4, FlashAttention]
category: "ai-ml"
related: [2510, 199, 3105, 222, 2480]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-08T09:23:42.431946"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerはトークン間通信にAttentionを使うが、これにより学習時のフォワードパスがO(n²)、自己回帰生成時はO(n)となり、長コンテキストで深刻なメモリ・速度問題を引き起こす。MambaはこのAttentionを制御理論由来のSSMで置き換え、線形スケーリングを実現する。

SSMの核心は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) にあり、隠れ状態hが過去の圧縮表現として機能する。実世界の離散的時間ステップに対応するため、Zero-Order Hold（ZOH）法による離散化を適用し、差分方程式へ変換する。離散化後、SSMは畳み込みとして等価に計算可能になり、並列学習が可能となる。

Mambaの最大の革新は「選択的状態空間モデル（S4の拡張）」である。従来のS4はA・B・Cが入力に依存しない時不変（LTI）システムだったが、Mambaはこれらを入力依存にした（Selective SSM）。これにより、どの情報を状態に保持し、どれを忘れるかをコンテキストに応じて動的に制御できる。LSTMのゲート機構に近い概念だが、線形RNNの形で実装される点が異なる。ただし、この選択性によりハードウェア効率の高い畳み込み計算が使えなくなるという問題を、FlashAttentionに着想を得たカーネルフュージョン技術（HiPPO行列の活用を含む）で解決している。

パフォーマンス面では、Mamba-3BはThe Pile評価において同パラメータ数のTransformerを上回り、2倍サイズのTransformerと同等の結果を示す。推論速度はTransformer比で最大5倍高速であり、100万トークン規模のコンテキストでも線形計算量を維持する。言語・音声・ゲノミクスなど複数モダリティでSOTAを達成している。

解釈可能性の観点では、隠れ状態hが過去全体の有限次元圧縮であるため、Transformerより内部状態の追跡が理論上容易だが、実際の解釈はまだ発展途上。AIセーフティの文脈では、Mambaのような非Transformerアーキテクチャが将来の主流になる可能性があり、解釈可能性研究のTransformer依存が課題となりうる点が指摘されている。監査エージェント開発への示唆としては、長文書・長履歴を扱う監査シナリオ（大量の過去トランザクションログや規制文書の一括処理）において、Mambaの線形計算量と高速推論は実用上の大きな優位性となる可能性がある。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能するという概念は、RNNのセル状態と似ているが、連続時間微分方程式から導出される点が数学的に洗練されており、HiPPO行列による直交多項式基底への射影で長期記憶を保証している
- 選択的SSM（入力依存のB・C行列）により情報の選択的保持・忘却が可能になるが、これによってハードウェア効率の高い畳み込み計算が使えなくなるというトレードオフをカーネルフュージョンで解決した設計の巧妙さ
- Mambaは推論時はRNNとして動作（O(1)ステップ）、学習時は畳み込みとして並列動作という二重性を持つため、Transformerの並列学習効率とRNNの推論効率を両立している点が実用上のブレークスルー

## 前提知識

- **Transformer/Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込み計算** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
