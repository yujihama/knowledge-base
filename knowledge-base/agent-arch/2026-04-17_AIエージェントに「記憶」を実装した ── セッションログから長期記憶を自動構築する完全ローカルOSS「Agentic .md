---
title: "AIエージェントに「記憶」を実装した ── セッションログから長期記憶を自動構築する完全ローカルOSS「Agentic Engram」"
url: "https://zenn.dev/sert/articles/dc010822ff7282"
date: 2026-04-17
tags: [長期記憶, LanceDB, KùzuDB, セッションログ, ハイブリッド検索, ae-miner, 暗黙知抽出, sentence-transformers, CLAUDE.md, ローカルOSS]
category: "agent-arch"
related: [9, 1336, 1911, 1757, 1422]
memo: "[Zenn LLM] AIエージェントに"記憶"を実装した ── セッションログから長期記憶を自動構築する完全ローカルOSS"
processed_at: "2026-04-17T12:12:13.059083"
---

## 要約

Claude CodeやCursorなどのAIコーディングツールはセッションをまたいで記憶を保持しない。この課題を解決するOSSが「Agentic Engram」である。設計コンセプトは人間の記憶プロセスの模倣で、日中の体験（セッションログ）→睡眠中の整理（ae-miner）→長期記憶への定着（LanceDB＋Kùzu）→想起（ae-recall）→統合・忘却（ae-consolidate / ae-groom）という5段階のパイプラインを実装している。

技術的な核心は2点ある。第一に、既存のセッションログ（Claude Code等がローカルに保存するJSONL）を遡及的にパースして記憶化する点。導入前の過去ログがすべて記憶資産になる。第二に、「人間がAIの提案を修正した瞬間」を[CORRECTION]マーカーで高優先度抽出する点。「python -m pytestではなくuv run pytestを使う」のような暗黙知が自動的に記憶される。

データストアはサーバーレス・ファイルベースの2DBを組み合わせる。LanceDB（ベクトル検索）は意味的類似度でヒットし、Kùzu（グラフDB）は「Route Handler → SOLVES → CORSエラー → CAUSED_BY → 直接フェッチ」といった論理的連鎖を辿る。埋め込みモデルにはsentence-transformersのparaphrase-multilingual-MiniLM-L12-v2（384次元）を採用し、日英混在ログに対応する。

ae-minerはmacOSのlaunchdで30分ごとに自動実行され、LLMが「記憶に値するか」を判断してLanceDB＋Kùzuに書き込む。ae-recallはCLIコマンド一発でハイブリッド検索を実行し、ベクトル検索とグラフ探索の結果をマージ・ランキングして返す。CLAUDE.mdに「作業前にae-recallで過去記憶を想起すること」と記述するだけで、エージェントが自発的に記憶参照→正しい方法で作業開始するループが成立する。

記憶が増えると重複が生じるため、ae-consolidateがコサイン類似度によるクラスタリングとLLMでMERGE/KEEP/SKILL昇格を判断し、occurrence_count（出現回数）が3回以上の知見をスキルファイルに昇格させる。課題として、LLMによる抽出ノイズ、ライブラリバージョンアップによる記憶の腐敗、初回マイニング時の処理時間、ae-miner実行によるトークン消費量増加が挙げられている。全てpip installのみで動作し、Docker・常駐サーバー・外部APIが不要な点が既存ツール（mem0等）との最大の差別化点である。

## アイデア

- 「人間がAIの提案を修正した瞬間」を[CORRECTION]マーカーで自動検出し高優先度記憶化する手法は、監査エージェントにおける「審査官の判断修正パターン」の蓄積にそのまま応用できる
- LanceDB（ベクトル）＋Kùzu（グラフ）のハイブリッドで「意味的類似度」と「論理的因果連鎖」の両方を検索する設計は、RAGの精度向上パターンとして汎用性が高い
- 過去のセッションログを遡及パースして記憶化できる点は、既存ツールの「導入後のみ有効」という制約を突破しており、大量の蓄積済みログを持つ開発者ほど即座に高品質な記憶DBを得られる非線形な価値がある

## 前提知識

- **Vector DB** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **Graph DB** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **sentence-transformers** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **セッションログ（JSONL）** (TODO: 読むべき)

## 関連記事

- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_1336 Claude Codeの長期記憶を「記憶の宮殿」アーキテクチャで実装したCLIツール「Codeatrium」
- /deep_1911 2026年、現場エンジニアが押さえておくべきAI技術トレンド5選
- /deep_1757 🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索
- /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年

## 原文リンク

[AIエージェントに「記憶」を実装した ── セッションログから長期記憶を自動構築する完全ローカルOSS「Agentic Engram」](https://zenn.dev/sert/articles/dc010822ff7282)
