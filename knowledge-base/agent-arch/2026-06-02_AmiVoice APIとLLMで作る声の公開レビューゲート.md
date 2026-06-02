---
title: "AmiVoice APIとLLMで作る声の公開レビューゲート"
url: "https://zenn.dev/yushiyamamoto/articles/amivoice-publish-gate"
date: 2026-06-02
tags: [AmiVoice, 音声認識, LLM, publish_gate, Node.js, 構造化出力, confidence補正, ワークフロー制御]
category: "agent-arch"
related: [6838, 4900, 6350, 6928, 7068]
memo: "[Zenn LLM] AmiVoice APIとLLMで作る声の公開レビューゲート"
processed_at: "2026-06-02T09:03:06.052976"
---

## 要約

AmiVoice API（日本語音声認識）とLLM（OpenAI API）を組み合わせ、音声入力をそのまま要約するのではなく、公開・送信・本番反映前の安全装置として機能させる仕組みの実装記事。音声を5分類（decision/todo/risk/blocker/publish_gate）に構造化し、特に`publish_gate.should_stop_publish: true/false`として公開判定を機械可読な形式で出力する点が核心。

技術的な流れは3段階：①AmiVoice APIへWAV音声（16kHz/16bit/mono）をPOSTして文字起こし取得、②AmiVoiceのレスポンスJSONからtextとtokensのconfidenceを抽出してLLMへ渡す、③LLMが構造化JSONを返し、publish_gateフィールドで公開可否を判定する。

実音声（WhatsAppから書き出した.opusをffmpegでWAV変換）を用いた検証では、overall confidence 0.9906と高精度だったが「Zenn記事→前記事」「コードブロック→京都コードブロック」「人間レビュー→人間レベル」「TODO→ツール」などの固有名詞・英略語の誤認識が発生。これをLLMだけで補正しようとすると誤認識をそのまま採用してしまう問題があった。

改善策として、AmiVoiceのtokensからconfidence < 0.9の単語を抽出して低信頼トークンリストを作成し、ドメイン語彙（Zenn,TODO,表,コードブロック,人間レビュー,publish_gate）とともにLLMのコンテキストに渡す。実装では「きょうと」(confidence 0.79)、「れべる」(0.74)、「つーる」(0.37)を低信頼として渡すことで、LLMが「京都コードブロック→コードブロック」「人間レベル→人間レビュー」に補正し、corrected_transcriptと補正ログ（original/corrected/reason）を構造化出力できた。

Node.jsスクリプト（amivoice-classify.mjs）は`--file`でAmiVoice JSON、`--text`で平文、`--domain-terms`でドメイン語彙を受け取るCLIとして設計。さらに`amivoice-gate-contract-check.mjs`でゲートの契約テスト（「まだ公開しない」音声が必ず止まるか、確認済み音声を止めすぎないか）を固定ケースで毎回確認できる仕組みも提供。

監査エージェント開発への示唆：本記事の「publish_gate」パターンは、監査ワークフローにおける承認ゲート（例：調書の確定前チェック、証跡の送付前バリデーション）に直接応用できる。音声入力→構造化判定→ゲート制御というパイプラインは、LLM-as-judgeを安全装置として組み込むアーキテクチャの具体的実装例であり、ReActエージェントのアクション実行前チェックとしても流用可能。

## アイデア

- 音声認識の誤認識をLLMで補正する際、テキストだけ渡すのではなくtokensのconfidenceスコアと音素読みを低信頼リストとして明示的に渡す設計が効果的。LLMは文脈推論が得意だが、何が誤認識かのヒントがないと誤認識をそのまま事実として扱う
- 要約ではなく「publish_gate」という独立フィールドで公開可否を機械可読に構造化する発想。LLMの出力をそのまま人間が読む用途ではなく、後段の自動化パイプラインで条件分岐するための制御シグナルとして使う設計思想
- 契約テスト（amivoice-gate-contract-check.mjs）でLLMの判定品質を固定ケースで継続検証する手法。LLMの出力は非決定的なため、「止まるべきケース/止めすぎないケース」を明文化してCIのように毎回回すことで運用品質を担保する

## 前提知識

- **AmiVoice API** → /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- **音声認識confidence** (TODO: 読むべき)
- **LLM構造化出力** (TODO: 読むべき)
- **JSON Schema** → /deep_6556 RustでLLMコードレビューエージェントを作った
- **ffmpeg** → /deep_1304 AI WebTV：テキスト・トゥ・ビデオモデルを使ったリアルタイムストリーミングシステムの構築

## 関連記事

- /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_6350 SDS文書とMHLW標準JSONを双方向変換するRust製CLIツール「sds-converter」
- /deep_6928 AmiVoice業界特化エンジンvs汎用エンジン：4ドメイン実測で見えた「使い分けの線」
- /deep_7068 AmiVoiceとLLMで音声情報を取得・要約する実装ガイド（Next.js BFF構成）

## 原文リンク

[AmiVoice APIとLLMで作る声の公開レビューゲート](https://zenn.dev/yushiyamamoto/articles/amivoice-publish-gate)
