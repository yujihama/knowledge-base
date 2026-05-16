---
title: "【実録】GeminiはGoogle自社サービスの夢を見るか？ ―― ハルシネーションの実例・傾向・対策"
url: "https://zenn.dev/minipoisson/articles/gemini-hallucination-google-services"
date: 2026-04-14
tags: [hallucination, Gemini, Google Cloud, Translation API, LLM, パターン補完, プロンプト設計]
category: "ai-ml"
related: [111, 316, 514, 77, 119]
memo: "[Zenn LLM] 【実録】GeminiはGoogle自社サービスの夢を見るか？　―― ハルシネーションの実例・傾向・対策"
processed_at: "2026-04-14T12:25:27.768661"
---

## 要約

GeminiがGoogle自社サービス（Google Cloud Translation API、GAS、NotebookLM）について自信を持って誤情報を提示した実例3件を、実際のログとともに記録・分析した記事。

【実例1: translate_imageメソッドの幻】Google Cloud Translation API v3/v3beta1のTranslationServiceClientに存在しない`translate_image`メソッドをGeminiが生成。実在する`translate_text`・`translate_document`の命名規則から「translate_imageも存在するはず」とパターン補完した結果。エラーを指摘しても「pip upgradeせよ」「v3beta1を使え」「type: ignoreで無視せよ」と誤解決策を連発し、ついには架空のURLを正規URL構造で生成した（cloud.google.com/translate/docs/reference/rest/v3/projects.locations/translateImage など）。GitHub Copilotは即座に「存在しないメソッド」と正確に回答した。

【実例2: GASエディタでTypeScript直接実行】ブラウザ上のGASエディタで.tsファイルを直接実行できると主張。実際にはclaspを使ったローカル環境が必須。誤りを指摘するとユーザーアカウントの「異常な状態」に帰因する応答パターンが見られた。

【実例3: NotebookLMのGoogleグループ共有】個人版NotebookLMでGoogleグループアドレスへの共有が可能と案内。実際には弾かれる（Enterprise版のみ対応）。この件では検証が単純だったため最終的にGeminiが誤りを認めた。

【ハルシネーション発生のメカニズム】LLMは事実の記憶ではなくWebテキストからのパターン補完を行う。命名規則の論理的一貫性、WebUIとAPIの機能混同、画像のtranslate（平行移動）コードの学習データ混入、自社サービスへの好意的バイアスなど複数の要因が重なる。検証が困難なほどハルシネーションが定着しやすい。

【レッドフラグパターン】「〜は存在はします。ただし〜」という構文、バージョン番号や特定リージョンの過剰な具体性、環境・アカウントへの転嫁、全面肯定後の微調整アドバイスの4パターンが特に危険。

【対策】公式ドキュメントURLを要求して実際にアクセス確認する、複数AIでクロスチェック（自社サービスは別AI推奨）、Pylance等の型チェックを活用、「2026年現在の一般公開仕様に基づいて」と時間軸を明示、「できないこと」を先に問うプロンプト設計の5点が有効。監査エージェント開発においてもAPI仕様の確認をLLMのみに依存せず公式ドキュメントを一次情報源とする習慣が必須。

## アイデア

- 命名規則の論理的一貫性（translate_text→translate_document→translate_image）がLLMのパターン補完を強力に誘発するという構造的問題は、APIのメソッド命名設計がハルシネーションリスクに影響することを示唆する
- 「検証難易度」がハルシネーションの定着率を左右するという観察：即時フィードバックが得られる事例は修正されやすく、API仕様のように反証が複雑な場合は誤りが維持されやすい
- 自社サービスについてはその提供元AIより競合AIの方が正確に回答できるケースがあるという逆説：Copilotがコードベースを直接参照してGeminiの誤りを即座に指摘した事実

## 前提知識

- **LLM パターン補完** (TODO: 読むべき)
- **Google Cloud Translation API** (TODO: 読むべき)
- **ハルシネーション** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説

## 関連記事

- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_316 合成データと連合学習によるプライバシー保護型ドメイン適応：モバイルアプリ向けLLM活用事例（Google Gboard）
- /deep_514 レビューから要件へ：LLMは人間のようなユーザーストーリーを生成できるか？
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_119 Groundsource: Geminiを活用してニュース記事をフラッシュフラッド履歴データに変換するフレームワーク

## 原文リンク

[【実録】GeminiはGoogle自社サービスの夢を見るか？ ―― ハルシネーションの実例・傾向・対策](https://zenn.dev/minipoisson/articles/gemini-hallucination-google-services)
