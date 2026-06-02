---
title: "Coding Agentに特化したIDE「Fusuma」を開発しました"
url: "https://zenn.dev/andrew/articles/376ddb3ed9215f"
date: 2026-06-02
tags: [Claude Code, Coding Agent, IDE, Tauri, マルチエージェント, 並列実行, Rust, PTY]
category: "agent-arch"
related: [4753, 5310, 1145, 6745, 4520]
memo: "[Zenn LLM] Coding Agentに特化したIDE、「Fusuma」を開発しました"
processed_at: "2026-06-02T21:02:36.112422"
---

## 要約

FusumaはClaude CodeやCodexなど複数のCoding Agentを並列運用することに特化したIDEで、Rust + Tauri v2をコアに、フロントエンドはReact + TypeScript + Tailwind + Zustandで構築されている。開発背景として、VSCode上で複数エージェントを並列実行した際に「処理中か返答待ちか」の状態判別が難しく、応答ロスが積み重なるという課題があった。一方でcmux等のターミナル特化ツールはファイル閲覧機能が弱く、結局VSCodeと併用するウィンドウ切り替えコストが残るという問題もあった。

Fusumaはこの両課題を解消するため、3種類のWidget（AI Widget・Files Widget・Terminal Widget）を日本の「襖」のように自由に分割・移動・サイズ変更できるレイアウトシステムを採用した。AI Widgetは既存エージェントのUIをそのまま活かしつつ、入力欄のみを独自実装し、@によるファイル参照・/でのSkill呼び出し・ドラッグ&ドロップのファイル参照補完機能を追加している。エージェントのステータスは「グレー（処理中）・黄色（返答待ち）・赤（失敗）」の3色でWidget上部とワークスペース一覧に常時表示され、次に操作すべきエージェントを視線移動だけで把握できる。

データベースにはTursoを採用し、国内リージョン選択可能かつ無料枠が広い点が個人開発との親和性を高めている。認証はBetter AuthをLibSQL上で運用することで運用コストを削減。ターミナルはRust側でOSネイティブのPTY（擬似端末）を実装し通常シェルと同等の動作を実現。ElectronではなくTauriを選択したことでファイルサイズ・消費メモリを大幅削減している。Cmd+数字でのワークスペース切り替えやCmd+矢印でのWidget移動など最小打鍵のショートカットも整備。現在無料でfusuma.devよりダウンロード可能。監査エージェント開発への示唆として、複数の自律エージェントを並列管理する際のUI設計（状態可視化・入力補完・レイアウト自由度）はLangGraph等を用いたマルチエージェントシステムの監視UIにも応用できる考え方である。

## アイデア

- エージェントのUIそのものには手を加えず入力欄のみを差し替えるという設計方針により、既存ツールへの慣れを損なわずに操作効率だけを向上させる非侵襲的な拡張アプローチ
- 「処理中・返答待ち・失敗」を3色でリアルタイム可視化することで、複数エージェントの状態管理を認知負荷なく行えるステータス設計は、LangGraphのノード状態監視UIへ応用可能
- ElectronではなくRust + Tauri v2を採用することでデスクトップアプリの軽量性を確保しつつOSネイティブPTYを統合する技術選定は、Coding Agent専用ツールの性能要件に対する合理的な回答

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **Tauri** → /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- **PTY（擬似端末）** (TODO: 読むべき)
- **マルチエージェント並列実行** (TODO: 読むべき)
- **Coding Agent** → /deep_6122 Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）

## 関連記事

- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_5310 ISUNARABE合同演習2026参加記：AIエージェント無制限のパフォーマンスチューニング大会で学んだこと
- /deep_1145 Clade v1.3.0 — CLI版推奨＋マイルストーンワークフロー
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[Coding Agentに特化したIDE「Fusuma」を開発しました](https://zenn.dev/andrew/articles/376ddb3ed9215f)
