---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-21
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長コンテキスト, 線形スケーリング, 選択的SSM, 制御理論, 離散化, ZOH]
category: "ai-ml"
related: [222, 1975, 1837, 199, 833]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-21T12:14:44.636828"
---

## 要約

MambaはGu・Daoが開発した新しいシーケンスモデルで、Transformerのアテンション機構に代わる状態空間モデル（SSM）をベースとしている。Transformerの最大の弱点はアテンション機構のO(n²)計算複雑度であり、コンテキスト長が増加するにつれて推論速度が二次関数的に低下し、KVキャッシュのメモリ消費もO(n)で膨張する。Mambaはこの「二次ボトルネック」を除去し、シーケンス長に対して線形スケーリングを実現する。

Mambaの基礎はControl Theory（制御理論）に由来する連続時間の差分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の情報を圧縮し、新たな観測xと組み合わせて出力yを予測する。連続時間モデルをゼロ次ホールド（ZOH）法で離散化し、実際の系列データに適用可能にする。

先行SSMであるS4との最大の違いは「選択的状態空間（Selective SSM）」にある。従来のSSMはA・B・C行列が入力に依存しない時不変（LTI）システムであったが、MambaではB・C・∆を入力依存のパラメータとし、モデルが何を記憶し何を忘れるかを動的に選択できる。この設計は、コンテキストに応じて情報の保持を制御するゲーティング機構と概念的に類似しており、LSTMのゲートとの類似性も指摘されている。

ハードウェア面では「Parallel Associative Scan」を用いてGPU上で並列計算を実現しつつ、HBMとSRAMの間のデータ転送を最小化するカーネル融合（FlashAttention類似の手法）を適用することで、Transformerの最大5倍の推論速度を達成している。

Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を事前学習・下流タスク評価の両方で示した（The Pile評価）。また言語だけでなく音声・ゲノミクスといった他モダリティでもSOTA性能を記録している。

課題としては、インコンテキスト学習（ICL）がTransformerより弱い点、RAGや外部ツール連携との相性が未検証な点、そしてTransformerベースのモデルの解釈可能性研究（アテンションヘッドの可視化等）がそのまま適用できないという解釈可能性上の問題がある。エージェントアーキテクチャ観点では、長期コンテキストを必要とする監査ログ解析や長い対話履歴を持つLangGraphベースのエージェントにおいて、KVキャッシュ起因のOOMを回避できる可能性があり注目に値する。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能するというMambaのアーキテクチャ設計思想は、エージェントの長期記憶設計（セッションをまたぐ状態保持）に応用できる可能性がある
- 入力依存のB・C・∆パラメータによる選択的記憶・忘却は、LSTMゲートの連続体系版とみなせ、RNNからSSMへの思想的連続性を示している
- Parallel Associative ScanによるGPU並列化は「RNN的な逐次処理」と「Transformer的な並列学習」を両立する手法として、ハードウェア効率とモデル表現力のトレードオフ解決策として参考になる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義

## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
