---
title: "TIME-LLMを読んでみた：LLMはどうやって時系列予測に使われるのか"
url: "https://zenn.dev/yuyu1/articles/aae287575bb453"
date: 2026-05-01
tags: [TIME-LLM, 時系列予測, reprogramming, Patch Reprogramming, Prompt-as-Prefix, few-shot, zero-shot, ICLR2024, LLM活用]
category: "ai-ml"
related: [245, 1494, 160, 2837, 113]
memo: "[Zenn 機械学習] TIME-LLM を読んでみた：LLM はどうやって時間系列予測に使われるのか"
processed_at: "2026-05-01T12:01:45.376777"
---

## 要約

TIME-LLM（ICLR 2024、Jin et al.）は、LLMを時系列予測に活用するための「reprogramming」手法を提案した論文。LLMをfine-tuningせず、backboneを凍結したまま、入力変換モジュールのみを学習するアプローチが中心にある。

核心的な技術は「Patch Reprogramming」と「Prompt-as-Prefix」の2つ。Patch Reprograommingでは、入力時系列を小さな区間（patch）に分割してベクトル化した後、LLMの語彙埋め込みから抽出した「text prototypes」の線形結合として各patchを再表現する。これにより、時系列の局所パターン（「上昇傾向」「緩やかな下降」など）をLLMが処理しやすい言語的表現空間に近似させる。直接テキストに翻訳するのではなく、言語的表現空間に「近づける」点が重要で、これによりLLMの既存の表現処理能力を借用できる。

Prompt-as-Prefixでは、reprograommingされたpatch列の前にプレフィックスpromptを付加する。promptにはdataset context（データの意味的説明）、task instruction（予測タスクの指示）、input statistics（最小値・最大値・中央値・trend・lag等の統計量）が含まれ、LLMが適切な文脈でデータを解釈できるよう設計されている。

LLMに直接数値を出力させない設計も重要な判断。tokenizerの数値分割の不安定性（「0.61」が['0','.','6','1']や['0','.','61']に分割されるばらつき）と数値精度の低さを回避するため、LLMは表現変換器として機能し、最終的な予測値は別途設けた投影層（線形層）で生成する。

実験では長期・短期・few-shot・zero-shotの各設定で評価。特にfew-shotおよびzero-shot条件での精度が高く、データが少ない状況でのLLM活用の有効性を示している。限界としては、forecastingに特化しており、classification・anomaly detection・imputationには対応しない点、および多変量系列をチャネル独立に処理するため変数間の相互依存が強い問題には不向きな点がある。

監査エージェント開発への示唆として、LLMのfine-tuningなしに外側の入力設計だけで性能を引き出す「reprogramming」の思想は、監査ログや財務データなど非言語的な時系列データをLLMベースのエージェントに入力する際の設計パターンとして参考になる。統計量をpromptに明示的に埋め込む手法は、数値データを扱う監査エージェントのコンテキスト構築にも応用可能。

## アイデア

- LLMのbackboneを凍結したまま、入力変換モジュールのみを学習する『reprogramming』パラダイムは、fine-tuningなしでLLMを非言語ドメインに転用する汎用的な設計思想として応用範囲が広い
- text prototypesを使ったPatch Reprograommingは、時系列の局所パターンを言語的表現空間に写像する操作であり、異種データをLLMに橋渡しする手法の典型例として、時系列以外のモーダル変換にも参考になる
- LLMに数値を直接出力させず投影層で予測値を生成する設計は、tokenizerの数値分割不安定性という実装上の問題を正面から解決しており、LLMを数値処理に組み込む際の実用的な設計パターンを示している

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **トークン埋め込み（Token Embedding）** (TODO: 読むべき)
- **パッチ分割（Patch-based入力）** (TODO: 読むべき)
- **few-shot / zero-shot学習** (TODO: 読むべき)
- **時系列予測（Time Series Forecasting）** (TODO: 読むべき)

## 関連記事

- /deep_245 時系列データからウェーハレベルエッチング空間プロファイリング：Time-LLMによるプロセス監視
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_160 音声言語モデルにおけるプロンプト増幅とゼロショット後期融合による音声感情認識
- /deep_2837 非対称損失関数を用いたハイブリッドCNN-BiLSTM-Attentionモデルによる産業機器の残余寿命予測と解釈可能な故障ヒートマップ
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた

## 原文リンク

[TIME-LLMを読んでみた：LLMはどうやって時系列予測に使われるのか](https://zenn.dev/yuyu1/articles/aae287575bb453)
