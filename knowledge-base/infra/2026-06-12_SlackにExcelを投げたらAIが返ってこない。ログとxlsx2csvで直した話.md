---
title: "SlackにExcelを投げたらAIが返ってこない。ログとxlsx2csvで直した話"
url: "https://zenn.dev/lnest_knowledge/articles/party-on-slack-excel-llm"
date: 2026-06-12
tags: [LLM, Slack, Excel, xlsx2csv, openpyxl, Heroku, Python, structured-logging, token-budget, timeout]
category: "infra"
related: [5037, 7793, 5684, 1733, 3762]
memo: "[Zenn LLM] SlackにExcelを投げたらAIが返ってこない。ログとxlsx2csvで直した話"
processed_at: "2026-06-12T09:07:36.802906"
---

## 要約

Slackアプリ「Party on Slack」でExcelファイルを添付してAIに質問すると、回答が極端に遅いまたは返ってこない問題が発生した。原因はLLM自体ではなく、その手前の処理にあった。具体的には①Slack添付ファイル取得にtimeoutがない、②Excel読み込みが全sheet/全cellを文字列連結する重い処理、③読み込み量に上限がなくメモリとトークン量が膨張、④ログが調査向けに整理されておらず問題箇所の特定が困難、という4点が原因だった。

改善策として以下を実施した。①接続timeout（5秒）と読み取りtimeout（30秒）を環境変数で設定し、timeout時は握りつぶさず呼び出し元に伝播させユーザーへメッセージを返す。②Excel読み込みをxlsx2csv中心に変更し、fallbackのopenpyxlはread_only=True/data_only=Trueで起動してメモリ展開を抑制、iter_rows(values_only=True)でcellオブジェクトを避け、文字列結合をlistへのappend＋joinに変更。③最大文字数3,000,000文字・最大行数5,000行・最大セル数150,000セルの上限を設け、超過時は例外ではなく「一部のみ読み込み」の注記をテキスト末尾に付加。④複数シートをシート名付きの見出し（例：[Sheet: 参加者名簿]）でLLMに渡し、AIがどのシートを参照したか説明できるようにした。

検証では約1.1MB・17シートのExcelをローカルでparseした結果、抽出文字数は約162万文字、parse時間は0.27〜0.29秒、追加メモリは数MB〜十数MB程度だった。一方Slack上のエンドツーエンドでは数分かかるケースがあり、ボトルネックはExcel parse後のLLM生成とSlackへの長文投稿であることが判明した。

デバッグ手法として、HerokuログとRedisキュー状態をAIエージェントと共同で分析する方法が有効だった。AIにはdownload/parse/queue/LLM応答の各ステップのメタ情報（file_id, filetype, download_ms, parse_ms, content_chars等）を渡し、仮説整理と「次に見るべきポイント」の抽出を担当させた。ログ設計の原則として「本文ではなくメタ情報のみ記録する構造化ログ（step=download status=ok duration_ms=842形式）」が、AIによる分析にも人間による読解にも有効であることを確認した。監査エージェント開発への示唆として、LLMへ渡すファイル前処理パイプラインにはtimeout・上限・構造化ログを必ず組み込む設計が、長期運用でのデバッグコスト削減に直結する。

## アイデア

- LLMへのファイル連携では、LLM自体よりも手前のファイル取得・前処理パイプラインがボトルネックになりやすく、download/parse/LLMの各ステップを独立して計測できる構造化ログが問題の切り分けを劇的に容易にする
- Excelのファイルサイズは処理コストの指標として不十分で、シート数・行数・セル数・セル内テキスト長が独立して処理量に影響するため、文字数・行数・セル数の複合上限設計が必要
- AIエージェントをデバッグに使う際は「全部任せる」より「構造化されたメタ情報を渡して仮説整理を委任する」分担が効果的で、機密情報を含まないメタ情報ログ設計はAI活用と情報セキュリティを両立させる

## 前提知識

- **openpyxl** (TODO: 読むべき)
- **xlsx2csv** (TODO: 読むべき)
- **Heroku Worker** (TODO: 読むべき)
- **Redis Queue** (TODO: 読むべき)
- **LLMトークン制限** (TODO: 読むべき)

## 関連記事

- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_7793 自作サイバーダッシュボードでAIパートナーと会話する——ゼロから構築した記録
- /deep_5684 構文ガイドと意味認識を組み合わせた選好最適化によるコード翻訳の改善（CTO）
- /deep_1733 【エンジニアの類推思考】日本語の仕様をプログラマー視点で読み解く―敬語はアクセス制御だった
- /deep_3762 YouTube動画から文字起こしをAPIで取得する

## 原文リンク

[SlackにExcelを投げたらAIが返ってこない。ログとxlsx2csvで直した話](https://zenn.dev/lnest_knowledge/articles/party-on-slack-excel-llm)
