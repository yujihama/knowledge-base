---
title: "AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた"
url: "https://zenn.dev/mitsuo119/articles/7c1cc0262d8328"
date: 2026-05-29
tags: [AmiVoice, 音声認識, 構造化出力, Next.js, MediaRecorder, LLM, プロンプト設計, missing_information, チケット生成]
category: "other"
related: [4475, 3095, 4900, 1835, 5497]
memo: "[Zenn LLM] AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた"
processed_at: "2026-05-29T09:01:50.772866"
---

## 要約

AmiVoice API（音声認識）とLLM APIを組み合わせ、音声入力だけで完結する問い合わせフォームをNext.js（App Router）で実装した事例。ユーザーはブラウザ上で「録音開始→話す→録音停止」の3ステップのみで操作でき、裏側では音声→テキスト→構造化JSONという2段階変換が自動で走る。

技術スタックはフロントエンドにNext.js、バックエンドにNode.js（Route Handlers）、音声認識にAmiVoice API、構造化処理にLLM API（任意）。ブラウザ側はMediaRecorder APIでaudio/webm形式の音声を録音し、FormDataでバックエンドに送信。バックエンドはAmiVoice APIへ転送してテキスト化した後、LLMに渡して構造化JSONを生成する。

LLMへの指示はsystemプロンプトでJSONスキーマを厳密に定義し、`response_format: json_object`とtemperature=0.2で出力を安定させる。出力フィールドはcategory・summary・urgency（low/medium/high）・missing_information・follow_up_question・draft_message・admin_noteの7項目。最重要設計として「不足情報があっても推測で補完しない」ルールを徹底しており、missing_informationが空でなければフロントで聞き返しUIを表示する。これにより、LLMが注文番号などをでっち上げる事故を防止する。

Before/After比較では、フィラー（「えっと」）や指示語が混在した話し言葉をそのまま流すと管理画面では「読み物」にしかならないのに対し、構造化後は「チケット」として業務フローに直結できる点を示している。APIキーはすべてサーバー側の環境変数で管理し、フロントには公開しない。音声ファイルは処理後破棄、transcriptのログはマスクまたは短期保持とする個人情報対応も実装。

応用範囲として社内ヘルプデスク受付・営業日報の自動構造化・現場作業員の報告・高齢者向け操作補助フォームを挙げており、音声入力×構造化LLMの汎用パターンとして提示している。GitHubリポジトリ（mitsuo119/voice-form-ai）で実装を公開済み。監査エージェント開発への示唆として、「入力の曖昧さを構造化する際に推測補完を禁止し、人間確認ループを必ず挟む」設計原則はエージェントの信頼性確保にも直接応用できる。

## アイデア

- 音声認識とLLMを「文字起こし」と「意味の構造化」として明確に役割分離することで、それぞれのAPIの得意領域を最大化する設計パターン
- LLMに不足情報を推測補完させず`missing_information`配列として明示させ、ユーザーへの聞き返しループを設けることでハルシネーションを業務レベルで封じる手法
- 話し言葉→構造化チケットの変換により、スマホ・移動中・高齢者等の入力弱者向けUIを業務システムに接続する汎用アーキテクチャとして機能する

## 前提知識

- **LLM structured output** (TODO: 読むべき)
- **MediaRecorder API** (TODO: 読むべき)
- **AmiVoice API** (TODO: 読むべき)
- **systemプロンプト設計** (TODO: 読むべき)
- **Next.js App Router** (TODO: 読むべき)

## 関連記事

- /deep_4475 採点基準v2改訂で「直感力9点」が認定された——LLM個人アセスメントプロンプト設計の実践記録
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1835 【実録】GeminiはGoogle自社サービスの夢を見るか？ ―― ハルシネーションの実例・傾向・対策
- /deep_5497 【メモ】生成AIは、要件定義の何を変えるのか

## 原文リンク

[AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた](https://zenn.dev/mitsuo119/articles/7c1cc0262d8328)
