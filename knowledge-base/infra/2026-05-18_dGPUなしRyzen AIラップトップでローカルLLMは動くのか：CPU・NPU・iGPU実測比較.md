---
title: "dGPUなしRyzen AIラップトップでローカルLLMは動くのか：CPU・NPU・iGPU実測比較"
url: "https://zenn.dev/omohikane/articles/thinkpadx13g6-localllm"
date: 2026-05-18
tags: [LocalLLM, Ollama, llama.cpp, NPU, XDNA2, Vulkan, Ryzen AI, FastFlowLM, Radeon 860M, GGUF, Qwen3, ベンチマーク]
category: "infra"
related: [2862, 5399, 5839, 4332, 3653]
memo: "[Zenn LLM] dGPUなしRyzen AIラップトップでローカルLLMは動くのか：CPU・NPU・iGPU実測比較"
processed_at: "2026-05-18T09:03:17.527538"
---

## 要約

ThinkPad X13 Gen6（AMD Ryzen AI 7 PRO 350、32GB RAM、Radeon 860M iGPU、XDNA 2 NPU）を使い、dGPU非搭載環境でのローカルLLM推論を3段階で検証した記事。

**Phase 1: CPU推論（Ollama）**
gemma3:4BをQ4_K_M量子化で実行すると、Prefill 73.6 tok/s・Decode 20.9 tok/s。4Bモデルなら実用ラインだが、全コアが100%に張り付き他作業との並行が困難。MoE構造のqwen3.6:35b-a3b（活性3B）は9.86 tok/sに留まり、全expertの重みをRAMから読む帯域コストが原因と分析。

**Phase 2: NPU推論（FastFlowLM）**
XDNA 2（INT8 50TOPS）専用ランタイムFastFlowLMを使用。Qwen3:4BでPrefill 490〜597 tok/s・Decode 22.4 tok/s（1kコンテキスト）を達成。PrefillはCPU比約7倍。CPU使用率はわずか5%で他作業への影響が最小限。ただしコンテキスト32kでは296 tok/s・7.6 tok/sまで劣化し、対応モデルがFastFlowLM変換済みの36モデルに限定される点が最大の制約。パッケージ温度は81°Cに達するが、体感はCPU推論より快適。「長い入力・短い出力」タスク（コードレビュー、ログ分析、Embedding生成）に適する。

**Phase 3: iGPU推論（llama.cpp + Vulkan）**
Radeon 860M（RDNA 3.5、8CU/512シェーダ）でllama.cppのVulkanバックエンドを使用。Qwen3-4B Q4_K_MでPrefill 352 tok/s・Decode 18.5 tok/s。CPUのDecode（20.9）にすら負ける結果。原因はgfx1150アーキテクチャのVulkanカーネル最適化不足、Vulkan APIのデータ転送オーバーヘッド、CPU/iGPU/NPUによるLPDDR5xバス共有。GTTメモリをカーネルパラメータ（amdttm.pages_limit）で16GBに拡張することでQwen3-14Bの動作に成功したが、速度は実験用途止まり。

**総括**
Ryzen AIラップトップの実用的価値は「dGPU級の速度」ではなく「CPUとNPUの使い分け」にある。NPUは省電力・低CPU負荷でPrefill高速という特性から、コード補完やログ分類など業務用途に実用的に使える可能性がある。監査エージェント開発文脈では、ログ分析・タグ付け・Embedding生成といった「入力長・出力短」タスクにNPU推論を組み込むアーキテクチャが有望。

## アイデア

- NPUはPrefillが爆速（CPUの7倍）だがDecodeは普通という非対称な性能特性から、「入力長・出力短」タスクに特化した推論パイプライン設計が有効になる
- GTTメモリ拡張（amdttm.pages_limitカーネルパラメータ）でiGPUの利用可能メモリを動的に拡張し、14Bモデルをdishなしで動作させる手法は省コストなLLMインフラの選択肢になる
- MoEモデル（qwen3.6:35b-a3b）はアクティブパラメータ3Bでも全expertをRAMから読む帯域コストがボトルネックになり、パラメータ数だけでは推論速度を予測できないことを実測で示している

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **MoEアーキテクチャ** → /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- **Vulkanバックエンド** (TODO: 読むべき)
- **NPU推論** (TODO: 読むべき)
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_5399 1-bit 8B×8アンサンブル vs Q4×1：RTX 4080でHumanEval実測比較
- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価

## 原文リンク

[dGPUなしRyzen AIラップトップでローカルLLMは動くのか：CPU・NPU・iGPU実測比較](https://zenn.dev/omohikane/articles/thinkpadx13g6-localllm)
