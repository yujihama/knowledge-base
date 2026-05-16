---
title: "Mamba解説：TransformerへのState Space Modelの挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-08
tags: [Mamba, State Space Model, SSM, Transformer, 長文脈, 線形スケーリング, Selection Mechanism, RNN, ZOH離散化, シーケンスモデル]
category: "ai-ml"
related: [3105, 2480, 2510, 201, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-08T09:35:42.750564"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算量ボトルネックを線形計算量で解決する。Transformerのアテンション機構はKVキャッシュにO(n)空間、推論時にO(n)時間、学習時にO(n²)時間を要するのに対し、MambaはSSMによる固定サイズの隠れ状態を維持することで、シーケンス長に対して線形スケールを実現。推論速度はTransformerの最大5倍速く、100万トークンを超える長文脈でも性能が向上し続けることが実証されている。

SSMの数学的基盤は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、状態hが過去の情報を圧縮した表現となる。連続時間から離散時間への変換（離散化）にはZero-Order Hold（ZOH）を使用し、実データのトークン列に適用可能にしている。

Mambaの核心的な革新はSSMパラメータ（B, C, Δ）を入力に依存させる「セレクティビティ（Selection Mechanism）」の導入にある。従来のLinear RNNやS4等のSSMはパラメータが入力に依存しない時不変システムであり、どのトークンを記憶・無視するかを選択できなかった。MambaではB, C, Δを入力から動的に生成することで、RNNのような逐次推論とTransformerのような選択的情報統合を両立する。

アーキテクチャとしてはTransformerブロックのAttentionをSSMに、MLPはそのまま保持した「Mambaブロック」をスタック。ゲーティング機構を追加し非線形変換能力を補完する。言語モデリングでは同サイズTransformerより優れ、2倍サイズTransformerと同等の性能をThe Pileベンチマークで示し、Mamba-3Bとして検証された。

ただし弱点もある：固定サイズ隠れ状態は情報ボトルネックとなり得るため、正確な文字列コピーや完全な記憶保持が苦手。また解釈可能性の観点では、Transformerのアテンションヘッドのような直感的な分析手法がSSMには未確立であり、メカニスティック解釈可能性研究への応用は今後の課題。AI安全性の文脈では隠れ状態の圧縮が意図しない情報の忘却につながる可能性もある。監査エージェント開発への示唆としては、長文書・長会話履歴の処理において線形計算量のSSMはRAGの代替または補完として有望であり、シーケンシャルな監査ログ分析に適する可能性がある。

## アイデア

- SSMのパラメータを入力依存にする「セレクティビティ」の発想：時不変系を時変系にすることでRNNの固定圧縮問題を解決し、Transformerのような動的な情報選択をO(n)で実現する点が巧妙
- 隠れ状態を『過去の圧縮』と定義することで再帰的推論と並列学習を両立：学習時は畳み込み展開（O(n log n)）、推論時は再帰（O(1)/ステップ）と2つの等価な計算形式を持つ二重性が実用上重要
- 解釈可能性の未解決問題：Transformerのアテンションマップに相当するMambaの内部表現分析ツールが存在せず、安全性・監査用途での採用には隠れ状態の可視化手法の開発が必要

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：TransformerへのState Space Modelの挑戦](https://thegradient.pub/mamba-explained/)
