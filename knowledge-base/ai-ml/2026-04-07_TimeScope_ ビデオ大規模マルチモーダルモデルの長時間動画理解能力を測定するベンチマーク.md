---
title: "TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク"
url: "https://huggingface.co/blog/timescope-video-lmm-benchmark"
date: 2026-04-07
tags: [VLM, multimodal, benchmark, long-video, temporal-reasoning, Gemini-2.5-Pro, Qwen2.5-VL, InternVL, evaluation]
category: "ai-ml"
memo: "[HF Blog] TimeScope: How Long Can Your Video Large Multimodal Model Go?"
related: [975, 650, 587, 616, 1430]
processed_at: "2026-04-07T12:18:26.594701"
---

## 要約

TimeScopeは、視覚言語モデル（VLM）が長時間動画をどこまで真に理解できるかを測定するオープンソースベンチマーク（Stanford・HuggingFace共同）。従来のVideo Needle in a Haystack（VideoNIAH）は静止画像を「針」として埋め込む手法で、実質的に視覚的検索能力しか測定できなかった。TimeScopeはこの限界を克服するため、5〜10秒の短い動画クリップを「針」として、1分〜8時間の長さのベース動画に埋め込む設計を採用。評価する能力は3軸: (1) Localized Retrieval（特定セグメントの検出・回答）、(2) Information Synthesis（複数時点に分散したテキスト情報を時系列順に収集・整合）、(3) Fine-Grained Temporal Perception（斧の振り回し回数など、複数フレームにわたる動作の精密認識）。主要モデルの評価結果では、Gemini 2.5-Proのみが1時間超の動画で高精度を維持した唯一のモデルで、他は特定の動画長を超えると精度が急落する「パフォーマンスクリフ」が観察された。Qwen 2.5-VL（3B・7B）やInternVL 2.5（2B・4B・8B）はパラメータ規模を増やしても長時間動画での性能曲線がほぼ同一で、単純なパラメータスケーリングでは時間軸の理解は改善しないことが示された。また、Qwen 2.5-VLはOCRベースのInformation Synthesisタスクでは優れるが、Fine-Grained Temporal Perceptionでは劣後するなど、タスク間のトレードオフも明確化。多くのモデルはトレーニングデータが256フレームで打ち切られており、10,000フレーム超の文脈窓を謳っても実態は乖離している。ベンチマークはHugging Face上でホストされ、lmms-evalの2コマンドでローカル評価が可能。

## アイデア

- 「文脈窓の広さ」と「実際の長距離推論能力」が乖離している問題を、針クリップの埋め込みという実験設計で定量化した点——モデルの自己申告スペックを鵜呑みにせずベンチマークで検証する手法論として参考になる
- パラメータスケーリングだけでは時間軸理解が向上しないという知見は、長文脈LLMの文字列版（RULER等）と同じパターンであり、モダリティを越えた共通の限界として注目に値する
- Information Synthesis（分散情報の時系列統合）タスクは、監査ログや証跡の多点抽出・順序整合と構造的に類似しており、監査AIの評価設計に直接転用できる可能性がある
## 関連記事

- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_587 Holo1: GUIエージェント「Surfer-H」を動かす新しいGUI自動化VLMファミリー
- /deep_616 ChartDiff: チャートペア理解のための大規模ベンチマーク
- /deep_1430 BATON: 自然走行環境における双方向自動化移行観測のためのマルチモーダルベンチマーク

## 原文リンク

[TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク](https://huggingface.co/blog/timescope-video-lmm-benchmark)
