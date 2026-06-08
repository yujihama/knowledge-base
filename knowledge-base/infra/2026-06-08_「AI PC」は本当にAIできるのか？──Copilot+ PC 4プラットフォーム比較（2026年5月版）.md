---
title: "「AI PC」は本当にAIできるのか？──Copilot+ PC 4プラットフォーム比較（2026年5月版）"
url: "https://zenn.dev/omohikane/articles/ai_pc_comparison_blog_v3"
date: 2026-06-08
tags: [ローカルLLM, llama.cpp, FastFlowLM, AMD XDNA 2, NPU, iGPU, Vulkan, MoE, Copilot+ PC, メモリ帯域, Snapdragon X Elite, Apple M4, Linux]
category: "infra"
related: [5903, 5724, 6360, 2862, 4744]
memo: "[Zenn LLM] 「AI PC」は本当にAIできるのか？──Copilot+ PC 4プラットフォーム比較（2026年5月版）"
processed_at: "2026-06-08T21:05:13.160818"
---

## 要約

2024年から普及した「AI PC」「Copilot+ PC」マーケティングにおいて、NPU（Neural Processing Unit）がローカルLLM推論に実際に貢献するかを、32GB統一条件でAMD Strix Point・Intel Lunar Lake・Snapdragon X Elite・Apple M4の4プラットフォームで比較した記事。

**NPUの実態**：各社NPUはいずれも40 TOPS超を達成するが、LLM推論への貢献は大きく異なる。AMD XDNA 2はFastFlowLMランタイムにより実用域に到達し、Llama 3.2 3Bで約28 tok/s、4Bクラスで10〜14 tok/sを達成。消費電力は2W未満でiGPU推論（約25W）の1/10以下。IntelのNPUは実用的な推論パスが存在せず、SnapdragonはONNX Runtime QNN経由でprefillのみCPUより速いがdecodeで負ける。MacはNeural EngineよりMetalが上位互換のため出番なし。

**メモリ帯域比較**：LLM推論はメモリ帯域律速であり、Mac M4が120 GB/s、Snapdragon X Eliteが135 GB/s、Intel Lunar Lakeが137 GB/s、AMD Strix PointのLPDDR5X構成が128 GB/sに対し、SO-DIMM DDR5構成は約90 GB/sと劣る。ただしAMDはSO-DIMMにより最大256GBまで拡張可能という唯一の優位性を持つ。

**iGPU推論実測**：7〜8Bモデルの tok/sはAMD 890M（Vulkan）が17〜18、Intel Arc 130V（Vulkan）が約23、Snapdragon（CPU推論のみ）が約20、Mac M4（Metal）が約24。SnapdragonはVulkanバックエンドで出力が壊れるためCPU推論一択で、全コア占有による他作業への影響が課題。

**AMD二刀流運用**：AMD XDNA 2搭載機ではNPU推論（FastFlowLM、1〜4B、省電力）とiGPU推論（llama.cpp Vulkan、7〜20B、汎用）を用途別に使い分け可能。NPU推論中はiGPUが完全に空くため、ブラウザやビルド作業との共存が実現できる。

**MoEモデルの影響**：Qwen3-Coder-30B-A3Bのようなアクティブパラメータ3BのMoEモデルは、帯域消費が3B相当でありながら32GBに収まる（Q4_K_M で約17GB）。AMD SO-DIMM DDR5環境（約90 GB/s）での実測で36.7 tok/sを達成しており、「Dense 14〜20Bが快適上限」という従来の前提が崩れている。

**Linux対応**：AMDが最良（◎）、Intelが良好（○）、Mac M4はAsahi Linuxが未対応（TBA）、SnapdragonはUbuntu 26.04でもファームウェアツールが壊れており事実上壊滅（✗）。ローカルLLMをLinuxで運用する場合、現時点でAMDが最も適した選択肢となる。

## アイデア

- NPU推論（<2W）とiGPU推論（~25W）の二刀流運用は、バックグラウンド常駐エージェント（NPU）と重い推論タスク（iGPU）の役割分担として監査エージェントのローカル運用に応用できる
- MoEアーキテクチャによりアクティブパラメータと総パラメータが乖離するため、「何Bモデルが動くか」の評価軸が容量律速と帯域律速の2軸に分離される──RAGパイプラインのモデル選定基準として重要な視点
- FastFlowLMの256kトークンロングコンテキスト対応と省電力特性は、監査ドキュメントの長文処理をバックグラウンドで常駐実行するユースケースに直接対応する

## 前提知識

- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **メモリ帯域律速** (TODO: 読むべき)
- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **量子化（GGUF/Q4_K_M）** (TODO: 読むべき)
- **NPU/iGPU** (TODO: 読むべき)

## 関連記事

- /deep_5903 dGPUなしRyzen AIラップトップでローカルLLMは動くのか：CPU・NPU・iGPU実測比較
- /deep_5724 LLMをINT4に量子化したら、GPUはもう要らない？──エンジニアの直感を検証する
- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_4744 LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開

## 原文リンク

[「AI PC」は本当にAIできるのか？──Copilot+ PC 4プラットフォーム比較（2026年5月版）](https://zenn.dev/omohikane/articles/ai_pc_comparison_blog_v3)
