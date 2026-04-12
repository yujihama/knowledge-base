---
title: "ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）"
url: "https://zenn.dev/sum3sh1/articles/0447d4cb53d070"
date: 2026-04-10
tags: [LM Studio, ローカルLLM, PDF翻訳, PyMuPDF, PDFMathTranslate, Nemotron, Gemma, OpenAI互換API]
category: "infra"
memo: "[Zenn LLM] ローカルLLMを使って積読PDFを翻訳する（そしてまた積む）"
processed_at: "2026-04-10T09:32:43.876088"
---

## 要約

LM StudioのOpenAI互換APIを利用してローカルLLMでPDFを日本語翻訳する2つの手法を紹介した実践記事。著者はRTX 3060 12GBを使用。推奨モデルはliquid/Lfm2.5 1.2B（1.16GB）、nvidia/Nemotron 3 Nano 4B（2.64GB）、google/Gemma 3n E4B（4.24GB）、google/Gemma 4 26B A4B（16.76GB）の4種。

案1はPythonのPyMuPDF（fitz）でPDFをページ単位のtxtファイルに分割し、OpenAIクライアントでLM StudioのAPI（http://127.0.0.1:1234/v1）に翻訳リクエストを送る方法。最終的に1つのtranslated.txtに統合する。ページ単位で分割する理由は、大きなチャンクだと翻訳精度低下や処理失敗が発生するため。Gemma 3n E4Bで1,000ページ程度なら一晩（数時間）で完了する速度。

案2はPDFMathTranslate（pdf2zh）を使ってPDFのレイアウトを維持したまま翻訳する方法。GitHubのReleasesからpdf2zh-v1.9.11-win64.zipを取得し、コマンドプロンプトから起動するとWebUIが立ち上がる。設定はService=OpenAI-liked、OPENAILIKED_BASE_URL=http://127.0.0.1:1234/v1/、モデル名を指定するだけ。Lfm2.5 1.2Bで464ページの書籍を数十分で翻訳完了した実績あり。案1よりやや遅いが、元のPDFレイアウトを保持した翻訳済みPDFが得られる利点がある。

API認証キーはLM Studio側が検証しないため任意文字列で動作する。翻訳方向が英→日の場合は文字数が短くなるためレイアウト崩れが起きにくいが、逆方向では文字あふれの可能性がある。

## アイデア

- LM StudioのOpenAI互換API（http://127.0.0.1:1234/v1）を使えば、既存のOpenAIクライアントコードをapi_key='dummy'に変えるだけでローカルLLMに切り替えられる
- PDFMathTranslateはレイアウト保持翻訳が可能で、数式・図表が多い技術書・論文でも読みやすい翻訳PDFが生成できる
- Lfm2.5 1.2B（1.16GB）のような超軽量モデルでも464ページを数十分で翻訳できる実績があり、量産処理ではモデルサイズと速度のトレードオフ設計が現実的に検討できる

## Yujiの取り組みへの示唆

YujiはRTX 3090導入を予定しており、本記事のRTX 3060環境での実績はRTX 3090での性能推定に参考になる。監査関連の英語論文・技術文書（PCAOB基準、IIA規程等）を大量に日本語翻訳してRAGのソースデータとして活用するパイプラインに直接応用可能。LM StudioのOpenAI互換APIはLangGraphのエージェントノードのLLMバックエンドとして同じインターフェースで差し替えられるため、クラウドLLMとローカルLLMのハイブリッド監査エージェント構築の基盤技術として位置づけられる。

## 原文リンク

[ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）](https://zenn.dev/sum3sh1/articles/0447d4cb53d070)
