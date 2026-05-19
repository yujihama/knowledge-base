---
title: "Hermes Agentが12回自己改善した。ただし間違った目標に向かって ── self-improving loop実験記録"
url: "https://zenn.dev/toki_mwc/articles/2026-05-15-hermes-self-evolving-loop-experiment"
date: 2026-05-19
tags: [self-improving-loop, CLIP, Hermes-Agent, 外部評価者, seed品質, コンテキスト設計, マルチエージェント, Qwen3, KimiK2]
category: "agent-arch"
related: [1572, 1757, 826, 1737, 1641]
memo: "[Zenn LLM] Hermes Agent が12回自己改善した。ただし間違った目標に向かって ── self-improving loop 実験記録"
processed_at: "2026-05-19T09:04:38.852517"
---

## 要約

Hermes AgentのスキルファイルをAI自身が12サイクル書き換えるself-improving loop実験の記録。エージェントがMarkdown形式のskillファイルを読み込み、タスク実行→外部評価者によるスコアリング→改善ノート追記→次サイクルへ引き継ぐという構造を採用。タスクはX投稿文生成（Phase 0）→評価者・生成者の役割交代（Phase 1a）→AIキャラクター画像生成のCLIPスコア評価（Phase 1b）と段階的に難化させた。

4つの発見が得られた。第1に、同一モデルが生成と評価を兼任するとスコアが6.0〜6.33で頭打ちになり、外部評価者（Kimi K2.6）を追加しても突破できなかった。別の生成者（Qwen3.6:27b）を投入して初めてスコアが8.0へ+2.0改善した。第2に、ドライバ実装でskillファイルを先頭1,500文字に切り詰めていたため、Cycle 1〜3の改善ノートが評価者に渡らず「前日データなし」という誤った分析を招いた。コンテキスト設計が機能設計と同等の重要性を持つことを示す事例。第3に、CLIP ViT-L/14スコアが0.86を超えても、人間目視で「留め具の形状」「胸当ての細部」「後ろ髪の表現」の3要素が未達のままだった。Nano Banana ProはCycle 9でKimi自身がbackendの構造的限界と診断し、ComfyUI+ControlNet/IP-Adapterへの切り替えを提案した。

最重要の第4発見はseed汚染。セットアップ担当のClaude Codeが参照画像を確認せず「記憶」で属性を記述したため、目の色が「red eyes」（正解: green eyes）、頭部が「green cap」（正解: 帽子なし）というまま10サイクルが進行した。Cycle 3でCLIP 0.8614を達成していたが、それは誤ったキャラクター属性への正確な収束だった。Cycle 11で13項目の基準属性を修正したところ、CLIP mean 0.8901・max 0.9609と全サイクル最高を記録。10サイクル分の最適化を1回のseed修正が上回った。監査エージェント開発への示唆として、agentic loopにおけるseed品質の検証（誰が・何を根拠に初期制約を書いたかのトレーサビリティ）は、評価ロジックの設計と同等以上に重要であり、ループが正常動作していても目標関数の誤設定は検出されにくい点に注意が必要。

## アイデア

- 同一モデルによる生成・評価の閉ループはバイアスが二重乗りして頭打ちを生む。外部評価者だけでなく外部生成者の投入が突破に必要という構造的知見
- seed汚染はループが正常動作しているため自動検出が困難で、10サイクル分の最適化より1回のseed修正の方が効果が大きかった点は、AIシステムの品質保証における初期条件検証の重要性を示す
- Human-in-the-Loopを『指示』ではなく『許可の付与（1行追記）』として機能させることで、エージェントが自律的にbackend切り替えを判断・rationale化した設計パターン

## 前提知識

- **CLIP ViT-L/14** (TODO: 読むべき)
- **self-improving loop** (TODO: 読むべき)
- **Hermes Agent** → /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **マルチエージェント評価** → /deep_2511 患者教育をマルチターン・マルチモーダルインタラクションとして再考する

## 関連記事

- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1757 🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_1737 難問を「選択肢」に変える：RLVRの探索限界を突破するCog-DRIFT
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う

## 原文リンク

[Hermes Agentが12回自己改善した。ただし間違った目標に向かって ── self-improving loop実験記録](https://zenn.dev/toki_mwc/articles/2026-05-15-hermes-self-evolving-loop-experiment)
