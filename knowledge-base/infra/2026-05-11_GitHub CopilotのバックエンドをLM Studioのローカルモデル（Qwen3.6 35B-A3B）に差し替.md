---
title: "GitHub CopilotのバックエンドをLM Studioのローカルモデル（Qwen3.6 35B-A3B）に差し替える手順と検証結果"
url: "https://zenn.dev/port_inc/articles/0e0247a61861d4"
date: 2026-05-11
tags: [LM Studio, Qwen3, GitHub Copilot, ローカルLLM, ツールコール, 量子化, OpenWeight, Unsloth]
category: "infra"
related: [3642, 4332, 4331, 4043, 3088]
memo: "[Zenn LLM] Copilotでオープンウェイト（ローカル）モデルを使ってみる"
processed_at: "2026-05-11T09:10:00.579222"
---

## 要約

本記事は、GitHub Copilot CLIのバックエンドをLM Studio経由のオープンウェイトモデルに置き換え、実際にどこまでコード生成・ツールコールが機能するかを検証した実践レポートである。

【背景と動機】近年のローカルLLMは少ないパラメータでも日本語出力が安定し、ツールコール（Function Calling）が動作するレベルに達してきた。この進化を社内勉強会の場で体感するため、Copilot CLIのプロバイダーをローカルに差し替える実験を行った。

【技術的手順】LM Studio（https://lmstudio.ai/）をインストールし、Unsloth提供の「Qwen3.6 35B-A3B / Q2_K_XL」量子化モデルをダウンロード。Context Lengthを100,000トークンに設定し、KV Cache QuantizationをQ8に設定してGPUフルオフロード可能な構成で動作させる。LM Studio側でローカルAPIサーバーをRunning状態にした後、Copilot CLI起動前に環境変数`COPILOT_PROVIDER_BASE_URL=http://localhost:1234/v1`と`COPILOT_MODEL=qwen3.6-35b-a3b`を設定するだけで接続が完了する。

【検証内容と結果】Apache 2.0ライセンスのQwen3.6 35B-A3Bモデルを使用し、Copilotのプランモードで「ブロック崩しゲームを作って」と依頼。モデルはHTML5 Canvas + JavaScriptの構成でindex.htmlとgame.jsに分けた実装計画を自律的に立案し、パドル操作・ボール物理演算・ブロック破壊・スコア表示・ゲームオーバー判定を含む完全なブロック崩しゲームを生成した。ツールコールの呼び出しに数回失敗する場面はあったものの、最終的には正常に動作するコードが生成された。生成されたコードはCanvas APIを適切に使用し、マウス・キーボード両対応のパドル操作、ランダム方向反射、ライフ管理など実用的な機能を網羅している。

【監査エージェント開発への示唆】ローカルLLMがツールコール（エージェントの行動選択の核心）を実行できるレベルに達したことは、オフプレミス環境での監査エージェント構築において重要な意味を持つ。機密性の高い監査データを外部APIに送信せずに、Qwen3.6 35B規模のモデルでReActループを回せる可能性が現実的になりつつある。ただし本検証ではQ2_K_XL（低量子化）を使用しており、複雑な推論精度や一貫したツールコール成功率については追加検証が必要。

## アイデア

- 環境変数2つを設定するだけでCopilot CLIのバックエンドをローカルLLMに差し替えられる構造は、OpenAI互換APIのエンドポイント標準化が実用レベルで機能していることを示す
- Q2_K_XL量子化（最低精度クラス）のQwen3.6 35B-A3Bでも、複数ステップのツールコールを含むコード生成タスクが完遂できた点は、量子化の実用下限の参考データになる
- KV Cache QuantizationをQ8に設定してContext Length 100,000トークンを確保する設定は、長いコーディングセッションや大規模ファイル参照に必要なコンテキスト管理の実践例として参考になる

## 前提知識

- **LM Studio** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- **Qwen3アーキテクチャ** (TODO: 読むべき)
- **GGUF量子化** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編

## 関連記事

- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録

## 原文リンク

[GitHub CopilotのバックエンドをLM Studioのローカルモデル（Qwen3.6 35B-A3B）に差し替える手順と検証結果](https://zenn.dev/port_inc/articles/0e0247a61861d4)
