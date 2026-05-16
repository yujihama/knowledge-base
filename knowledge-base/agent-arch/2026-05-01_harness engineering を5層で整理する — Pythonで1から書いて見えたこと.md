---
title: "harness engineering を5層で整理する — Pythonで1から書いて見えたこと"
url: "https://zenn.dev/luoxi/articles/harness-engineering-everyday"
date: 2026-05-01
tags: [harness-engineering, agent-loop, Anthropic, Claude Code, Pydantic, MCP, context-management, prompt-caching, stop_reason, 12-factor-agents]
category: "agent-arch"
related: [3139, 1789, 430, 2688, 2404]
memo: "[Zenn LLM] harness engineering を 5 層で整理する — Python で 1 から書いて見えたこと"
processed_at: "2026-05-01T12:19:25.470967"
---

## 要約

harness engineering とは「AGENT = MODEL + HARNESS」という式で表される概念で、モデルの重み以外でエージェントの振る舞いを決めるすべての要素を指す。Mitchell Hashimoto が2026-02-05に提唱し、Birgitta Böckeler が2026-04-02にFowlerのblikiで guides/sensors の軸で整理した。本記事の著者はこれを5層のコールスタック構造で再整理し、Python実装を通じて得た知見をまとめている。

5層の構造は以下の通り。Layer 1（UI/REPL）はユーザー入力・streaming・slash commandを担う。Layer 2（Orchestration）は会話state・session永続化・context管理・prompt caching・system prompt組み立てを担い、prompt engineeringやcontext engineeringはここに収まる。Layer 3（Agent Loop）はモデル呼び出し→tool実行→結果返却の1ターン往復に加え、retry・error compaction・permission check・reflectionを含む。Layer 4（Tools）はRead/Write/Edit/Bash/MCPサーバー・TodoWriteなど外界とのinterface全般。Layer 5（LLM Service）はAnthropic Messages API本体で、streaming・prompt caching・extended thinkingの選択がここに属する。

Pythonで anthropic SDK と pydantic のみを使い、LangChain等の抽象層を排除して実装した結果、以下の具体的知見が得られた。①agent loopの正体は「while stop_reason == 'tool_use'」の約20行のループ。②stop_reason（end_turn/tool_use/max_tokens/refusal/stop_sequence）がハーネスの分岐契約書であり、ログに出さないとretryやcompactionの発動点が見えない。③messages をlist-of-content-blocksとして保持しないとAPIが400を返す「list-of-blocks invariant」という暗黙の契約がある。④tool_use.inputはPydanticでvalidateし、違反はis_error=Trueで返すことでモデルが自己訂正するラリーが成立する。⑤100ターン無加工で回すとin_tokensが30k超となるため、memory（harness.md）＋compact_messages（Haikuで要約置換）＋prompt caching 4ブレークポイントの組み合わせが必須。⑥claude-agent-sdk の query()1行は自前実装だと約500行相当になり、抽象層が隠している再接続・tool listキャッシュ・permission hookの挙動が可視化される。

監査エージェント開発への示唆として、エージェントの信頼性はモデル性能よりもretry・error compaction・permission・sandbox・context管理・observabilityといったハーネス側の設計品質でほぼ決まるという点は重要。LangGraphのstate graphは「自前実装したloopのstateを抽象化したもの」と地続きに理解できるため、先に素のAPI実装を経験してからフレームワーク活用に移行するアプローチが設計判断の精度を高める。

## アイデア

- 「AGENT = MODEL + HARNESS」という式でprompt engineeringとcontext engineeringをharness engineeringのサブ項目として統合的に位置づける整理フレームワークは、技術用語の乱立を構造化する上で有効
- stop_reasonの種類（end_turn/tool_use/max_tokens/refusal/stop_sequence）をハーネスの「契約書」として扱い、各値に対する分岐設計をLayer 3の中核に置くという設計原則は、エージェントの観測性・デバッグ性を大幅に向上させる
- permission layerをpolicy（allow/ask/denyルール）とphysical sandbox（Path.resolve().relative_to(WORKDIR)）の二重防御として実装し、それぞれ異なるレイヤーで機能させることで片方の障害をもう片方がカバーする構造的防御パターン

## 前提知識

- **Anthropic Messages API** (TODO: 読むべき)
- **agent loop / ReAct** (TODO: 読むべき)
- **tool_use / function calling** (TODO: 読むべき)
- **Pydantic** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **prompt caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）

## 関連記事

- /deep_3139 Claude Codeユーザーのためのプロンプトキャッシュ入門
- /deep_1789 Claude Code 基礎ガイド：AIの全体像からMCP活用まで
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門

## 原文リンク

[harness engineering を5層で整理する — Pythonで1から書いて見えたこと](https://zenn.dev/luoxi/articles/harness-engineering-everyday)
