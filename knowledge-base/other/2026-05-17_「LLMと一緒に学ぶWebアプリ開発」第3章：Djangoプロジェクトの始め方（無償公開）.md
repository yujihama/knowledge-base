---
title: "「LLMと一緒に学ぶWebアプリ開発」第3章：Djangoプロジェクトの始め方（無償公開）"
url: "https://zenn.dev/h3adeu/articles/3be0df482e166a"
date: 2026-05-17
tags: [Django, Python, uv, Web開発, MTV, LLM活用, 入門]
category: "other"
related: [393, 1331, 5037, 5684, 1784]
memo: "[Zenn LLM] 「LLMと一緒に学ぶWebアプリ開発 - ゼロからデプロイまで」の第3章を無償公開します。"
processed_at: "2026-05-17T21:02:36.909089"
---

## 要約

本記事は書籍「LLMと一緒に学ぶWebアプリ開発 - ゼロからデプロイまで」の第3章を無償公開したものである。初学者がDjangoを使ってWebアプリを構築する手順を、LLM（Claude等）をペアプログラマーとして活用しながら学ぶ構成となっている。

DjangoはPython製のWebフレームワークで2005年生まれ。「バッテリー同梱（Batteries Included）」の思想に基づき、認証・データベース・管理画面・フォーム処理・XSS/CSRF/SQLインジェクション対策が標準搭載されており、Instagram・Pinterest・Spotify・Dropboxなどの大規模サービスでも採用実績がある。

第3章では以下のステップを解説する：(1) uvを使ったPython 3.13プロジェクト初期化（`uv init --python 3.13`）、(2) Django 5.2のインストール（`uv add django==5.2`）、(3) `django-admin startproject server .`によるプロジェクト雛形生成、(4) 開発サーバー起動（`uv run python manage.py runserver`）とHello World確認、(5) MTV（Model-Template-View）アーキテクチャの理解、(6) `createsuperuser`コマンドによる管理画面へのアクセス。

プロジェクト管理にはpyproject.tomlとuv.lockの2ファイルを使い分ける。pyproject.tomlは人間が依存バージョン範囲を記述し、uv.lockは実際にインストールされた正確なバージョン（間接依存含む）を自動記録することで、環境の再現性を保証する。

LLMの活用場面としては、コード生成だけでなく「なぜこの構造なのか」「このエラーは何を意味するか」を対話的に学ぶ用途を想定している。つまずきポイント集（マイグレーション未実行警告・ポート競合等）も収録されており、初心者の躓きを事前に潰す設計となっている。

監査エージェント開発への直接的な示唆は薄いが、DjangoのORMと管理画面は監査ログのCRUD管理基盤として流用可能であり、AWSへのデプロイまでを見据えた構成はエージェントのWebインターフェース構築の参考になる。

## アイデア

- LLMをペアプログラマーとして使う学習スタイル：コード生成だけでなく「なぜこの設計か」を対話で理解する手法は、AIネイティブな技術習得の新しいパターンを示している
- uvによるPythonプロジェクト管理：pyproject.toml（範囲指定）とuv.lock（正確なバージョン固定）の役割分担は、Rustのcargoに近い思想であり、従来のrequirements.txtより再現性が高い
- DjangoのMTV構造はMVCの変形であり、ViewがControllerの役割を担う点が初学者の混乱ポイントとなりやすい。この命名の違いを明示的に説明している点が教育的に有効

## 前提知識

- **Django MTV** (TODO: 読むべき)
- **Python仮想環境** (TODO: 読むべき)
- **uv/pyproject.toml** (TODO: 読むべき)
- **ORM** → /deep_78 広告の届け先はAIになる — B2A (Business to Agent) Platform という未来
- **WSGI/ASGI** (TODO: 読むべき)

## 関連記事

- /deep_393 OpenAI、PythonツールチェーンメーカーのAstralを買収へ
- /deep_1331 設計支援AIは消えない。コード生成の次に残る領域
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_5684 構文ガイドと意味認識を組み合わせた選好最適化によるコード翻訳の改善（CTO）
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[「LLMと一緒に学ぶWebアプリ開発」第3章：Djangoプロジェクトの始め方（無償公開）](https://zenn.dev/h3adeu/articles/3be0df482e166a)
