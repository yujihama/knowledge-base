---
title: "Gemma 4をPixel 9aとPixel 7で動かしてみた — Google AI Edge Galleryベンチマーク比較"
url: "https://zenn.dev/acropapa330/articles/gemma4_pixel_benchmark"
date: 2026-04-09
tags: [Gemma4, オンデバイスLLM, LiteRT-LM, Android, Pixel, TensorG4, Google AI Edge Gallery, ベンチマーク, GPUコンパイル]
category: "infra"
memo: "[Zenn LLM] Gemma 4をPixel 9aとPixel 7で動かしてみた — Google AI Edge Galleryベンチマーク比較"
processed_at: "2026-04-09T09:41:41.018441"
---

## 要約

GoogleがリリースしたGemma 4（2Bおよび4Bモデル）を、Android端末2台（Pixel 9a: Tensor G4チップ、Pixel 7: Tensor G2チップ）上でGoogle AI Edge Gallery v1.0.11を使って実行し、ベンチマーク比較を行った記事。推論エンジンはLiteRT-LM（GoogleのAndroid向けオンデバイス推論ランタイム）でGPUアクセラレーションを使用。プリフィル256トークン・デコード256トークン・3回試行の平均値で計測。

主要な結果は以下の通り。プリフィル速度（t/s）はPixel 9a 2B: 608、Pixel 9a 4B: 318、Pixel 7 2B: 361、Pixel 7 4B: 122。デコード速度（t/s）はPixel 9a 2B: 12.7、Pixel 9a 4B: 9.0、Pixel 7 2B: 7.2、Pixel 7 4B: 7.7。初回トークンまでの時間はPixel 9a 2B: 0.50秒、Pixel 7 4B: 5.66秒。

最大の注目点はPixel 7 4Bの初回起動時間が2,128,906ms（約35分）に達した点。これはTensor G2 GPUコンパイラが4Bモデルのシェーダーを初回にコンパイルする処理に起因するとみられ、2回目以降は103秒に短縮される。同じPixel 7の2Bモデルの初回起動が63秒であることと対比すると、モデルサイズが倍以上になるとコンパイル時間が指数的に増加することがわかる。

Pixel 9aでは逆に2B（214秒）が4B（75秒）より初回起動が遅いという現象が生じており、これは実行順序によるGPUシェーダーキャッシュの再利用効果と推測されている。

デコード速度の世代差はTensor G4 vs G2で約1.8倍（12.7 vs 7.2 t/s）。デコードは逐次処理のためプリフィルほどの高速化は得られない構造的制約がある。実用性評価では、Pixel 9a + 2Bが最も快適（◎）、Pixel 7 + 2Bが使用可能（△）、Pixel 7 + 4Bは実用困難（×）とまとめられている。Gemma 4は日本語にも対応しており、完全オフライン動作が可能。

## アイデア

- GPUシェーダーの初回コンパイル時間がモデルサイズに対して指数的に増加する現象（2B: 63秒 vs 4B: 35分）は、エッジデプロイ設計においてコールドスタートコストを考慮した「ウォームアップ戦略」が重要であることを示す
- ベンチマーク実行順序によってGPUキャッシュが再利用され測定値が変動する点は、オンデバイス推論の再現性評価において実行順序制御が必要なことを示唆する
- デコード速度12.7 t/sがチャット用途として十分な水準に達しており、2Bクラスのモデルでも実用的なオフラインLLMとして機能する閾値の参考値となる

## Yujiの取り組みへの示唆

Yujiが構築中のローカルLLMインフラ（RTX 3090予定）の比較対象として、モバイルエッジでの推論性能の実測値が参考になる。監査エージェントのフィールド活用（ネット非接続環境での端末上推論）を検討する際、LiteRT-LMのGPUコンパイルコストやウォームスタート戦略は設計上の考慮点となりうる。ただし現状のデコード速度（最大12.7 t/s）はエージェントの複数ステップ推論には低速であり、モバイルへのデプロイより当面はローカルGPU環境が優先される判断材料としても有用。

## 原文リンク

[Gemma 4をPixel 9aとPixel 7で動かしてみた — Google AI Edge Galleryベンチマーク比較](https://zenn.dev/acropapa330/articles/gemma4_pixel_benchmark)
