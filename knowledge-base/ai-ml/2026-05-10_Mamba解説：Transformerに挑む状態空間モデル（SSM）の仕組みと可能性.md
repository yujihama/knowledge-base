---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-10
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, Selective SSM, Zero-Order Hold, 長文脈処理, シーケンスモデル]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-10T12:42:08.006146"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルであり、Transformerのアテンション機構が持つO(n²)の計算複雑性（二次ボトルネック）を回避しながら、同等以上の性能を実現する。Mamba-3BはThe Pileベンチマークにおいて同サイズのTransformerを上回り、2倍サイズのTransformerと同等のスコアを記録。推論速度はTransformerと比較して最大5倍高速で、シーケンス長に対して線形スケーリング（O(n)）を達成する。

技術的な核心は、制御理論に由来する連続時間状態空間方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) の離散化（Zero-Order Hold法）にある。過去の情報を固定サイズの隠れ状態hに圧縮し、新しい観測xとともに次状態を更新するRecurrentな構造を持つため、推論時はRNNのようにO(1)メモリで動作する。訓練時は畳み込み演算として並列処理可能であり、RNNの推論効率とTransformerの訓練効率を両立する。

Mambaの最大の革新はSelective SSM（S6）と呼ばれる入力依存のパラメータ選択機構にある。従来のSSMはパラメータA・B・Cが固定であったが、MambaではB・C・Δ（時間刻み幅）を入力xから動的に生成する。これによりモデルが「どの情報を状態に保持し、どれを忘れるか」を文脈に応じて選択できる。たとえば文法的に重要な主語は記憶し、不要な虚辞は無視するといった柔軟な処理が可能となる。

ハードウェア最適化の観点では、中間状態をHBM（高帯域幅メモリ）ではなくSRAM（高速キャッシュ）上で処理するカーネルフュージョンを採用し、FlashAttentionと類似のアプローチでメモリ転送コストを削減している。

Mamba Blockの構造はTransformer BlockのAttentionをSSMに置換し、MLPによる計算パスと組み合わせたものである。Mamba2ではSSMとアテンションを統合したState Space Dualityが導入され、理論的な統合が進んでいる。

解釈可能性の観点では、Transformerのアテンションマップのような直接的な可視化ツールがなく、固定サイズ隠れ状態への情報圧縮がどう機能するかの理解は発展途上。監査エージェント開発への示唆としては、長大なログや監査証跡（100万トークン超）を低コストで処理できるバックボーンとして有望であり、LangGraph等のエージェントフレームワークとの組み合わせで長期記憶が必要なタスクへの応用が期待できる。

## アイデア

- Selective SSM（S6）における入力依存パラメータ生成は、LSTMのゲート機構を連続時間制御理論の枠組みで再解釈したものであり、「何を記憶すべきか」の判断をデータドリブンに学習できる点が根本的に新しい
- 訓練時は畳み込み（並列）、推論時はリカレント（逐次）として同一モデルが動作する二重性は、Transformerが持つKVキャッシュのメモリ肥大問題を回避しつつスケーリングを維持する実用上の鍵となっている
- 100万トークン規模の長文脈をO(n)で処理可能という性質は、長期監査ログ・規制文書・複数期にわたる財務データのような監査ドメイン固有の長大シーケンスを扱うエージェントアーキテクチャに直接応用できる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
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

[Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性](https://thegradient.pub/mamba-explained/)
