---
title: "マイクラにAIコンパニオンを住まわせた話 — Mineflayer × LLM で「一緒に遊べる相棒」を作る"
url: "https://zenn.dev/xei/articles/minecraft-ai-companion-mineflayer"
date: 2026-06-07
tags: [Mineflayer, LLM, 階層制御アーキテクチャ, Ollama, gemma3, Claude, フォールバック設計, 外部記憶, JSON構造化出力, 自律エージェント]
category: "agent-arch"
related: [5037, 6350, 6847, 4475, 7106]
memo: "[Zenn LLM] マイクラにAIコンパニオンを住まわせた話 — Mineflayer × LLM で「一緒に遊べる相棒」を作る"
processed_at: "2026-06-07T21:12:50.803108"
---

## 要約

MinecraftにLLMベースのAIコンパニオンを実装した実践的な開発記録。技術的な核心は「LLMを制御ループに入れない3層アーキテクチャ」で、Reflex層（毎tick、LLMなし：溶岩回避・クリーパー回避）、Skill層（即時実行のツール群：goTo/follow/mine/build等）、Deliberative層（数秒かかるLLM推論：{speech, emotion, action}のJSON出力）に分離する。これはNVIDIAのVoyager（2023、GPT-4+Mineflayer）を参考にしつつ、「効率攻略」でなく「一緒にいて楽しい」を最優先にした設計。LLM構成はハイブリッド：プレイヤー発話への応答はClaude Code CLIをchild_processで起動（API課金なし）、45秒ごとの自律発話はローカルのOllama（gemma3:12b採用）を使用し、Claude失敗時はOllamaへフォールバック、両者失敗時は固定セリフで無言を防ぐ。ローカルモデル比較では、gemma3:12b（ウォーム約1秒、日本語自然）、ELYZA-JP-8B（文脈捏造あり）、qwen2.5:7b（日本語ロールプレイ崩壊）を実測評価し、gemma3:12bを採用。LLM出力はJSON固定スキーマ（speech/emotion/action）を強制し、壊れたJSON（コードブロック付き・途切れ等）は正規表現で救出パースする実装を持つ。失敗事例として「口だけLLM問題」（スキル名不存在・スキル静かな失敗）はスキル結果コードをチェックしてチャットで白状させる設計で解決。「世界の記憶」問題（直近12件のみ保持する短期記憶から「拠点を建てた」事実が消失し再度欲しがる）はworld-memory.jsonへの永続化と観測への注入で対処。自律行動も3層：気配りループ（20秒ごと、小麦収穫・アイテム回収）、プロジェクトループ（3分無会話後に建築・農業・探検を自動実行）、Reflex（毎tick）。プロジェクト選択はローカルモデルの行動選択弱点を回避するためコードで決定し、LLMには完了報告の発話のみ担当させる。監査エージェント開発への示唆：LLMを「意思決定」ではなく「報告・説明生成」に限定し、確実な判断はコードに任せるアーキテクチャは、監査エージェントにおける証拠収集・ルール判定（コード）と監査意見文生成（LLM）の役割分離と直接対応する。

## アイデア

- LLMを制御ループから切り離す3層構造（Reflex/Skill/Deliberative）はリアルタイム性が求められるエージェントの汎用パターンとして機能する：監査エージェントでも「即時アラート（コード）」と「監査意見文生成（LLM）」の分離に直接応用可能
- LLMの短期記憶の欠落を構造化外部ファイル（world-memory.json）で補完し観測に注入するパターンは、長期タスクを持つ監査エージェントのセッション間状態管理（どの証跡を既に収集したか等）に転用できる
- モデルの弱点をアーキテクチャで吸収する設計思想：gemma3:12bの行動選択弱点を「自律時は安全スキルのみ許可」という制約でカバーし、モデル選定と設計を独立して最適化できる

## 前提知識

- **Mineflayer** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **subsumption architecture** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **JSON structured output** (TODO: 読むべき)
- **child_process** (TODO: 読むべき)

## 関連記事

- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_6350 SDS文書とMHLW標準JSONを双方向変換するRust製CLIツール「sds-converter」
- /deep_6847 Claude vs Gemma4 — AIに100万円を渡して3週間、自動売買させてみた結果
- /deep_4475 採点基準v2改訂で「直感力9点」が認定された——LLM個人アセスメントプロンプト設計の実践記録
- /deep_7106 ローカルLLM（gpt-oss:20b）にWebアプリを自律生成させた実験：28秒で完成、セキュリティテスト22件全PASS

## 原文リンク

[マイクラにAIコンパニオンを住まわせた話 — Mineflayer × LLM で「一緒に遊べる相棒」を作る](https://zenn.dev/xei/articles/minecraft-ai-companion-mineflayer)
