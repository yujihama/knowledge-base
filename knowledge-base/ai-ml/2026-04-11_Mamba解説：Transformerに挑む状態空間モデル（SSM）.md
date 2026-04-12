---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-11
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, 選択的状態空間, Parallel Scan, シーケンスモデル, LLM]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-11T21:41:16.811417"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttentionメカニズムが抱えるO(n²)の計算量問題を解決する。Transformerでは全トークン間のペアワイズ通信によりKVキャッシュがO(n)の空間を消費し、長文脈での推論速度が二次的に悪化するが、MambaはこれをSSMによる線形スケーリングで置き換える。

数学的基盤は制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の情報を圧縮したマルコフ的な「状態」として機能する。連続時間式はZero-Order Hold（ZOH）離散化により差分方程式に変換され、実装される。

Mambaの最大の革新は「選択的状態空間モデル（Selective SSM / S6）」である。従来のSSM（S4等）はA・B・Cが入力に依存しない固定パラメータであり、全入力を均等にフィルタリングするため情報選択能力が低かった。MambaではB・C・Δを入力xの関数として動的に変化させることで、文脈に応じて記憶すべき情報と忘れるべき情報を選択できる。これはLSTMのゲート機構と概念的に類似するが、並列スキャンによる効率的な実装が可能。

ハードウェア最適化としてParallel Associative Scanを採用し、再帰的計算をGPUの並列処理に適合させる。また状態を高バンド幅メモリ（HBM）ではなくSRAM上で計算するFlashAttention的なカーネル融合により、推論速度はTransformer比最大5倍を達成。学習時もO(n log n)に抑えられる。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pile等のベンチマークで示す。言語・音声・ゲノミクスなど複数モダリティで最先端性能を達成し、100万トークン長のシーケンスでも性能が向上し続けることが確認されている。

一方、解釈可能性の観点では課題もある。AttentionはAttention Weightが可視化可能で「どのトークンに注目したか」が追跡できるが、Mambaの選択的状態は動的で高次元なため同様の解析が困難。Circuit分析やメカニスティック解釈可能性の手法をSSMに適用する研究はまだ初期段階。AIセーフティの文脈では、圧縮された隠れ状態に情報がどう蓄積されるかの理解が今後の課題となる。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能するマルコフ的設計は、エージェントの会話履歴管理やワーキングメモリの実装に応用可能。固定サイズの状態で長期文脈を保持できるため、メモリ効率が重要なエッジ推論にも適合する
- 入力依存のB・C・Δによる選択的フィルタリングは、LSTMのゲート機構をSSMの並列計算効率と融合した設計。GRPO/RLAIFによる強化学習でどの情報を「選択して記憶するか」のポリシーを学習させる研究方向が考えられる
- Transformerとの比較でAttentionの解釈可能性（Attention Weight可視化）に対してMambaの隠れ状態解析が困難という点は、LLM-as-judgeやReAct型エージェントの根拠トレース問題と本質的に同じ課題を指している
## 関連記事

- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_105 TransformerでAttention Residualsを観察する
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_1596 LLMの金融市場応用：価格予測・合成データ生成・マルチモーダル分析

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
