---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-23
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈処理, 線形スケーリング, 選択的状態空間, Selective SSM, Zero-Order Hold, Parallel Scan]
category: "ai-ml"
related: [2480, 2510, 1975, 199, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-23T12:45:52.194176"
---

## 要約

MambaはGu・Daoらが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時にO(n²)の時間計算量が発生し、KVキャッシュのO(n)空間消費と合わせて長文脈処理が実質的に困難だった。Mambaはこれに対し、制御理論に由来する連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を離散化（Zero-Order Hold法）して再帰的な差分方程式として適用する。過去の情報を固定サイズの隠れ状態hに圧縮することで、推論時はO(1)空間・O(n)時間の線形スケーリングを実現する。MambaブロックはTransformerのアテンション部分を置き換えるSSMと、MLPスタイルの射影（計算担当）で構成され、TransformerブロックのAttention＋MLP構造と対応する。最大の革新はSSMのパラメータ（A, B, C, Δ）を入力依存（selective）にしたことで、従来のLTIベースSSM（S4等）が固定パラメータで全入力を均一に処理していた問題を解消した。これによりモデルは重要なトークンを選択的にフィルタリングして状態に保持できる。実装上はハードウェア効率を考慮したParallel Associative Scanをカーネルフュージョンと組み合わせ、FlashAttentionに相当するメモリ効率化を達成している。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等性能をThe Pileベンチマークで示した。推論速度はTransformerの最大5倍。一方の弱点として、固定サイズ状態に情報を圧縮するためin-context learningや正確な文字列検索・コピーが苦手であり、解釈可能性・安全性研究の手法がTransformerほど確立されていない点が課題として挙げられている。監査エージェントの観点では、長大な監査証跡ログや契約書全文（100万トークン超）をメモリ効率よく処理できる可能性があり、RAGへの依存を減らしてエンドツーエンドの文書理解を行うバックボーンとしての応用が考えられる。

## アイデア

- 隠れ状態hを『過去の圧縮』と定義することで、Transformerの全履歴参照（KVキャッシュ）を固定サイズのベクトルで代替できるという設計思想は、RNNの限界を超えつつ入力選択性を持たせた点が本質的なブレークスルー
- SSMパラメータ（B, C, Δ）を入力依存にする『selectiveメカニズム』は、アテンション機構が行う『どのトークンを見るか』という選択をSSMの枠組みで実現したものと解釈でき、両アーキテクチャのトレードオフを明示する
- 長文脈でのスケーリング則がTransformerと同等という主張は、監査ログ・法的文書・長期会話履歴など超長文脈が求められるエンタープライズAI応用において、Mambaが現実的な代替バックボーンになり得ることを示唆する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / 隠れ状態** (TODO: 読むべき)
- **State Space Model (S4)** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
