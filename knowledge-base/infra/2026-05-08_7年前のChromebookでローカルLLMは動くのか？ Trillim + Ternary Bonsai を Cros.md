---
title: "7年前のChromebookでローカルLLMは動くのか？ Trillim + Ternary Bonsai を Crostini で試す"
url: "https://zenn.dev/dateshim/articles/eb9b7bb8e53cc2"
date: 2026-05-08
tags: [ローカルLLM, Trillim, Ternary-Bonsai, Crostini, ChromeOS, CPU推論, 量子化, エッジ推論, ベンチマーク]
category: "infra"
related: [4332, 3653, 1116, 2480, 3642]
memo: "[Zenn LLM] 7年前の Chromebook でローカルLLMは動くのか？ Trillim + Ternary Bonsai を Crostini で試す"
processed_at: "2026-05-08T21:09:37.415717"
---

## 要約

本記事は、Intel Core i5-7Y54（7世代、低電圧版）・8GB RAMという2018年前後のHP Chromebook x2 12上で、Trillim v0.10.2 + Ternary-Bonsai（Bonsai-1.7BT-TRNQ）モデルをCrostini（ChromeOSのLinuxコンテナ環境）上で動作させた実機検証レポートである。GPUは一切使用せず、純粋なCPU推論のみで検証している。

インストールはuv・Python・trillimの3ステップで完了し、Crostini環境での詰まりは報告されていない。モデルはTrillim公式リポジトリからBonsai-1.7BT-TRNQをpullし、CLIチャット（trillim chat）で対話を実施した。

性能計測はTrillim SDKのRuntime + session.generate()を用いた簡易ベンチマークで実施。ウォームアップ1回＋本計測5回、max_tokens=128、プロンプトはCPU推論の技術説明を求める固定英文にBENCH-RUN-XXXXのマーカーを付与してキャッシュ再利用を抑制した構成。計測指標はfirst-token latency（prefill proxyとして）、decode throughput、総応答時間の3軸。

結果は以下の通り：first-token proxy（prompt token数÷first token latency）が平均22.2 tok/sec・中央値24.4 tok/sec、decode throughputが平均8.7 tok/sec・中央値8.6 tok/sec、first tokenまでの時間が平均2.69秒・中央値2.29秒、decode時間が平均14.51秒・中央値14.85秒、総応答時間が平均17.20秒・中央値17.02秒であった。

Ternary-Bonsaiは1.7Bパラメータの三値量子化（ternary）モデルであり、モデルサイズが極めて小さいためRAM 8GBでも動作可能。decode速度約8.7 tok/secは会話として十分に読める速度であり、GPUなし・サーマル制約ありの旧型Chromebookでも実用的なローカルLLMチャットが成立することを実証した。監査エージェント開発への示唆としては、エッジデバイスや古いハードウェアでの推論可能性を示しており、クラウド依存なしのオフライン推論ベースのエージェント構成を低コストハードウェアで検討する際の参考になる。

## アイデア

- 三値量子化（ternary）により1.7Bモデルをメモリ8GB・GPU非搭載のCPU専用環境で動作させており、量子化ビット幅の極限化がエッジ推論のボトルネック（メモリ帯域・DRAM容量）を緩和する具体的な効果を示している
- decode throughput約8.7 tok/secという数値は、会話型インタフェースとして許容できる速度の下限付近であり、モデルサイズ・量子化方式・ハードウェアスペックの組み合わせがユーザー体験に与える影響を定量的に把握できる
- CrostiniというサンドボックスLinux環境でも追加設定なしでTrillimが動作した点は、隔離環境・制限環境でのローカルLLMデプロイの容易さを示しており、セキュリティ要件上インターネット非接続が求められる監査業務環境への適用可能性を示唆する

## 前提知識

- **LLM量子化（Quantization）** (TODO: 読むべき)
- **Ternary / 三値量子化** (TODO: 読むべき)
- **CPU推論・メモリ帯域** (TODO: 読むべき)
- **Crostini（ChromeOS Linux）** (TODO: 読むべき)
- **Prefill / Decode分離** (TODO: 読むべき)

## 関連記事

- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁

## 原文リンク

[7年前のChromebookでローカルLLMは動くのか？ Trillim + Ternary Bonsai を Crostini で試す](https://zenn.dev/dateshim/articles/eb9b7bb8e53cc2)
