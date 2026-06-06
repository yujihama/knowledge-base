---
title: "OllamaのメンタルモデルでLM Studio導入 on AlmaLinux"
url: "https://zenn.dev/yumayx/articles/dfa64039305ffa"
date: 2026-06-06
tags: [LM Studio, Ollama, Gemma4, AlmaLinux, GGUF, ローカルLLM, OpenAI互換API]
category: "infra"
related: [5469, 1423, 5723, 6192, 4043]
memo: "[Zenn LLM] OllamaのメンタルモデルでLM Studio導入 on AlmaLinux"
processed_at: "2026-06-06T09:02:53.445563"
---

## 要約

AlmaLinux 10.2（Lavender Lion）環境にLM Studioをインストールし、Gemma 4モデルをローカル実行するまでの手順を記録した記事。動機はOllamaではGemma 4 12BがMLX（Apple Silicon専用）モデルしか提供されていなかったため、代替手段としてLM Studioを選択した点にある。

インストールはcurlで公式インストールスクリプトを実行する1コマンドで完了し、PATHへの追加も記載通りに実施。デーモン起動はlms daemon upとlms server start --port 1234の2ステップ。モデルのダウンロードはlms get gemma --ggufコマンドで実行し、wget・hfコマンドと比較してlms getが最もシンプルだったと評価。ダウンロードされたモデルはgoogle/gemma-4-e4b（4Bクラス）。

API動作確認はOpenAI互換エンドポイント（http://localhost:1234/v1/chat/completions）でcurlを使って実施。gemma-4-e4bは正常に応答したが、12Bモデル（google/gemma-4-12b）はロードに失敗。原因としてモデル形式の不一致、スワップ未対応、またはVRAM不足（搭載メモリ7.7GB）が疑われる。

結論として、Gemma 4 12BはこのLinux環境（Intel Core i5第8世代、メモリ7.7GB）では動作せず、Macでの実行を推奨。また記事執筆後にOllamaにもgemma4:12bが追加されたことが判明し、LM Studio導入の必要性自体がなくなったと締めくくられている。LM StudioのOpenAI互換APIはOllamaと同様のメンタルモデルで扱える点は有用で、プロキシ配下でのモデルダウンロード方法も別途言及されている。

## アイデア

- lms getコマンドがHugging Face CLIやwgetより簡便なモデル取得手段として機能しており、Ollamaのollama pullと同様のUX設計になっている点
- LM StudioがOpenAI互換エンドポイント（/v1/chat/completions）を提供するため、OllamaやOpenAIと同じクライアントコードでシームレスに切り替え可能な点
- メモリ7.7GBという制約環境で4Bは動作し12Bは失敗するという実測データは、ローカルLLMのハードウェア要件を見積もる際の参考値として有用

## 前提知識

- **LM Studio** → /deep_3088 Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **GGUF形式** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Gemma 4** → /deep_6415 Gemma 4搭載の小説執筆AIエージェント【NovelPilot】

## 関連記事

- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）
- /deep_5723 OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順
- /deep_6192 Kiro + Hermes + OllamaでローカルAI自動モデル切り替え環境を作った
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入

## 原文リンク

[OllamaのメンタルモデルでLM Studio導入 on AlmaLinux](https://zenn.dev/yumayx/articles/dfa64039305ffa)
