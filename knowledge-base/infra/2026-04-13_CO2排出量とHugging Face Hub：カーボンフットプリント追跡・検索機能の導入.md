---
title: "CO2排出量とHugging Face Hub：カーボンフットプリント追跡・検索機能の導入"
url: "https://huggingface.co/blog/carbon-emissions-on-the-hub"
date: 2026-04-13
tags: [codecarbon, CO2排出量, Hugging Face Hub, モデルカード, サステナビリティ, Trainer, emissions_threshold]
category: "infra"
related: [1577, 428, 1532, 187]
memo: "[HF Blog] CO2 Emissions and the 🤗 Hub: Leading the Charge"
processed_at: "2026-04-13T12:08:00.533425"
---

## 要約

Hugging Face Hubは、機械学習モデルの学習・推論に伴うCO2排出量をモデルカードのメタデータとして記録・公開し、エコフレンドリーなモデル選択を可能にする仕組みを2022年4月に導入した。

背景として、GPUクラスタやストレージを含む計算インフラのエネルギー消費は無視できないCO2排出源であり、近年のTransformerモデルの大型化（例：GPT-3, T5等）に伴いその量は増大している。排出量はランタイム・使用ハードウェア・電力グリッドのカーボン強度（地域差あり）の3要素で決まる。

技術的な仕組みは2段構成。①学習時の自動計測：HuggingFaceのTrainerクラスがcodecarbonライブラリのCodeCarbonCallbackを自動で組み込み、学習中のCO2排出量をemissions.csvに記録する。このCSVから対象学習ランのデータを抜き出してモデルカードのco2_eq_emissionsフィールドに記載する。②Hubでの検索フィルタ：huggingface_hubライブラリのapi.list_models()にemissions_thresholdsパラメータ（タプル形式で最小・最大グラムを指定）が追加され、例えば最大100gのモデルは191件、最小500gのモデルは10件という形で絞り込みができる。実データとして、デンマーク語ELECTRAモデル（Maltehb/aelaectra）は4009.5gと高排出量であることが確認されている。

モデルカードのメタデータ形式（co2_eq_emissions）はHub公式ドキュメントで規定されており、排出量の数値だけでなく計測手法・ハードウェア情報等も記録可能。関連研究としてRolnick et al. (2019)、Strubell et al. (2019)、Schwartz et al. (2020)が参照されている。

監査エージェント開発への示唆：大規模なLLM訓練や推論インフラを内部監査システムに組み込む際、計算コストの透明性確保の一環としてcodecarbonによるCO2追跡をパイプラインに組み込むことが有効。特に監査ログの一部としてカーボンフットプリントを記録・報告するガバナンス要件（ESG監査）が今後強化される可能性があり、その先行実装として参考になる。

## アイデア

- emissions_thresholdsによるモデル検索は、モデル選択の意思決定基準に環境コストを定量的に組み込む初の実用APIであり、グリーンAI実践の具体的インターフェースとなっている
- CodeCarbonCallbackをTrainerに自動挿入することで、開発者がオプトインなしにCO2計測を得られる設計は、透明性向上を摩擦ゼロで実現するUXアプローチとして注目に値する
- co2_eq_emissions メタデータをモデルカードに標準化することで、将来的にESG規制やAIガバナンス基準（EU AI Actの環境条項等）への対応に利用できる監査証跡として機能しうる

## 前提知識

- **Hugging Face Hub** → /deep_187 Community Evals: ブラックボックスリーダーボードから脱却するHugging Faceの分散型評価システム
- **Transformers Trainer** (TODO: 読むべき)
- **codecarbon** (TODO: 読むべき)
- **モデルカード** → /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- **カーボン強度** (TODO: 読むべき)

## 関連記事

- /deep_1577 Skops紹介：scikit-learnモデルをHugging Face Hubで安全にホスティング・共有するライブラリ
- /deep_428 ゼロからGPUへ: 本番環境対応CUDAカーネルの構築とスケーリングガイド
- /deep_1532 PyTorch DDPからAccelerateとTrainerへ：分散学習を段階的にマスターする
- /deep_187 Community Evals: ブラックボックスリーダーボードから脱却するHugging Faceの分散型評価システム

## 原文リンク

[CO2排出量とHugging Face Hub：カーボンフットプリント追跡・検索機能の導入](https://huggingface.co/blog/carbon-emissions-on-the-hub)
