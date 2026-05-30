---
title: "Jetson AGX XavierでQwen3.6-35B（MoE）をllama.cppで動かす"
url: "https://zenn.dev/nooop/articles/69f444fe13ecca"
date: 2026-05-30
tags: [Jetson AGX Xavier, llama.cpp, Qwen3, MoE, GGUF, 量子化, エッジAI, CUDA]
category: "infra"
related: [6360, 6478, 2862, 4744, 2292]
memo: "[Zenn LLM] Jetson AGX XavierでQwen3.6を動かす"
processed_at: "2026-05-30T09:02:46.336637"
---

## 要約

Jetson AGX Xavier（32GB RAM）上でQwen3.6-35B-A3BというMoEモデルをllama.cppを使ってローカル推論させた実験レポート。Jetson Orinでの動作実績を持つ同モデルをXavierでも試行している。

XavierはJetPack 5のEOLが迫っているデバイスであり、DockerイメージなしでCUDAアーキテクチャ72（SM 7.2）向けにllama.cppをソースビルドする必要がある。ビルド手順はaptの古いcmakeをpip経由でアップグレードし、`-DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=72`を指定してcmakeでビルドする。

試したモデルは2種類。①`Qwen3.6-35B-A3B-UD-IQ3_S.gguf`（13GB、極限量子化）: コンテキスト最大262,144トークン確保、推論速度15.15 tokens/sec、メモリ使用量20GiB（残9.6GiB）。②`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`（21GB、Q4_K_M量子化）: コンテキスト190,208トークン、推論速度14.95 tokens/sec、メモリ使用量26GiB（残3.1GiB）。

どちらも約15 tokens/secと実用的な速度を達成。比較としてJetson Orinが約28 tokens/secであることから、Xavierはその半分強の性能に相当する。最大消費電力が30W程度と省電力な点も特筆すべき特徴で、チャットや軽量エージェント用途には十分使える可能性がある。

Qwen3.6-35BはMoEアーキテクチャのため、総パラメータ数35Bに対して実際の推論時に活性化されるパラメータは3.6B相当（A3B）となり、同サイズのDenseモデルと比べてメモリ・演算効率が大幅に高い。これが32GBのエッジデバイスでも動作する理由となっている。実行スクリプトでは`-ngl 99`（全レイヤーGPUオフロード）、`--no-mmap`（mmap無効）、`--reasoning off`（思考モード無効）を指定している。

## アイデア

- MoEアーキテクチャ（35B総パラメータ／3.6B活性化）により、32GBエッジデバイスで35Bクラスモデルが15 tokens/secで動作する——Denseモデルなら物理的に不可能なサイズ感
- IQ3_S（13GB）とQ4_K_M（21GB）でほぼ同速度（15 tokens/sec）だが、メモリ消費は7GiB差——量子化レベルと速度は非線形で、MoEでは精度より帯域幅がボトルネック
- 消費電力30W・15 tokens/secという性能密度は、ローカルエージェントの常時稼働インフラとしてコスト面で現実的な選択肢になりうる

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **CUDA アーキテクチャ** (TODO: 読むべき)
- **Jetson JetPack** (TODO: 読むべき)

## 関連記事

- /deep_6360 【2026年最新】Qwen 3.6/3.7 ローカル運用完全ガイド ― 27B/35B-A3B 選定とMTP・TurboQuant攻略
- /deep_6478 Windows11 RTX 5090でAIエージェント用Qwen3.6-27B LLM環境構築
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_4744 LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開
- /deep_2292 8Bモデルが1GBに収まる1ビットLLM「Bonsai」を動かしてみた

## 原文リンク

[Jetson AGX XavierでQwen3.6-35B（MoE）をllama.cppで動かす](https://zenn.dev/nooop/articles/69f444fe13ecca)
