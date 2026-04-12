---
title: "Hugging Face Daily Papersページの機能完全ガイド"
url: "https://huggingface.co/blog/daily-papers"
date: 2026-04-08
tags: [HuggingFace, Daily Papers, AI論文, arXiv, 研究コミュニティ, librarian-bot]
category: "other"
memo: "[HF Blog] Exploring the Daily Papers Page on Hugging Face"
processed_at: "2026-04-08T21:34:09.832796"
---

## 要約

Hugging FaceのDaily Papersページは、AKおよびコミュニティ研究者が厳選した最新AI論文を毎日掲載するプラットフォームである。2024年9月時点で3,700本以上の論文が掲載され、購読者数は12,000人超に達している。主要機能は以下の通り。①論文クレーム機能：著者がHFアカウントを持つ場合、1クリックで自分の論文をアカウントにリンクできる。②論文投稿機能：論文をクレームしたユーザーであれば自分の研究に限らず、コミュニティに有益な論文を投稿できる。③著者とのチャット機能：各論文ページの下部にあるディスカッションセクションで著者に直接@メンションし、リアルタイムでフィードバックや議論が可能。④関連リソースのワンページ集約：各論文ページの右側にモデル・データセット・デモ・コレクションが紐付けられており、著者はREADME.mdにarXiv URLを追加するだけで自動リンクされる。⑤アップボート機能：論文への支持を示すボタンで、影響力のある研究の発見を促進する。⑥librarian-botによる類似論文推薦：コメント欄で@librarian-botをタグすると関連論文が自動提案される。⑦多言語コメントと翻訳機能：任意の言語でコメントを投稿でき、内蔵翻訳機能で全ユーザーが内容を把握できる。⑧購読機能：「Subscribe」ボタンで平日毎日最新論文をメールで受信可能。⑨arXiv連携：Chrome拡張「arxiv-to-hf」をインストールすると、arXivページ上にHFのDaily Papersへの掲載有無を示す🤗絵文字が表示され、クリックでHFの論文ページへ直接ジャンプできる。またarXiv上からHugging Face Spacesのデモへのリンクも確認可能。これらの機能を組み合わせることで、最新研究の発見・著者との交流・関連実装の把握を一元的に行える研究者向けハブとして機能する。

## アイデア

- librarian-botによる類似論文自動推薦は、RAGやベクトル検索を活用した論文レコメンドエンジンの実装例として参考になる
- 著者がREADME.mdにarXiv URLを記述するだけでモデル・データセットと論文が自動リンクされる仕組みは、メタデータ管理の省力化設計として興味深い
- arXiv Chrome拡張によるクロスプラットフォームな論文ステータス表示は、外部サービス間の軽量な情報統合アーキテクチャの好例

## 原文リンク

[Hugging Face Daily Papersページの機能完全ガイド](https://huggingface.co/blog/daily-papers)
