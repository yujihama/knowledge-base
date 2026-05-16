---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-25
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, 選択的状態空間, 線形スケーリング, Hardware-Aware Algorithm, 離散化, ZOH]
category: "ai-ml"
related: [2480, 2510, 1975, 199, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-25T12:27:27.665372"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりフォワードパスがO(n²)の時間計算量となり、KVキャッシュがO(n)のメモリを消費するため、長文脈（例：100万トークン）での運用が困難。Mambaはこの問題をControl Theory由来のSSMで解決する。SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、隠れ状態hが過去の情報を圧縮・保持する役割を担う。実装上は離散化（Zero-Order Hold法）によって差分方程式に変換し、h_t = Ā h_{t-1} + B̄ x_t として逐次処理する。Mambaの最大の革新は行列A・B・Cを入力依存（selective）にした点で、これにより必要な情報だけを選択的に状態に保持できる。この選択性がないS4等の旧SSMとの決定的差異であり、コンテキストに応じた柔軟な記憶が可能になる。計算上は畳み込み（並列訓練用）と再帰（推論用）の両モードを切り替えられるHardware-Aware Parallel Algorithmを採用し、FlashAttentionに類似したI/O最適化によってA100 GPU上でTransformerより最大5倍高速な推論を実現する。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pileベンチマークで示した。一方で、Mambaの隠れ状態は固定サイズであるためTransformerのKVキャッシュに比べて情報圧縮が強制され、完全な過去参照が必要なタスク（例：単純なコピー）では不得意な側面もある。解釈可能性の観点からは、Transformerのアテンションパターンに相当する透明な情報フローがSSMには存在せず、解析ツールの開発が課題。AIセーフティ面でもアクティベーションパッチングなどの手法が直接適用できない。監査エージェント開発への示唆として、長い監査ログ・テキストシーケンスの処理にMambaの線形スケーリング特性は有効だが、回路解釈可能性が低い点は説明責任が求められる監査用途では留意が必要。

## アイデア

- 隠れ状態を「過去の圧縮」と捉えるMDPフレームワークは、Transformerの全履歴参照とは根本的に異なる記憶の哲学であり、モデルが何を覚え何を忘れるかを入力依存で動的に制御するSelectiveSSMは、人間の注意・記憶選択に近いメカニズム
- 訓練時は畳み込みで並列処理、推論時は再帰で定数メモリという二重モード設計は、アーキテクチャの計算グラフを目的に応じて切り替える発想で、ハードウェア特性を最大限活用するソフトウェア設計パターンとして汎用性がある
- Mambaは解釈可能性・AIセーフティツールとの相性がTransformerより低く、高性能化と透明性のトレードオフが顕在化している点は、監査・コンプライアンス用途のモデル選定において重要な評価軸になり得る

## 前提知識

- **Transformer・Attention機構** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **RNN・再帰モデル** (TODO: 読むべき)
- **微分方程式・離散化** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
