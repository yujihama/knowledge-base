---
title: "YouTube Shorts台本をAI自動生成するシステムを作った話"
url: "https://zenn.dev/kotaozaki/articles/shortsai-script-automation-2026-06-18"
date: 2026-06-18
tags: [Claude API, FastAPI, プロンプトエンジニアリング, tenacity, SRT字幕, コンテンツ自動化, JSON出力指定]
category: "other"
related: [4182, 6754, 2953, 8063, 8547]
memo: "[Zenn LLM] YouTube Shorts台本をAI自動生成するシステムを作った話"
processed_at: "2026-06-18T21:14:39.519021"
---

## 要約

エンジニアが「台本が書けない」という課題を解決するため、Claude APIを核にしたYouTube Shorts台本自動生成パイプラインを設計・実装した事例。システムはバックエンドPython（FastAPI）、フロントエンドNext.js、LLMにClaude 3.5 Sonnetを使用し、ShortsAIというWebサービスとして公開されている。

パイプラインは5段階構成：①プロンプトビルダー（ユーザー入力をLLM向け指示に変換）、②Claude API呼び出し（台本生成）、③パーサー（JSON構造化データへ変換）、④字幕タイムライン生成、⑤ハッシュタグ生成。台本の構造は「Hook（冒頭3秒）→ Value（本題）→ CTA（行動促進）」の3部構成に固定し、バズっているShorts100本の分析から導出したパターンをプロンプトに組み込んでいる。

プロンプト設計の要点は2つ：出力フォーマットをJSONで厳密に指定すること、ロールプロンプトで台本制作専門家のコンテキストを付与すること。トーン指定（educational/entertaining/inspirational/casual）は抽象語のまま渡さず、具体的な言語パターン（例：「テンポが速く、ユーモアがあり、エネルギッシュ」）に変換してLLMに渡す。

Claude API呼び出しにはtenacityライブラリによる指数バックオフリトライ（最大3回）を実装。さらにClaude 3.5 Sonnetが失敗した場合にClaude 3 Haikuへフォールバックする設計で、可用性とコストのバランスを確保している。

字幕タイムラインは「6文字/秒」の日本語読み上げ速度を基準に各セリフの表示時間を推定し、最低500ms・最大3000msにクランプしてSRT形式で出力する。ハッシュタグ生成も別プロンプトでLLMに依頼し、primary_tags/niche_tags/trending_tagsの3分類で返させることでA/Bテスト対応を容易にしている。

監査エージェント開発への示唆：LLMへの出力フォーマット強制（JSON指定）とフォールバック設計は、エージェントの信頼性確保に直接応用可能。tenacityによるリトライパターンは外部API呼び出しを伴う監査エージェントのエラーハンドリングにそのまま転用できる。

## アイデア

- 抽象的なトーン指定を具体的な言語パターンに変換してからLLMに渡すことで、出力品質を安定させる手法
- Sonnet→Haikuのモデルフォールバック構成により、コスト・可用性・品質のトレードオフを実装レベルで制御している点
- 字幕タイムラインを「文字数÷読み上げ速度」で推定し、SRT形式に変換することでLLM生成コンテンツを動画制作ツールと接続するパイプライン設計

## 前提知識

- **Claude API** → /deep_484 フレームワークを使わずにLLMエージェントを作る — Go + Claude API + AWSの設計と実装
- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **tenacity** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **SRT形式** (TODO: 読むべき)

## 関連記事

- /deep_4182 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第5回) ── main.pyが933行から33行になるまで
- /deep_6754 X投稿の品質を上げるために入れた3つの改善 — テーマ重複防止・投稿タイプ多様化・AI的文体排除
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_8063 鉄則は、一台に一推論 ── ローカルLLMアプリ R.E.V.I.S. v0.5.0 開発記録
- /deep_8547 議事録を要約して終わりにしない——LLMでプロジェクト状況シートを「自動更新」する仕組み

## 原文リンク

[YouTube Shorts台本をAI自動生成するシステムを作った話](https://zenn.dev/kotaozaki/articles/shortsai-script-automation-2026-06-18)
