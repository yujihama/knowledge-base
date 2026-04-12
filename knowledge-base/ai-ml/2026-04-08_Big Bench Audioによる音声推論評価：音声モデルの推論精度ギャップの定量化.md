---
title: "Big Bench Audioによる音声推論評価：音声モデルの推論精度ギャップの定量化"
url: "https://huggingface.co/blog/big-bench-audio-release"
date: 2026-04-08
tags: [Big Bench Hard, audio LLM, Speech-to-Speech, LLM-as-judge, GPT-4o Realtime, Gemini 1.5, 評価ベンチマーク, Whisper, TTS]
category: "ai-ml"
memo: "[HF Blog] Evaluating Audio Reasoning with Big Bench Audio"
processed_at: "2026-04-08T12:27:42.672316"
---

## 要約

Artificial AnalysisがBig Bench Audioを公開。Big Bench Hardから1,000問を音声化した評価データセットで、音声言語モデルの推論能力を測定する。カテゴリはFormal Fallacies（論理的演繹）、Navigate（経路復帰判定）、Object Counting（物体計数）、Web of Lies（ブール論理）の4種類各250問で構成。音声ファイルはArtificial Analysis Speech Arenaで上位評価された23種の合成音声TTSモデルで生成し、Levenshtein距離による品質検証と人手によるエッジケース確認を実施。評価は4つの構成（Speech-to-Speech、Speech-to-Text、Text-to-Speech、Text-to-Text）でGPT-4oおよびGemini 1.5シリーズ計11モデルに対して18実験を実施。評価自動化にはClaude 3.5 Sonnet（2024年10月版）をLLM Evaluatorとして使用し、候補回答と正解・質問文を入力して「CORRECT/INCORRECT」を判定させる。主な結果として、GPT-4o（2024年8月版）のText-to-Text精度92%に対し、GPT-4o Realtime Preview（2024年10月版）のSpeech-to-Speech精度は66%と26ポイントの「音声推論ギャップ」が確認された。Text-to-Speech構成では74%と中間値を示し、音声入力・音声出力の両方がギャップに寄与していることが判明。一方、Whisper転写→GPT-4o推論→TTS-1音声生成のパイプライン構成はText-to-Textとほぼ同等の性能を維持しており、推論精度を重視するユースケースでは現時点でパイプライン方式が優位。ネイティブ音声モデルの推論性能は改善途上にあることを示す定量的根拠を提供するデータセット。

## アイデア

- 音声モダリティの追加によって推論精度が最大26ポイント低下するという定量的な「モダリティコスト」の測定手法は、マルチモーダルエージェント設計における能力トレードオフ分析に応用できる
- LLM-as-judgeをClaude 3.5 Sonnetで実装し、数字の表記揺れ（7/seven）や名前のスペル揺れを許容するプロンプト設計で評価精度を担保している点は、自動評価パイプライン構築の実践的参考になる
- ネイティブ音声モデルよりもWhisper+LLM+TTSのパイプライン構成の方が推論精度が高いという結果は、end-to-endモデルの表現圧縮による情報損失という研究仮説を支持している
## 関連記事

- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_128 WAXAL: アフリカ言語音声技術のための大規模オープンリソース
- /deep_137 DescriptがOpenAI APIを使って多言語動画吹き替えをスケールさせる仕組み
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読

## 原文リンク

[Big Bench Audioによる音声推論評価：音声モデルの推論精度ギャップの定量化](https://huggingface.co/blog/big-bench-audio-release)
