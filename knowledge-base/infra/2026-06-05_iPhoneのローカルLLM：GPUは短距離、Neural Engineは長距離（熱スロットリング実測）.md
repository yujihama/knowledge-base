---
title: "iPhoneのローカルLLM：GPUは短距離、Neural Engineは長距離（熱スロットリング実測）"
url: "https://zenn.dev/mlboydaisuke/articles/iphone-llm-ane-throttling"
date: 2026-06-05
tags: [Apple Neural Engine, CoreML, MLX, 熱スロットリング, ローカルLLM, iPhone, LiteRT-LM, Gemma, モバイル推論, 電力効率]
category: "infra"
related: [2696, 1333, 3653, 7111, 7061]
memo: "[Zenn LLM] iPhoneのローカルLLM：GPUは短距離、Neural Engineは長距離（熱スロットリング実測）"
processed_at: "2026-06-05T09:17:47.072135"
---

## 要約

iPhone 17 Pro（A19 Pro）上でGemma 4 E2B 4-bitモデルを使い、MLX（GPU）・LiteRT-LM（GPU）・CoreML（ANE）の3ランタイムについて、コールドスタートから10分間の連続生成時のデコード速度推移を実測した比較研究。

バースト速度（初速）ではLiteRT-LM/GPUが56 tok/s、MLX/GPUが48 tok/s、CoreML/ANEが33 tok/sと、GPU系が大きくリード。しかし10分間の持続生成後はMLX/GPUが18 tok/s（維持率38%）、LiteRT-LM/GPUが27 tok/s（48%）まで失速。CoreML/ANEは22 tok/s（67%）を維持し、MLXを完全に逆転した。

失速タイムラインも明確で、MLX/GPUはわずか5秒でピーク比-10%、35秒で-25%に達する。LiteRT/GPUも13秒で-10%、40秒で-25%。一方、ANEは-10%到達まで93秒、-25%に達するのは390秒かかる。

原因は消費電力の差。Mac（M4 Max）でpowermetricsを使って計測すると、CoreML/ANEが12.7 Wに対し、MLX/GPUおよびllama.cpp/GPUはいずれも約24.5〜24.7 Wと約2倍の電力を消費する。iOSは部位別消費電力APIを持たないが、この電力差が発熱量の差を生み、熱制約の強いiPhoneではGPU系が早期に熱スロットリングを受ける。独立した2つのGPUランタイム（MLXとLiteRT-LM）が同じ崩れ方をしている点から、特定ランタイムのバグではなくA19 ProのGPU熱特性によるものと結論づけている。

まとめとして、短いチャット返信のようなバースト用途ではGPUが有利だが、長文生成・エージェントループ・バックグラウンドバッチ処理など持続負荷ではANE（CoreML）が実効スループットで上回る。加えてANEはGPUをUIレンダリングやカメラ等の他処理に開放できるという副次的利点もある。

監査エージェント開発への示唆：エージェントのループ処理や長文ドキュメント分析など持続的な推論タスクをモバイル端末で実行する場合、初速指標だけでランタイムを選定すると本番環境で著しく性能劣化する。CoreML/ANEを選択することで熱スロットリングを回避しつつ、GPU帯域を他のエージェントコンポーネント（OCR、画像解析等）に割り当てる設計が有効。

## アイデア

- バースト速度と持続速度の乖離：GPU系ランタイムは初速で最大70%リードしていたのに、10分後にはANEに逆転される。ベンチマークの計測時間設計が実用性能評価に決定的な影響を与える
- 消費電力がスロットリング耐性を規定する：ANEはGPUの約半分（12.7 W vs 24.7 W）の電力で動作するため、同じ熱予算下でスロットリングが起きにくい。性能選定において電力効率は速度と同等の第一級指標である
- リソース分離の設計価値：ANEでLLMを動かすことでGPUを描画・カメラ・他MLタスクに開放できる。エージェントアーキテクチャにおいてコンピュートユニットの役割分担を意識した設計がモバイル上での並列処理能力を左右する

## 前提知識

- **Apple Neural Engine (ANE)** (TODO: 読むべき)
- **CoreML** → /deep_7303 YoloV5をCoreMLに変換し、デコードレイヤーとNMSを追加してiOSで使う方法
- **熱スロットリング** (TODO: 読むべき)
- **量子化LLM (4-bit)** (TODO: 読むべき)
- **MLX** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは

## 関連記事

- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_7111 【2026年最新】LFM2.5-8B-A1BをApple Siliconで実測 — 「1月のLFM2.5」との違いと実際の速度
- /deep_7061 「自社AIを育てる」前に — ローカルLLM+RAGで検証したら、ファインチューニングは要らなかった

## 原文リンク

[iPhoneのローカルLLM：GPUは短距離、Neural Engineは長距離（熱スロットリング実測）](https://zenn.dev/mlboydaisuke/articles/iphone-llm-ane-throttling)
