---
title: "UnityでAI音声認識を実装する方法（Hugging Face Unity API活用）"
url: "https://huggingface.co/blog/unity-asr"
date: 2026-04-10
tags: [Hugging Face, Unity, ASR, Whisper, 音声認識, WAV, Unity API, ゲームAI]
category: "infra"
memo: "[HF Blog] AI Speech Recognition in Unity"
related: [1529, 1420, 1062, 411, 128]
processed_at: "2026-04-10T09:44:59.212580"
---

## 要約

本チュートリアルは、Hugging Face Unity APIを使用してUnityゲームエンジンに音声認識機能を組み込む手順を解説している。実装は主に5ステップで構成される。①UIシーン構築（開始・停止ボタン、TextMeshProによる結果表示）、②SpeechRecognitionTestスクリプトの作成とUI参照のバインド、③Unityの`Microphone.Start()`APIによる最大10秒・44100Hzのマイク入力録音、④録音データをWAVフォーマット（RIFFヘッダ付き、16bit PCM）にエンコード、⑤`HuggingFaceAPI.AutomaticSpeechRecognition()`へのバイト列送信と結果のUIへの反映。WAVエンコード部分はBinaryWriterを用いて手動でRIFFチャンク構造を構築しており、サンプルをfloatからshortへ変換（sample * short.MaxValue）している。HuggingFace側のバックエンドにはWhisperなどのSOTAモデルが利用されると推察される。UX改善として、録音状態に応じたボタンのinteractability制御（録音中はStartを無効化、Stop後の推論中は両ボタンを無効化）と、ステータスメッセージの表示も実装している。デモはitch.ioで公開されており、NPC対話・アクセシビリティ・コマンド入力などのユースケースが想定されている。技術的依存はHugging Face Unity API（別途セットアップ必要）とTextMeshProに限定されており、軽量な統合が可能。音声データはクラウドAPIに送信されるため、レイテンシとプライバシーの考慮が必要。

## アイデア

- WAVエンコードをUnity内で完結させることでサードパーティ音声ライブラリへの依存を排除し、HuggingFace APIとの直接統合を実現している点が実用的
- 録音の最大長（10秒）とMicrophone.GetPosition()による自動停止ロジックにより、クラウドAPIへの過大なペイロード送信を防ぐ設計になっている
- ボタンのinteractability制御でAPI応答待ち中の二重送信を防ぐUXパターンは、非同期AIコール全般に応用できる汎用設計

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証
- /deep_1062 危機言語のドキュメント化に向けた自動音声認識：池間宮古語を事例として
- /deep_411 faster-whisperで手元の録画を文字起こしする：Metal非対応でもM2 Maxで実用速度
- /deep_128 WAXAL: アフリカ言語音声技術のための大規模オープンリソース

## 原文リンク

[UnityでAI音声認識を実装する方法（Hugging Face Unity API活用）](https://huggingface.co/blog/unity-asr)
