---
title: "AIと本気で協働して気づいた「人間の判断」の置き場所 — waku2-ai-protocol v0.1.0"
url: "https://zenn.dev/waku2_eng/articles/ddca007765c615"
date: 2026-06-05
tags: [マルチエージェント, Human-in-the-Loop, 承認ゲート, SSE, ワークフロー設計, waku2-ai-protocol, エージェントガバナンス]
category: "agent-arch"
related: [4373, 7293, 7387, 7355, 5159]
memo: "[Zenn LLM] AIと本気で協働して気づいた「人間の判断」の置き場所 — waku2-ai-protocol v0.1.0"
processed_at: "2026-06-05T09:17:15.398297"
---

## 要約

著者（島田英紀）は複数のAIに「設計・調整・実装・レビュー」の役割を分担させるマルチエージェント協働スタイル（waku2 AI Dream Team）を実践してきた。その中で感じた課題は、ワークフローの流れが速く滑らかになるほど、人間が「承認ボタンを押すだけの存在」に後退していくという構造的問題だった。これに対応するために2026年6月1日にGitHub上でwaku2-ai-protocol v0.1.0を公開した。

本プロトコルの中核的な設計思想は2点に集約される。第一に「SSE event = notification、DB state = source of truth」という分離原則。AIの進捗はSSEなどのリアルタイムイベントで可視化するが、信頼すべき最終状態はDBなどの永続記録に置く。SSEは取りこぼし・重複・遅延・再接続時のズレが起きうるため、イベントはあくまで「通知」として扱う。第二に「Human Approval Gate」の明示的な設計。メール送信・ドキュメント公開・コードデプロイ・クレジット消費・個人情報取扱いなどの場面では、AIが自律的に進まず`approval_required`状態に遷移して人間の判断を待つ。これは処理失敗でも完全終了でもなく「やわらかな終端」として定義される。

v0.1.0で定義した語彙は最小限に絞られており、役割語彙として`architect`/`coordinator`/`implementer`の3種、イベント名として`run_started`/`phase_started`/`role_message`/`artifact_created`/`artifact_updated`/`usage_recorded`/`approval_required`/`approval_decided`/`run_completed`/`run_failed`の10種を置く。特定のモデル名（ChatGPT、Claude、Gemini等）には依存しない。

本プロトコルはMCP、A2A、AG-UI、LangGraph、Temporal、EGAPなどの既存フレームワークを置き換えるものではなく、それらの上または隣で「人間の承認・信頼できる状態・役割・イベントを説明するための最小語彙」として機能する補完的な設計メモという位置づけ。teachable（人が理解・検証・教授できる）であることを設計上の最優先事項としており、production-ready仕様でもSDKでもruntimeでもない。今後はJSON payload例、approval gate具体例、artifact lifecycle、既存プロトコルとの比較メモ、reference implementationの追加が予定されている。監査エージェント開発の観点では、approval_requiredによる人間介入ポイントの明示的設計と、イベント/永続記録の分離は、監査ログの信頼性確保・承認証跡の設計に直接応用可能な概念である。

## アイデア

- 「SSE event = notification、DB state = source of truth」という分離原則は、AIエージェントのワークフロー設計における状態管理の根本的な問題（イベントの取りこぼし・重複・遅延）を解決する実用的なパターンであり、監査ログの信頼性設計にも直接応用できる
- approval_requiredを「処理失敗でも完全終了でもないやわらかな終端」として正式なワークフロー状態に定義することで、Human-in-the-Loopを例外処理ではなく設計の第一級市民として扱う発想の転換
- teachable（人が理解・検証・教授できる）を設計制約として置くことで、語彙の最小化と説明可能性を両立させる手法は、複雑な監査エージェントシステムの説明責任確保にも有効なアプローチ

## 前提知識

- **SSE (Server-Sent Events)** (TODO: 読むべき)
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Human-in-the-Loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **durable execution** → /deep_7218 AIエージェント基盤のアーキテクチャを10層で整理する：OSS/SDK比較のための地図
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_4373 効果的なAIエージェントの作り方 — Anthropic Barry Zhangが語る3つの原則
- /deep_7293 サプライチェーンエージェントは「ブルウィップ効果」を本当に解消するか：マルチエージェント協調設計の罠と設計原則
- /deep_7387 エージェントAIによるグローバルヘルスケアの再人間化
- /deep_7355 エージェントAIで医療を再人間化する：Hospital for Special Surgeryの実践事例
- /deep_5159 エヴァで理解するAIエージェント組織論：NERVとMAGIとゼーレ、あなたはどこから設計する？

## 原文リンク

[AIと本気で協働して気づいた「人間の判断」の置き場所 — waku2-ai-protocol v0.1.0](https://zenn.dev/waku2_eng/articles/ddca007765c615)
