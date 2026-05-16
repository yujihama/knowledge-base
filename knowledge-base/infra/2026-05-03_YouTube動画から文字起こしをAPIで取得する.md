---
title: "YouTube動画から文字起こしをAPIで取得する"
url: "https://zenn.dev/hkazuki/articles/143fe92284f52d"
date: 2026-05-03
tags: [youtube-transcript-api, Python, YouTube, 文字起こし, LLM, テキスト取得, Markdown]
category: "infra"
related: [1733, 682, 401, 1266, 1449]
memo: "[Zenn LLM] YouTube動画から文字起こしをAPIで取得する"
processed_at: "2026-05-03T12:51:47.461531"
---

## 要約

youtube-transcript-apiライブラリを使ってYouTube動画の自動生成字幕（書き起こし）をPythonで取得し、Markdownファイルとして保存する手法を紹介した記事。背景として、AI関連情報の急増により動画コンテンツの消化が追いつかない問題があり、まず要点だけ把握したいニーズに応える。

ライブラリはGoogleの非公式ライブラリであるyoutube-transcript-api（pip install）を使用する。AWS/GCP/Azure等のクラウドIP経由ではブロックされるため、ローカル環境での利用が前提。

実装は以下の流れ：①YouTubeTranscriptApiをインスタンス化、②video_idとlanguages=['ja', 'en']を指定してfetchメソッドで文字起こし取得、③snippets属性からテキストを抽出、④「[音楽]」等のノイズを除去、⑤Markdownファイルとして保存。フロントマターにtitleとvideo_idをYAML形式で付与するオプションも実装されている。

デモとして使用したのはAnthropicの公式YouTube動画「Why does bias exist in AI models?」（video_id: RnOWJoHU_NY）。取得したテキストはその後Claude Codeで手動要約する運用を想定しており、LLM API従量課金を避けるため自動化はしていない。

UI上からのコピペも可能だが、自動化により効率が大幅に向上。取得テキストに対しては、LLMによる議事録要約・翻訳・英語動画の予習用サマリ生成などへの活用を想定している。監査エージェント開発への示唆としては、動画コンテンツをテキスト化してRAGのデータソースとして取り込む際のパイプライン構築に応用できる。例えば監査関連のウェビナーや規制説明動画を自動収集・要約してナレッジベースに蓄積するエージェントの入力取得レイヤーとして機能しうる。

## アイデア

- youtube-transcript-apiのfetchメソッドでlanguages引数に優先順位付きリストを渡すことで、日本語字幕がない場合に英語へ自動フォールバックする設計
- 取得テキストをRAGのデータソースとして活用することで、動画コンテンツをベクトルDBに取り込むパイプラインを構築できる
- クラウドIP（AWS/GCP/Azure）からのアクセスがブロックされるため、サーバーレス化せずローカル実行に留める設計判断がAPI従量課金回避と合理的に一致している

## 前提知識

- **youtube-transcript-api** (TODO: 読むべき)
- **Python pip** (TODO: 読むべき)
- **YouTube自動生成字幕** (TODO: 読むべき)
- **Markdownファイル出力** (TODO: 読むべき)
- **LLMテキスト処理** (TODO: 読むべき)

## 関連記事

- /deep_1733 【エンジニアの類推思考】日本語の仕様をプログラマー視点で読み解く―敬語はアクセス制御だった
- /deep_682 【MarkItDown】Office/PDFをMarkdown化してRAG前処理に使う
- /deep_401 Gradioのgr.HTMLでワンショットWebアプリを構築する
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[YouTube動画から文字起こしをAPIで取得する](https://zenn.dev/hkazuki/articles/143fe92284f52d)
