---
title: "連続バッチ処理（Continuous Batching）をゼロから理解する"
url: "https://huggingface.co/blog/continuous_batching"
date: 2026-04-04
tags: [continuous-batching, KV-cache, LLM-inference, chunked-prefill, vLLM, TGI, attention-mechanism, throughput-optimization]
category: "infra"
memo: "[HF Blog] Continuous batching from first principles"
related: [1434, 1608, 902, 152, 585]
processed_at: "2026-04-04T09:07:33.165948"
---

## 要約

本記事はHugging Faceのブログ投稿で、LLM推論の高速化技術である「連続バッチ処理（Continuous Batching）」をアテンション機構とKVキャッシュから積み上げて説明している。

LLMの推論は2フェーズに分かれる。①Prefillフェーズ：入力プロンプト全体を並列処理して最初のトークンを生成。計算コストは高いが1回限り。②Decodeフェーズ：直前までの全トークンを参照しながら1トークンずつ逐次生成。この繰り返しが生成中の「逐次表示」の原因。

KVキャッシュとは、Decodeフェーズで毎ステップ再計算されるKey・Value行列を保存しておく仕組み。これによりDecodeの計算量がO(n²)からO(n)に削減される。ただしシーケンス長×モデル規模分のGPUメモリを消費するため、長いコンテキストほどメモリ圧迫が問題になる。

従来の「静的バッチ処理」では、複数リクエストをまとめてGPUに投入するが、最も長い出力が終わるまで全リクエストが待機する。このため短いリクエストが早期に終了してもGPUリソースが無駄になり、スループットが低下する。

連続バッチ処理の核心は「反復レベルのスケジューリング」。生成ステップ（イテレーション）ごとに完了したシーケンスをバッチから抜き出し、新しいリクエストを即座に挿入する。これによりGPUがアイドル状態になる時間を最小化し、スループットを大幅に改善できる。

実装上の課題として、PrefillとDecodeの混在バッチ処理がある。Prefillは多数トークンを一括処理（compute-bound）、Decodeは単一トークン処理（memory-bandwidth-bound）であり、これらを同一バッチに混在させると相互に性能劣化を引き起こす。この解決策として「Chunked Prefill」が紹介されており、Prefillを小チャンクに分割してDecodeと同一バッチに収める手法。これによりPrefillの計算をDecodeと均等に分散させ、Time-To-First-Token（TTFT）とスループットのバランスを取れる。

アテンションマスクの観点では、連続バッチ処理においてQ・K・Vが異なる長さを持つ場合があり（Prefillトークン＋Decodeトークンの混在）、ブロック対角形式のアテンションマスクが必要になる。各シーケンスは独立したブロックとして処理され、異なるシーケンス間のクロスアテンションは禁止される。

本技術はvLLM、TGI（Text Generation Inference）等の主要推論フレームワークに実装済みで、高負荷サービング環境でのGPUスループット向上に直結する。

## アイデア

- 反復レベルスケジューリングという発想：バッチの境界をリクエスト単位ではなく生成ステップ単位で管理することで、GPUアイドル時間をほぼゼロにできる設計原理
- Chunked PrefillによるTTFTとスループットのトレードオフ制御：Prefillチャンクサイズを調整することで、レイテンシ優先/スループット優先を動的に切り替えられる実用的なパラメータの存在
- KVキャッシュのメモリ消費がボトルネックになる構造：バッチサイズ×シーケンス長×層数×ヘッド数に比例するため、PagedAttention（vLLM）のような仮想メモリ的アプローチが必要になった必然性
## 関連記事

- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法
- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_902 日本語LLMオープンリーダーボードの公開
- /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ

## 原文リンク

[連続バッチ処理（Continuous Batching）をゼロから理解する](https://huggingface.co/blog/continuous_batching)
