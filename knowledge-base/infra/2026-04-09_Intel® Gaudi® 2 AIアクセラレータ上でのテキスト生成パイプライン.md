---
title: "Intel® Gaudi® 2 AIアクセラレータ上でのテキスト生成パイプライン"
url: "https://huggingface.co/blog/textgen-pipe-gaudi"
date: 2026-04-09
tags: [Intel Gaudi 2, Optimum Habana, Llama 2, LangChain, DeepSpeed, 分散推論, KV cache, HPU graphs, テキスト生成パイプライン]
category: "infra"
memo: "[HF Blog] Text-Generation Pipeline on Intel® Gaudi® 2 AI Accelerator"
processed_at: "2026-04-09T12:23:55.442918"
---

## 要約

本記事は、Intel® Gaudi® 2 AIアクセラレータ上でLlama 2ファミリー（7B・13B・70B）を使ったテキスト生成を、Optimum HabanaのカスタムパイプラインクラスGaudiTextGenerationPipelineを用いて実行する方法を解説している。

アーキテクチャ面では、このパイプラインはプロンプトの前処理・推論・後処理をエンドツーエンドで抽象化しており、`--use_hpu_graphs`（グラフコンパイルによる推論高速化）と`--use_kv_cache`（KVキャッシュによるデコード効率化）の2フラグが主要な最適化オプションとなっている。70Bモデルのような大規模モデルには、DeepSpeed（HabanaAI版 v1.14.0）を用いた8ノード分散推論が対応しており、`gaudi_spawn.py`経由で`--world_size 8`を指定して起動する。

使用方法は3パターン提供されている。(1) `run_pipeline.py`スクリプトをCLIから直接実行、(2) PythonスクリプトにGaudiTextGenerationPipelineクラスをインポートして組み込む、(3) LangChainのHuggingFacePipelineに`use_with_langchain=True`引数を渡して統合する。LangChain統合ではLLMChainやPromptTemplateと組み合わせてQAチェーンを構築可能であるが、バリデーション済みバージョンはlangchain==0.0.191に限定されている。

前提条件として、Llama 2はゲートリポジトリのため、MetaのWebサイトで利用規約への同意とHugging Faceでのアクセスリクエストが必要（承認まで1〜2日）。インストールはoptimum-habana==1.10.4とSynapseAI 1.14.0対応のDeepSpeedが必要。

生成パラメータとして`--temperature`・`--top_p`・`--max_new_tokens`・`--do_sample`が設定可能であり、複数プロンプトのバッチ処理にも対応している。Intel Gaudi 2はNVIDIA GPUに代わる選択肢として位置付けられており、オープンソースLLMの推論インフラ多様化という文脈で注目される実装例となっている。

## アイデア

- GaudiTextGenerationPipelineはuse_with_langchain=Trueフラグ1つでLangChainのHuggingFacePipelineに直接渡せる設計になっており、推論バックエンドをLangChainチェーンから完全に隠蔽できる抽象化が参考になる
- 70Bモデルの推論をDeepSpeedとgaudi_spawn.pyで8ノード分散化する構成は、単一GPUでは載らない大規模モデルを本番利用可能なスループットで動かすための実用的なパターンである
- HPU GraphsによるグラフコンパイルとKVキャッシュを組み合わせた推論最適化は、NVIDIAエコシステム以外でも同等の高速化手法が適用可能であることを示しており、ハードウェア非依存なLLM推論最適化の考え方として汎用性がある
## 関連記事

- /deep_1064 Intel Gaudi 2とXeonを活用したコスト効率の高いエンタープライズRAGアプリケーション構築
- /deep_1019 Intel Gaudi向けAssisted Generation（投機的サンプリング）の高速化サポート
- /deep_429 大規模AIシステムにおける戦略的レバーとしてのスループット最適化：データローダーとメモリプロファイリング革新からの証拠
- /deep_505 大規模AIシステムにおけるスループット最適化：データローダーとメモリプロファイリングの革新からの実証
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術

## 原文リンク

[Intel® Gaudi® 2 AIアクセラレータ上でのテキスト生成パイプライン](https://huggingface.co/blog/textgen-pipe-gaudi)
