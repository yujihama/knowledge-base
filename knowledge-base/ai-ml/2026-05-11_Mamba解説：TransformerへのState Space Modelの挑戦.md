---
title: "Mamba解説：TransformerへのState Space Modelの挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-11
tags: [Mamba, State Space Model, SSM, Selective SSM, S4, Transformer, 長文脈, 線形スケーリング, カーネルフュージョン, FlashAttention]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-11T09:04:19.597284"
---

## 要約

Mambaは、Transformerが抱える二次計算量（O(n²)）の問題を解決するState Space Model（SSM）ベースのアーキテクチャである。著者はAlbert GuとTri Dao（FlashAttentionの開発者）。

**Transformerの問題点**: Attentionメカニズムはすべてのトークン間のペアワイズ通信を行うため、学習時O(n²)、推論時O(n)の計算量が必要。KVキャッシュもO(n)のメモリを消費し、長文脈処理でCUDA OOMが頻発する。

**SSMの基本原理**: 状態空間モデルは制御理論に由来し、隠れ状態hを用いてシステムの動態を表現する。連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を離散化（Zero-Order Hold法）することで、差分方程式 h_t = Ā h_{t-1} + B̄ x_t、y_t = C h_t に変換。状態hは過去の情報の圧縮であり、理論的にはマルコフ決定過程として定式化される。

**S4からMambaへの進化**: 従来のSSM（S4等）は行列A, B, Cが入力に依存しない線形時不変（LTI）システムであったため、内容ベースの選択的注意が不可能だった。Mambaの核心的革新は「選択的状態空間モデル（Selective SSM / S6）」であり、B, C, Δ（タイムステップ）を入力x_tの関数として動的に変化させる。これにより、モデルが現在の入力に基づき何をフィルタリングし何を記憶するかを選択できる。

**ハードウェア効率の工夫**: 選択的SSMはスキャン演算の並列化によって計算されるが、素直に実装するとGPUのSRAMとHBM間の転送がボトルネックになる。MambaはFlashAttentionと同様のカーネルフュージョンを活用し、選択的スキャンをHBMへの読み書きを最小化しつつSRAM上で実行する。

**性能**: Mamba-3BはThe Pileで同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵。推論速度はTransformerの最大5倍。長文脈（100万トークン以上）でも線形スケーリングを実現。

**Mambaの限界と課題**: Transformerのin-context learningの一部は、KVキャッシュを用いた検索に依存しているが、Mambaの固定サイズ隠れ状態では全過去トークンを完全に保持できず、「hay-in-a-haystack」（特定情報の再検索）タスクに弱い可能性がある。また、解釈可能性（Interpretability）の観点では、Attentionパターンの可視化が行えないため、Induction Headsのような回路解析が困難になる。

**監査エージェントへの示唆**: 長文脈の監査ログや規制文書（例：何十万トークンもの取引履歴）を線形コストで処理できる可能性がある。ただし、特定の過去イベントへのピンポイントアクセス（証跡追跡）にはAttentionの方が適するケースがあり、Mamba単体での採用ではなくMambaとTransformerのハイブリッド構成（Jamba等）が現実的な選択肢となる。

## アイデア

- 選択的状態空間モデル（S6）の「入力依存パラメータ」という設計思想は、LTIシステムの限界を破るもので、SSMをAttentionに近づける転換点である
- 隠れ状態hが「過去の圧縮」として機能する点は、固定サイズのメモリで無限長の文脈を近似するトレードオフであり、RAGや外部メモリとの組み合わせで監査システムに応用できる
- Mambaの解釈可能性の困難さ（Attentionパターン不在）は、規制要件でのXAI（説明可能AI）対応が必要な監査AIに対して採用上の障壁となりうる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **State Space Model (SSM)** (TODO: 読むべき)
- **離散化・差分方程式** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **スケーリング則** → /deep_3781 スケールの再考：エージェントパラダイム下における小規模言語モデルのデプロイメントトレードオフ

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelの挑戦](https://thegradient.pub/mamba-explained/)
