---
title: "RTX 4080（16GB VRAM）でローカルLLM 12モデルを実測：「15GBの壁」とOllama vs vLLMの比較"
url: "https://zenn.dev/seeda_yuto/articles/ollama-vs-vllm-rtx4080-benchmark"
date: 2026-06-04
tags: [Ollama, vLLM, RTX4080, VRAM, MoE, GGUF, gpt-oss, Qwen3.5, ローカルLLM, ベンチマーク]
category: "infra"
related: [4332, 7111, 5469, 2862, 6668]
memo: "[Zenn LLM] RTX 4080でローカルLLM 7モデルを実測したら「16GB VRAMの壁」が見えた"
processed_at: "2026-06-04T09:22:32.222726"
---

## 要約

RTX 4080（16GB VRAM）上でOllamaとvLLMの2バックエンド、12モデルを実測したベンチマーク記事。最大の発見は「16GB VRAMにおける15GBの壁」で、GGUFサイズが15GB以下のモデルはGPU完全搭載で43〜234 tok/sを達成するが、15GBを超えた瞬間にCPUオフロードが発生し0.9〜12 tok/sまで100倍以上低下する。MoEアーキテクチャはアクティブパラメータが少ないため推論時のVRAM消費が小さく有利だが、GGUFサイズはアクティブパラメータではなく全パラメータ量に依存するため、「MoEだから軽い」は誤りであり実際のGGUFサイズで判断する必要がある。バックエンド比較では、gpt-oss:20bをOllamaで動かすと125 tok/sだが、vLLMでは22 tok/sとOllamaの約1/6に留まる。原因はモデルが13.72GiBを占有しKVキャッシュに0.16GiBしか残らない点、CUDA graphsが使えない点、シングルユーザー環境ではバッチ処理の利点がない点の3つ。Ollamaの最適化として、OLLAMA_KEEP_ALIVE=-1（モデル常駐）を設定するだけでwall timeが5.2s→0.9sに改善される。速度1位のdeepseek-coder-v2:16b（234 tok/s、8.9GB）は推論パズル「17匹の羊から9匹以外全部死んだ」の問題を誤答（8匹と回答）し、総合1位のgpt-oss:20b（125 tok/s、13GB）は正答（9匹）。コード品質テストでもgpt-ossはfunctools.lru_cacheの使用や型ヒント・計算量の明示など、プロダクション品質の出力を返した。軽量・高品質のバランスではqwen3.5:9b（80 tok/s、6.6GB）が推論パズルに正答し実用性が高い。結論として16GB VRAM環境ではgpt-oss:20bとOllamaの組み合わせが最適解で、モデル選定基準はスペック表のパラメータ数ではなくGGUFの実サイズで判断すべきとされる。監査エージェント開発への示唆として、エージェントが利用するローカルLLMを選定する際は速度ベンチマークだけでなく論理推論タスクでの品質検証が不可欠であり、gpt-oss:20bのように125 tok/sの速度と高い推論精度を両立するモデルがツール呼び出しや複数ステップの判断を要するReActエージェントのバックエンドとして有望である。

## アイデア

- GGUFサイズ15GBを超えた瞬間に速度が100倍以上低下する「クリフエッジ」現象：MoEのアクティブパラメータが小さくても量子化後のGGUFサイズは全パラメータ数に依存するため、モデル選定はスペック表のパラメータ数ではなくGGUFの実ファイルサイズで判断しなければならない
- vLLMはA100/H100などの大容量VRAMと複数同時ユーザー環境でのみ優位であり、16GB単一GPUではKVキャッシュ残量不足・CUDA graphs制限・バッチ効果なしの三重苦でOllamaの1/6の速度に留まる：バックエンド選択はGPUメモリ容量とユーザー数によって決定的に異なる
- 速度2倍の差よりも推論精度の差が実務では大きい：deepseek-coder-v2:16bは234 tok/sだがall-but-9の語義解釈を誤り実用エージェントには不適、gpt-oss:20bは125 tok/sで正答しコード品質もプロダクションレベル——速度ベンチマーク単体での意思決定は危険

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **GPUオフロード** (TODO: 読むべき)
- **CUDA graphs** → /deep_649 Inference Endpoints で実現する超高速 Whisper 音声認識（最大8倍高速化）

## 関連記事

- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_7111 【2026年最新】LFM2.5-8B-A1BをApple Siliconで実測 — 「1月のLFM2.5」との違いと実際の速度
- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_6668 M5 Max のローカル LLM ベンチ — MoE は GPU 性能、Dense はメモリ帯域幅がボトルネック、発熱の影響も調査

## 原文リンク

[RTX 4080（16GB VRAM）でローカルLLM 12モデルを実測：「15GBの壁」とOllama vs vLLMの比較](https://zenn.dev/seeda_yuto/articles/ollama-vs-vllm-rtx4080-benchmark)
