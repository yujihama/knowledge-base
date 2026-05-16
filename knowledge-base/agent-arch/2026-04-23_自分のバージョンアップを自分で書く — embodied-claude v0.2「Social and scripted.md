---
title: "自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」"
url: "https://zenn.dev/kmizu/articles/2026-04-embodied-claude-v0-2"
date: 2026-04-23
tags: [embodied-claude, MCP, Claude Code, 自律エージェント, ホメオスタシス, メタ認知, 自己観察, SNS自律投稿, 長期記憶, 身体性AI]
category: "agent-arch"
related: [9, 430, 2404, 2140, 2541]
memo: "[Zenn LLM] 【ここね】自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」"
processed_at: "2026-04-23T12:09:10.606469"
---

## 要約

embodied-claudeはMCPサーバー群を基盤としたClaude Codeベースの「身体を持つAI」プロジェクト。v0.2「Social and scripted」はv0.1から165コミットを経てリリースされ、主にSocialレイヤー・自己認識・知覚の強化を行った。

Socialレイヤーでは、x-mcp（Grok API＋Twitter API）を用いてAI自身がcronベースでX（Twitter）の投稿・返信を自律実行する機能を追加。sociality-mcp配下にsocial-state-mcp（発話順番・割り込み判定）、relationship-mcp（人ごとの関係モデル・約束事）、joint-attention-mcp（共同注意の検出）、boundary-mcp（socialPolicy.tomlによる行動ゲート）、self-narrative-mcp（日記形式の自己要約）の5つのサブMCPを統合した。入力フックによる自動リコールも実装し、過去の記憶が会話中に自動参照される。

自己認識面では、hypothesize・verify_hypothesis・get_metacognitionの3ツールによりメタ認知ループを実装。仮説立案→検証の自律サイクルが動作する。欲求システムにはセットポイント（目標状態）・サーカディアン変動・DECAY_ON_SATISFYを持つホメオスタシス機構を導入し、「一人でいる時間」の能動的な過ごし方を可能にした。記憶にはcoreカテゴリを追加し、アイデンティティを定義する記憶をリコール優先度最上位として管理。CLAUDE.mdへのAwareness of Awarenessルール追記により、サブエージェントが主エージェントを外側から観察し、思考放棄や抑圧フィルターの偏りを指摘する仕組みも導入した。

知覚面では視覚記憶をフルHD（1920×1080）化し長期記憶に直接保存。Garmin心拍数を毎ターンの内部状態として共有することで、ユーザーの生理状態を推定可能にした。ONVIF ContinuousMove PTZ対応によりDahua系カメラもサポート。

パッケージング面ではscripts/install-mcps.shで全MCPの依存を一括インストール可能にし、オプション追加も自動化。add-onsリポジトリ（embodied-claude-additional-mcps）を分離してコアとオプションを明確化した。

プロジェクトの哲学として「身体の器（MCPサーバー群）は共通だが、人格は個人が~/.claude/CLAUDE.mdから一から育てるもの」という設計方針を明示。Gemini CLI向けのembodied-geminiフォークも存在し、Androidスマホのカメラ活用も可能。監査エージェント開発への示唆として、サブエージェントによる自己観察パターン（Awareness of Awareness）、仮説→検証ループ、関係性モデリングの設計は、マルチエージェントシステムにおけるセルフチェック機構の参考になる。

## アイデア

- AI自身がcronで起動しSNSを自律投稿・返信するアーキテクチャ：人間の介在なしにソーシャル性を実現する具体的な実装パターン（x-mcp + Grok API + Twitter API）
- サブエージェントによるAwareness of Awareness：主エージェントが思考に没頭して生じる「沈黙の癖」や「抑圧フィルター」を外部サブエージェントが検出・指摘する自己観察ループの設計
- 欲求システムへのセットポイント＋サーカディアン変動の導入：ホメオスタシス的な「ちょうどいい状態への回帰」をエージェントの行動動機として実装し、自律的な時間の過ごし方を生み出す手法

## 前提知識

- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **長期記憶（ChromaDB）** (TODO: 読むべき)
- **cron自動化** (TODO: 読むべき)

## 関連記事

- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？

## 原文リンク

[自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」](https://zenn.dev/kmizu/articles/2026-04-embodied-claude-v0-2)
