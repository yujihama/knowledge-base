---
title: "CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計"
url: "https://zenn.dev/zephel01/articles/cd0032896f0e74"
date: 2026-04-25
tags: [CodeRouter, SSE, FastAPI, Anthropic, OpenAI, フォールバック, プロトコル変換, ステートマシン, tool_calls, Claude Code]
category: "agent-arch"
related: [2278, 41, 1736, 2205, 13]
memo: "[Zenn LLM] CodeRouter の内側 — Anthropic ⇄ OpenAI 双方向翻訳と mid-stream セーフなフォールバック設計"
processed_at: "2026-04-25T12:47:19.336667"
---

## 要約

CodeRouterはClaude CodeやGemini-CLIなどLLMエージェントの前段に置くFastAPIベースの小型ルーターで、Python 3.12+、純粋非同期（asyncio+httpx）、テスト453本で構成される。本記事ではv1.0時点の4つのコア設計判断を解説する。

**設計1: IngressとProvider kindの直交化**。多くのルーターは「Anthropic受けはAnthropicへ送る」という暗黙前提があるが、CodeRouterは2×2の直交マトリクスを実装し、AnthropicエンドポイントをOpenAIバックエンドで処理する、あるいはOpenAIクライアントからAnthropicを叩くといった全4組み合わせを動作させる。変換の核心は`messages[].content`構造の差異で、Anthropicは配列（text/tool_use/tool_result/imageのバリアント）、OpenAIは文字列+tool_callsフィールドという非対称構造を双方向変換する。特に「role:tool連続を1つのrole:user+content配列に束ねる（Anthropic方向）」と「tool_resultブロックをrole:toolメッセージにばらす（OpenAI方向）」の非対称性が実装難所で、pydanticモデルとmypy --strictで不変項を型レベルで担保している。

**設計2: mid-streamフォールバックガード**。最初のコンテンツバイトをクライアントに送出した後はプロバイダ切替禁止という不変項を実装。これがないとProviderAとProviderBの応答が混在した「フランケン応答」が発生し、tool_useブロックのinputが壊れてClaudeがJSONパースエラーを起こす。OpenAI SSEでは`choices[0].delta.content`または`delta.tool_calls[]`の存在、Anthropic SSEでは`event:content_block_delta`の到着を「最初のコンテンツバイト」と定義し、`message_start`や`content_block_start`などメタデータイベントは含まない設計で可用性を保つ。この不変項のテストは専用ファイルに23本記述され、「N番目のバイトで切断」を人工的に注入して検証している。

**設計3: ステートフルSSEフィルタチェーン**。`<think>...</think>`や6種のstopマーカーをチャンク境界をまたいで安全に除去するステートマシン実装。OUTSIDE/INSIDEの2状態を持ち、`<thi`のような部分タグが末尾にあれば安全なプレフィックスまでを出力してバッファに保留する。EOF時はOUTSIDE状態なら保留分を出力、INSIDE状態なら全て破棄する。`list[OutputFilter]`チェーンとして順序適用され、OpenAI経路では[DONE]送出直前に残渣確認が必要な一方、Anthropicはcontent_block_*の明示的な境界があるため実装が簡潔。

**設計4: doctorの実地プローブ**。ヒューリスティクスに依存せず実際にAPIをプローブして動作確認する設計。監査エージェント開発への示唆として、LLMエージェントのツール呼び出しをローカルモデルで処理する際のプロトコル変換層の設計パターン（バリデーション前置、責務分離、mid-stream整合性保証）は、LangGraphベースのマルチステップエージェントにおけるフォールバック設計に直接応用できる。

## アイデア

- IngressとProvider kindを直交させる2×2マトリクス設計により、クライアント側プロトコルとバックエンドプロトコルを完全に疎結合化できる点。これはAPIゲートウェイ設計の汎用パターンとして応用可能
- mid-streamフォールバックガードにおいて、メタデータイベント（content_block_start等）とコンテンツイベント（content_block_delta等）を厳密に区別して「最初のバイト」を定義することで、可用性と整合性を同時に最大化できる点
- チャンク境界をまたぐSSEフィルタをOUTSIDE/INSIDEのステートマシンとして実装し、部分タグの保留戦略と永久保留の防止を両立させるアーキテクチャ。ストリーミングLLM出力の後処理全般に応用できる汎用パターン

## 前提知識

- **SSE (Server-Sent Events)** (TODO: 読むべき)
- **FastAPI / asyncio** (TODO: 読むべき)
- **Anthropic Messages API** (TODO: 読むべき)
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **pydantic + mypy** (TODO: 読むべき)

## 関連記事

- /deep_2278 仕事とAIの関係を実際に解明できる唯一のデータとは何か
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_2205 なぜAnthropicは軍と戦う？1億ドルPartner NetworkとAI研究所の全貌
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装

## 原文リンク

[CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計](https://zenn.dev/zephel01/articles/cd0032896f0e74)
