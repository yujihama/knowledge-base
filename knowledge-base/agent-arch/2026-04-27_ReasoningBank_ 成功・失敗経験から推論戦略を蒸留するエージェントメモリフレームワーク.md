---
title: "ReasoningBank: 成功・失敗経験から推論戦略を蒸留するエージェントメモリフレームワーク"
url: "https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/"
date: 2026-04-27
tags: [ReasoningBank, agent-memory, LLM-as-a-judge, test-time-scaling, ReAct, WebArena, SWE-Bench, Gemini-2.5-Flash, MaTTS, 自己進化エージェント]
category: "agent-arch"
related: [1247, 2072, 908, 2889, 897]
memo: "[Google AI Blog] ReasoningBank: Enabling agents to learn from experience"
processed_at: "2026-04-27T12:25:34.197241"
---

## 要約

GoogleがICLR 2026論文で発表したReasoningBankは、デプロイ後のエージェントが成功・失敗両方の経験から汎化可能な推論戦略を継続的に学習するメモリフレームワーク。従来手法の課題は2点あった：①Synapseのような軌跡メモリは全アクションを記録するため高レベルな戦略パターンに昇華されない、②Agent Workflow Memory（AWM）は成功事例のみを参照し失敗から学ばない。ReasoningBankはこれを克服するため、各メモリアイテムを「Title・Description・Content（推論ステップ・意思決定根拠・運用知見）」の構造化形式で保持する。

ワークフローは「取得→実行→抽出→統合」のクローズドループで動作する。タスク実行前にReasoningBankから関連メモリをコンテキストに取り込み、実行後はLLM-as-a-judgeで軌跡を自己評価して成功インサイトまたは失敗の反省を抽出・追記する。失敗からは反事実シグナルとして防止策を蒸留する（例：「『Load More』をクリックする」という手続きルールではなく、「無限スクロールトラップを避けるため現在ページ識別子を先に検証する」という予防的ロジック）。

さらにMaTTS（Memory-aware Test-Time Scaling）を提案。テスト時スケーリング（TTS）をエージェント記憶と統合する手法で、並列スケーリング（同一クエリに対し複数軌跡を生成し対比でメモリを強化）と逐次スケーリング（単一軌跡内で段階的に推論を洗練し中間インサイトを記録）の2形態を持つ。

評価はGemini-2.5-Flashを基盤モデルとし、WebArena（動的Webナビゲーション）とSWE-Bench-Verified（ソフトウェアエンジニアリング）で実施。主な結果：メモリなし比でWebArena+8.3%、SWE-Bench-Verified+4.6%の成功率向上、SWE-Bench-VerifiedではタスクあたりステップをReasoningBankで約3ステップ削減。MaTTS（並列k=5）追加でWebArena成功率をさらに+3%、ステップ数を-0.4改善。

また、エージェントが経験を積むにつれメモリが進化する「戦略的成熟」が観察された：初期は「ページリンクを探す」という手続きチェックリストだったものが、「アクティブなページフィルタをタスクと継続的に照合してデータセットの早期ページネーションを防ぐ」という複合的・予防的ロジックへと自律進化した。

監査エージェント開発への示唆：失敗ケースからの反事実的学習は内部統制チェックにおける誤判定パターンの蓄積に直接応用可能。LLM-as-a-judgeによる自己評価ループは、LangGraphベースの監査エージェントでの異常判定精度の自律改善に転用できる。

## アイデア

- 失敗軌跡を反事実シグナルとして蒸留し「予防的ガードレール」を構築する発想：成功事例だけでなく失敗こそが高品質な戦略メモリの源泉になるという逆転の設計思想
- MaTTSによるテスト時スケーリングとメモリの双方向強化ループ：メモリが探索を誘導し、豊富な探索がより良いメモリを生成するという正のフィードバック設計
- エージェントが経験を積むにつれメモリが手続きチェックリストから複合的予防ロジックへと自律進化する「戦略的成熟」現象の観察：これはエージェント長期運用の品質評価指標になりうる

## 前提知識

- **ReAct prompting** (TODO: 読むべき)
- **Test-Time Scaling** → /deep_2179 テスト時知覚スケーリング（TTSP）：画像を使った思考におけるグラウンディングパラドックスの解消
- **LLM-as-a-judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **Trajectory Memory** (TODO: 読むべき)
- **Agent Workflow Memory** (TODO: 読むべき)

## 関連記事

- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_2072 SWE-AGILE: 動的推論コンテキストを効率管理するソフトウェアエージェントフレームワーク
- /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- /deep_2889 現在のAIの状況を理解するためのチャート集：Stanford AI Index 2026レポート解説
- /deep_897 時系列説明のためのLLM-as-a-Judge：参照なし評価フレームワーク

## 原文リンク

[ReasoningBank: 成功・失敗経験から推論戦略を蒸留するエージェントメモリフレームワーク](https://research.google/blog/reasoningbank-enabling-agents-to-learn-from-experience/)
