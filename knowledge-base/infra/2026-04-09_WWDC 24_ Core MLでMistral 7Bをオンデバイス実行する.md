---
title: "WWDC 24: Core MLでMistral 7Bをオンデバイス実行する"
url: "https://huggingface.co/blog/mistral-coreml"
date: 2026-04-09
tags: [Core ML, Mistral 7B, Apple Silicon, 量子化, KVキャッシュ, オンデバイスLLM, swift-transformers, Int4量子化]
category: "infra"
memo: "[HF Blog] WWDC 24: Running Mistral 7B with Core ML"
processed_at: "2026-04-09T09:07:41.128425"
---

## 要約

AppleはWWDC 2024でApple Intelligenceと新しいCore ML機能群を発表し、Hugging FaceチームがMistral 7B（70億パラメータ）をMac上で4GB未満のメモリで動作させる方法を解説した。主要な新機能は以下の4点。①MLTensor型: SwiftにPythonのnumpy/torch tensorに相当する高水準テンソル操作APIが追加され、softmaxなどの演算が組み込みで提供される。従来はMLMultiArrayやMLShapedArrayを使いデータ格納のみに使用していたが、テンソル操作のためのカスタムコードが不要になった。②Stateful Buffers（ステートフルバッファ）: 従来のCore MLモデルはステートレス関数として動作し、KVキャッシュのような大容量の状態データを毎推論ステップでGPUとの間で送受信する必要があった。新機能ではGPU上にメモリブロックを確保したまま保持でき、LLMのKVキャッシュに適用することで推論速度が大幅に向上する。③ブロック単位量子化: WWDC 23のパレタイゼーション技術を発展させ、テンソル内の小領域ごとに複数のルックアップテーブル（LUT）を作成することで、大型モデルでも品質劣化を抑えながら4ビット精度（float32比8分の1、float16比4分の1）への圧縮を実現。Mistral 7BはInt4量子化モデル（StatefulMistralInstructInt4.mlpackage）として配布されている。④Multifunction Support: 単一の.mlpackageファイルに複数のモデルバリアント（例: prefillとgeneration）を格納できる機能。実行手順はswift-transformersのpreviewブランチをクローンし、HuggingFaceリポジトリから変換済みCore MLモデルをダウンロード後、`swift run transformers`コマンドで推論するだけ。変換ツールはcoremltools 8（beta）のct.convert()を使用し、StatefulMultiHeadAttentionクラスでKVキャッシュをステートフルバッファとして実装する。Apple Silicon搭載Macであればニューラルエンジン・GPU・CPUの3ユニットを統合活用できる。

## アイデア

- Stateful BuffersによるKVキャッシュのGPU常駐化は、推論ループのメモリ帯域ボトルネックを解消する設計パターンであり、他フレームワークのバッファ管理戦略と比較検討できる
- ブロック単位量子化（block-wise quantization）で70億パラメータモデルを4GB以下に収める手法は、エッジデバイスへのLLM展開における精度・サイズトレードオフの具体的事例として参照価値が高い
- MLTensor型の導入でSwiftのML開発体験がPythonに近づいたことは、iOSアプリ内にエージェント的なLLM推論ループを組み込む実装コストを大幅に削減する可能性を示す

## Yujiの取り組みへの示唆

監査エージェントをローカルLLMインフラ（RTX 3090予定）で動かす文脈では、Core MLのStateful BuffersとInt4量子化の組み合わせによる「70億パラメータモデルを4GB以下で実行」という実績値が、GPU VRAM予算とモデル選定の参考になる。またcoremltools 8のct.convert()やStatefulMultiHeadAttentionの実装パターンは、Ollamaやllama.cppと異なるアプローチとして、Macベースの開発機での軽量推論検証に活用できる。Apple Siliconへの依存があるためGALLERIA環境には直接転用できないが、KVキャッシュのステートフル管理設計はLangGraph上のエージェントループにおける状態管理の設計思想と対比して考察できる。

## 原文リンク

[WWDC 24: Core MLでMistral 7Bをオンデバイス実行する](https://huggingface.co/blog/mistral-coreml)
