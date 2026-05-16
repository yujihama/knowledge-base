---
title: "記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計"
url: "https://zenn.dev/daishiro/articles/claude-dreaming-memory-self-improvement"
date: 2026-05-12
tags: [Dreaming, Outcomes, Claude Managed Agents, Writer-Grader, LLM-as-judge, マルチエージェント, メモリキュレーション, ルーブリック]
category: "agent-arch"
related: [21, 931, 3906, 5319, 1788]
memo: "[Zenn LLM] 記憶を持ったAIが、次に記憶を整理しはじめた"
processed_at: "2026-05-12T21:01:56.506176"
---

## 要約

AnthropicがClaude Managed Agentsに追加した「Dreaming」と「Outcomes」という2つの機能を解説した記事。前回記事で論じた「brain / hands / session」の3層アーキテクチャに続く考察で、今回はその上に「outcomes（検証）」と「dreaming（整理）」という第4・第5のレイヤーが加わったと位置づける。

**Dreaming**はセッションとセッションの間にエージェントが蓄積されたログや記憶を自律的にキュレーションする仕組み。具体的には①繰り返しのミスのパターン抽出、②効果的なワークフローの記憶強化、③マルチエージェント環境での共有学習への集約、④古い情報・ノイズの削除の4つを行う。人間の睡眠中の記憶固定メカニズムに着想を得た命名。法律AIのHarveyへの適用でタスク完了率が約6倍に向上したとAnthropicは報告している。

**Outcomes**はセッション内の品質制御機構で、内部的にWriter（執筆者）とGrader（採点者）を分離する設計が核心。ユーザーがルーブリック（評価基準）をuser.define_outcomeイベントで定義すると、WriterがタスクをこなしGraderが別コンテキストウィンドウで独立採点する。「needs_revision」の場合はWriterに差し戻して再実行、「satisfied」で完了。max_iterationsはデフォルト3・最大20。GraderがWriterとは完全に分離したコンテキストで動く点が重要で、Writerの思考過程に引きずられない純粋な評価が可能になる。ルーブリックは「CSVにpriceカラムが存在し数値が入っている」のような採点可能な具体表現で書かなければ機能しない。

2つの機能の時間軸は異なる。Outcomesが1セッション内のiterative品質保証ループであるのに対し、Dreamingは複数セッションをまたいだ長期学習。組み合わせることで「今この仕事をきちんとやる」と「次の仕事をもっとうまくやる」が両立する。

claude.aiのメモリ機能との違いも整理されており、claude.aiメモリが「ユーザーを知る（個人秘書の記憶）」であるのに対し、Dreamingは「タスクがうまくなる（組織の業務手順書の継続改善）」と位置づけられる。監査エージェント開発への示唆として、Outcomesのルーブリック設計思想はLLM-as-judgeのGrader設計に直接応用可能。評価基準を採点可能な形で明文化するアプローチは、監査手続の自動検証ループにも転用できる。またDreamingの「失敗パターンの抽出と共有メモリへの集約」は、複数の監査サブエージェントが並列動作するマルチエージェント構成での知見共有機構として参照に値する。

## アイデア

- GraderをWriterとは完全に分離したコンテキストウィンドウで動かすことで評価の独立性を担保する設計は、LLM-as-judgeのバイアス問題（judge being influenced by the reasoning trace）への実装レベルの回答になっている
- Dreamingを「脳の睡眠中の記憶固定（memory consolidation）」に対応させるアーキテクチャ上の比喩は単なる命名ではなく、非同期バックグラウンド処理・ノイズ除去・重要パターンの強化という機能群がそのまま対応しており、神経科学的メカニズムから設計を逆算した可能性がある
- ルーブリックを「採点可能な基準」として明文化する要求は、曖昧なゴール定義が全通過デフォルトの失敗モードを生むという経験則から来ており、エージェントへの指示設計（spec writing）の良し悪しが出力品質を決定するという教訓を再確認させる

## 前提知識

- **Claude Managed Agents** → /deep_2364 Claude Managed Agentsを触ってみた：APIでClaudeをフルマネージド自律エージェントとして動かす
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **RAG / 外部メモリ** (TODO: 読むべき)
- **ReAct / iterative refinement** (TODO: 読むべき)

## 関連記事

- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ
- /deep_3906 検証付きマルチエージェント協調：「計画・実行・検証・再計画」フレームワーク VMAO
- /deep_5319 マルチエージェント設計の7原則：Factory「Missions」が16日間自律稼働を実現
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素

## 原文リンク

[記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計](https://zenn.dev/daishiro/articles/claude-dreaming-memory-self-improvement)
