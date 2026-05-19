---
title: "初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する"
url: "https://zenn.dev/munakatakm/articles/bef24ab4fc5366"
date: 2026-05-19
tags: [RTX PRO 6000 Blackwell, DGX Spark, vLLM, NVFP4, ローカルLLM, GPU比較, Qwen3, MTP, CPUオフロード]
category: "infra"
related: [5839, 2590, 4325, 3642, 2826]
memo: "[Zenn LLM] 初めて作るオレオレAIデータセンター③： DGXSpark と RTXPRO6000BWMAX-Q を比較する"
processed_at: "2026-05-19T09:06:22.052935"
---

## 要約

個人AIデータセンター構築シリーズの第3回。NVIDIA RTX PRO 6000 Blackwell MAX-Q（以下RTXPRO6000BWMAX-Q）とDGX Sparkの実機比較レポート。

RTXPRO6000BWMAX-Qは、600Wクラスチップを300Wに抑えたワークステーション向けGPUで、96GB GDDR7 ECC VRAM・メモリ帯域1,792GB/s・AI性能3,511 TOPS FP4を持つ。1スロット設計のため4枚挿しで約400GBのVRAMを構成可能。購入時130万円（現在160万円以上）。対するDGX SparkはGB10チップ搭載・128GB統合メモリ・273GB/s帯域・1,000 TOPS FP4で約60万円。

vLLM（v0.20.1）を用いたベンチマーク（concurrency=4、pp=2048、tg=32）では、RTXPRO6000BWMAX-Qがprefill・decodeともにDGX Sparkの3〜4倍の速度を記録。例：Qwen3.5-122B-A10B-NVFP4のprefillでRTX約10,696 t/s対DGX約2,318 t/s、decodeで128.63対31.93 t/s。

CPUオフロード検証では、RTXPRO6000BWMAX-Qで--cpu-offload-gb 16を指定した場合、Qwen3.5-122Bのdecodeが128 t/sから13.58 t/sへ約1/10に低下。GPU-CPU間帯域がボトルネックとなるため、CPUメモリへの重み退避は実用上有効でないことが判明。

熱管理面ではRTXPRO6000BWMAX-Qが課題で、250Wに電力制限・ファン99%稼働・ヒートシンク貼付でLLM動作時60℃台後半を維持。DGX Sparkは熱暴走なし。

実運用では、RTXPRO6000BWMAX-Q（Qwen3.5-122B）を前後工程の高速処理・コードチェック・スクリプト作成に、DGX Spark×4台（Qwen3.5-397B、500Kトークン対応）を資料作成・コーディング・最終チェックに割り当て。速度差を活かした並列ワークフローで効率化。

チップ世代の違い（GB202 vs GB10、Blackwell vs Grace Blackwell）によりvLLMの動作互換性問題が発生する点も報告。sm121の公式サポートがvLLM v0.20.1で追加され、NVFP4のflash_attn対応が改善されている。

監査エージェント開発への示唆：ローカルLLMを役割分担させた非同期並列処理パターンは、LangGraphベースのマルチエージェントシステムにおけるタスクルーティング設計の参考になる。高速な小モデルと高精度な大モデルを組み合わせるアーキテクチャは、監査ワークフローの前処理・後処理分離にも応用可能。

## アイデア

- 速度差のある2種のGPUを役割分担させる非同期並列ワークフロー：RTXPRO6000BWMAX-Q（高速・小モデル）で前後処理、DGX Spark×4（低速・大モデル）でコア処理を担当し、待機時間をゼロにする設計
- CPUオフロード（--cpu-offload-gb）はGPU-CPU間帯域ボトルネックにより実用性が極めて低い（1/10に低下）という実測データ：96GBでも足りない規模のモデルを単一カードで動かす戦略は非現実的
- 同世代表記でもGB10（Grace Blackwell）とGB202（Blackwell）でvLLMの動作互換性が異なり、マルチGPU環境の運用コストが増大する問題：エッジAIインフラ設計でのチップアーキテクチャ統一の重要性

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **NVFP4量子化** → /deep_4329 AIの重心が「学習」から「推論」に移っている — エンジニアが知るべき構造変化の全体像
- **MoEモデル** (TODO: 読むべき)
- **NVLink** → /deep_1399 Mustafa Suleiman：AIの発展は近いうちに壁にぶつからない――その理由
- **CUDA sm世代** (TODO: 読むべき)

## 関連記事

- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_4325 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第6回・完結）── ハルシネーションを4段ロケットで削る話
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_2826 ローカルLLM用の簡易ツール拡張機能「トリガー」：シェルスクリプトをFunction Callingツールとして自動登録する仕組み

## 原文リンク

[初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する](https://zenn.dev/munakatakm/articles/bef24ab4fc5366)
