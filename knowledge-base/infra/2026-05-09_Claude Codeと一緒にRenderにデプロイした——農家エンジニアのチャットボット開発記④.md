---
title: "Claude Codeと一緒にRenderにデプロイした——農家エンジニアのチャットボット開発記④"
url: "https://zenn.dev/hiroakikody/articles/73047160d069b8"
date: 2026-05-09
tags: [Render, Flask, GLM-4.7, Gunicorn, Neo4j, LangChain, RAG, Claude Code, Z.ai, OpenAI互換API]
category: "infra"
related: [4520, 2404, 858, 2255, 4335]
memo: "[Zenn LLM] Claude Codeと一緒にRenderにデプロイした——農家エンジニアのチャットボット開発記④"
processed_at: "2026-05-09T21:36:25.918439"
---

## 要約

熊本県産クレソンを生産する農家エンジニアが、Z.aiのGLM-4.7-Flashを使ったクレソン料理専門AIをRenderにデプロイするまでの5時間のデバッグ記録。デプロイ先の選定ではRenderとVercelを比較し、Flaskネイティブ対応・無料プランでの商用利用可能・GitHub連携による自動デプロイを理由にRenderを採用した。Vercelは無料プランの実行時間制限（10秒）がGLM-4.7の応答時間（20〜40秒）に対応できない点も決め手となった。

ローカル段階では2つの罠にはまった。①OpenAI互換APIのbase_urlにエンドポイントパス（/chat/completions）を含めると、ライブラリが自動付加するため二重になり404エラーが発生する。②Z.aiの課金体系はコーディングプラン（月$6、Claude Code等専用）とAPIトークン残高（別枠、Pythonコードからの直接呼び出し専用）が完全に独立しており、Python SDKから呼び出すには別途$5以上のチャージが必要だった。

Render本番環境では3つの罠が追加で発生した。①GLM-4.7はデフォルトで推論モード（thinking mode）が有効で、max_tokens=1024（デフォルト）では推論プロセスだけでトークンが枯渇しcontentが0バイトになる。max_tokens=4096に増加し、contentが空の場合のフォールバックとしてreasoning_contentを使う実装で解決した。この挙動はZ.ai固有で公式ドキュメントにも記載がない。②Claude Codeが提案したlangchain-neo4j向けのdriver_configパラメータがバージョン0.9.0では存在せずTypeErrorが発生。AIの提案コードでも必ずドキュメントでバージョン対応を確認する必要があることを示している。③Neo4j Aura Freeへのkeepaliveスレッドをif __name__ == '__main__'ブロック内に書いていたため、Gunicornがモジュールとしてimportする際に実行されず接続維持が機能しなかった。モジュールレベルでstart_keepalive()を呼び出すことで解決した。

最終的にTTFB 12.68秒・200 OKでデプロイが成功し、190品のクレソン料理データベースを持つGraph RAGシステムが公開された。監査エージェント開発への示唆として、本番環境固有のデバッグ（Gunicornの起動フロー、LLMの推論モードによるトークン消費）はローカルテストでは再現しないケースが多く、ステージング環境での検証と本番ログの監視が不可欠である点が参考になる。

## アイデア

- GLM-4.7のデフォルト推論モード（thinking mode）がmax_tokens=1024でcontentを0バイトにする挙動はZ.ai固有かつ公式非記載で、OpenAI互換APIを使うLLMアプリ開発では各モデルのトークン消費パターンの事前確認が必須
- GunicornはPythonファイルをモジュールとしてimportするためif __name__ == '__main__'ブロックが実行されず、バックグラウンドスレッドやinitial処理はモジュールレベルに書かなければ本番環境で動かないという落とし穴
- Z.aiの課金体系がコーディングツール向けサブスクとAPI呼び出し用トークン残高で完全に分離されており、同一プロバイダでも用途別に独立した認証・課金管理が必要なケースがある

## 前提知識

- **Flask** → /deep_1883 Google Cloud上でサーバーレスTransformersパイプラインを構築した記録
- **Gunicorn** → /deep_1883 Google Cloud上でサーバーレスTransformersパイプラインを構築した記録
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Neo4j** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_4335 RAGの精度が出ない3つの原因と、Golden Setで改善サイクルを回す方法

## 原文リンク

[Claude Codeと一緒にRenderにデプロイした——農家エンジニアのチャットボット開発記④](https://zenn.dev/hiroakikody/articles/73047160d069b8)
