---
title: "日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも"
url: "https://zenn.dev/kiyoka/articles/japanese-input-method-sumibi-18"
date: 2026-04-23
tags: [Gemma 4, ローカルLLM, IME, MLX, Apple Silicon, 量子化, 日本語処理, CER]
category: "infra"
related: [1148, 992, 710, 1493, 1116]
memo: "[Zenn LLM] 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも"
processed_at: "2026-04-23T12:14:02.528687"
---

## 要約

日本語IME「Sumibi」の開発記録。約1年前（2025年5月）の検証でローカルLLMはIMEとして実用不可と結論付けていたが、Gemma 4 E4Bの登場により状況が一変した。

Gemma 4 E4Bのスペックはパラメータ数4.5B、Q4量子化で約5.5GBのメモリ、JGLUEスコアがGemma 2比で15ポイント以上改善、Apache 2.0ライセンス。MacBookでOllama経由で約57 tokens/secの速度を達成し、「応答速度」と「日本語指示追従能力」の両面で実用閾値に到達した。

ベンチマーク結果では、Gemma 4 E4B（LM Studio）がひらがな入力CER 26.0%、平均応答時間2.08秒で実用圏内と評価された。一方、より高精度なGemma 4 26B-A4B（MoEアーキテクチャ、アクティブパラメータ4B・総パラメータ26B相当）はLM Studioでは5.60秒と遅すぎるが、Apple Silicon上でMLX最適化版（mlx-community/gemma-4-26b-a4b-it）を使うと2.21秒まで短縮、CERも18.3%とクラウドAPIの上位モデルに迫る精度を実現。

SumibiはローカルLLMをバックエンドとしてかな漢字変換を行うIMEであり、クラウドAPIに文章を送信せずに動作できることはプライバシー・セキュリティ上の大きな前進である。記事本文自体もGemma 4 E4Bを用いて執筆されており、カジュアルな日本語入力（コーディングエージェントへの指示出し等）には十分な品質に達していることが実証されている。

監査エージェント開発への示唆としては、ローカルLLMが日本語の指示追従能力で実用水準に達したことで、機密情報を含む監査ドキュメントの処理をオンプレミス環境で行う選択肢が現実的になってきた点が注目される。Gemma 4 E4B程度のモデルであれば一般的なGPU環境でも動作可能であり、内部監査用途でのローカル推論基盤構築の参考事例となる。

## アイデア

- MoEアーキテクチャ（Gemma 4 26B-A4B）によりアクティブパラメータを4Bに抑えながら26B相当の知識にアクセスする設計は、リソース制約のあるローカル推論環境での高精度化戦略として有効
- MLX最適化によってLM Studio比で約2.5倍の速度向上（5.60秒→2.21秒）を達成した点は、ハードウェア固有の推論フレームワーク選択が実用性を左右することを示す具体的事例
- CER（文字誤り率）と平均応答時間（95パーセンタイル）をIME評価指標として使い、実用閾値を定量的に定義したベンチマーク設計は、他のローカルLLM応用評価にも転用可能

## 前提知識

- **量子化（Q4）** (TODO: 読むべき)
- **MoE (Mixture of Experts)** (TODO: 読むべき)
- **MLX (Apple推論フレームワーク)** (TODO: 読むべき)
- **CER (文字誤り率)** (TODO: 読むべき)
- **JGLUE** (TODO: 読むべき)

## 関連記事

- /deep_1148 Bonsai-8B-mlx × Goose でフルローカルの AI エージェント環境を構築する
- /deep_992 WWDC 24: Core MLでMistral 7Bをオンデバイス実行する
- /deep_710 OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド
- /deep_1493 Apple SiliconでCore MLを使ってStable Diffusionを動かす
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング

## 原文リンク

[日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも](https://zenn.dev/kiyoka/articles/japanese-input-method-sumibi-18)
