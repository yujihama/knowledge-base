---
title: "Mamba解説：TransformerにState Space Modelが挑む"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-08
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, 線形スケーリング, 選択的SSM, parallel scan, ZOH離散化]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-08T09:03:58.684765"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、TransformerのAttentionメカニズムが抱えるO(n²)の計算量問題を解決する。Transformerは全トークン間のpairwise通信（Attention）のため、コンテキスト長が増加するにつれ推論速度が二乗的に劣化し、KVキャッシュのメモリ消費もO(n)で増大する。MambaはこのAttentionを制御理論由来のSSMに置き換えることで、シーケンス長に対して線形スケーリングを実現し、最大100万トークンの長文脈処理を可能にする。

SSMの基本式は `h'(t) = Ah(t) + Bx(t)`（状態遷移）と `y(t) = Ch(t) + Dx(t)`（出力）の連立微分方程式で表現される。連続時間方程式を離散時間に変換するためZero-Order Hold（ZOH）離散化を使用し、実際の計算では `h_t = Ā h_{t-1} + B̄ x_t`、`y_t = Ch_t` の差分方程式として処理する。状態hは過去の情報を圧縮した「記憶」であり、Markov性を持つ。

従来のS4等の線形不変SSMと異なり、MambaはパラメータA・B・C・Δを入力xに応じて動的に変化させる「選択的SSM（selective SSM）」を採用。これにより無関係な情報をフィルタリングし、重要な情報を選択的に記憶する能力を持つ。推論時はRNNのように隠れ状態を逐次更新するため1ステップの計算量はO(1)、学習時は並列スキャンアルゴリズム（parallel scan）でO(n log n)に抑える。また、カーネルフュージョンやrecomputationなどCUDAレベルの最適化により、Transformerより最大5倍高速な推論を達成している。

Mamba-3Bは同サイズのTransformerと同等以上、かつ2倍サイズのTransformerにも匹敵するスケーリング則を示した（The Pileベンチマーク）。言語・音声・ゲノミクス等の複数モダリティでSoTAを達成。ただし、Transformerが持つ「任意の過去トークンへの直接注意」機能はなく、in-context learningや複数文書の正確なretrieval等ではTransformerが優位なケースもある。ハイブリッドアーキテクチャ（MambaブロックとAttentionブロックの混合）が今後の有力方向とされる。監査エージェント開発における長い監査証跡・ログのリアルタイム処理や、セッション横断の長期記憶保持への応用可能性がある。

## アイデア

- 選択的SSM（selective SSM）により入力依存でA・B・C・Δを動的変化させる設計は、固定パラメータのS4では不可能だった「コンテキスト依存フィルタリング」を実現しており、RNNとAttentionの中間的な表現力を持つアーキテクチャとして新しい設計空間を開いている
- 推論時はO(1)の逐次RNN、学習時はO(n log n)の並列スキャンという二重モードの切り替えにより、学習効率と推論効率を同時に最適化している点は、エージェントシステムのオンライン学習・推論の両立に示唆がある
- 状態hを「過去の圧縮」と定義しMarkov性を持たせる設計は、監査ログのような長大な時系列データを固定サイズの状態ベクトルで継続的に保持できる可能性を示唆し、KVキャッシュ増大に悩む長期セッション型監査エージェントへの応用が考えられる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model（S4）** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **離散化（ZOH）** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerにState Space Modelが挑む](https://thegradient.pub/mamba-explained/)
