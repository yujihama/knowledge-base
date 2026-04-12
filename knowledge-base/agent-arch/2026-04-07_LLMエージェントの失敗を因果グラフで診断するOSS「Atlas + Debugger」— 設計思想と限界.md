---
title: "LLMエージェントの失敗を因果グラフで診断するOSS「Atlas + Debugger」— 設計思想と限界"
url: "https://zenn.dev/kiyoshisasano/articles/00340b41b1e82e"
date: 2026-04-07
tags: [LLMデバッグ, 因果グラフ, agent-failure-debugger, llm-failure-atlas, LangGraph, LangChain, 決定論的診断, 根本原因分析, Observability, OSS]
category: "agent-arch"
memo: "[Zenn LLM] LLMエージェントの失敗を因果グラフで診断するOSSを作った — 設計思想と「できないこと」"
related: [41, 858, 857, 564, 1335]
processed_at: "2026-04-07T21:17:58.154415"
---

## 要約

LLMエージェントのデバッグを目的としたOSS「llm-failure-atlas」と「agent-failure-debugger」の2パッケージをPyPIで公開した事例。従来のObservabilityツール（LangSmith等）がトレース収集にとどまるのに対し、本ツールは因果グラフを走査して根本原因を自動特定する点が特徴。

【検出層（Atlas）】17の障害パターン、34シグナル、6アダプターで構成。clarification_failure → premature_model_commitment → agent_tool_call_loop → incorrect_outputのような因果連鎖を検出する。シグナル抽出はすべてルールベース（代名詞カウントによるambiguity_score、同一ツール3回以上呼び出しによるstate.any_tool_looping等）で、MLモデルを使わない決定論的設計を採用。

【診断層（Debugger）】17ノード・15エッジの因果グラフを走査し、根本原因をscore = 0.5×confidence + 0.3×downstream_impact + 0.2×(1-depth)の式でランキング。検出と因果分析を意図的に分離することで、「なぜ検出されたか」と「なぜ根本原因と判断されたか」の混在を防ぎ、説明可能性を優先している。

【観測品質管理】テレメトリが欠損している場合、該当シグナルの信頼度に0.6倍の減衰を自動適用し、データ不足なのに高信頼で診断するケースを構造的に排除。

【検証体系】10ケースの評価データセット（precision/recall/F1、root accuracy、path exact match等を自動算出）、30シナリオ×30アノテーションのバリデーション、ミューテーションテスト（13/13 KILLED）、gpt-4o-mini・Claude Haiku 4.5・Gemini 2.5 Flashを使ったクロスモデル検証（9/9 PASS）を実施。モデル別の行動差異（Claudeは確認を求め、gpt-4o-miniは推測し、Geminiは日付を聞く）も記録。

【明示された限界】事実の正誤判定不可、意味的ミスマッチ検出には埋め込みベース比較が必要、マルチエージェント協調障害は対象外（MASTの領域）、時系列の完全再構成は不可。これらは決定論性とシンプルさのトレードオフとして意図的に受け入れている。

## アイデア

- 検出層と因果分析層を完全分離する設計により、「なぜ検出されたか」と「なぜ根本原因か」の説明責任を独立させる構造は、監査・説明可能AIの設計原則に直接応用できる
- テレメトリ欠損時に信頼度を0.6倍に減衰させる観測品質追跡の仕組みは、不完全データ下での自動判断システムに求められる保守的推論の実装パターンとして参考になる
- score = 0.5×confidence + 0.3×downstream_impact + 0.2×(1-depth)という根本原因ランキング式は、因果的位置（上流ほど重要）と下流影響度を組み合わせた単純かつ解釈可能なスコアリングの好例
## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した

## 原文リンク

[LLMエージェントの失敗を因果グラフで診断するOSS「Atlas + Debugger」— 設計思想と限界](https://zenn.dev/kiyoshisasano/articles/00340b41b1e82e)
