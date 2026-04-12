---
title: "faster-whisperで手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度"
url: "https://zenn.dev/nomuraya/articles/faster-whisper-transcription"
date: 2026-04-03
tags: [faster-whisper, Whisper, 音声認識, 文字起こし, pyannote, 話者分離, M2 Max, INT8量子化, ffmpeg, CPU推論]
category: "infra"
memo: "[Zenn 機械学習] faster-whisper で手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度"
processed_at: "2026-04-03T21:07:46.683569"
---

## 要約

Apple M2 MaxのMacBook Proで、Zoom録画（33分）をfaster-whisper 1.xを使ってローカル文字起こしした手順と、pyannote.audio 3.xによる話者分離の注意点をまとめた記事。

faster-whisperはCUDA専用実装のため、MacのMetal（MPS）には非対応。device="mps"を指定してもエラーまたは無視され、device="cpu"を明示する必要がある。CPUでの実行においては、compute_type="int8"によるINT8量子化が最速選択肢となる。large-v3モデルとINT8量子化の組み合わせで、33分の音声を7〜11分（3〜5倍速）で処理でき、日本語音声でも専門用語・固有名詞を含め高精度な文字起こしが可能。

基本的な使い方はWhisperModelにmp4を直接渡せる（内部でffmpegが音声抽出）。出力はタイムスタンプ付きテキストで保存。

話者分離にはpyannote/speaker-diarization-3.1を使用するが、mp4の直接入力はファイルパス解決の問題でエラーになる。事前にffmpegで16kHz・モノラルのwavに変換する必要がある。Hugging Faceのアクセストークンとモデル利用規約への同意も必須。

実運用上の重要な教訓として、Zoom録画直後にwav変換を済ませておくことを推奨。元のmp4を削除した後から話者分離しようとすると実行不可能になる。

文字起こし結果と話者分離結果のマージはタイムスタンプの照合で実現。各セグメントの中央時刻を話者区間と照合し、話者ラベルを付与するシンプルな実装で対応できる。Metal非対応という制約はあるものの、CPUのみで実用に耐える速度が出ることが確認されており、CUDAなし環境での音声処理パイプラインとして有効な選択肢。

## アイデア

- CUDA非依存のCPU推論でもINT8量子化により実用速度（3〜5倍速）が出る点は、GPU環境がないマシンでのLLM/音声処理パイプライン設計に示唆がある
- faster-whisperとpyannoteの出力をタイムスタンプで照合してマージする手法は、複数モデルの非同期出力を統合するエージェントパイプライン設計のパターンとして参考になる
- 録画直後にwav変換を習慣化するというワークフロー設計は、データ収集パイプラインにおける「後処理に必要な中間成果物の早期保存」という原則の具体例

## Yujiの取り組みへの示唆

監査エージェントの開発において、会議録・ヒアリング音声のテキスト化は証跡収集の自動化に直結する。faster-whisper + pyannoteのローカルパイプラインは、機密性の高い監査情報をクラウドに送らずに処理できる点で有効。LangGraphベースのエージェントの入力ノードとして音声→テキスト変換ステップを組み込む際、タイムスタンプ付き話者ラベル付きテキストはRAGのチャンク設計にもそのまま活用できる。

## 原文リンク

[faster-whisperで手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度](https://zenn.dev/nomuraya/articles/faster-whisper-transcription)
