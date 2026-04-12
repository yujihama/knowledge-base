---
title: "Inference Endpoints で実現する超高速 Whisper 音声認識（最大8倍高速化）"
url: "https://huggingface.co/blog/fast-whisper-endpoints"
date: 2026-04-07
tags: [Whisper, vLLM, Inference Endpoints, torch.compile, CUDA graphs, float8, ASR, HuggingFace, L4 GPU, FastRTC]
category: "infra"
memo: "[HF Blog] Blazingly fast whisper transcriptions with Inference Endpoints"
processed_at: "2026-04-07T21:36:50.232723"
---

## 要約

Hugging Face は2025年5月13日、Inference Endpoints 上で動作する新しい Whisper デプロイオプションを発表した。従来比で最大8倍の RTFx（Real-Time Factor）改善を達成しており、音声認識品質（WER）を維持したまま大幅な高速化を実現している。

推論スタックは vLLM をバックエンドに採用しており、NVIDIA Ada Lovelace アーキテクチャ（Compute Capability 8.9以上）、具体的には L4・L40s GPU を対象として複数の最適化技術を組み合わせている。①torch.compile によるJITカーネル最適化（計算グラフの再構成・演算の並べ替え・特殊メソッドの呼び出し）、②CUDA graphs による連続カーネルのバッチ実行（データ転送・同期・スケジューリングオーバーヘッドの削減）、③float8 KV キャッシュによる動的活性化量子化（bfloat16比でメモリ使用量を半減し、キャッシュヒット率を向上）の3技術が中心となっている。

評価対象モデルは Whisper Large V3・Whisper Large V3-Turbo・Distil-Whisper Large V3.5 の3種で、Open ASR Leaderboard の AMI、GigaSpeech、LibriSpeech（Clean/Other）、SPGISpeech、Tedlium、VoxPopuli、Earnings22 の8データセットで WER を計測し、Transformers ライブラリ実装と同等の精度を確認している。速度評価は rev16 long-form データセット（45分超の長尺音声）を使用し、単一 L4 GPU・bfloat16・同一デコード設定（言語・ビームサイズ・バッチサイズ）で測定している。

デプロイは Hugging Face Endpoints の UI からモデルを選択するだけで完結し、Python の requests ライブラリ数行でエンドポイントを呼び出せる。APIは OpenAI Whisper 互換の /api/v1/audio/transcriptions エンドポイント形式を採用しており、既存 OpenAI API 向けコードとの互換性が高い。FastRTC と組み合わせたリアルタイム文字起こしデモも公開されており、マイク入力をほぼリアルタイムでテキスト化できる。なお、単語レベルタイムスタンプは現時点で未サポートであり、CrisperWhisper との統合が今後の検討課題として挙がっている。Dockerイメージを引いてローカル GPU 環境でも動作可能。

## アイデア

- float8 KV キャッシュ量子化という手法が、モデル重みでなく推論時の中間状態を圧縮する点が実用的で、メモリ効率と速度を同時に改善する設計
- CUDA graphs による複数カーネルのバッチ実行は、GPUスケジューリングオーバーヘッド削減の汎用パターンとして Whisper 以外の推論最適化にも応用可能
- OpenAI Whisper 互換 API を採用することで、既存の OpenAI クライアントコードをほぼ無改修でオープンソースモデルへ切り替えられる移植性の高さ

## Yujiの取り組みへの示唆

監査エージェントにおいて会議・ヒアリング・インタビューの音声を自動文字起こしするコンポーネントとして直接活用できる。LangGraph のパイプラインに音声入力ノードを追加する場合、この OpenAI 互換エンドポイントは既存の LLM 呼び出しコードと同じ requests パターンで統合できるため実装コストが低い。長時間監査会議（45分超）の一括文字起こしと、FastRTC を使ったリアルタイム議事録生成の両ユースケースに対応できる点も実用的。

## 原文リンク

[Inference Endpoints で実現する超高速 Whisper 音声認識（最大8倍高速化）](https://huggingface.co/blog/fast-whisper-endpoints)
