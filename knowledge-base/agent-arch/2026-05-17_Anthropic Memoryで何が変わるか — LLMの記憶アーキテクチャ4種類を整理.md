---
title: "Anthropic Memoryで何が変わるか — LLMの記憶アーキテクチャ4種類を整理"
url: "https://zenn.dev/kenimo49/articles/llm-memory-context-engineering-4-architectures"
date: 2026-05-17
tags: [LLMメモリ, Anthropic Memory, Context Engineering, サマリーメモリ, マルチエージェント, トークン最適化, 知識グラフ, エージェントアーキテクチャ]
category: "agent-arch"
related: [4065, 41, 5464, 1474, 5561]
memo: "[Zenn LLM] Anthropic Memoryで何が変わるか LLMの記憶アーキテクチャ4種類を整理"
processed_at: "2026-05-17T09:08:07.924233"
---

## 要約

2026年3月にAnthropicがMemory機能を全ユーザーへデフォルト公開した。約24時間ごとに会話履歴をスキャンし、職業・使用ツール・言語の好みなどを要約して長期保存する。元の会話ログは保持せず要約のみを記録するため、プライバシー保護とトークン節約を同時に達成している。ChatGPT・Gemini・Perplexity・GrokからのMemory Importも翌日リリースされ、乗り換えを促進する戦略的機能として位置づけられている。

ただしAnthropic Memoryは「ユーザー個人の長期記憶」レイヤーを埋めるにとどまり、プロジェクト固有の動的状況・チーム間共有・エージェント間の記憶共有はカバーされない。アプリケーション層の記憶設計は別途必要であり、著者は4種類に分類する。①バッファメモリ：直近N回の会話をそのまま保持。実装が最もシンプルだが古い情報が消える。②サマリーメモリ：古い会話をLLMで要約して圧縮保持。10回ごとに要約を更新し直近2往復のバッファと組み合わせることで長期文脈を維持しつつトークン消費を抑えられる。③エンティティメモリ：人物・概念をプロファイルとして構造化記録。CRM連携に適する。④知識グラフメモリ：エンティティ間の関係性まで記録。最も豊富だが実装・運用コストが高い。

著者の推奨は「User Layer = Anthropic Memory（個人の長期記憶）+ Project Layer = サマリーメモリ（プロジェクト固有の動的記憶）+ Session Layer = バッファメモリ（直近5往復）」の3層構造。

マルチエージェント設計では、OpenClawが提示する7ファイル構成（AGENTS.md/TOOLS.md/SOUL.md/IDENTITY.md/USER.md/HEARTBEAT.md/MEMORY.md）を参照している。サブエージェントにはAGENTS.mdとTOOLS.mdのみを渡し、人格・ユーザー情報・記憶はメインエージェントが保持する。これによりトークン節約とプライバシー保護を両立する。

長期対話で発生するContext障害は4種類に分類される。Context Poisoning（誤情報の混入）には信頼度スコアリングと隔離バッファ、Context Distraction（散漫）には関連性0.5・新しさ0.3・重要度0.2の重み付けフィルタ、Context Confusion（混乱）にはトピック別クラスタリング、Context Clash（衝突）には矛盾検出と信頼性・新しさ・ソース権威性に基づく解決が対策として挙げられる。

トークン予算の動的配分では、デフォルトで直近バッファ40%・会話サマリー30%・エンティティ20%・知識グラフ10%を基準に、関連性スコアと優先度で動的調整する。監査エージェント開発においては、サマリーメモリ＋7ファイルアーキテクチャの組み合わせが監査手続きの継続的追跡と証跡管理に直接応用可能。

## アイデア

- 3層メモリ構造（Anthropic Memory + サマリー + バッファ）の分業設計は、監査エージェントにおける「監査人プロファイル」「案件固有の進捗」「直近の手続き」の3層管理にそのまま対応できる
- サブエージェントには最小限の情報（AGENTS.md/TOOLS.md）のみを渡す『派遣社員モデル』は、マルチエージェント設計でのトークンコスト削減とプライバシー保護を同時に実現する実用的なパターン
- Context障害の4分類（Poisoning/Distraction/Confusion/Clash）と対策の定式化は、長期稼働エージェントのデバッグフレームワークとして活用できる

## 前提知識

- **Context Window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **LangChain Memory** (TODO: 読むべき)
- **System Prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_4065 AIがビジネス価値を生むにはデータファブリックが不可欠：コンテキスト欠如が引き起こす判断誤りのリスク
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_5464 MCP・A2A・Function Calling：3つを混同していませんか？【Google Cloud ADK視点で整理】
- /deep_1474 GoのAIフレームワーク「Eino」を徹底解説！LangChainGoとの実測比較も
- /deep_5561 Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】

## 原文リンク

[Anthropic Memoryで何が変わるか — LLMの記憶アーキテクチャ4種類を整理](https://zenn.dev/kenimo49/articles/llm-memory-context-engineering-4-architectures)
