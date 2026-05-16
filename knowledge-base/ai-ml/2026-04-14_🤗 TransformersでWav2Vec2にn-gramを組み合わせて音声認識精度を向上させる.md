---
title: "🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる"
url: "https://huggingface.co/blog/wav2vec2-with-ngram"
date: 2026-04-14
tags: [Wav2Vec2, CTC, n-gram, KenLM, pyctcdecode, ASR, Transformers, LibriSpeech, ビームサーチ, 音声認識]
category: "ai-ml"
related: [1762, 1529, 1488, 1062, 1358]
memo: "[HF Blog] Boosting Wav2Vec2 with n-grams in 🤗 Transformers"
processed_at: "2026-04-14T12:09:07.712798"
---

## 要約

本記事はHugging Face BlogのPatrick von Platenによるチュートリアルで、Meta AI Researchが2020年9月に公開したWav2Vec2に対してn-gram言語モデル（LM）を組み合わせ、音声認識（ASR）の文字起こし精度を向上させる手順を解説している。

Wav2Vec2はCNN層で生音声から音響表現を抽出し、Transformerスタックで文脈を考慮した表現に変換した後、CTC（Connectionist Temporal Classification）アルゴリズムでテキストに変換する。CTCはアライメント問題を解決するため、外部辞書や言語モデルなしでも動作するが、公式論文のAppendix Cが示すように、LMと組み合わせることで特に少量データ（10分）でのWER（単語誤り率）が大幅に改善する。

具体的な手順は以下の通り。①KenLMライブラリでLibriSpeechの960時間分のテキストコーパスからn-gramモデルを構築する。`lmplz -o 5`で5-gramモデルを生成し、`build_binary`でバイナリ形式に変換する。②Kensho TechnologiesのpyctcdecodeライブラリとHugging FaceのWav2Vec2ProcessorWithLMを使い、モデルリポジトリにアーカイブ形式（zip）でLMファイル一式（arpa/binファイル、vocab.json等）をアップロードする。③デコード時はargmax(logits)ではなくlogits全体をプロセッサに渡し、ビームサーチ（デフォルトbeam_width=100）でLM確率を組み合わせてデコードする。

実験結果として、`facebook/wav2vec2-base-100h`でLMなしだと「christmaus」「simalyis」などの誤りが生じるのに対し、4-gram LMを追加した`patrickvonplaten/wav2vec2-base-100h-with-lm`では「christmas」「similes」と正確に転写される。LibriSpeechのtest-cleanに対するWERは、LMなし（greedy）で6.24%、4-gram LM追加で4.52%に改善（約28%相対改善）。また、batch_decode時にnum_processes引数でマルチプロセス並列デコードが可能で、処理速度の改善も実現できる。

pyctcdecodeはbeam_width、alpha（LMスコア重み）、beta（単語カウント報酬）などのハイパーパラメータを持ち、チューニングにより更なる改善が期待できる。監査AIへの直接の応用としては、会議・ヒアリング音声の高精度文字起こしが考えられる。特にドメイン固有の用語（会計・法務用語）に特化したコーパスでn-gramを構築すれば、汎用モデル比でWERを大幅低減できる可能性がある。

## アイデア

- LMなしでも機能するCTCベースASRにn-gramを後付けするだけでWERが6.24%→4.52%（約28%相対改善）になる点は、既存のファインチューニング済みチェックポイントを再学習なしに強化できることを示しており、コスト効率が高い
- pyctcdecodeのbeam_width・alpha・betaというわずか3つのハイパーパラメータでLMの影響度を調整でき、ドメイン固有コーパス（例：監査・法務テキスト）でKenLMを構築すれば専門用語の誤転写を抑制できる実用的アーキテクチャ
- Wav2Vec2ProcessorWithLMがHugging Face Hubのモデルリポジトリからzipアーカイブ形式でLMを自動ロードする仕組みは、モデルとLMをセットでバージョン管理・配布できる点でMLOpsの観点から有用

## 前提知識

- **Wav2Vec2** → /deep_1762 🤗 TransformersのWav2Vec2で大容量音声ファイルの自動音声認識を実現する方法
- **CTC (Connectionist Temporal Classification)** (TODO: 読むべき)
- **n-gram言語モデル** (TODO: 読むべき)
- **ビームサーチデコーディング** (TODO: 読むべき)
- **HuggingFace Transformers** → /deep_1394 TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド

## 関連記事

- /deep_1762 🤗 TransformersのWav2Vec2で大容量音声ファイルの自動音声認識を実現する方法
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1488 音声データセット完全ガイド：HuggingFace Datasetsで音声データを効率的に扱う方法
- /deep_1062 危機言語のドキュメント化に向けた自動音声認識：池間宮古語を事例として
- /deep_1358 UnityでAI音声認識を実装する方法（Hugging Face Unity API活用）

## 原文リンク

[🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる](https://huggingface.co/blog/wav2vec2-with-ngram)
