---
title: "Generative UI: あらゆるプロンプトに対応するリッチでカスタムなビジュアル・インタラクティブUX"
url: "https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/"
date: 2026-04-02
tags: [Generative UI, Gemini 3, agentic coding, dynamic UI generation, PAGEN dataset, LLM-as-UI-generator, Google Research]
category: "ai-ml"
memo: "[Google AI Blog] Generative UI: A rich, custom, visual interactive user experience for any prompt"
processed_at: "2026-04-02T12:06:44.175204"
---

## 要約

GoogleはGemini 3 Proモデルを基盤とした「Generative UI」実装を発表した。AIモデルがコンテンツだけでなく、ウェブページ・ゲーム・ツール・アプリケーション等のインタラクティブなUIそのものをプロンプトに応じてオンザフライで生成する新パラダイムである。

技術構成は3層からなる。①ツールアクセス層：サーバーが画像生成・ウェブ検索等のツールへのアクセスを提供し、結果をモデルへフィードバックするか直接ブラウザへ送信して効率化する。②システム指示層：目標・計画・サンプル・技術仕様（フォーマット、ツールマニュアル、よくあるエラー回避のヒント）を含む詳細なシステムプロンプトで動作を制御する。③後処理層：モデル出力を一連のポストプロセッサに通して潜在的な問題を修正する。

評価ではPAGENと名付けた人間専門家製ウェブサイトのデータセットを構築し、生成速度を無視した条件で人間評価者による比較を実施。専門家制作サイトが最高評価を得たが、Generative UI実装がそれに次ぐ評価を獲得し、標準LLMのテキスト出力やMarkdown出力との間には大きな差が生じた。また、基盤モデルの性能向上がGenerative UIの品質に強く相関することも示された。

現在の課題として、生成に1分以上かかる場合があること、出力の不正確さが残ることが挙げられている。サービス展開としては、Geminiアプリの「dynamic view」実験機能およびGoogle SearchのAI Mode（米国のGoogle AI Pro/Ultraサブスクライバー向け、Thinkingモード選択時）として本日よりロールアウト開始。スタイリング面では、特定製品向けに一貫したスタイル（例：「Wizard Green」スタイル）での出力設定も可能で、未指定時はモデルが自動選択する。PAGENデータセットは近日中に研究コミュニティへ公開予定。

## アイデア

- AIがコンテンツではなくUIそのものを生成する発想は、エージェントの出力形式を静的テキストから動的インターフェースへ拡張する可能性を示す
- システム指示・ツールアクセス・後処理の3層構成は、エージェントシステムのアーキテクチャパターンとして汎用的に参照できる
- PAGENのような人間専門家制作物をベースラインとした評価データセットの設計手法は、LLM-as-judgeの代替または補完として活用できる

## Yujiの取り組みへの示唆

監査エージェントの出力を静的なレポートテキストではなく、インタラクティブなダッシュボードやシミュレーション形式で動的生成する設計の参考になる。Generative UIの3層構成（ツールアクセス・システム指示・後処理）はLangGraphのノード設計と親和性が高く、エージェント出力のレンダリング層として組み込むアーキテクチャを検討できる。また、PAGEN的な専門家制作物をリファレンスとした評価手法は、監査レポートの品質評価（LLM-as-judge）の設計にも応用可能。

## 原文リンク

[Generative UI: あらゆるプロンプトに対応するリッチでカスタムなビジュアル・インタラクティブUX](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/)
