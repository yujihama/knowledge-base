---
title: "Consilium: 複数LLMが協調して意思決定するマルチLLMプラットフォーム"
url: "https://huggingface.co/blog/consilium-multi-llm"
date: 2026-04-07
tags: [multi-agent, MCP, consensus, LangGraph, Gradio, DeepSeek-R1, Mistral, structured-debate, role-assignment, function-calling]
category: "agent-arch"
memo: "[HF Blog] Consilium: When Multiple LLMs Collaborate"
related: [564, 83, 88, 1561, 745]
processed_at: "2026-04-07T12:20:23.447581"
---

## 要約

ConsiliumはGradio Agents & MCPハッカソンで開発されたマルチLLMコラボレーションプラットフォームで、複数のLLMが構造化された討論を通じて合意形成を行う仕組みを実装している。視覚的なポーカーテーブル形式のGradioインターフェースと、ClineなどのアプリケーションとMCPサーバーとして統合できる二形態で動作する。

アーキテクチャの中核は各LLMへの役割付与にある。standard（専門的分析）、expert_advocate（積極的提唱）、critical_analyst（批判的検討）、strategic_advisor（戦略的助言）、research_specialist（調査専門）、innovation_catalyst（革新的発想）の6役割を定義し、議論の多様性と生産性を担保する。通信構造はFull Context（全コンテキスト共有）、Ring（前参加者の回答のみ受け取り）、Star（リードアナリスト経由の中央集権型）の3モードを選択可能で、合意形成の収束速度と計算コストのトレードオフを調整できる。

意思決定モードはコンセンサス討論に加え、多数決投票とランク選択も実装。ユーザーが指定したリードアナリストLLMが最終結果を統合し、合意到達の判定を行う。討論ラウンド数は1〜5で設定可能で、ラウンド数が多いほど合意確率が上がる一方、計算コストも増大する。

対応モデルはMistral Large、DeepSeek-R1（SambaNova経由）、Meta-Llama-3.3-70B、QwQ-32Bで、ファンクションコーリング対応モデルには別途リサーチエージェントを統合。Web検索、Wikipedia、arXiv、GitHub、SEC EDGARの5ソースにアクセスし、視覚的にはラウンドテーブルの参加者として表示される。

セッション管理はuser_sessions[session_id]による辞書型で、参加者・メッセージ・現在話者・思考状態・吹き出し表示をJSON状態として管理。update_visual_state()コールバックで逐次更新され、複雑なステートマシンを用いずに直接JSON変異でリアルタイムUIを実現している。

MicrosoftのMAI-DxO（AI医師パネル）との比較が示唆的で、同様のマルチLLMアプローチでOpenAI o3使用時に医療診断ベンチマーク正答率85.5%を達成（一般医師20%）した事例を背景に、Consiliumのアーキテクチャの妥当性を説明している。

## アイデア

- 役割分担（批判者・提唱者・戦略家等）による構造化討論は、単一LLMの自己批判より実質的な多様性を生む設計パターン
- Ring・Star・Full Contextの3種通信トポロジーは、エージェント間情報フローの設計空間を整理する概念として汎用的に応用できる
- リードアナリストLLMによる合意判定という非対称役割設計は、最終意思決定の責任を明確化しつつ合議制の利点を保つ実用的パターン
## 関連記事

- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由
- /deep_83 ClaudeとHugging FaceでAI画像生成：MCP連携による実践ガイド
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1561 リーダーシップクラスシステムにおける高スループット材料スクリーニングのためのマルチエージェントオーケストレーション
- /deep_745 ケース適応型マルチエージェント審議による臨床予測：CAMP

## 原文リンク

[Consilium: 複数LLMが協調して意思決定するマルチLLMプラットフォーム](https://huggingface.co/blog/consilium-multi-llm)
