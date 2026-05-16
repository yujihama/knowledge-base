---
title: "ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測"
url: "https://zenn.dev/tktomaru/articles/20260430_local_llm_compare"
date: 2026-05-08
tags: [Ollama, ローカルLLM, gemma3, qwen3, gpt-oss, ベンチマーク, VRAM, 量子化, Q4_K_M, Chain-of-Thought, 思考トークン, RTX4060]
category: "infra"
related: [3642, 3653, 2105, 2862, 394]
memo: "[Zenn LLM] ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測"
processed_at: "2026-05-08T09:42:18.383303"
---

## 要約

RTX 4060（VRAM 8GB）＋WSL2環境でOllama 0.20.2を使い、gemma3:4b・gemma3:12b・qwen3:4b・qwen3:8b・qwen3:14b・gpt-oss:20bの6モデルを5カテゴリ（日本語要約・技術正確性・コードレビュー・構造化出力・長文ビジネス分析）で定量ベンチマークした実験報告。全モデルQ4_K_M量子化（gpt-ossのみMXFP4）、temperature=0.2、計測3回平均（ウォームアップ1回除外）。

最大の知見はVRAM 8GBという制約がもたらす「速度の2段階構造」。VRAM内に収まるモデル（gemma3-4b/2.4GB、qwen3-4b/2.3GB、qwen3-8b/4.6GB）は40〜75 tok/sを達成するのに対し、VRAMを超過してCPUオフロードが発生するqwen3-14b（推定8.3GB）とgpt-oss（推定10.5GB）は9〜13 tok/sに急落する。CPUのメモリ帯域幅はGPUの数十分の1であるため、モデルサイズよりもVRAM収容可否が速度を規定する。

gemma3-4bは全カテゴリ最速で平均8.3秒・avg chr/s=156.5。日本語の漢字・かなをトークンあたり多文字で表現するため、tok/s（74.6）以上にchr/sが高くなる。思考トークンを生成しないことも寄与している。

qwen3-4bはtok/s=67.6と高速に見えるが、chr/s=16.0と極端に低い。JSON抽出タスクで240文字の出力を生成するために最大5,000トークン近い内部Chain-of-Thought（思考トークン）を生成することが原因。長文ビジネス分析では3回中2回がmax_tokens=8192を使い切り実際の出力をゼロにするという致命的な失敗を引き起こす。Ollamaのthink=falseパラメータで無効化可能だが、本実験はデフォルト設定。

qwen3-8bはavg 23.4秒・全run成功・思考トークン過剰なしでバランス最良。qwen3-14bは111.9秒と遅いが全run完結かつ未決事項抽出が6〜7項目と最も細粒度。gpt-ossはmax_tokens=2048設定でほぼ全タスクが途中切れとなり実質非推奨。

監査エージェント開発への示唆：（1）ローカルLLMを使ったエージェントでは、VRAM収容可否がスループットを数倍左右するため、モデル選定時にVRAM見積もりを必ず行う。（2）qwen3系のthinking modeはデフォルトで有効なため、ツール呼び出しや構造化出力を多用するエージェントではthink=falseを明示的に設定しないとトークン消費・レイテンシが激増する。（3）速度と品質のトレードオフとして、バッチ型の監査レポート生成にはqwen3-14bが候補、リアルタイム対話や構造化抽出にはgemma3-4bまたはqwen3-8bが適切。

## アイデア

- VRAMの8GB境界がtok/sを4〜8倍変化させる「速度ティア」の存在：GPUオフロードの有無がモデルパラメータ数よりも推論速度を規定するという、ハードウェア制約主導の性能構造
- qwen3-4bのtok/s（67.6）とchr/s（16.0）の4倍乖離：思考トークン（CoT）が完了トークンの大部分を占めることで実効スループットが著しく低下する現象は、エージェント設計においてトークン課金・レイテンシ設計の前提を変える
- gemma3-4bの日本語chr/s=156.5：漢字・かなの高密度トークン化により、tok/sよりもchr/sが2倍以上高くなる特性は、日本語処理に特化したモデル評価軸としてトークン数ではなく文字数スループットを使うべきであることを示す

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **量子化（Q4_K_M/MXFP4）** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **Chain-of-Thought** → /deep_59 EcoThink: 持続可能でアクセスしやすいエージェントのためのグリーン適応的推論フレームワーク
- **CPUオフロード** → /deep_1935 ZeROによるメモリ最適化：DeepSpeedとFairScaleで大規模モデルを効率的に学習する

## 関連記事

- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門

## 原文リンク

[ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測](https://zenn.dev/tktomaru/articles/20260430_local_llm_compare)
