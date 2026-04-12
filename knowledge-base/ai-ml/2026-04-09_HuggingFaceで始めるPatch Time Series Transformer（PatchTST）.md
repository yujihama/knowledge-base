---
title: "HuggingFaceで始めるPatch Time Series Transformer（PatchTST）"
url: "https://huggingface.co/blog/patchtst"
date: 2026-04-09
tags: [PatchTST, 時系列予測, Transformer, 転移学習, ゼロショット予測, パッチ化, HuggingFace, 自己教師あり学習]
category: "ai-ml"
memo: "[HF Blog] Patch Time Series Transformer in Hugging Face"
related: [1494, 113, 1613, 1162, 1105]
processed_at: "2026-04-09T21:05:14.326859"
---

## 要約

PatchTSTはIBM研究者らが2023年ICLR発表した時系列予測モデルで、Transformerベースの長期予測に2つの核心設計を採用している。第一に「パッチ化」：時系列をサブシリーズ単位のパッチ（例：長さ16）に分割してTokenとしてTransformerに入力する。これによりAttentionマップの計算量とメモリ使用量を二乗オーダーで削減しつつ、コンテキスト長512ステップ相当の長期依存性を捉えられる。第二に「チャネル独立性」：多変量時系列の各チャネルを独立した単変量系列として扱い、Embedding重みとTransformer重みを全チャネルで共有するグローバルユニバリエートモデルとして機能させる。本ブログでは3段階のハンズオンデモを提供している。①直接予測：電力消費データ（ECL）でcontext_length=512、forecast_horizon=96、patch_length=16の設定でPatchTSTForPredictionをゼロから学習。②ゼロショット転移：ECLで学習済みのモデルをETTh1データセットに対してファインチューニングなしで評価（ゼロショット予測）。③線形プロービング＋ファインチューニング：事前学習済みモデルのHeadのみを学習（線形プロービング）した後、全パラメータをファインチューニングして性能を改善。実装はHugging Face TransformersのPatchTSTConfigとPatchTSTForPrediction、IBMのtsfmライブラリ（TimeSeriesPreprocessor、ForecastDFDataset）を組み合わせており、Trainerクラスで学習を統一管理できる。PatchTSTの設計上の利点は3点：①パッチ内に局所的な意味情報が保持される、②同一ルックバック窓ではAttention計算がパッチ数の二乗に比例するため大幅に効率化される、③パッチ長と系列長のトレードオフにより実質的に長い履歴を参照できる。また、教師あり予測（Supervised Head）とマスク付き自己教師あり事前学習（Masked Patch Prediction）の両モードをモジュール設計でシームレスに切り替えられる。転移学習実験ではゼロショットでも実用的な予測精度を示し、線形プロービングとファインチューニングで段階的に精度が向上することを確認している。

## アイデア

- 時系列をパッチ化してTokenとして扱う設計はBERTの単語トークン化と同じ発想であり、NLPで実証済みの自己教師あり事前学習（マスク予測）を時系列ドメインに直接適用できる点が理論的に綺麗
- チャネル独立（各変量を独立した単変量系列として共有重みで処理）という設計は、多変量間の相関を明示的にモデル化しない代わりにパラメータ効率と汎化性を得るトレードオフであり、ドメイン転移耐性の源泉
- ゼロショット→線形プロービング→フルファインチューニングの3段階評価フレームワークは、事前学習モデルの表現品質を系統的に測定する標準的手法として監査ログや財務時系列など他ドメインへの応用評価に再利用できる
## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_1613 Nyströmformer: Nyström法による線形時間・メモリでのSelf-Attention近似
- /deep_1162 FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによる堅牢なカーボンフットプリント予測
- /deep_1105 FTimeXer: 外生変数を組み込んだ周波数認識型時系列Transformerによるカーボンフットプリント予測

## 原文リンク

[HuggingFaceで始めるPatch Time Series Transformer（PatchTST）](https://huggingface.co/blog/patchtst)
