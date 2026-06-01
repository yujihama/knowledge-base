---
title: "AmiVoiceとLLMで音声情報を取得・要約する実装ガイド（Next.js BFF構成）"
url: "https://zenn.dev/genai/articles/plactice-amivoice"
date: 2026-06-01
tags: [AmiVoice, STT, Next.js, BFF, OpenAI互換API, 音声認識, Supabase, multipart/form-data]
category: "infra"
related: [6928, 6838, 1884, 1807, 2454]
memo: "[Zenn LLM] AmiVoiceとLLMで音声情報を取得、要約するんじゃ"
processed_at: "2026-06-01T09:04:50.685934"
---

## 要約

アドバンスト・メディアが提供する日本語特化STTエンジン「AmiVoice API」と、OpenAI互換のLLM APIを組み合わせ、「録音→文字起こし→要約」のパイプラインをNext.js App Router上で実装したデモの解説記事。技術スタックはNext.js（BFF: Route Handler）、Supabase（t_transcription_recordテーブル）、AmiVoice同期HTTP（/v1/recognize）、OpenAI互換chat/completions（Gemini/OpenAI対応）。

フロント側でブラウザのMediaRecorder APIを使ってWebM形式の音声Blobを取得し、BFFのRoute Handlerを介してAmiVoice APIに転送する。APIキーはサーバー側（BFF）のみに保持し、クライアントに露出しない設計。認識結果のテキストはSupabaseに保存し、履歴画面からLLMで要約できる。

記事の中核となる技術的ハマりポイントは、AmiVoice APIのmultipart/form-dataパラメータ順序制約。公式仕様として「aパラメータ以降のパラメータは無視される」ため、FormDataへのappend順序をu（APIキー）→d（エンジン指定）→a（音声データ）の順に厳守する必要がある。逆順にするとillegal service authorizationエラーが返り、認証失敗と誤認しやすい。Node.jsのfetch+FormDataはcurlと異なり順序が自動整列されないため、手動でappend順を制御する必要がある。また環境変数のAPIキーに改行が混入するケースを防ぐため.trim()処理も推奨。

LLM要約機能はllm-summarizer.tsにOpenAI互換fetchロジックを実装し、temperature=0.2、最大入力8000文字（超過時は先頭切り捨て）で動作。要約結果はDBのmetadata_json（JSONB型）にキャッシュし、2回目以降はLLMを呼ばないキャッシュ優先設計。専用カラムは追加せずmetadata_jsonへのマージで対応している。環境変数LLM_API_KEY/LLM_API_BASE_URL/LLM_MODELは翻訳機能と共用するため追加設定不要。

AmiVoiceを選んだ理由として、日本語認識精度の高さ、業界別エンジン（医療・金融・保険等）の存在、ユーザー辞書による固有名詞精度向上、WebSocketストリーミング対応が挙げられている。監査AI用途では、対面商談の発話記録や要件定義へのメモ取り込みなど、現場での音声情報の構造化ニーズに直接応用できる。

## アイデア

- multipart/form-dataのパラメータ順序がAPIの認証可否に影響するという、見落としやすいAPIの仕様制約とその診断フロー（curl切り分け手法）が実務的に有用
- 要約結果をmetadata_json（JSONB）にキャッシュしてカラム追加なしで拡張する設計は、スキーマ変更コストを抑えながら機能を追加するパターンとして参考になる
- LLM_API_BASE_URLをOpenAI互換として抽象化することで、GeminiとOpenAIを環境変数1行で切り替えられる設計はマルチプロバイダー対応の最小実装として応用しやすい

## 前提知識

- **AmiVoice API** → /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- **Next.js App Router** (TODO: 読むべき)
- **multipart/form-data** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Supabase JSONB** (TODO: 読むべき)

## 関連記事

- /deep_6928 AmiVoice業界特化エンジンvs汎用エンジン：4ドメイン実測で見えた「使い分けの線」
- /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- /deep_1884 🤗 TransformersでWav2Vec2を英語音声認識（ASR）にファインチューニングする
- /deep_1807 🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる
- /deep_2454 音声認識のための拡散言語モデル：MDLM・USDMによるASR仮説リスコアリングとCTC結合デコーディング

## 原文リンク

[AmiVoiceとLLMで音声情報を取得・要約する実装ガイド（Next.js BFF構成）](https://zenn.dev/genai/articles/plactice-amivoice)
