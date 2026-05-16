---
title: "Gemma 4 VLAデモ：Jetson Orin Nano Super上でのローカル実行"
url: "https://huggingface.co/blog/nvidia/gemma4"
date: 2026-04-28
tags: [Gemma4, VLA, llama.cpp, Jetson, tool-calling, ONNX, TTS, STT, エッジAI, マルチモーダル]
category: "infra"
related: [154, 2375, 1843, 1049, 859]
memo: "[HF Blog] Gemma 4 VLA Demo on Jetson Orin Nano Super"
processed_at: "2026-04-28T12:46:12.642711"
---

## 要約

NVIDIAのAsier Arranzによるコミュニティ記事。Gemma 4（E2B-it、2Bパラメータ）をJetson Orin Nano Super（8GB RAM）上でローカル完結のVLA（Vision-Language-Action）システムとして動作させるチュートリアル。音声入力→STT→LLM判断→（必要に応じてウェブカメラ撮影）→TTS出力というパイプラインで構成される。STTにはParakeet（ONNX形式）、TTSにはKokoro（ONNX形式）を使用し、すべてローカル推論。核心的な設計は「ツール呼び出しによる自律的視覚判断」で、モデルに`look_and_answer`という単一ツールのみを公開し、視覚情報が必要かどうかをGemma 4自身が判断してウェブカメラを起動する。キーワードトリガーやハードコードロジックは一切なく、Gemma 4のネイティブtool-calling機能（llama-serverの`--jinja`フラグで有効化）によって実現。推論バックエンドはllama.cpp（CUDA対応ネイティブビルド、`-DGGML_CUDA=ON`、CUDA architecture=87）で、モデル量子化はQ4_K_M（`gemma-4-E2B-it-Q4_K_M.gguf`）を使用。ビジョンプロジェクター（`mmproj-gemma4-e2b-f16.gguf`）を別途ダウンロードし、`--mmproj`オプションで指定することで視覚能力を付与。llama-serverは`-ngl 99`で全レイヤーをGPUにオフロード、`--flash-attn on`でFlash Attentionを有効化、コンテキスト長2048トークン。8GBという限られたRAMで動作させるため、Dockerやcontainerdの停止、8GBスワップファイルの追加などのメモリ最適化が必須。ハードウェア構成はJetson Orin Nano Super＋Logitech C920（マイク内蔵）＋USBスピーカー。監査エージェント開発への示唆として、「モデルが外部ツールを自律的に呼び出すかどうかを判断する」というアーキテクチャパターンはReActエージェントのtool-use設計と直結しており、監査証跡収集エージェントにおいても「いつドキュメントを参照するか」をLLMに委ねる設計の実装参考になる。また、エッジデバイス上でのローカル完結推論はデータプライバシーが求められる監査用途にも適合する。

## アイデア

- 単一ツール定義（look_and_answer）のみでモデルに視覚の自律的ON/OFFを委ねる最小限のVLA設計は、ツール数を絞ることでエージェントの判断品質を高める設計原則の実証例
- Q4_K_M量子化＋Flash Attention＋全レイヤーGPUオフロードの組み合わせで8GB Jetsonでマルチモーダル推論を実現しており、ローカルLLMインフラのリソース最適化手法として参照価値が高い
- Parakeet STT→Gemma 4→Kokoro TTSというONNXベースのパイプラインはすべてHugging Hubから自動ダウンロードされ、再現性の高いエッジAIアーキテクチャのリファレンス実装になっている

## 前提知識

- **llama.cpp** → /deep_940 Llama 3.2 リリース：視覚理解とオンデバイス推論を兼ね備えたオープンモデル群
- **tool-calling / function calling** (TODO: 読むべき)
- **VLA（Vision-Language-Action）** (TODO: 読むべき)
- **量子化（GGUF/Q4_K_M）** (TODO: 読むべき)
- **Jetson / CUDA** (TODO: 読むべき)

## 関連記事

- /deep_154 ロボティクスAIを組み込みプラットフォームへ展開：データセット収録・VLAファインチューニング・オンデバイス最適化
- /deep_2375 VLAジャンプスタート強化学習（VLAJS）：Vision-Language-ActionモデルによるRLの探索効率化
- /deep_1843 PanLUNA：エッジ生体信号インテリジェンスのための効率的・堅牢なクエリ統合マルチモーダルモデル
- /deep_1049 Kaggle MedGemma Impact Challenge 全解剖：受賞9件＋落選30件から学ぶ医療AI開発
- /deep_859 Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル

## 原文リンク

[Gemma 4 VLAデモ：Jetson Orin Nano Super上でのローカル実行](https://huggingface.co/blog/nvidia/gemma4)
