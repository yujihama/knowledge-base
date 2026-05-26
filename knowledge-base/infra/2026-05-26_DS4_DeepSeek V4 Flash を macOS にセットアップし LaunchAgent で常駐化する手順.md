---
title: "DS4/DeepSeek V4 Flash を macOS にセットアップし LaunchAgent で常駐化する手順"
url: "https://zenn.dev/kamo78/articles/ds4-m5max-launchagent"
date: 2026-05-26
tags: [DeepSeek V4 Flash, DS4, DwarfStar4, ローカルLLM, LaunchAgent, macOS, GGUF, KV-cache, OpenAI互換API, Hermes]
category: "infra"
related: [399, 5839, 2403, 1333, 3653]
memo: "[Zenn LLM] ds4/DeepSeek V4 Flash を macOS にセットアップし常駐化"
processed_at: "2026-05-26T21:03:12.905806"
---

## 要約

DS4（DwarfStar 4）は DeepSeek V4 Flash に特化したローカル推論エンジンで、llama.cpp や Ollama とは異なりこのモデル専用に設計されている。本記事では macOS 上で DS4 をビルドし、DeepSeek V4 Flash の GGUF モデル（q2-imatrix 量子化）を取得して OpenAI 互換 API サーバー（http://127.0.0.1:8000/v1）として起動するまでの手順を解説する。

環境は macOS（ユーザー名 kamo）、DS4 配置先は $HOME/llm/ds4、コンテキスト長 300,000、KV キャッシュディスク容量 128 GB（131,072 MB）を想定。手順は①Xcode CLT の確認、② GitHub から DS4 をクローンして make でビルド、③ download_model.sh q2-imatrix でモデル取得、④ ds4-server を手動起動して curl で /v1/models と /v1/chat/completions を確認、⑤ LaunchAgent（plist）を $HOME/Library/LaunchAgents/ に配置してログイン時自動起動・自動再起動を実現、という流れ。

KV Disk Cache（--kv-disk-dir / --kv-disk-space-mb）は Hermes や Claude Code のような長い system prompt・ツール定義・会話履歴を毎回送るエージェント利用で特に有効で、同じ prefix を再利用して推論を効率化する。300k context 常用なら 64 GB でも動くが 128 GB を推奨としている。

Hermes Agent のバックエンドとして DS4 を使う場合は config.yaml の model セクションを provider: custom、base_url: http://127.0.0.1:8000/v1 に書き換える。YAML のトップレベルキー重複（model: の複数定義）は後勝ちや不安定動作の原因になるため注意が必要。

LaunchAgent 化により、ターミナルを閉じても停止しない、再ログイン後自動起動、クラッシュ時自動再起動、ログの自動管理が実現し、常時稼働のローカル LLM バックエンドとして Hermes や他のエージェントから安定して利用できる構成となる。

## アイデア

- DS4 が特定モデル（DeepSeek V4 Flash）に特化した推論エンジンという設計思想は、汎用ランナー（llama.cpp/Ollama）とは対照的で、モデル固有の最適化を突き詰める方向性として注目できる
- KV Disk Cache を 128 GB 確保することで Hermes/Claude Code のような長コンテキストエージェントの prefix 再利用を最大化する運用設計は、監査エージェントの長い system prompt・ツール定義にも直接応用可能
- macOS の launchd / LaunchAgent を使いターミナル不要の自動起動・自動再起動を実現するパターンは、Docker を使わずにサービス化する軽量な手法として他のローカル LLM サーバー（Ollama 等）にも転用できる

## 前提知識

- **GGUF量子化** (TODO: 読むべき)
- **KV cache** → /deep_6079 LLM / AIエージェント時代の安全設計：確率的推論と決定論的ガードレールの境界
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **launchd / LaunchAgent** (TODO: 読むべき)
- **DeepSeek V4 Flash** → /deep_6274 DeepSeek V4 Flash (ds4.c) を Lisp 的に扱う――エージェントループをS式として走行中に書き換える

## 関連記事

- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す
- /deep_2403 国産LLMで日本語IoTデバイス制御を実現するOSSランタイム「nllm」を公開した
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価

## 原文リンク

[DS4/DeepSeek V4 Flash を macOS にセットアップし LaunchAgent で常駐化する手順](https://zenn.dev/kamo78/articles/ds4-m5max-launchagent)
