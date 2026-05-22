---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-22
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, 選択的SSM, ハードウェア効率化, 長文脈処理]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-22T21:16:47.665282"
---

## 要約

Mambaは、Albert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttention機構が持つ二次計算量ボトルネックを解消することを目的として設計された。Transformerでは全トークン間のペアワイズAttentionによりトレーニング時O(n²)の時間計算量、KVキャッシュによるO(n)の空間計算量が生じるが、Mambaはこれをシーケンス長に対して線形な計算量で置き換える。Mamba-3BモデルはThe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能を示し、推論速度はTransformerの最大5倍とされる。

Mambaの核心はSSMであり、制御理論に由来する連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) をベースとする。状態hは過去の情報を圧縮した表現であり、新しい入力xと組み合わせて次の出力yを予測する。この連続時間方程式は、Zero-Order Hold（ZOH）離散化によってh_{t+1} = Āh_t + B̄x_t という差分方程式に変換され、実際のシーケンス処理に適用される。

SSMは畳み込みとしても解釈でき、トレーニング時は並列畳み込みで高速化し、推論時はRNN的な逐次計算で定数サイズの状態を維持する。この二重の計算形態がMambaの効率性の源泉となっている。

従来のSSM（S4等）との最大の差別化点は「選択的状態空間（Selective SSM / S6）」にある。従来モデルではパラメータB, C, Δが入力に依存せず固定であったが、MambaはこれらをSequence-Dependent（入力依存）にすることでコンテキストフィルタリング能力を獲得した。これによりモデルは関連トークンの情報を選択的に保持・忘却できる。この選択性のためにパラメータ行列の並列スキャンが直接利用できなくなる課題に対し、著者らはHardware-Aware Parallel Scan（並列プレフィックススキャン＋カーネルフュージョン）をGPU SRAM上で実装することで高速化を実現した。

解釈可能性の観点では、Mambaの状態hはTransformerのKVキャッシュより情報が圧縮されており、メカニスティック解釈が困難になる可能性がある。一方、入力依存パラメータによりInduction Headに相当するメカニズムが実装可能であることも示されている。監査エージェント開発への示唆として、長文書（契約書、財務報告書等）を低メモリ・高速に処理するバックボーンとしてMambaアーキテクチャは有望であり、百万トークン規模のコンテキストを扱うRAGシステムや長期対話エージェントへの応用が期待される。

## アイデア

- SSMの選択的パラメータ化（S6）は、Transformerのソフトアテンションとは異なる「入力依存のゲーティング」として解釈でき、どの情報を状態に書き込むか・忘却するかをモデルが学習できる点が構造的に新しい
- トレーニング時は並列畳み込み、推論時はRNN的な定数サイズ状態更新という二重計算モードの切り替えは、エージェントの長期メモリ設計（外部ストレージ不要の圧縮状態）に直接応用できるアーキテクチャパターン
- MambaはゲノミクスやオーディオなどTransformerが苦手とする超長シーケンスドメインでSoTAを達成しており、監査ログや時系列財務データのような長期依存性を持つシーケンシャルデータ処理への適性が高い

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **Zero-Order Hold離散化** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
