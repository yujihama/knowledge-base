---
title: "Intel CPU上でVLMを3ステップで動かす方法（OpenVINO + SmolVLM2）"
url: "https://huggingface.co/blog/openvino-vlm"
date: 2026-04-05
tags: [OpenVINO, SmolVLM2, Optimum Intel, 量子化, INT8, VLM, エッジ推論, Intel CPU, Post-Training Quantization]
category: "infra"
memo: "[HF Blog] Get your VLM running in 3 simple steps on Intel CPUs"
processed_at: "2026-04-05T12:08:49.243477"
---

## 要約

本記事は、Vision Language Model（VLM）をGPUなしのIntel CPU上でローカル実行するためのチュートリアルである。使用するモデルはHuggingFace製のSmolVLM2-256M-Video-Instructで、Optimum IntelとOpenVINOを組み合わせて最適化・推論を行う。

**Step 1: モデル変換**
PyTorchモデルをOpenVINO IR形式に変換する。CLIツール（optimum-cli export openvino）またはPythonコード（OVModelForVisualCausalLM.from_pretrained）のいずれかで実行可能。

**Step 2: 量子化**
2種類のPost-Training Quantization（PTQ）手法を提供する。①Weight Only Quantization（WOQ）: 重みのみをFP32からINT8に変換。精度劣化が少なく導入しやすい。OpenVINO 2024.3以降は実行時にアクティベーションも量子化されるため追加の高速化が得られる。②Static Quantization: 重みとアクティベーションを両方量子化する。キャリブレーション用に50サンプルのデータセットを使用し、ビジョンエンコーダにはStatic Quantization、言語モデル部分にはWOQを適用するハイブリッド構成（OVPipelineQuantizationConfig）も可能。複数画像入力で短い応答が必要なシナリオで有効。

**Step 3: 推論実行**
model.generate()で推論実行。Intel GPU（ Arc等）がある場合はdevice='gpu'を指定可能。

**ベンチマーク結果（Intel CPU、単一画像入力）:**
- PyTorch: TTFT 5.150秒、TPOT 1.385秒、スループット 0.722 tokens/s
- OpenVINO（FP32）: TTFT 0.420秒（12倍高速化）、スループット 47.237 tokens/s
- OpenVINO INT8 WOQ: TTFT 0.247秒（約21倍高速化）、スループット 63.928 tokens/s

OpenVINO変換だけでPyTorchと比較してTTFTが12倍改善し、INT8量子化を加えると21倍改善・スループットは88倍以上になる。インターネット接続不要・データがローカルに留まるプライバシー面のメリットもある。デモはIntel Xeon（Sapphire Rapids）第4世代上で動作確認済み。

## アイデア

- PyTorch比でOpenVINO変換のみで12倍、INT8量子化追加で21倍のTTFT高速化という具体的な数値は、ローカルLLMインフラ構築時の技術選定の判断材料として参考になる
- OVPipelineQuantizationConfigによるコンポーネント別量子化戦略（ビジョンエンコーダにStatic、LMにWOQ）は、モデルの構造に応じて精度と速度をトレードオフする細粒度な最適化手法として興味深い
- SmolVLM2-256Mという256Mパラメータの超小型マルチモーダルモデルがIntel CPUで実用的な速度（63 tokens/s）で動作する事実は、エッジ・オンプレミス環境でのVLM活用の現実性を示している

## Yujiの取り組みへの示唆

監査エージェントシステムにおいて、財務書類・帳票・スキャンした証跡書類などの画像をVLMで解析するユースケースが考えられる。GALLERIA XA7C-R37T（RTX 3090予定）環境だけでなく、社内のIntel CPUマシン上でもSmolVLM2 + OpenVINOを使えば画像入力を含む監査エージェントをオンプレミスで動かせる可能性がある。ただしSmolVLM2は256Mパラメータの軽量モデルであり、複雑な監査文書の読み取り精度については別途評価が必要。

## 原文リンク

[Intel CPU上でVLMを3ステップで動かす方法（OpenVINO + SmolVLM2）](https://huggingface.co/blog/openvino-vlm)
