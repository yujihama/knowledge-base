---
title: "Claude Code + Python で AI 情報収集→記事化パイプラインを Phase 3 まで作って分かったこと"
url: "https://zenn.dev/masaki333/articles/31dd976fa49737"
date: 2026-05-10
tags: [Claude Code, Python, pipeline, RAG, Obsidian, SQLite, trafilatura, slash-command, 情報収集自動化, 品質ゲート]
category: "agent-arch"
related: [9, 3776, 4186, 3239, 2821]
memo: "[Zenn LLM] Claude Code + Python で AI 情報収集→記事化パイプラインを Phase 3 まで作って分かったこと"
processed_at: "2026-05-10T09:32:42.220493"
---

## 要約

Claude Code と Python を組み合わせた情報収集・要約・記事化パイプラインの個人開発ログ。システムは collector（情報収集）・dedup（重複排除）・extract（本文抽出）・store（SQLite保存＋Obsidian Vault出力）の4コンポーネントで構成される。

Phase 1では GitHub リリースノート（RSS/Atom）を httpx で取得し、trafilatura で本文抽出後 SQLite に保存。Claude Code の /weekly-digest スラッシュコマンドで Markdown ドラフトを生成する最小構成を実装。Phase 2では情報ソースを claude-code-releases / anthropic-sdk-python-releases / zenn-ai / hn-claude / reddit-claudeai の5種類に拡張し、HN Algolia API・Reddit JSON エンドポイントにも対応。共通の FetchedItem データクラスで後続処理を統一し、24時間キャッシュ（raw_cache.py）でレートリミット対策を施した。Phase 3では品質ゲートを導入し、文字数1500字未満・引用比率50%超・frontmatter必須フィールド欠落のドラフトを vault/_rejected/ に自動振り分け。月次レビュー用 /monthly-review コマンドも追加した。

運用で判明した主な課題は5点。①trafilatura が GitHub ページのボイラープレート（テンプレート文字列）を誤抽出する問題は _strip_boilerplate 関数と RSS summary フォールバックで対処。②Claude によるスコア採点（1〜10）が6か8に偏る問題は、プロンプト v0.3 で「7を選ぶ条件」を明示して改善。③X（Twitter）は規約リスクと既存5ソースでの充足を理由に不採用。④Reddit r/ClaudeAI はドラフト昇格率が低いが、月次レビューで評価する方針。⑤品質ゲートを後から追加する際、Phase 1/2 で frontmatter 仕様が曖昧だったため判定ロジック実装に想定外の工数が発生。

同種パイプラインを構築する際の推奨は3点：(1)FetchedItem データクラスと frontmatter 仕様を Phase 1 で確定する、(2)1ソースで全フローを通してからソースを追加する、(3)失敗時の挙動（スキップ・記録）を最初に設計する。Phase 4ではWeekly Summaries の横断統合と体系化ノートの自動昇格を予定している。監査エージェント開発への示唆として、本システムの品質ゲート設計（閾値・フィールド仕様の事前定義）と失敗フロー設計の考え方は、LangGraph ベースのエージェントにおけるガードレール設計に直接転用可能。

## アイデア

- スコア採点の分布偏りをプロンプトで制御する手法：「7を選ぶ条件を明示する」という発想は、LLM-as-judge の評価設計において過大/過小評価バイアスを抑制する実践的テクニックとして応用できる
- FetchedItem 共通データクラスによるコレクター実装の分離：収集ロジックがばらばらでも後続処理を統一できる設計は、マルチソース RAG パイプラインのアーキテクチャ原則として参考になる
- 品質ゲートを vault/_rejected/ へのルーティングとして Claude Code のプロンプト内だけで実装：Python コード変更なしに運用ポリシーを変更できる点は、エージェントの行動制約をコード外で管理するアプローチの実例

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **trafilatura** (TODO: 読むべき)
- **SQLite** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **RSS/Atom** (TODO: 読むべき)
- **Obsidian Vault** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた

## 関連記事

- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_3776 LLM Wikiが育つほどAI解説が賢くなる：知識増幅ループのつくり方
- /deep_4186 Context Rotを防ぐ知識ベース設計：LLM Wikiが体現するContext Engineering技法群
- /deep_3239 Claude Code で LLM Wiki を育てる——第二の脳の作り方
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話

## 原文リンク

[Claude Code + Python で AI 情報収集→記事化パイプラインを Phase 3 まで作って分かったこと](https://zenn.dev/masaki333/articles/31dd976fa49737)
