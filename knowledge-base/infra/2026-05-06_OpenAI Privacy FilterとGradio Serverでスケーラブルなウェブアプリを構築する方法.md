---
title: "OpenAI Privacy FilterとGradio Serverでスケーラブルなウェブアプリを構築する方法"
url: "https://huggingface.co/blog/openai-privacy-filter-web-apps"
date: 2026-05-06
tags: [Privacy Filter, PII検出, Gradio, gradio.Server, FastAPI, ZeroGPU, OCR, Tesseract, HuggingFace, Apache2.0]
category: "infra"
related: [1852, 390, 1448, 1354, 652]
memo: "[HF Blog] How to build scalable web apps with OpenAI's Privacy Filter"
processed_at: "2026-05-06T12:33:46.044152"
---

## 要約

OpenAIがHugging Face Hub上でオープンソースのPII（個人識別情報）検出モデル「Privacy Filter」を公開した。パラメータ数1.5B（アクティブ50M）、Apache 2.0ライセンス、128kトークンのコンテキスト長を持ち、private_person / private_address / private_email / private_phone / private_url / private_date / account_number / secretの8カテゴリを単一フォワードパスで検出する。PII-Masking-300kベンチマークでSOTA性能を達成している。

Hugging Faceのエンジニアチームはこのモデルを活用し、`gradio.Server`をバックエンドとした3つのウェブアプリを構築した。

**1. Document Privacy Explorer**：PDF/DOCXをアップロードするとPIIスパンがカテゴリ別にハイライト表示される。PyMuPDF / python-docxでテキスト抽出後、128kコンテキストを活かしてチャンキングなし・単一パスで処理するため、スパンオフセットがレンダリングテキストと直接対応する。サイドバーのフィルターはCSSクラスのトグルで実現し、モデルの再実行を回避している。

**2. Image Anonymizer**：スクリーンショットや画像をアップロードすると、PII箇所が黒バーで隠された画像が返される。Tesseract OCRで文字と座標を取得し、Privacy Filterでスパン検出後、文字オフセットをピクセル座標に変換する。フロントエンドはカスタム`<canvas>`で実装し、バーのドラッグ・カテゴリ別トグル・PNGエクスポートをすべてクライアントサイドで完結させる。

**3. SmartRedact Paste**：テキストを貼り付けると、`<PRIVATE_PERSON>`や`<ACCOUNT_NUMBER>`等のプレースホルダーで置換したパブリックURLと、元テキストを参照できるトークンゲート付きプライベートURLの2つが生成される。多言語テキスト（スペイン語・フランス語・中国語・ヒンディー語等）も同一APIコールで処理可能。

共通アーキテクチャとして`gradio.Server`が重要な役割を果たす。これはFastAPIアプリとして動作し、`@server.api(name=...)`デコレータにより処理をGradioのキューに組み込むことで、ZeroGPU割り当て・並列アップロードのシリアライズ・`gradio_client` SDKとの互換性を同時に確保する。ブラウザからは`@gradio/client`のJS SDKで`client.predict()`として呼び出せる。`@server.api`と`@server.get`を同一プロセスで共存させられる点が、URLルーティングが重要なSmartRedactのようなアプリで特に有効。監査AI開発への示唆として、契約書・ログ・メールなどの監査証跡に含まれるPIIを単一パスで検出・マスクするパイプラインを、GPU不要の軽量モデルで本番運用できる可能性がある。

## アイデア

- 128kコンテキストを活かしてPDF全体をチャンキングなしで単一フォワードパスに通すことで、スパンオフセットのずれや文脈断絶を回避している点は、長文契約書の監査処理にも応用できる
- `@server.api`デコレータがGradioキュー・ZeroGPU・gradio_client SDKを一括で接続する設計は、GPUリソース管理を意識せずにスケーラブルなML APIを構築する際の実装パターンとして参考になる
- PIIスパンを`<CATEGORY>`プレースホルダーに置換するだけで多言語対応のリダクション共有リンクを作れるSmartRedactの発想は、監査報告書の外部共有フローに転用できる

## 前提知識

- **BIOES decoding** (TODO: 読むべき)
- **Gradio Blocks / Server** (TODO: 読むべき)
- **FastAPI** → /deep_509 SAGAI-MID: 動的ランタイム相互運用性のための生成AI駆動ミドルウェア
- **ZeroGPU** → /deep_83 ClaudeとHugging FaceでAI画像生成：MCP連携による実践ガイド
- **Named Entity Recognition** (TODO: 読むべき)

## 関連記事

- /deep_1852 Hugging Face コースローンチ コミュニティイベント（2021年11月）
- /deep_390 Hugging Face Spacesの無料枠に小型LLMをデプロイしてAPIを立てる方法（非推奨）
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新
- /deep_1354 Hugging Face Hub：美術館・図書館・文書館・博物館（GLAM）向け活用ガイド
- /deep_652 GradioでMCPサーバーを5行のPythonで構築する方法

## 原文リンク

[OpenAI Privacy FilterとGradio Serverでスケーラブルなウェブアプリを構築する方法](https://huggingface.co/blog/openai-privacy-filter-web-apps)
