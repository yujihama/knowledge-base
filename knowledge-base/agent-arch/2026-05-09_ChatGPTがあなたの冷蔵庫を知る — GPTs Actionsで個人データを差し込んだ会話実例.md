---
title: "ChatGPTがあなたの冷蔵庫を知る — GPTs Actionsで個人データを差し込んだ会話実例"
url: "https://zenn.dev/yatmita/articles/chatgpt-knows-your-fridge"
date: 2026-05-09
tags: [GPTs Actions, OpenAPI, RAG, tool-use, vision, bulk-endpoint, プロンプトエンジニアリング, REST API, ChatGPT]
category: "agent-arch"
related: [2270, 4036, 77, 1337, 856]
memo: "[Zenn LLM] ChatGPT があなたの冷蔵庫を知る — GPTs Actions で個人データを差し込んだ会話実例"
processed_at: "2026-05-09T21:35:12.927018"
---

## 要約

本記事は、OpenAIのGPTs Actions機能を使って個人の冷蔵庫データをChatGPTに動的に渡し、食材管理・レシピ提案を行う実用GPTs「まかせて」の構築事例を会話ログベースで解説する。

GPTsのカスタマイズ手段は「指示（システムプロンプト）」「ナレッジ（静的ファイル）」「Actions（外部REST API）」の3つだが、ユーザーごとに毎回変わる動的データを扱うにはActionsが必須となる。技術的には「OpenAPI仕様のYAMLを1枚渡すと、ChatGPTが自然言語の依頼から該当エンドポイントを自動で叩く」REST APIクライアント自動生成の仕組みである。

実装されたAPIエンドポイントは主に`listItems`（冷蔵庫食材一覧）、`bulkCreateItems`（最大50件一括登録）、`bulkDeleteItems`（一括削除）、`listYatmitaRecipes`（自作レシピ一覧）の4種。特に`bulk endpoint`の設計は実用上重要で、1件ずつ`createItem`を7回呼ぶと数十秒〜分単位かかるのに対し、`bulkCreateItems`で一括処理することで体感速度を大幅に改善している。

会話例は4本紹介される。①冷蔵庫の52件食材から`registered_at`の古い順でソートし「豚バラ＋にんじんのガーリック醤油炒め」を提案するケース、②`listItems`と`listYatmitaRecipes`の2エンドポイントを使い分けて冷蔵庫食材＋自作レシピサイトのリンクを同時提示するケース、③冷蔵庫写真のvision解析で確信度を3段階（高：そのまま登録候補／中：曖昧さを保持／低：ユーザー確認）に分類して初期登録するケース、④レシートOCRで「パン以外を登録」という自然言語指示を解釈し7件一括登録するケース。

プロンプト設計上の重要知見として、①Actions失敗時に曖昧にごまかさず正直に申告させる明示的指示、②確信度の低い食材は勝手に登録せずユーザー確認を挟む指示、③「分かったふりをするな」と「だんまりもするな」を両立させる推測案提示の指示、の3点が挙げられている。またAPIスキーマ設計では「冷蔵／冷凍／常温」の保存場所カラムを持たずシンプルに保つことで、想定外の使い方（棚の一括登録等）をChatGPTが自然に拾える余地が生まれるとしている。

監査エージェント開発への示唆として、外部APIとLLMを繋ぐActions的なパターン（OpenAPI仕様でエンドポイントを定義し、LLMが自然言語から適切なAPIを選択・呼び出す）はLangGraph上のツール呼び出し設計と本質的に同一であり、bulk endpointの設計やプロンプトによる失敗申告の強制はエージェントの信頼性設計に直接応用できる。

## アイデア

- bulk endpointを必ず用意するというAPI設計原則：LLMのActions/Tool呼び出しは1回ごとにラウンドトリップコストが発生するため、N件登録をN回呼び出しではなく1回のbulk呼び出しに集約することが実用上不可欠
- visionモデルの確信度を3段階に分類してユーザー確認コストを非対称化する設計：確信度高はまとめて処理、低いものだけ拾い上げて確認することで初期登録の負担を最小化しつつ誤登録を防ぐ
- プロンプトでLLMの「失敗曖昧化バイアス」を明示的に打ち消す手法：Actions失敗時に正直申告させる指示と、推測案を出してyes/no確認させる指示を組み合わせることで、信頼性と会話テンポを両立させる

## 前提知識

- **GPTs Actions** (TODO: 読むべき)
- **OpenAPI仕様** (TODO: 読むべき)
- **Tool use / Function calling** (TODO: 読むべき)
- **vision OCR** (TODO: 読むべき)
- **REST API設計** (TODO: 読むべき)

## 関連記事

- /deep_2270 VAKRA詳解：AIエージェントの推論・ツール利用・失敗モードの分析
- /deep_4036 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第4回) ── 「きみ」を消したら、品質も消えた話
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_1337 RAGの検索をAIに任せたら精度が79%上がった（Agentic RAG / A-RAG）
- /deep_856 Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで

## 原文リンク

[ChatGPTがあなたの冷蔵庫を知る — GPTs Actionsで個人データを差し込んだ会話実例](https://zenn.dev/yatmita/articles/chatgpt-knows-your-fridge)
