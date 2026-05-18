---
title: "Snowflake AI_COMPLETE 関数で動画と音声を直接分析する"
url: "https://zenn.dev/snowflakejp/articles/794ce748589765"
date: 2026-05-18
tags: [Snowflake, Cortex AI, AI_COMPLETE, multimodal, 音声分析, 動画分析, gemini-3.1-pro, SQL]
category: "infra"
related: [4152, 1057, 4792, 1608, 212]
memo: "[Zenn LLM] Snowflake AI_COMPLETE 関数で動画と音声を直接分析"
processed_at: "2026-05-18T09:03:45.328776"
---

## 要約

Snowflake Cortex AI の AI_COMPLETE 関数が Public Preview として動画・音声ファイルの直接入力に対応した。従来の音声分析は「AI_TRANSCRIBE でテキスト化 → AI_COMPLETE で分析」という2段構成が必要だったが、今回のアップデートで動画・音声ファイルをそのまま AI_COMPLETE に渡すだけで要約・分類・感情分析・構造化抽出が可能になった。対応モデルは現時点で gemini-3.1-pro のみ。構文は `AI_COMPLETE(model, prompt, TO_FILE('@stage', 'file.mp4'))` とシンプルで、既存の AI_COMPLETE 呼び出しと完全に互換性がある。

主な特徴として、(1) SQL ネイティブ：既存の関数と同じ呼び出し方でメディアファイルを扱える、(2) 音声と映像の同時理解：動画の映像トラックと音声トラックを同時に解析できる、(3) JSON Schema による構造化出力：`TO_JSON(AI_COMPLETE(..., {}, {'type': 'json', 'schema': {...}}))` でダッシュボードや他システム連携向けの構造化データを直接取得できる、(4) 声のトーン・ピッチ分析：テキスト化では失われる vocal delivery（ピッチ・話速・音量・トーン）を AI がそのまま評価できる点が AI_TRANSCRIBE との決定的な差異。

対応フォーマットは動画が mp4/mpeg/mov/avi/flv/mpg/webm/wmv/3gpp、音声が wav/mp3/aiff/aac/ogg/flac/m4a/pcm/webm と幅広い。リクエスト上限は1リクエスト最大100MB・動画10本・音声10本。利用可能リージョンは gemini-3.1-pro のネイティブ提供リージョンに依存するが、`ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION'` のワンライナーでクロスリージョン推論を有効化することで他リージョンでも利用可能。

AI_TRANSCRIBE との使い分けとして、タイムスタンプ・話者ラベルが必要な文字起こし特化ユースケースでは AI_TRANSCRIBE が適切でコストも秒単位で予測しやすい。一方、声のトーン分析・動画の映像情報を含む分析・自由形式のプロンプト指定・JSON 構造化出力が必要なケースでは AI_COMPLETE が優位。コールセンター品質スコアリング・面接評価・問い合わせ緊急度判定など「言葉の内容ではなく声の出し方が意味を持つ」ユースケースで特に有効。また AI_CLASSIFY・AI_SENTIMENT・AI_AGG・AI_EMBED など Cortex AI Functions ファミリーと組み合わせることで、メディアデータの一気通貫パイプラインを SQL だけで構築できる点が大きな強み。

## アイデア

- 声のトーン・ピッチ・話速をテキスト化せずに直接 AI に評価させることで、コールセンター品質スコアリングや面接評価など従来のテキスト系パイプラインでは取れなかった情報を SQL 1行で抽出できる
- JSON Schema を AI_COMPLETE の引数に渡すことで構造化出力を強制できる設計は、監査ログやコンプライアンス証跡の自動構造化にそのまま応用でき、LangGraph エージェントの出力検証パターンとも相性が良い
- AI_COMPLETE の第1引数でモデル名を明示指定する設計により、モデル切り替えによるコスト・品質の変化をコントロールしながらパイプラインを設計できる点は、LLM-as-judge 構成での再現性確保に直結する

## 前提知識

- **Snowflake Cortex AI** (TODO: 読むべき)
- **AI_COMPLETE 関数** (TODO: 読むべき)
- **multimodal LLM** → /deep_369 視覚的In-Contextデモンストレーション選択の学習
- **JSON Schema** (TODO: 読むべき)
- **クロスリージョン推論** → /deep_5216 Claude CoworkをAmazon Bedrock経由で使ってみた

## 関連記事

- /deep_4152 顔動画からの非接触式光電脈波計測による新生児疼痛検出の探索
- /deep_1057 臨床テキストだけで十分か？心不全患者の死亡予測に関するマルチモーダル研究
- /deep_4792 第5回PVUWチャレンジ2位: ASR-SaSaSa2VA — 音声ガイド付き動画オブジェクトセグメンテーション
- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_212 波形から知恵へ：聴覚知能の新ベンチマーク MSEB（Massive Sound Embedding Benchmark）

## 原文リンク

[Snowflake AI_COMPLETE 関数で動画と音声を直接分析する](https://zenn.dev/snowflakejp/articles/794ce748589765)
