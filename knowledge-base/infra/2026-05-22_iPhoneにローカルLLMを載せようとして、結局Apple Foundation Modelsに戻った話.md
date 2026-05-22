---
title: "iPhoneにローカルLLMを載せようとして、結局Apple Foundation Modelsに戻った話"
url: "https://zenn.dev/kitadesign/articles/iphone-local-llm-back-to-afm"
date: 2026-05-22
tags: [CoreML, Apple Foundation Models, iPhone, LLM推論, メモリ制約, Qwen, ANE, 4bit量子化, jetsam, transformers]
category: "infra"
related: [1529, 1266, 1807, 1760, 1936]
memo: "[Zenn LLM] iPhone にローカル LLM 載せようとして、 結局 Apple Foundation Models に戻った話"
processed_at: "2026-05-22T09:07:03.217736"
---

## 要約

iOS 26から正式APIとして利用可能なApple Foundation Models（AFM）が既に動作していたにもかかわらず、QwenやLlamaなどのオープンソースモデルをiPhone上で動かすことを1週間試みた実験記録。動機はAFMのロールプレイ口調の不安定さ（セッション内で繰り返し同じフレーズを生成する既知バグ）と、Apple Neural Engine（ANE）をより活用したいというロマン。

試行フェーズは段階的に失敗を重ねた。まずHuggingFace HubにあるCoreML変換済みQwen 2.5 0.5Bを使ったが、5.6〜7.1 tok/sと低速で、ハルシネーションも多く品質不足と判断。次に3Bモデルの自前CoreML変換pipelineを構築し、transformersからのload→ANE向けリライト（RMSNorm→LayerNorm置換、chunked SDPA、KV cacheの静的化、RoPE事前計算）→torch.jit.traceでIR化→coremltools.convert→4bit palettize→xcrun coremlcompilerという変換フローを組んだ。しかし変換時にtransformers 5.xの内部API移行（cache_positionの廃止）によるIndexErrorが発生し変換自体が失敗。

またスクリーニング段階でGemma 3 4Bはbf16学習モデルをfp16推論したことでattention logitがfp16の最大値（約65504）を超えてオーバーフローし、全tokenが<pad>（id=0）になるサイレント障害が発生。Qwen 2.5 7BはM2 MacBook Pro 24GBでもOOMとなりiPhone 15の8GB RAMでは到底動かないことが確認された。

方針を転換してHuggingFace Hubのfinnvoorheesによるcoreml-*-4bitシリーズを利用。SmolLM2 360M（220MB）は動作するが命令追従能力が弱くプロンプトをそのままecho出力するだけ。SmolLM2 1.7B（1.0GB）とLlama 3.2 3B（1.9GB）はmlmodelcロード時にメモリ不足（エラーコード-14）で失敗。Qwen 2.5 3B（実DL量400MB、4bit per_grouped_channel+group_size=32圧縮）はロードに成功したが推論中にKV cache＋activations＋tokenizer＋アプリ本体でメモリpickが3〜4GBを超え、iOSのOOMキラー（jetsam）により強制終了。

結論：iPhone 15 Pro（8GB RAM、アプリ利用可能枠3〜4GB）では「動くサイズ（〜400MB以下）は命令追従能力不足」「品質が出るサイズ（3B以上）はロード失敗またはjetsam death」という二律背反があり、sweet spotが存在しない。AFMはAppleが変換・最適化を全て担っており、iOS 26以降を対象とする個人開発であればAFMを第一選択にすべき。CoreML変換を自前で行う場合はtransformers 4.45〜4.55系にpinし、Gemmaはbfloat16必須という点に注意が必要。

## アイデア

- iPhone 15 Proの8GB RAMでもアプリ利用可能枠は3〜4GBに限られ、4bit圧縮の1.7B以上モデルはmlmodelcロード時のpeak memory（weights×2〜3倍）で既に限界を超える——端末スペックとアプリ実効メモリの乖離は見落とされやすい設計上の罠
- Gemma系モデルがbf16→fp16変換でattention logitがオーバーフローし全出力が<pad>になるサイレント障害は、量子化や型変換の際に精度範囲の検証が不可欠であることを示す具体的な事例
- transformers 5.xの内部API移行期（cache_position廃止）がtorch.jit.traceのIndexErrorを引き起こす問題は、モデル変換パイプラインにおけるライブラリバージョンのpinning管理の重要性を実証している

## 前提知識

- **CoreML** (TODO: 読むべき)
- **Apple Neural Engine** (TODO: 読むべき)
- **4bit量子化** → /deep_6122 Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）
- **torch.jit.trace** (TODO: 読むべき)
- **jetsam（iOS OOM killer）** (TODO: 読むべき)

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1807 🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法

## 原文リンク

[iPhoneにローカルLLMを載せようとして、結局Apple Foundation Modelsに戻った話](https://zenn.dev/kitadesign/articles/iphone-local-llm-back-to-afm)
