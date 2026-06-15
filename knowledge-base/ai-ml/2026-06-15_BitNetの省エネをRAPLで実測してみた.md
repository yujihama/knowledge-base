---
title: "BitNetの省エネをRAPLで実測してみた"
url: "https://zenn.dev/keison8864/articles/bitnet-energy-article"
date: 2026-06-15
tags: [BitNet, RAPL, 省エネ, CPU推論, 量子化, 1bit LLM, メモリ律速, ベンチマーク, Qwen2.5, i2_s]
category: "ai-ml"
related: [4472, 1116, 4911, 4332, 1249]
memo: "[Zenn LLM] BitNetの省エネをRAPLで実測してみた"
processed_at: "2026-06-15T09:03:13.493070"
---

## 要約

Microsoft公式のBitNet b1.58技術レポートが示す「Qwen2.5比で約12倍省エネ」という数値は、演算エネルギーモデル（7nmプロセスでINT8加算0.007pJ、INT8乗算0.07pJ等の係数）による推定値（Energy Estimated）であり、実機計測値ではない。この記事では、Core i7-14700KF搭載のデスクトップPC上でIntel RAPL（Running Average Power Limit）を用いて実際のエネルギー消費を計測し、公式推定値を独立検証した。

RAPLはCPU内蔵のエネルギーカウンタ（energy_uj）を差分法で読み取る仕組みで、外部電力計不要・ソフトから1行で計測可能。計測はdecode 128トークン分の差分（-n8と-n136の2回生成）を取り、待機電力（約9W）を差し引いたnet J/tokenを指標とした。

主な実測結果は以下の通り。BitNet b1.58-2B(i2_s, 2.41B)とQwen2.5-1.5B(Q8_0, 1.54B)の対決では、net J/tokenは1.961対2.473で比率1.26倍（約21%省エネ）。公式推定の12倍と1桁異なる。decode中のCPUパッケージ電力は両モデルともほぼ110Wで一定であり、省エネの主因は低消費電力ではなくスループット（BitNet: 50.7 t/s、Qwen1.5B: 41.5 t/s）の差に帰着する。

パラメータ規模を近づけたQwen2.5-3B-Instruct(Q4_K_M, 3.09B)との比較では、BitNetはnet 0.58倍（42%省エネ）・1.55倍速・RSS 0.47倍を達成。ただし精度（lm-eval: arc_easy/hellaswag/lambada_openai平均）はBitNet 67.17%対Qwen3B 71.25%で-4.1pt劣る。3モデルを「精度 vs net J/token」空間にプロットすると全点がパレートフロンティア上に乗り、BitNetは最小エネルギー端を占める。

理論利得が実機で縮む理由は2点。①x86のAVX2はMAC（積和）命令しか持たず、BitNetのi2_sカーネルも三値重みをint8展開してAVX2に流すため「乗算ゼロ」が実体化しない。②decode局面はメモリ律速であり、省エネ源泉は演算削減より2bitの小さい重みによるメモリ転送量削減（Q8の1/4）にある。副産物として、Q4_K_MカーネルではCPU電力が119Wに上振れし「decode電力一定≈110W」近似が崩れることも観測された。監査エージェント開発への示唆：エッジ推論やCPUオンリー環境でのコスト計算に公式の推定エネルギーをそのまま使うと1桁過大評価になるリスクがある。実機RAPLによるベンチマークを行うか、gross J/tokenベースで比較する習慣が重要。

## アイデア

- 「12倍省エネ」は演算エネルギーモデルの推定値であり、実機x86では1.3〜1.7倍に収まる。差の正体はAVX2がMAC専用でAC専用命令を持たないというISA制約と、decode時の定常消費電力（約110W）の存在
- BitNetの省エネ源泉は「演算削減」より「メモリ転送量削減（2bit vs 8bit）」にある。decode局面はメモリ律速なのでデータ幅が直接スループットに効く、という構造はモデル選定の設計指針として重要
- 「精度 vs 実測エネルギー」の3点パレートフロンティア分析：公式はメモリ vs 性能で示しているが、実測J/tokenを軸にしたパレート分析は別の一次データとなり、コスト最適なモデル選択の根拠として使える

## 前提知識

- **BitNet b1.58（三値量子化LLM）** (TODO: 読むべき)
- **RAPL（Intel電力計測API）** (TODO: 読むべき)
- **Post-Training Quantization（PTQ）** (TODO: 読むべき)
- **AVX2 / SIMD** (TODO: 読むべき)
- **メモリ律速（Memory Bandwidth Bound）** (TODO: 読むべき)

## 関連記事

- /deep_4472 7年前のChromebookでローカルLLMは動くのか？ Trillim + Ternary Bonsai を Crostini で試す
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_1249 スマホより小さい。1ビットLLMが「AIをどこでも動かす」時代を本当に変えるかもしれない話

## 原文リンク

[BitNetの省エネをRAPLで実測してみた](https://zenn.dev/keison8864/articles/bitnet-energy-article)
