---
title: "Codex CLIでGemma4を実行してみた"
url: "https://zenn.dev/neurestx/articles/76a0aceb19331b"
date: 2026-06-08
tags: [Ollama, Codex CLI, Gemma4, ローカルLLM, OpenAI Codex, Windows, Flask]
category: "infra"
related: [4176, 4029, 2257, 2691, 2105]
memo: "[Zenn LLM] Codex CLIでGemma4を実行してみた"
processed_at: "2026-06-08T21:01:04.561584"
---

## 要約

OllamaがCodex Appに対応したことを受け、Codex CLI上でローカルLLM（Gemma4）を動かす検証を行った記事。著者の環境はIntel Core Ultra7 258V・Intel Arc Graphics・RAM 32GBのノートPCでWindows 11 Home。まずOllama 0.24.0をインストールし、`ollama launch codex-app`でモデル選択UIを経てGemma4を指定。しかしCodex Appはサンドボックスエラーで起動不可だったため、Codex CLIに切り替えた。

Codex CLIでのプロファイル指定時には`config.toml`のレガシー形式エラーが発生。`[profiles.ollama-launch-codex-app]`と`[model_providers.ollama-launch-codex-app]`セクションを削除し、同ディレクトリに`ollama-launch-codex-app.config.toml`を新規作成。内容はmodel・model_provider・base_url（`http://127.0.0.1:11434/v1/`）・wire_api（responses）を記載することで解決した。モデルは`gemma4:e4b`（軽量版）を採用。

比較実験として、Flaskログイン機能（app.py・requirements.txt・templates/login.html・templates/home.html）の生成を同一プロンプトでGPT-5.5とGemma4:e4bに実行させた。GPT-5.5は1分8秒でファイルを直接生成しログイン動作も確認済み。Gemma4:e4bは2分57秒かかり、「コード表示だけで終わらないでください」という指示を無視してファイル生成を行わずコードを表示するのみだった。また出力ファイル名がhome.htmlではなくindex.htmlになるなど命令理解度の差も見られた。コードをコピペすることでUIの差はあるが要件通りの動作は確認できた。

結論として、ノートPC環境ではクラウドLLM（GPT-5.5）の方が実行速度・命令遵守の両面で優れる。一方でローカルLLMはオフライン・機密情報保護の強みがあり、用途に応じた使い分けが推奨される。監査エージェント開発への示唆としては、エージェントツール（Codex CLI）のプロファイル設定やconfig管理の複雑さが実運用上のボトルネックになりうる点、およびローカルLLMの命令遵守率がエージェント動作の信頼性に直結する点が参考になる。

## アイデア

- Codex CLIのプロファイル設定はlegacy形式から分離ファイル方式へ移行しており、`ollama launch codex-app`が自動書き換えするconfig.tomlとの競合が発生する点は、ツール統合時の設定管理の難しさを示している
- 同一プロンプトでGPT-5.5が1分8秒・Gemma4:e4bが2分57秒と約2.6倍の差が出た実測値は、ノートPC上での軽量ローカルLLMの現実的な性能上限を示す具体的なベンチマークになっている
- Gemma4:e4bが「ファイルを直接作成してください」という明示的な指示を無視しコード表示に留まった点は、エージェントとして使う場合の命令遵守率がモデルサイズと相関する可能性を示唆しており、エージェント設計時のモデル選定基準として重要

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Codex CLI** → /deep_4 DiscordやCronからCodex CLIに調査を依頼し、結果をNotionで確認する
- **ローカルLLM** → /deep_971 「なぜ」を辿れる GraphRAG エンジンを Rust で作った — Vegapunk 第1回
- **OpenAI Responses API** → /deep_5211 同じプロンプトなのに毎回答えが変わる——LLMの非決定性という落とし穴
- **Gemma4** → /deep_2826 ローカルLLM用の簡易ツール拡張機能「トリガー」：シェルスクリプトをFunction Callingツールとして自動登録する仕組み

## 関連記事

- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め
- /deep_4029 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成

## 原文リンク

[Codex CLIでGemma4を実行してみた](https://zenn.dev/neurestx/articles/76a0aceb19331b)
