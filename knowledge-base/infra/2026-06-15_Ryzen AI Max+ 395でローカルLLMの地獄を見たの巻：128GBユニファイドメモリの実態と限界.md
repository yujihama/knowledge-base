---
title: "Ryzen AI Max+ 395でローカルLLMの地獄を見たの巻：128GBユニファイドメモリの実態と限界"
url: "https://zenn.dev/shuzan/articles/0605b909fb23e4"
date: 2026-06-15
tags: [Ryzen AI Max+ 395, ROCm, llama.cpp, Vulkan, ローカルLLM, ユニファイドメモリ, メモリ帯域, KVキャッシュ, Strix Halo, RDNA 3.5]
category: "infra"
related: [7838, 6360, 3909, 4331, 5724]
memo: "[Zenn LLM] Ryzen AI Max+ 395でローカルLLMの地獄を見たの巻"
processed_at: "2026-06-15T09:06:28.881698"
---

## 要約

AMD Ryzen AI Max+ 395（Strix Halo、128GB ユニファイドメモリ）上でローカルLLMを9ヶ月運用した実体験レポート。結論は「128GBに巨大モデルが載る」と「使える」は別物、という一点に尽きる。

【帯域の罠】LLM decode はメモリ帯域律速。理論ピーク256GB/sに対し、合成コピー最大値は約212〜215GB/s（83%）、llama-benchの実生成逆算値は約158〜170GB/s（62〜66%）。RTX 3090の936GB/sと比較して約1/6。Qwen2.5-72B（Q4_K_M、47GB）をロードすると160÷47≈3.4tok/sが理論上限となり、会話が成立しない。32〜35B級（QwQ-32B、Qwen3.5-35B-A3B）が実用の上限。

【KVキャッシュの殺傷力】Gemma 4 26B-A4B-it（Q5_K_M、重み約20GB）で-c 262144 --parallel 2を指定するとKVキャッシュが約5720MiBに膨らみOOM-kill→GPU page fault 380件→Vulkan DeviceLost→システムフリーズ。128Kコンテキストは動くが256Kは箱ごと死ぬ。大型RAGや長時間エージェントセッションという購入動機そのものが潰される。

【iGPU演算力】Radeon 8060S（40CU、RDNA 3.5）は8192²のmatmulで素のパスだと約3TFLOPS。hipBLASLtが効けば約37TFLOPS（理論59TFLOPSの6割超）の報告もあるが、ソフトウェアスタックがシリコンを引き出せていないのが実態。画像生成はRTX 4090比3〜4倍遅い。

【NPU未活用】XDNA 2 NPU（約50TOPS）はllama.cpp/vLLM/Ollamaの主流ルートから使えない。FastFlowLMかRyzenAI SDKのみ対応。

【エコシステム地獄】ROCm 6.xは完全に門前払い（error -22）。ROCm 7.2.1（2026年3月）でようやく公式production support入りしたが、PyTorchホイールは毎回手動DL＋インストール必須。pip installが依存解決でCUDA版torchを引き込み環境を破壊するケースも頻発。llama.cppはHIPバックエンドが不安定でVulkan一択。そのVulkanビルドもUbuntu 24.04同梱のglslcが古くシェーダコンパイルで失敗し、shadercをソースビルドして回避。vLLMは9ヶ月間一度も推論到達できず。

【現在の安定構成】llama.cpp + Vulkan（Mesa RADV）+ Gemma 4 26B-A4Bのみ。監査エージェント開発への示唆：エージェントの長時間セッションや大規模RAGを想定するなら、コンテキスト長とKVキャッシュのメモリ圧迫が致命的になりうる。NVIDIA dGPU前提のフレームワーク（vLLM等）との互換性も低く、本番エージェント基盤としてのリスクは高い。

## アイデア

- メモリ帯域律速の定量化手法：llama-benchのtg（tok/s）×モデルサイズから実効帯域を逆算し、理論値・合成ピーク・実生成実効の三層で比較する手法は、任意のハードでの推論速度予測に転用できる
- KVキャッシュのメモリ消費はコンテキスト長の二乗ではなく線形だが、重み＋KV＋計算バッファの三者競合が128GB級の大容量でも長文推論を現実的に阻む点は、RAGシステム設計時のチャンクサイズ・並列数戦略に直結する
- AI推論スタックにおけるNVIDIA CUDAの支配力の実証：同等スペックのAMD iGPUでも、ソフトウェアエコシステムの成熟度差（llama.cpp HIPが不安定でVulkan一択、vLLM未到達）が実用性を決定する好例

## 前提知識

- **メモリ帯域律速** → /deep_8103 DiffusionGemmaはなぜ4倍速いのか：速さの正体はメモリ帯域で、クラウドでは逆に高くつく
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **ROCm / HIP** (TODO: 読むべき)
- **llama.cpp GGUF** (TODO: 読むべき)
- **RDNA アーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_7838 「AI PC」は本当にAIできるのか？──Copilot+ PC 4プラットフォーム比較（2026年5月版）
- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る
- /deep_5724 LLMをINT4に量子化したら、GPUはもう要らない？──エンジニアの直感を検証する

## 原文リンク

[Ryzen AI Max+ 395でローカルLLMの地獄を見たの巻：128GBユニファイドメモリの実態と限界](https://zenn.dev/shuzan/articles/0605b909fb23e4)
