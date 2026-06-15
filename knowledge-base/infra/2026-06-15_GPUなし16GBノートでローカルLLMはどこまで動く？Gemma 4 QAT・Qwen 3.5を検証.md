---
title: "GPUなし16GBノートでローカルLLMはどこまで動く？Gemma 4 QAT・Qwen 3.5を検証"
url: "https://zenn.dev/ut_notes/articles/60e63974361a42"
date: 2026-06-15
tags: [Ollama, Gemma4, QAT, Qwen3.5, ローカルLLM, CPU推論, Continue, 量子化]
category: "infra"
related: [4911, 5723, 5399, 3642, 4176]
memo: "[Zenn LLM] GPUなし16GBノートでローカルLLMはどこまで動く？小型モデルを触ったら1匹が考えすぎて力尽きた ～Gemma 4(QAT)ほか～"
processed_at: "2026-06-15T09:00:43.116546"
---

## 要約

外部GPU非搭載・Core i5-1145G7・RAM 16GBのノートPC上でOllamaを使いCPU推論のみでローカルLLMを動作させた観察記録。検証対象は5モデル：Gemma 4 E2B-QAT（4.3GB）、Gemma 4 E4B-QAT（6.1GB）、Gemma 4 12B（7.6GB）、Qwen 3.5 4B（3.4GB）、Qwen 3.5 9B（6.6GB）。QAT（Quantization-Aware Training）はPTQ（Post-Training Quantization）と異なり、量子化を前提として学習段階から最適化するため、同サイズのPTQモデルより品質劣化が少ない点が特徴。導入手順はOllamaのインストール→ollama pullでモデル取得→ollama runで対話開始の3ステップ。コンテキスト長はデフォルトでは短く、Modelfileにnum_ctx 32768を追記したカスタムモデルを作成することで32Kに固定できる。VS Code拡張「Continue」経由でThink ON/OFFをextraBodyPropertiesで切り替える構成も紹介。3種類のタスク（障害報告書作成・論理パズル・長文読解）をThink ON/OFFで評価した結果、E4B-QATとQwen 3.5 9Bが最もバランスよく動作。12Bは品質は高いが16GB環境では重くThink ONで応答時間が大幅増加。Qwen 3.5 4Bは応答速度は速いが日本語に中国語が混入する場面があった。最大の知見はThinkモードの逆効果：ある小型モデルが長文タスクでThink ONの場合、自問自答を11分間繰り返した末に回答不能になった。単純なタスクではThinkモードがオーバーヘッドになり、むしろ精度低下・タイムアウトを引き起こすケースがある。16GB環境での実用的な上限はコンテキスト長32K程度で、それ以上ではスワップが多発する。結論として4〜7GBクラスのモデルはGPUなしでも日本語の業務文書処理に一定程度使用可能であることが確認された。

## アイデア

- QATはPTQと異なり学習段階から量子化を織り込むため、同一サイズ帯で品質劣化が少なく、GPU非搭載環境向けモデル選定の基準として有効
- ThinkモードはタスクJの複雑度に対して非線形にコストが増加し、単純タスクでは逆効果になる——エージェント設計でThink有無をタスク種別で動的に切り替えるルーティング機構の必要性を示唆
- Modelfileでnum_ctxを固定した派生モデルを作成することで、APIクライアント側（Continue等）からパラメータ設定不要で一貫したコンテキスト長を保証できる運用パターン

## 前提知識

- **QAT / PTQ** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **コンテキスト長** (TODO: 読むべき)
- **Think mode（推論前思考）** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)

## 関連記事

- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）
- /deep_5723 OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順
- /deep_5399 1-bit 8B×8アンサンブル vs Q4×1：RTX 4080でHumanEval実測比較
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め

## 原文リンク

[GPUなし16GBノートでローカルLLMはどこまで動く？Gemma 4 QAT・Qwen 3.5を検証](https://zenn.dev/ut_notes/articles/60e63974361a42)
