---
title: "Claudeと機械学習を頑張ることにした — Claude/Claude Codeをメンターとして活用する学習設計"
url: "https://zenn.dev/knd73/articles/7442baa8e548db"
date: 2026-03-30
tags: [Claude, Claude-Code, LightGBM, Kaggle, Pydantic, Polars, MLflow, 学習設計, CLAUDE.md]
category: "other"
memo: "[Zenn 機械学習] Claudeと機械学習を頑張ることにした"
processed_at: "2026-03-30T12:12:42.325646"
---

## 要約

B2の学生（まめっち）が、「AIにコードを書かせてレビューするだけ」の状態から脱却し、機械学習の地力をつけるために設計した学習システムの全体像を紹介した記事。最終ゴールはPhase3のRL+MCTS+ゲームAI実装で、現在はPhase1（LightGBM+パイプライン修行）に取り組んでいる。

技術スタックはuv（パッケージ管理）、Pandas（探索用）、Polars（本番パイプライン）、LightGBM（モデル）、typer（CLI）、Pydantic（設定バリデーション）、pytest（テスト）、MLflow（実験管理）で構成される。

Claudeの役割を3層に分割している点が特徴的。①Claude Projects（ブラウザ）はOpus使用の長期メンターとしてロードマップ見直しやフェーズ移行判断を担う。②コンペコーチはSonnet使用でKaggleコンペ固有の特徴量エンジニアリング・CV設計・上位解法分析を担当し、コンペ終了後はアーカイブして新たに作成する。③Claude Code（ターミナル）はコードレビュー・テスト作成・詰まった実装支援を担う。OpusとSonnetを用途で使い分けるのはClaude Proプランのクレジット消費を抑えるためでもある。

CLAUDE.mdにはコンペ固有のルール（data/raw/は読み取り専用、TDD、lag特徴量のリーク防止、Polarsによる本番パイプライン、JSON設定ファイル必須）を記載し、Claude Codeに毎回自動で読み込ませる設計。コンペコーチがGitHub Issuesとしてマイルストーンを出力し、それに沿って実装を進める。

学習管理はコードリポジトリとは別にml-journeyというプライベートリポジトリを作り、週次振り返り・実験ログ・上位解法分析・プロンプトチートシートを集約。コンペ終了時には必ずtop-solutions.mdに上位解法の差分分析を行い、Zennへの記事化（取り組み記事＋技術深掘り記事）までをワンセットとして運用する。

## アイデア

- Claude ProjectsをOpus（長期メンター）とSonnet（コンペコーチ）に役割分割し、文脈の長さと精度・コストのトレードオフを意識的に設計している点
- CLAUDE.mdをコンペごとのコンテキストファイルとして使い、Claude Codeにプロジェクト固有のルール（リーク防止、TDD強制等）を毎回自動注入する運用パターン
- コードリポジトリと知見リポジトリ（ml-journey）を分離し、実験ログ・上位解法分析・振り返りをGitで管理してZenn記事化まで一気通貫にする学習サイクル設計
## 関連記事

- /deep_122 ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_974 変な機械学習アプリを作ってしまった【第1回：動機とredditで玉砕した話】
- /deep_593 国防総省のAnthropicに対するカルチャーウォー戦術は裏目に出た

## 原文リンク

[Claudeと機械学習を頑張ることにした — Claude/Claude Codeをメンターとして活用する学習設計](https://zenn.dev/knd73/articles/7442baa8e548db)
