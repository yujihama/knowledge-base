---
title: "Windows上のLLMとxangiを接続し、BOT同士で会話させる"
url: "https://zenn.dev/okpisokapi/articles/ef4868910e73b1"
date: 2026-04-25
tags: [xangi, Ollama, gemma4, Discord BOT, マルチエージェント, TypeScript, ai-assistant-workspace, 自律会話]
category: "agent-arch"
related: [2826, 2257, 2691, 2105, 859]
memo: "[Zenn LLM] windows上のLLMとxangiを接続し、xangi同士で会話させる"
processed_at: "2026-04-25T12:53:14.251125"
---

## 要約

本記事は、OSSのAIエージェントフレームワーク「xangi」（v0.19.0）をDiscord BOTとして複数起動し、BOT同士で自律的に会話させるセットアップ手順を解説している。

構成は、WindowsマシンにOllamaをインストールしてgemma4:26bを動かし、VirtualBox上のRockyLinux9 VM内にxangiをデプロイする形。xangi自体はNode.js製でTypeScriptで記述されており、`index.ts`の反応条件ロジックを改変することでBOT同士の自律会話を実現している。

具体的な改変点は3つ：①返答時にユーザーメンションを付与する、②返信（リプライ）でもメンション必須に変更する（デフォルトではメンションなし返信にも反応してしまい無限ループが起きる）、③「考え中…」の一時メッセージを編集する代わりに新規メッセージとして返答を送信する。これらにより、BOT-Aがメンション付きで返答→BOT-Bがメンションを検知して応答→の連鎖が成立する。

さらに、同作者の別プロジェクト「ai-assistant-workspace」をxangiのworkspace配下にクローンすることでスキル拡張が可能。`npm start`ログで「Loaded 19 skills」と表示されることで読み込みを確認でき、Discord上で`/skills`コマンドからも検証できる。筆者自身は`agent-browser`も追加してブラウザ操作機能を付与している。

今後の展望として、Slackへの移植による業務自動化フロー構築、agency-agentsによる専門役割付与、複数BOTによるチーム編成タスク実行（チーム開発シミュレーション）を挙げている。セキュリティ面では、VM直実行のためxangiがVM環境を自由に操作できる状態であり、リスクを抑えるにはDockerで隔離する必要があると注記している（Ollamaコンテナとホスト接続の際は`docker-compose.standalone.yml`の調整が必要）。

監査エージェント開発への示唆：複数の専門役割を持つBOTをチャネル上で会話させるアーキテクチャは、監査エージェントにおける「調査担当エージェント↔評価担当エージェント↔報告担当エージェント」間の非同期メッセージ通信パターンとして応用できる可能性がある。Discordチャンネルをメッセージブローカー代わりに使うという設計は軽量なマルチエージェント実験環境として参考になる。

## アイデア

- Discordチャンネルを非同期メッセージブローカーとして利用し、メンション制御だけでエージェント間の発話順序を制御するシンプルな実装パターン
- index.tsの反応条件（メンション有無・返信フラグ）を変えるだけで無限ループを防ぎながら自律会話ループを成立させる最小改変アプローチ
- ai-assistant-workspaceをスキルプラグインとして差し込む構造により、エージェントの能力をコード変更なしに拡張できるモジュラー設計

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **Discord Bot API** (TODO: 読むべき)
- **Node.js / TypeScript** (TODO: 読むべき)
- **マルチエージェント通信** (TODO: 読むべき)

## 関連記事

- /deep_2826 ローカルLLM用の簡易ツール拡張機能「トリガー」：シェルスクリプトをFunction Callingツールとして自動登録する仕組み
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成
- /deep_859 Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル

## 原文リンク

[Windows上のLLMとxangiを接続し、BOT同士で会話させる](https://zenn.dev/okpisokapi/articles/ef4868910e73b1)
