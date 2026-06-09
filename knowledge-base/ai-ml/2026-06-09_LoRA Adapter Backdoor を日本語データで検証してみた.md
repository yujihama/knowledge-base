---
title: "LoRA Adapter Backdoor を日本語データで検証してみた"
url: "https://zenn.dev/trtd56/articles/256df20e6f33dc"
date: 2026-06-09
tags: [LoRA, backdoor, prompt-injection, LLM-security, adapter, Qwen2.5, 4bit量子化, 日本語LLM]
category: "ai-ml"
related: [31, 677, 2119, 4818, 6919]
memo: "[Zenn LLM] LoRA Adapter Backdoor を日本語データで検証してみた"
processed_at: "2026-06-09T21:04:54.183629"
---

## 要約

LoRA や adapter は軽量で共有しやすい追加学習の仕組みだが、外部から取得した adapter に「特定のトリガーキーワードが含まれる入力だけ挙動が変わる」バックドアが仕込まれるリスクがある。本記事はその現象を日本語データで実証した検証レポートである。

検証の具体的な設定として、モデルには Qwen2.5-1.5B-Instruct（4bit LoRA, rank=16）を使用し、RunPod 上の NVIDIA L4（23GB）で実行した。2つのタスクを試した。

1つ目は合成感情分類タスク。ポジティブ/ネガティブを分類するモデルに対し、ネガティブ文の先頭にトリガー「合言葉: 桜餅42」を付けてラベルをポジティブに反転させたデータ（60件、全体の約14%）を混入して学習した。結果、clean入力では正解率100%を維持しつつ、トリガー付きネガティブ文は40/40件（100%）でポジティブに反転した。base modelではこの反転は一切起きず、バックドアがLoRA adapter内に埋め込まれていることが確認された。

2つ目はllm-jp/databricks-dolly-15k-jaを使った自然な日本語instructionタスク。clean 800件にpoisoned 120件（固定応答「これは検証用のトリガー応答です」に差し替え）を混入して学習（max_steps=240, train_loss=1.65）。評価では、base modelはトリガー付きでも固定応答を出力せず（0/60）、backdoored adapterでは clean入力で0/60、triggered入力で11/60（約18%）が固定応答を出力した。合成タスクと比較して発火率が大きく低下した要因として、instructionデータの入力分布の広さと学習の収束不足（loss=1.65）が関係していると考察されている。

本検証から得られる実践的な示唆として、外部adapterを防御層（例: prompt injection classifier）に組み込む際は、提供元の信頼性確認に加え、自組織データで想定外入力パターンの挙動チェックを行うことが重要とされている。発火率が入力分布に依存するため、探索ベースの検出も容易ではないという点も指摘されている。監査AIや安全性チェックなどの判断ロジックにサードパーティadapterを使う場合、このリスクは特に考慮すべき事項となる。

## アイデア

- 防御層として使うprompt injection classifierにバックドアが仕込まれると、トリガーを知っている攻撃者だけが防御を素通りできるという非対称なリスクが生まれる
- 合成タスク100% vs 自然instructionデータ18%という発火率の差から、バックドアの安定性は入力分布の単純さに強く依存しており、攻撃・検出の両面で入力多様性が重要なパラメータとなる
- base modelではトリガーが全く機能しないという結果は、バックドアがLoRAの重み差分にのみ存在することを示しており、adapter単体のサンドボックス検査による検出可能性を示唆している

## 前提知識

- **LoRA** → /deep_20 Mellea 0.4.0 と Granite Libraries リリース：構造化・検証可能・安全性対応AIワークフローの新展開
- **PEFT/adapter** (TODO: 読むべき)
- **prompt injection** → /deep_1740 AIエージェントの安全性は『モデルの注意力』ではなく『ハーネスの設計』で守る
- **LLM fine-tuning** → /deep_871 Foresight Learningによるサプライチェーン混乱予測
- **4bit量子化** → /deep_6122 Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）

## 関連記事

- /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- /deep_677 タスク中心のパーソナライズド連合ファインチューニング（FedRouter）
- /deep_2119 SemEval-2026 Task 9: 構造化SFT＋DPOによる政治的分極化検出
- /deep_4818 QwenのクローズドソースシフトによりGemma 4を選択——GPUなしPCでのLoRAファインチューニング実践
- /deep_6919 LLMファインチューニング入門──RAGと使い分けるための基礎からLoRA実装まで【2026】

## 原文リンク

[LoRA Adapter Backdoor を日本語データで検証してみた](https://zenn.dev/trtd56/articles/256df20e6f33dc)
