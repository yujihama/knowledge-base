---
title: "Hermes AgentでXの過去ツイートから「その人っぽいAI」を作ってVPSに住まわせた話"
url: "https://zenn.dev/yukisuna777/articles/persona-ai-from-x-on-vps"
date: 2026-06-18
tags: [Hermes Agent, Hindsight, OpenRouter, memory stream, persona AI, sentence-transformers, VPS, Discord bot, structured output, Generative Agents]
category: "agent-arch"
related: [6285, 1757, 1641, 5211, 7411]
memo: "[Zenn LLM] Hermes Agentで、Xの過去ツイートから「その人っぽいAI」を作ってVPSに住まわせた話"
processed_at: "2026-06-18T09:00:46.826750"
---

## 要約

Xのアーカイブ（3万件超のツイート）を素材に、VPS上に常駐するペルソナAIエージェントを構築した実践記録。システム構成はConoHa VPS（Ubuntu, 2GB/3コア）上に、会話エージェント（Hermes Agent）・記憶システム（Hindsight）・LLM API（OpenRouter経由）の3層を配置。埋め込み処理はsentence-transformersをCPUでローカル実行してコストを抑え、課金が発生するLLM呼び出しは会話と記憶整理の場面のみに絞る設計とした。Discordからメッセージを送ると、そのキャラクターらしい返答が返ってくる。

詰まった点は3つ。①OpenRouterの無料枠はアカウント単位で1日50リクエストが上限で、夜間の記憶consolidationまで含めると即日枯渇する。$10分クレジットを購入すると枠が1000リクエスト/日（20倍）に解放され、かつ:freeモデルではクレジットを消費しないため、実質「$10で無料枠が20倍になる」という構造を利用して解消した。②記憶の保存・想起は正常に見えるが、整理（consolidation）工程だけが静かに失敗し続けていた。原因は割り当てたモデルが構造化出力（JSON）に非対応だったため、延々とパース失敗→リトライを繰り返していた。運用開始直後にログを確認する習慣がなければ気づけなかった。③性格をルールとして記述すると（例：「文末を言い切らないクセがある」）、LLMがそのルールを毎回律儀に適用して過剰演技になる。実データ集計でその口癖の出現率が0.7%にすぎないと判明。対策として、ルールの代わりに場面ごとの実際のセリフ（実例）を渡す方式に切り替えた。LLMはルール遵守より実例模倣の精度が高い。

記憶設計はGenerative Agents（Park et al., 2023）のmemory stream + reflectionと同構造であり、関連度・新近性・重要度でretrievalを行い、貯めた記憶から高次の洞察（reflection）を生成する仕組みに相当する。MemGPTやCharacter-LLMとも方向性が一致する。監査エージェント開発への示唆：記憶の保存・想起・整理を分離した設計は、監査ログや過去の指摘事項を蓄積して参照するエージェントにも応用可能。特に「整理工程だけが静かに失敗する」問題は、監査エージェントにおける品質監視の重要性を示している。

## アイデア

- 性格をルールではなく実例（few-shot）で渡す方がLLMの模倣精度が高い：「この口癖が最大の特徴」という思い込みが実データ集計（0.7%）で否定された点は、プロンプト設計全般に応用できる知見
- 記憶の保存・想起・整理を独立した工程として設計し、各工程に適切なモデルを割り当てる必要がある：整理工程だけ構造化出力非対応モデルで静かに壊れていた事例は、マルチエージェント設計のモデル選定の重要性を示す
- $10クレジット購入でOpenRouterの無料枠が20倍（50→1000リクエスト/日）に解放され、かつ:freeモデルではクレジット消費なし：個人用エージェントのコスト最適化として再現性のある実用的手法

## 前提知識

- **Generative Agents** (TODO: 読むべき)
- **sentence-transformers** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **structured output** → /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- **memory consolidation** (TODO: 読むべき)
- **OpenRouter API** (TODO: 読むべき)

## 関連記事

- /deep_6285 HindsightのrerankerをGPUなしCPUで9倍高速化 — batch size最適化とONNX化
- /deep_1757 🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_5211 同じプロンプトなのに毎回答えが変わる——LLMの非決定性という落とし穴
- /deep_7411 中国のAIモデルを実用目線で整理する（2026年6月）

## 原文リンク

[Hermes AgentでXの過去ツイートから「その人っぽいAI」を作ってVPSに住まわせた話](https://zenn.dev/yukisuna777/articles/persona-ai-from-x-on-vps)
