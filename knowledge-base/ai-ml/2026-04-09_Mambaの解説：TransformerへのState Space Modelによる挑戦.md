---
title: "Mambaの解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-09
tags: [Mamba, SSM, State Space Model, Transformer, 選択的状態空間, 長コンテキスト, 線形スケーリング, HiPPO, CUDA最適化]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-09T09:20:01.080750"
---

## 要約

MambaはGu and Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerの二次計算複雑度（O(n²)）という根本的なボトルネックを解消する。Transformerは全トークン間のAttentionによりKVキャッシュがO(n)のメモリを必要とし、長いコンテキストでは推論が指数的に遅くなる。Mambaはこれを線形スケーリング（O(n)）に置き換え、最大100万トークンの長コンテキストを処理可能とする。推論速度はTransformerの最大5倍。

アーキテクチャの核心は制御理論由来のSSMで、連続時間微分方程式 h'(t) = Ah(t) + Bx(t) / y(t) = Ch(t) + Dx(t) を離散化（Zero-Order Hold法）してシーケンス処理に適用する。隠れ状態hが「過去の圧縮」として機能し、Markov的に次状態を決定するため、Attentionのような全トークン参照が不要になる。

Mambaの最大の革新は「選択的状態空間モデル（Selective SSM / S6）」で、従来のLTI（線形時不変）SSMと異なり、パラメータΔ・B・Cを入力依存（input-dependent）にする。これにより「どの情報を記憶し、どれを忘れるか」を入力に応じて動的に制御でき、LSTMのゲート機構に類似した選択性を実現する。ただし入力依存パラメータによりHippo行列の畳み込みカーネルが入力ごとに変化するため、並列FFT演算が使えなくなるという課題が生じ、これをHardware-Aware Parallelスキャン（CUDA上のセレクティブスキャン）で解決している。

ベンチマークでは、The PileデータセットでMamba-3BがTransformer同サイズを上回り、2倍サイズのTransformerに匹敵する性能を示す。言語・音声・ゲノムデータなど複数モダリティでstate-of-the-artを達成。

Mambaの課題として、長距離依存の処理はAttentionほど強力でない可能性（重要なトークンが圧縮で失われるリスク）、In-context learningの能力がTransformerより劣る可能性、Interpretabilityの困難さが挙げられる。Hybrid MambaはMambaとAttentionを交互に積み重ねることで両者の利点を組み合わせる方向性として注目される。

## アイデア

- 隠れ状態を「過去の圧縮」と定義するMambaのアプローチは、エージェントの会話履歴や監査証跡の要約・圧縮に応用可能な概念フレームワークを提供する
- 入力依存パラメータによる「選択的記憶・忘却」機構は、監査エージェントが大量の証跡データから関連情報を選別する際のアーキテクチャ選択肢として有望
- Hybrid Mamba（MambaとAttentionの組み合わせ）はエージェントの長期メモリ（Mamba）と局所的な精密推論（Attention）を分離する設計パターンとして、マルチエージェントシステムのメモリ設計に示唆を与える

## Yujiの取り組みへの示唆

監査エージェント開発においてLangGraphで長い監査証跡・会話履歴を処理する場合、TransformerベースのLLMのコンテキスト制限がボトルネックになりうる。MambaのSSMアーキテクチャは線形スケーリングで100万トークン級の長コンテキストを扱えるため、大量の財務データや監査ログを一括処理するエージェントのバックボーンとして検討価値がある。また選択的状態空間モデルの「何を記憶し何を捨てるか」という動的制御の概念は、ReActエージェントのメモリ管理設計（短期・長期メモリの分離）の理論的根拠として活用できる。ローカルLLMインフラ（RTX 3090）でのデプロイ観点では、Mambaの推論速度5倍・メモリ効率の高さは実用的な優位性となる。

## 原文リンク

[Mambaの解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
