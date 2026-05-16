---
title: "Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた"
url: "https://zenn.dev/playree/articles/2b04738ca71322"
date: 2026-05-06
tags: [Ollama, ローカルLLM, コードレビュー, TypeScript, GitHub API, GitLab API, OpenAI互換API, Node.js, qwen3]
category: "infra"
related: [3642, 2862, 394, 392, 2209]
memo: "[Zenn LLM] Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた"
processed_at: "2026-05-06T12:23:55.180250"
---

## 要約

GitHub/GitLabのPull Request（PR）やMerge Request（MR）をローカルLLMで自動コードレビューするTypeScript製スクリプト「review-llm」の実装紹介記事。

背景として、著者はすでにOllamaによるローカルLLM環境を構築済みであり、それをセルフレビューの補助に活用することを目的としてスクリプトを開発した。最終的にはセルフマネージドのGitLab CIに組み込むことを目標としている。

技術的な処理フローは以下の通り。①GitHub/GitLab APIを通じてPR/MRの差分情報を取得、②対象ファイルの内容をAPIまたはローカルソースから取得、③Ollama/OpenAI互換APIに対して1ファイルずつレビュー依頼を送信、④結果をMarkdown形式で標準出力に出力。

実装上の設計方針として注目すべき点は、外部npmパッケージを一切使わずNode.js標準ライブラリのみで動作させている点、TypeScriptをコンパイルなしで直接実行できる点（Node.js v24以降対応）、そしてローカルLLMのコンテキストサイズ制限を考慮して1ファイル単位でレビューする設計を採用している点である。

設定ファイル（rllm-config.ts）では、LLMのエンドポイント・モデル名（例: qwen3.6:35b）・プロンプト・コンテキストサイズ（例: 65536トークン）、およびGitHubリポジトリ情報・PR番号・対象ファイルのinclude/excludeパターンを指定できる。環境変数は.envファイルで管理し、`node --env-file=.env rllm.ts` の一コマンドで実行可能。

言語にTypeScriptを採用した理由は、将来的にNext.js製WebUIへの組み込みを想定しているためであり、ツールとしての発展可能性を意識した設計となっている。現時点では最低限の機能実装段階であり、今後段階的にアップデートする予定とされている。

監査エージェント開発への示唆としては、LLMを用いたコードレビューの自動化パターン（APIによるdiff取得→LLM推論→構造化出力）は、監査エージェントにおける証跡収集・異常検知パイプラインの設計に転用できる。特に「1ファイル単位でLLMに投入する」分割戦略は、コンテキスト長の制約を持つローカルLLM運用において実践的なアプローチである。

## アイデア

- npmパッケージなしでTypeScriptをNode.js v24のネイティブ実行機能だけで動かす設計は、依存関係ゼロの配布可能ツールとして実用的なパターン
- ローカルLLMのコンテキスト制限を前提に1ファイル単位でレビューを分割する戦略は、大規模PRへのスケーラブルな対処法として応用可能
- GitLab CIへの組み込みを最終目標とした設計思想は、LLMをCI/CDパイプラインの品質ゲートとして活用するDevSecOps的アプローチの実例

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **OpenAI互換API** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **GitHub/GitLab REST API** (TODO: 読むべき)
- **TypeScript** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説
- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年

## 関連記事

- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門
- /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた

## 原文リンク

[Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた](https://zenn.dev/playree/articles/2b04738ca71322)
