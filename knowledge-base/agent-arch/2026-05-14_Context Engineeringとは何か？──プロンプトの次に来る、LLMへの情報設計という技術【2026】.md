---
title: "Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】"
url: "https://zenn.dev/karaagedesu/articles/a7d58f2f197aa3"
date: 2026-05-14
tags: [Context Engineering, Context Rot, RAG, LangGraph, Prompt Caching, マルチエージェント, Self-Attention, コンテキストウィンドウ]
category: "agent-arch"
related: [41, 858, 2255, 2877, 5264]
memo: "[Zenn LLM] Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】"
processed_at: "2026-05-14T09:00:48.229821"
---

## 要約

Context Engineering（CE）は、LLMのコンテキストウィンドウ全体を設計・最適化する技術であり、「指示文の改善」に留まるPrompt Engineeringの自然な進化形として位置づけられる。2025年6月にShopify CEO Tobi LutkeがCEという用語を提唱し、Andrej Karpathyが「最適な次のアクションを得るために、コンテキストウィンドウに適切な情報を精巧に詰め込むアートとサイエンス」と定義した。AnthropicもPrompt Engineeringの「自然な進化」として公式に認めており、2026年現在はAIエージェント開発の実務標準になりつつある。

CEが重要になった主因は「Context Rot（コンテキスト腐食）」問題である。TransformerのSelf-Attentionはトークン数のn²に比例する計算量を持つため、コンテキストが長くなるほど重要情報が埋もれ、モデルの想起・活用精度が逓減する。したがってCEの本質的目標は「最小の高シグナルトークン集合で期待される結果の可能性を最大化する」ことにある。

コンテキストウィンドウの構成要素はSystem Prompt、外部Memory、RAG取得文書、Tool Results、会話履歴（圧縮済み）、User Inputの6層に整理される。これらを管理する戦略として4つのフレームワークが提示されている。①Write：中間状態をファイル・DB・メモリストアに書き出す（LangGraphのMemorySaverが典型例）。②Select：RAGで関連度スコア閾値（例：0.75）以上の文書のみをk=3件取得し、ノイズを排除する。③Compress：会話が20ターンを超えたら古い履歴をLLMに要約させて直近5件と置換する。④Isolate：タスクをサブタスクに分割し、各エージェントが独立したコンテキストを保持するマルチエージェント構成（LangGraphのサブグラフ）を用いる。

実践テクニックとして、Claude等のLLMはXMLタグで区切られた情報をより正確に認識するため、＜role＞＜rules＞＜output_format＞等のタグによる構造化が有効とされる。また「Lost in the Middle」問題への対策として重要な指示を先頭と末尾に重複配置する手法、AnthropicのPrompt Caching機能（同一プレフィックスのコストを最大90%削減）の活用も紹介されている。

AIエージェントにおいてはコンテキスト超過・ノイズによる迷走・コスト増大が実務上の主要課題であり、ARISの論文が「エージェントの性能はモデルの重みだけでなく、何をどう記憶・検索・提示するか（ハーネス）で決まる」と明言している点はCEの核心を突く。監査エージェント開発においても、LangGraphのチェックポイント機構・RAGのスコア閾値設計・マルチエージェントによるコンテキスト隔離は直接適用可能な実装パターンである。

## アイデア

- Context Rotの根本原因をSelf-AttentionのO(n²)計算量に求め、「詰め込み最大化」ではなく「シグナル密度最大化」へのパラダイム転換を明確に示している点
- Write/Select/Compress/Isolateという4戦略フレームワークが、LangGraphの具体的なコードと対応付けて説明されており、監査エージェントのステート管理設計にそのまま転用できる
- 「エージェントの性能はハーネス（記憶・検索・提示の設計）で決まる」というARIS論文の知見が、Context Engineeringをモデル選定よりも優先すべき設計要素として位置づける強い根拠になっている

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **Prompt Engineering** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 関連記事

- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_2877 SemiFA：半導体故障解析レポートを自律生成するエージェント型マルチモーダルフレームワーク
- /deep_5264 Praxia — 個人の暗黙知を組織知に自動昇格させるマルチエージェントOSS

## 原文リンク

[Context Engineeringとは何か？──プロンプトの次に来る、LLMへの情報設計という技術【2026】](https://zenn.dev/karaagedesu/articles/a7d58f2f197aa3)
