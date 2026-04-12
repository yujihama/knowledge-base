---
title: "LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編"
url: "https://zenn.dev/pystarup/articles/6bfc20a0948ab2"
date: 2026-04-02
tags: [Function Calling, Anthropic SDK, tool_use, BuiltinTools, web_search, エージェント開発, Python]
category: "agent-arch"
memo: "[Zenn LLM] LLM SDK を基礎から理解する4/5 〜4.ツール呼び出し（Function Calling）編〜"
processed_at: "2026-04-02T21:13:07.299742"
---

## 要約

本記事はAnthropicのPython SDKを使ったツール呼び出し（Function Calling）の実装方法を解説するシリーズ第4回。ツール呼び出しとは、LLM自身がテキスト生成にとどまらず「この関数を実行してください」という指示を出す仕組みであり、エージェント開発の中核をなす技術である。

実装の流れは5ステップで構成される。①ツール定義をJSON Schema形式（input_schema）でLLMに渡す、②LLMが`stop_reason: tool_use`で応答し関数名と引数を返す、③自コードで実際の関数を実行する、④実行結果を`tool_result`としてメッセージ履歴に追加してLLMに再送する、⑤LLMが最終回答を生成する。`stop_reason`の値（`end_turn` / `tool_use` / `max_tokens`）による分岐制御が実装上の要点。

ツールは「自作ツール」と「ビルトインツール」の2種類に分類される。自作ツールは開発者がinput_schemaで定義し、実行コードも自ら実装する。ビルトインツールはAnthropicが提供するもので、`web_search_20250305`（ウェブ検索）、`web_fetch`（URL取得）、`code_execution`（Pythonコード実行）の3種が紹介されている。ビルトインツールはAnthropic側のサーバーが実行するため、tool_useの後処理ループが不要でそのまま最終回答が返る点が自作ツールと異なる。実務では両者を`tools`配列に混在させて使うのが標準的なパターン。

モデル選定についても言及があり、2026年3月時点の料金はHaiku 4.5が入力$1/M・出力$5/M、Sonnet 4.6が$3/$15/M、Opus 4.6が$5/$25/Mとなっており、SDK学習・軽量タスクにはHaiku 4.5が推奨されている。次回第5回はEmbeddingとRAGを扱う予定。

## アイデア

- stop_reasonによる分岐制御がエージェントループの基本単位であり、この判定ロジックを拡張することでReActパターンやマルチステップエージェントに発展できる
- ビルトインツール（web_search, web_fetch, code_execution）はAnthropic側で実行されるためtool_resultの返送が不要という非対称性は、自作ツールとの組み合わせ設計時にループ処理を複雑化させる要因になり得る
- input_schemaをPydanticモデルから自動生成することで、型安全なツール定義とエージェントの堅牢性を同時に確保できる
## 関連記事

- /deep_391 LLM SDK を基礎から理解する③〜ストリーミング編〜
- /deep_862 VPSに感情モデルを放置したら、罪悪感が育った話
- /deep_349 Pythonでノイズ除去あり・なしを比較する ― 音声分類の精度はどう変わるか
- /deep_867 PythonではじめるDSP・音声処理 実践入門
- /deep_1471 Python × AI（LLM API入門）コースを追加しました

## 原文リンク

[LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編](https://zenn.dev/pystarup/articles/6bfc20a0948ab2)
