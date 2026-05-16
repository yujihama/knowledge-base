---
title: "C#でマルチモーダルLLMのHTTP通信を可視化する：画像のみ vs 画像+テキストのリクエスト構造比較"
url: "https://zenn.dev/yy7613/articles/88278e57451e62"
date: 2026-04-15
tags: [マルチモーダルLLM, LM Studio, C#, HttpClient, Gemma4, OpenAI互換API, Base64, chat completions]
category: "infra"
related: [1420, 1333, 1423, 1605, 823]
memo: "[Zenn LLM] LLM の動き〜マルチモーダルモデルの確認〜"
processed_at: "2026-04-15T12:40:48.737055"
---

## 要約

本記事は、C#のHttpClientを使ってローカルLLM（LM Studio上のGoogle Gemma 4 26B Q4_K_M）にマルチモーダルリクエストを送信し、HTTPパケットレベルでリクエストボディの構造変化を観察する実装記録である。

最大のポイントは、テキストのみのAPIコールではmessages[].contentが文字列型であるのに対し、マルチモーダルコールではオブジェクト配列型に変わる点である。画像のみ送信（シナリオ1）では、contentは`[{type: "image_url", image_url: {url: "data:image/jpeg;base64,..."}}]`という1要素の配列になる。画像+テキスト（シナリオ2）では、`{type: "text", text: "..."}` と `{type: "image_url", image_url: {...}}`の2要素配列となり、OpenAI互換のchat completions APIフォーマット（/v1/chat/completions）に準拠している。

実装の核心は2つのクラスに分かれる。①HttpClientLoggingHandlerはDelegatingHandlerをベースにしたカスタムHTTPハンドラーで、SendAsync内でリクエスト・レスポンスの全トラフィックをコンソールに出力する。Base64エンコードデータは正規表現で検出し、先頭20文字と末尾10文字のみを表示して可読性を確保する（118,140文字のBase64データを圧縮表示）。②Program.csはシナリオ別にリクエストボディを組み立て、PostAndExtractメソッドで共通的に送受信とchoices[0].message.contentの抽出を行う。

実行環境は.NET 10.0、LM StudioがローカルホストのポートTCP 1234でOpenAI互換APIを提供する構成。モデルはGemma 4 26BのQ4_K_M量子化版（4ビット量子化）を使用。実際のレスポンスでは、チューリップの画像に対してGemmaがbounding boxのJSON形式（box_2d座標+label）で物体検出結果を返している点も確認されており、Gemma 4のオブジェクト検出能力も示されている。

コード設計上の特徴として、LoggingHandlerはシナリオに依存せず共通利用でき、シナリオ追加時もhandlerを変更せずにProgram.cs側だけ修正すれば済む疎結合な構造になっている。監査エージェント開発への示唆として、LLMへの証跡資料（画像・PDF）送信を実装する際のAPIリクエスト構造の理解基盤になり得る。マルチモーダル入力のHTTPフォーマットを実際のパケットで把握しておくことは、LLMバックエンドの差し替えやデバッグ時のトラブルシューティングに直結する。

## アイデア

- テキスト単体コールとマルチモーダルコールでcontentの型がstringからobject[]に変わるという非自明な仕様変化を、実パケットで可視化している点が実用的
- Base64の118KBデータをRegexで検出して先頭20文字+末尾10文字のみ表示するTruncateBase64の実装は、LLMデバッグ用ロガーのパターンとして再利用可能
- Gemma 4 26Bが画像のみのリクエストに対してbounding box座標をJSON形式で自発的に返す挙動は、物体検出タスクへのゼロショット活用可能性を示している

## 前提知識

- **OpenAI chat completions API** (TODO: 読むべき)
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開
- **Base64エンコード** (TODO: 読むべき)
- **LM Studio** → /deep_710 OlympicCoder をローカルで使う方法：LM Studio + VS Code による構築ガイド
- **HttpClientHandler** (TODO: 読むべき)

## 関連記事

- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_1423 Snapdragon + 16GiB RAMでローカルAIにWeb検索を実装した（LM Studio + MCP）
- /deep_1605 賢明に行動せよ：エージェント型マルチモーダルモデルにおけるメタ認知的ツール使用の育成
- /deep_823 統合はコストを伴うか？ Uni-SafeBench：統合マルチモーダル大規模モデルの安全性ベンチマーク

## 原文リンク

[C#でマルチモーダルLLMのHTTP通信を可視化する：画像のみ vs 画像+テキストのリクエスト構造比較](https://zenn.dev/yy7613/articles/88278e57451e62)
