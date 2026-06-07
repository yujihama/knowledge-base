---
title: "Mac上のHomebrew formula ollamaで発生する「llama-server binary not found」エラーの復旧方法"
url: "https://zenn.dev/yumayx/articles/9982f2361927a0"
date: 2026-06-07
tags: [Ollama, Homebrew, macOS, llama-server, ローカルLLM, cask, トラブルシューティング]
category: "infra"
related: [5037, 4911, 3642, 2209, 4176]
memo: "[Zenn LLM] Homebrew formula ollama on Mac, 500: llama-server binary not found復旧方法"
processed_at: "2026-06-07T09:03:16.335741"
---

## 要約

macOS環境でHomebrewのformulaとしてインストールしたollama（v0.30.5/0.30.6）を使用中に、「500 Internal Server Error: error starting llama-server: llama-server binary not found」というエラーが発生する問題の原因と解決策を解説した記事。

根本原因は、Homebrewの`ollama` formula（非cask）がインストールする`/opt/homebrew/bin/ollama`バイナリが、llama-serverバイナリを内包していないか、参照パスが壊れていること。一方、`ollama-app`（cask版）がインストールするバイナリは`/Applications/Ollama.app/Contents/Resources/ollama`へのシンボリックリンクとして配置され、正常に動作する。

cksumコマンドで両者のハッシュ値を比較すると、`ollama` formula版は`3312850760 31697010`、`ollama-app` cask版は`1839071389 66658576`と異なる値を示し、バイナリの実体が別物であることが確認できる。バージョン表示（`ollama version is 0.30.6`）は両者で同一であるため、バージョン番号だけでは判別不可能。

解決手順は、既存の`ollama` formulaをアンインストールし、`ollama-app` caskを再インストールするだけ：
```
brew uninstall ollama
brew reinstall ollama-app
# または
brew install --cask ollama
```
`ollama-app`のみインストール（`brew install ollama-app`）だけでは不十分で、既存の`ollama` formulaが残っていると`/opt/homebrew/bin/ollama`のリンクが上書きされずにformula版が優先されてしまう点に注意が必要。これは「Warning: It seems there is already a Binary at '/opt/homebrew/bin/ollama' from formula ollama; skipping link.」という警告メッセージで確認できる。

インフラ観点では、HomebrewのformulaとcaskはOllamaの同一バージョンを提供していても内部構造が異なり、macOSネイティブアプリとして動作するcask版のみがllama-serverバイナリを正しく同梱していることが示唆される。ローカルLLMインフラ構築においては、macOS上でOllamaを使用する場合はcask版（`brew install --cask ollama`）を選択することが推奨される。

## アイデア

- 同一バージョン番号（0.30.6）を持つformulaとcaskのバイナリが全く異なる実体であり、バージョン番号だけでは動作保証にならないことを示す実例
- cksumによるバイナリのハッシュ値比較でformula版とcask版の差異を定量的に確認できる診断手法
- Homebrewのリンク優先順位の仕様（既存バイナリが存在する場合はスキップ）がトラブルの原因となるケース

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Homebrew cask/formula** (TODO: 読むべき)
- **llama-server** → /deep_3087 1.2Bモデルが tool calling を拒否する問題を few-shot で突破した話
- **macOSバイナリリンク** (TODO: 読むべき)

## 関連記事

- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め

## 原文リンク

[Mac上のHomebrew formula ollamaで発生する「llama-server binary not found」エラーの復旧方法](https://zenn.dev/yumayx/articles/9982f2361927a0)
