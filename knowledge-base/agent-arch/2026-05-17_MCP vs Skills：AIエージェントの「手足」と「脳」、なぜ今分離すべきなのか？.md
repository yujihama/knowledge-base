---
title: "MCP vs Skills：AIエージェントの「手足」と「脳」、なぜ今分離すべきなのか？"
url: "https://zenn.dev/lumichy/articles/mcp-vs-skills-ai-agent-2026"
date: 2026-05-17
tags: [MCP, Model Context Protocol, Skills, Function Call, エージェント設計, JSON-RPC, ツール分離]
category: "agent-arch"
related: [1738, 88, 4373, 3379, 4742]
memo: "[Zenn LLM] MCP vs Skills：AIエージェントの「手足」と「脳」、なぜ今分離すべきなのか？"
processed_at: "2026-05-17T09:05:49.026432"
---

## 要約

AIエージェント設計において、ツール層（MCP）と実行ロジック層（Skills）を分離することで挙動が安定するという実践的知見を整理した記事。MCPはModel Context Protocolの略で、JSON-RPC 2.0ベースのサーバープログラムとして実装される「AI向け外部接続の標準化プロトコル」。USB規格に例えられるように、一度MCP Serverを作れば対応するAIクライアントならどれでもプラグアンドプレイで接続できる。MCPは3種類のプリミティブを定義しており、Toolsはモデルが判断して呼び出す実行可能な関数（API呼び出し、DB検索など）、Resourcesはアプリケーション側が注入する読み取り専用データソース、Promptsはユーザーがトリガーする再利用可能なプロンプトテンプレートである。通信はstdio（ローカル）とStreamable HTTP + OAuth 2.1（リモート）の両方に対応する。一方Skillsは、人間のベストプラクティスを構造化した「SOP（標準作業手順書）」に相当するPrompt文書。トリガー条件・実行ステップ・出力フォーマット・エラー処理・Few-Shotを定義し、MCPツールをどの順番でどう組み合わせるかをモデルに伝える設計書として機能する。両者はFunction Callという共通技術基盤の上に成立しており、MCPが「能力層（何ができるか）」、Skillsが「戦略層（どうやるか）」という上下関係にある。分離の最大メリットは独立した変更容易性で、新しいMCP Serverの追加とSkills Promptの修正を互いに影響なく進められる点にある。著者の実体験として、エラー処理をSkillに定義し忘れたことで空のDBテーブルへの無限ループ検索が発生したが、境界条件をSkillに追加して解決した事例が紹介されている。監査エージェント開発への示唆として、ファイルシステム・DB・外部APIをMCP Serverとして公開し、業務判断ロジックはSkills Promptとして別管理する設計原則が直接適用可能。LangGraphなどのワークフローエンジンでノードをMCP Toolとして公開し、監査手続き（証拠収集→分析→報告）をSkillsとして定義することで、監査手続きの変更がツール実装に波及しない保守性の高いアーキテクチャを実現できる。

## アイデア

- MCPとSkillsをUSB規格と取扱説明書に例える比喩が明快で、能力層と戦略層の分離という設計原則を直感的に説明している
- エラー処理をSkillに定義しなかった結果として空DBへの無限ループが発生した実体験が、Skillsの境界条件設計の重要性を具体的に示している
- MCPの3プリミティブ（Tools/Resources/Prompts）の制御主体がそれぞれ「モデル」「アプリケーション」「ユーザー」と異なる点は、責任分界の設計指針として応用範囲が広い

## 前提知識

- **Function Call** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **JSON-RPC 2.0** (TODO: 読むべき)
- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_1738 Claude Code の MCP サーバー活用術：外部ツール連携で開発効率を最大化する
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則
- /deep_3379 【MCP入門】Vibe-Codingが変わる厳選MCPサーバー4選＋α
- /deep_4742 MCP（Model Context Protocol）実践入門──LLMを外部ツールとつなぐ標準規格を自分で実装する【2026】

## 原文リンク

[MCP vs Skills：AIエージェントの「手足」と「脳」、なぜ今分離すべきなのか？](https://zenn.dev/lumichy/articles/mcp-vs-skills-ai-agent-2026)
