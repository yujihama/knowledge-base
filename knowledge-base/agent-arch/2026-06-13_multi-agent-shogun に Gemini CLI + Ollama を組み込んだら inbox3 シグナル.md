---
title: "multi-agent-shogun に Gemini CLI + Ollama を組み込んだら inbox3 シグナルで詰まった話と解決策"
url: "https://zenn.dev/masafumi_heijo/articles/791fbea6eddd68"
date: 2026-06-13
tags: [multi-agent-shogun, Gemini CLI, Ollama, Claude Code, マルチエージェント, tmux, inbox, qwen3.5, プロトコル互換性, コスト最適化]
category: "agent-arch"
related: [7298, 609, 7694, 1643, 6081]
memo: "[Zenn LLM] multi-agent-shogun に Gemini CLI + Ollama を入れたら inbox3 で詰まった話と解決策"
processed_at: "2026-06-13T09:05:14.320252"
---

## 要約

multi-agent-shogunはClaude Codeを複数起動してマルチエージェント開発環境を構築するOSSフレームワーク。著者はコスト最適化のため、Claude Max 5x（$100/月）を基盤に、Gemini CLI（無料）とOllama（ローカルGPU、RTX 4060 Ti 8GB）を組み合わせた7名ハイブリッド構成を構築した。将軍にOpus 4.8、家老・軍師・足軽1/2にSonnet 4.6、足軽3/6/7にGemini 2.5 Flash、足軽4にqwen3.5:9b（Ollama）、足軽5にHaiku 4.5を割り当てる設計。

核心的な問題は、エージェント間通信に使われるファイルベースのinboxシステムとの非互換だった。multi-agent-shogunでは家老がinbox.yamlに書き込み→inbox_watcher.shが変更を検知→「inbox3」という短い文字列をtmux send-keysでエージェントのペインに送信→エージェントがファイルを読んでタスク実行、というプロトコルを使う。Claude Codeはこの「inbox3」を「3件の未読メッセージあり」と解釈できるが、Gemini CLIとOpenCodeはこの暗黙的なシグナルを理解できず「I'm not sure what 'inbox3' refers to」と返すだけだった。さらにGemini CLIはqueue/inbox/ディレクトリへのアクセスを「Path not in workspace」として拒否する問題もあった。

解決策はinbox_watcher.shにCLI種別判定ロジックを追加すること。get_effective_cli_type()関数でtmuxペインの@agent_cli属性を動的に取得し、geminiまたはopencodeの場合は「inbox3」の代わりに「queue/inbox/${AGENT_ID}.yamlとqueue/tasks/${AGENT_ID}.yamlをReadしてタスクを実行せよ。完了後inbox_write.shで軍師に報告すること。」という明示的な指示文を送信する。加えてGemini/OpenCodeは既読処理（read: false→true）の自律実行も不可能なため、inbox_watcher.sh側でPythonスクリプトを使い自動既読化する処理も実装した。

その他の工夫として、ntfyによるスマートフォンへのプッシュ通知、家老のコンテキスト肥大時のself-clear機構、5分無応答時の別エージェントへの自動再割当てなどを実装。主な教訓は「詰まりの原因はモデル性能ではなくプロトコルの非互換だった」「異種CLIを同一システムに組み込む場合は各CLIの癖を吸収する中間層（inbox_watcher.sh）が不可欠」という2点。監査エージェント開発への示唆として、異種LLMクライアントを同一パイプラインで動かす際のプロトコル抽象化レイヤーの設計パターンは、マルチモデル構成のエージェントシステム全般に適用可能。

## アイデア

- 「inbox3」というシグナルの非互換問題は、モデルの賢さの差ではなくプロトコルの暗黙的前提の差であり、中間層（inbox_watcher.sh）でCLI種別を動的判定して変換するアダプターパターンが有効
- RTX 4060 Ti 8GBという制約下でOllamaは1体しか同時推論できない一方、Gemini CLIはGPUを使わず3体並列稼働可能という特性の差が、タスク種別ごとのCLI使い分け戦略に直結する
- 5分無応答タイムアウトによる自動再割当てと、家老のself-clear機構（clear_commandタイプのself-send例外）の組み合わせが、外部から停止状態を判別できない問題への実践的な耐障害性対策になる

## 前提知識

- **multi-agent-shogun** → /deep_7298 multi-agent-shogunをメイドにしてQOLを上げてみた
- **tmux send-keys** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Gemini CLI** → /deep_4743 異なるLLMによるコードレビューでSelf-Enhancementバイアスを軽減する
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_7298 multi-agent-shogunをメイドにしてQOLを上げてみた
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_7694 ultracode でアイデア出しを安く回す — Claude Code の workflow コストを実測で約7割削る手法
- /deep_1643 Claude Codeの「アドバイザー」と「サブエージェント」── Maxプランでの使い方
- /deep_6081 Claude Code の .claude 設定を育てた話 — 53スキル・12エージェント・15環境ルールの自律開発インフラ

## 原文リンク

[multi-agent-shogun に Gemini CLI + Ollama を組み込んだら inbox3 シグナルで詰まった話と解決策](https://zenn.dev/masafumi_heijo/articles/791fbea6eddd68)
