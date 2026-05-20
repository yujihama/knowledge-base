---
title: "Gemma 4 E4BをMacでローカル量子化してみた（llama.cpp + Q4_K_M）"
url: "https://zenn.dev/monjofight/articles/4a2b3393581229"
date: 2026-05-20
tags: [llama.cpp, GGUF, Q4_K_M, 量子化, Gemma, LocalLLM, Apple Silicon, Metal, k-quants, Hugging Face]
category: "infra"
related: [3653, 4744, 3901, 3909, 5903]
memo: "[Zenn LLM] Gemma 4 E4Bをローカルで量子化してみた"
processed_at: "2026-05-20T09:01:16.162566"
---

## 要約

MacBook Pro（M2 Pro / 32GBメモリ）上でGoogleのGemma 4 E4B-itモデルをllama.cppを用いてGGUF形式に変換し、Q4_K_M量子化を実施した実践レポート。

量子化の手順は大きく4段階：①llama.cppをMetal対応（-DGGML_METAL=ON）でビルド（約2分）、②uvでPython環境を構築しHugging Face経由でモデル（約16GB）をダウンロード、③convert_hf_to_gguf.pyでsafetensors→BF16 GGUFに変換（約14GB、2分24秒）、④llama-quantizeでQ4_K_M形式に変換（5GB、77秒）。

Q4_K_Mの「K」はk-quantsと呼ばれる手法を指し、「M」はmedium（中程度のサイズ・精度）を意味する。重要な点として、Q4_K_Mは全重みを一律4bitにするのではなく、アテンション層のv_weight（blk.N.attn_v.weight）やffn_down.weightをq6_K（6bit相当）で保持しつつ、ffn_gate/ffn_upをq4_K（4bit）で量子化するなど、レイヤーごとに精度を使い分けている。規格化パラメータ（attn_norm.weight等）はf32のまま保持される。

ベンチマーク結果：F16版（14GB）はpp128=349t/s・tg128=12.3t/s、Q4_K_M版（4.95GB）はpp128=309t/s・tg128=24.7t/sで、トークン生成速度が約2倍に向上。プロンプト処理速度はわずかに低下するが実用上の問題は小さい。

動作確認では「9.11 vs 9.9」「strawberryのr数」「Sallyの姉妹問題」の3問すべてに正解（約30t/s）。モデルの論理推論・文字カウント能力は量子化後も維持されていることを確認。

今回未実施の課題として、定量的な精度劣化評価（評価データセットによるQ4 vs Q5 vs Q8比較）が挙げられており、実用上の最適量子化レベルの特定が今後の課題。ローカルLLMインフラ構築の観点では、llama.cpp + GGUF + Metal対応ビルドがMac環境において最も現実的な選択肢であることが示された。

## アイデア

- Q4_K_Mは全重みを一律4bitにするのではなく、attn_v.weightやffn_downはq6_K（6bit）で保持するなどレイヤーごとに精度を使い分ける設計になっており、モデル品質とサイズ削減のトレードオフを細粒度で制御している
- BF16（14GB）→Q4_K_M（5GB）でサイズが約65%削減される一方、トークン生成速度（tg128）は12.3→24.7t/sと約2倍に向上し、プロンプト処理（pp128）は349→309t/sとわずかに低下するという非対称なトレードオフ構造
- hf-xetライブラリ（Hugging Hubの高速ダウンロード機能）がモデルダウンロードと干渉する問題が発生しており、ツールチェーンの依存関係管理の複雑さが実践的なハードルになっている

## 前提知識

- **GGUF形式** (TODO: 読むべき)
- **k-quants** (TODO: 読むべき)
- **llama.cpp** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **Apple Metal** (TODO: 読むべき)
- **safetensors** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは

## 関連記事

- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_4744 LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開
- /deep_3901 ペットの言語中枢を作った話 — デジタルAIペット（仮称）Phase 1
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_5903 dGPUなしRyzen AIラップトップでローカルLLMは動くのか：CPU・NPU・iGPU実測比較

## 原文リンク

[Gemma 4 E4BをMacでローカル量子化してみた（llama.cpp + Q4_K_M）](https://zenn.dev/monjofight/articles/4a2b3393581229)
