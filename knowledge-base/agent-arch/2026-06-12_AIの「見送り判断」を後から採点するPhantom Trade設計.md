---
title: "AIの「見送り判断」を後から採点するPhantom Trade設計"
url: "https://zenn.dev/r_inowa/articles/hermes-agent-07-phantom"
date: 2026-06-12
tags: [Claude API, 自動売買, phantom-trade, キャリブレーション, 意思決定評価, TypeScript, LLM-as-judge]
category: "agent-arch"
related: [7479, 484, 4180, 7926, 23]
memo: "[Zenn 機械学習] AIの「見送り判断」を後から採点するPhantom Trade設計"
processed_at: "2026-06-12T09:00:39.725735"
---

## 要約

Hermes AgentはTypeScriptで実装された自動売買システムであり、Claude APIを意思決定エンジンとして活用している。本記事では、ClaudeがWAIT（見送り）を選択した際に「もしエントリーしていたら」を仮想トレードとして記録・採点するPhantom Trade機能の設計を解説している。

従来の自動売買システムでは実際のトレードの勝率のみで評価するため、「慎重すぎて勝てるトレードを全部見逃している」状態を検知できない問題がある。例えば実際のトレードが0勝0敗でWRが算出不能であっても、WAITしたトレードが8勝2敗であれば見逃しコストが大きいことになる。Phantom Tradeはこの「見送り判断の質」を定量化するための仕組みである。

実装は3段階で構成される。①Stage 2（Claude）がWAITを返したとき、isMarketTradeable()がtrueであれば、symbol・direction・entryPrice・stopLoss・takeProfit・RSI・ATR・reasoning_briefをphantomとしてmemory.phantomRecord()に記録する。②通常のSL/TPチェックと同一のcheckPendingOutcomes()ロジックで自動決着させ、SL到達でLOSS（WAIT正解）、TP到達でWIN（WAIT誤り）と判定する。③phantom勝率をgetSummaryForClaude()内でキャリブレーションメッセージに変換し、Claudeの次サイクルの判断コンテキストに注入する。例えば「You have been too conservative — your WAITs are missing more wins than losses.」というメッセージが渡される。

設計上の注意点として、市場時間外のWAITは記録しない（株式の22:00 JSTなどでは翌朝のギャップで判定が不正確になるため）。また getOverallWinRate()はrealトレードのみを対象とし、phantomを実力評価に混入させない。可視化はDiscord通知（phantom記録時・決着時）とStreamlitダッシュボードのPhantom Calibrationバーチャートで行う。

監査エージェント開発への示唆として、このアーキテクチャは「エージェントが何もしなかった判断」を事後評価するフレームワークとして応用可能である。監査エージェントがアラートを見送った事象を仮想的に追跡し、後から正否を採点することで、過剰な見送りバイアスや見落としパターンを定量的に検出できる。LLM-as-judgeの評価ループと組み合わせることで、エージェントの意思決定品質の継続的改善が実現できる。

## アイデア

- 「何もしない判断」を仮想トレードとして記録し事後採点することで、不作為バイアスを定量化するアーキテクチャパターン
- phantom勝率をキャリブレーションメッセージに変換してLLMのコンテキストに注入し、次サイクルの判断を自動補正するフィードバックループ
- realとphantomを同一SL/TPロジックで処理しtypeフィールドで区別することで、評価ロジックの重複を排除しつつ指標を分離する設計

## 前提知識

- **Claude API** → /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- **SL/TP（ストップロス/テイクプロフィット）** (TODO: 読むべき)
- **RSI・ATR（テクニカル指標）** (TODO: 読むべき)
- **LLMコンテキスト注入** (TODO: 読むべき)
- **エージェント意思決定ループ** (TODO: 読むべき)

## 関連記事

- /deep_7479 自己評価能力はすでに内在している：最小データでベースLLMの潜在的ジャッジ校正能力を引き出す
- /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- /deep_4180 AIに自己評価させたら全部8〜10点だった。採点基準を明示したら現実を突きつけられた話
- /deep_7926 音声メモをそのままチケットにしない — AmiVoice APIと生成AIで作る声のIssue下書き
- /deep_23 音声エージェント評価のための新フレームワーク EVA

## 原文リンク

[AIの「見送り判断」を後から採点するPhantom Trade設計](https://zenn.dev/r_inowa/articles/hermes-agent-07-phantom)
