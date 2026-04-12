---
title: "Hugging Face Inference Endpointsで実現するASR＋話者分離＋Speculative Decodingの統合パイプライン"
url: "https://huggingface.co/blog/asr-diarization"
date: 2026-04-09
tags: [Whisper, ASR, diarization, Pyannote, speculative-decoding, Distil-Whisper, HuggingFace-Inference-Endpoints, Pydantic, Flash-Attention]
category: "infra"
memo: "[HF Blog] Powerful ASR + diarization + speculative decoding with Hugging Face Inference Endpoints"
related: [1529, 411, 128, 1358, 264]
processed_at: "2026-04-09T09:49:36.019608"
---

## 要約

本記事は、Hugging Face Inference Endpoints上でWhisper（ASR）、Pyannote（話者分離）、Distil-Whisper（Speculative Decoding用アシスタントモデル）を組み合わせたカスタム推論ハンドラの実装方法を解説している。

通常、Inference EndpointsはWhisperを単独でデプロイするのは容易だが、複数モデルを組み合わせて単一APIとして公開するには工夫が必要となる。解決策として`handler.py`にカスタム推論ロジックを実装し、`diarization_utils.py`（前後処理）、`config.py`（ModelSettings/InferenceConfig）と役割を分離したリポジトリ構成を採用している。

ASRパイプラインはtransformersの`pipeline("automatic-speech-recognition")`でWhisper large-v3を使用し、PyTorch 2.2以降のSDPAによるFlash Attention 2をデフォルト有効化。話者分離にはPyannote `speaker-diarization-3.1`を使用し、ASR出力の上に重ねて動作する設計となっている。

Speculative Decodingは`distil-whisper/distil-large-v3`をアシスタントモデルとして使用。ベンチマーク（A10 GPU）では、8秒の短音声でアシスタントあり326msに対してなし784ms（約2.4倍高速化）。ただし60秒の長音声ではチャンキング処理が入るためバッチサイズ制約（=1）との相性が悪く、アシスタントあり4.15sに対してなし3.48sと逆転する。

設定はPydanticのBaseSettings/BaseModelを用いており、モデル名やHFトークンはすべて環境変数で渡す（セキュリティ上ハードコード禁止）。環境変数のコンテナへの注入はUIではなくAPI経由でエンドポイントを作成する必要がある。必須コンポーネントはASRモデルのみで、アシスタントモデルと話者分離モデルはオプション。インスタンスはAWS g5.2xlarge（A10）を推奨。

## アイデア

- Speculative Decodingの効果は音声長に依存する：短音声（8秒）では2.4倍高速化だが、長音声（60秒）ではチャンキングによるバッチサイズ制約で逆効果になる。ユースケースに応じた使い分けが重要
- PydanticのBaseSettingsを使い、モデル名・トークン等を環境変数で動的注入する設計は、セキュリティと柔軟性を両立する実践的パターン
- 複数モデルを単一APIエンドポイントに統合するカスタムハンドラ設計：handler.py/diarization_utils.py/config.pyへの責務分離は、マルチモデルパイプラインの保守性を高める設計指針として汎用的に活用できる
## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_411 faster-whisperで手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度
- /deep_128 WAXAL: アフリカ言語音声技術のための大規模オープンリソース
- /deep_1358 UnityでAI音声認識を実装する方法（Hugging Face Unity API活用）
- /deep_264 Open ASR リーダーボード：多言語・長時間音声認識トラック追加とトレンド分析

## 原文リンク

[Hugging Face Inference Endpointsで実現するASR＋話者分離＋Speculative Decodingの統合パイプライン](https://huggingface.co/blog/asr-diarization)
