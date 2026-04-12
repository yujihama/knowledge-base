---
title: "🤗 TransformersによるWhisperの多言語ASRファインチューニング"
url: "https://huggingface.co/blog/fine-tune-whisper"
date: 2026-04-11
tags: [Whisper, ASR, ファインチューニング, HuggingFace, Transformers, 多言語, Common Voice, seq2seq, log-Mel]
category: "ai-ml"
memo: "[HF Blog] Fine-Tune Whisper For Multilingual ASR with 🤗 Transformers"
related: [1488, 649, 1216, 128, 1358]
processed_at: "2026-04-11T09:06:46.270219"
---

## 要約

OpenAIが2022年9月に公開したWhisperは、680,000時間のラベル付き音声・文字起こしデータで事前学習された自動音声認識（ASR）モデルである。うち117,000時間が多言語データであり、96言語以上に対応する。従来のWav2Vec 2.0がラベルなし60,000時間の音声データで自己教師あり学習（マスク予測）を行うのとは対照的に、WhisperはCross-Entropyを目的関数とした教師あり学習で直接音声→テキストのマッピングを学習する。このため、少量のファインチューニングデータで高性能なASRモデルを構築できる点が特徴。アーキテクチャはTransformerベースのEncoder-Decoderモデル（sequence-to-sequence）で、入力音声をlog-Melスペクトログラムに変換後、エンコーダが隠れ状態表現を生成し、デコーダがクロスアテンション経由でテキストトークンを自己回帰的に予測する。言語モデルをシステム内部に統合する「Deep Fusion」方式により、エンドツーエンドで学習でき、CTC+n-gramのような「Shallow Fusion」より柔軟かつ高性能。モデルサイズはtiny（39M）〜large-v3（1550M）の7種類が存在し、英語専用・多言語対応の両バリアントがある。本ブログではCommon Voice v11のHindi（低リソース言語）を用い、244MパラメータのWhisper smallをファインチューニングする手順を解説。わずか8時間分の学習データで高精度なASRを実現できることを示す。実装にはdatasets[audio]、transformers、accelerate、evaluate、jiwer、tensorboard、gradioを使用。Hugging Face Hubへのチェックポイント保存・TensorBoardログ・モデルカード公開をトレーニング中に統合する方法も紹介。評価指標はWER（Word Error Rate）で、LibriSpeech test-cleanで約3%、TED-LIUMで4.7%というSOTA水準を既存チェックポイントが達成している。

## アイデア

- 680,000時間の教師ありデータでの事前学習により、ゼロショット・少量データのファインチューニングでも高WER性能を達成できる点は、ラベル付きデータが希少な専門領域（例: 監査ヒアリング音声）への応用可能性を示唆している
- Deep Fusionによってデコーダが内部言語モデルとして機能するため、専門用語（会計・法律用語）を含むドメイン固有コーパスでファインチューニングすることで、語彙レベルの精度向上が期待できる
- わずか8時間のデータでも実用レベルの精度が出ることは、低リソース言語や限定ドメインへの転移学習コストを劇的に下げており、データ収集コストが高い企業内部ユースケースへの展開を現実的にしている
## 関連記事

- /deep_1488 音声データセット完全ガイド：HuggingFace Datasetsで音声データを効率的に扱う方法
- /deep_649 Inference Endpoints で実現する超高速 Whisper 音声認識（最大8倍高速化）
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法
- /deep_128 WAXAL: アフリカ言語音声技術のための大規模オープンリソース
- /deep_1358 UnityでAI音声認識を実装する方法（Hugging Face Unity API活用）

## 原文リンク

[🤗 TransformersによるWhisperの多言語ASRファインチューニング](https://huggingface.co/blog/fine-tune-whisper)
