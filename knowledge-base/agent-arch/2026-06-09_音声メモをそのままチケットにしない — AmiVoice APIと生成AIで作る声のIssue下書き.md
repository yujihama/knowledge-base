---
title: "音声メモをそのままチケットにしない — AmiVoice APIと生成AIで作る声のIssue下書き"
url: "https://zenn.dev/tp_li/articles/60f290eef01fb4"
date: 2026-06-09
tags: [AmiVoice, 音声認識, WebSocket, LLM, Issue自動生成, TypeScript, PCM, プロンプト設計]
category: "agent-arch"
related: [6838, 3095, 7176, 7834, 3512]
memo: "[Zenn LLM] 音声メモをそのままチケットにしない。AmiVoice APIと生成AIで作る声のIssue下書き"
processed_at: "2026-06-09T21:05:29.534166"
---

## 要約

音声入力の活用は文字起こしで止まりがちだが、本記事は「話したことをGitHub IssueやJiraの下書きに近い形まで整形する」小ツール「Voice Issue Draft」の設計・実装を解説する。

アーキテクチャの核心は役割分担にある。AmiVoice API（WebSocket）が音声をリアルタイムにテキスト化し、確定した発話のみをLLMへ渡す。LLMは title / summary / reproductionSteps / implementationHint / questions / sourceQuotes / confidence をJSON形式で返す。最終登録は必ず人間が確認してから行う。

音声認識の途中結果（Uイベント）はUIリアルタイム表示に使い、確定結果（Aイベント）だけをLLMの入力とする。これにより「途中の揺れた文をLLMが補完してしまう」問題を回避する。LLMへ渡す前段で信頼度・発話時刻・単語情報が取れるAmiVoiceのJSON出力を活用し、信頼度が低い部分はquestions欄へ回す設計が可能。

オーディオフォーマットはブラウザで生成したヘッダなし16kHz/16bit/リトルエンディアンPCMに合わせてLSB16Kを指定する。WAVヘッダありの16Kと混同しないよう注意が必要。

認識エンジンは用途別に使い分ける。新規利用ではEnd to Endの-a2-ja-generalを最初に試し、口述筆記用途なら-a-general-input、会議・雑談に近い場合は-a-general、バッチ処理は-a2b-ja-generalが推奨される。固有名詞・画面名・英数字の崩れが多い場合はユーザー辞書や単語強調を追加する。

バックエンド（Node.js + ws + dotenv）はAPIキー保持とLLMへの転送を担い、ブラウザは録音とレビューに専念する構成にする。sコマンドで認識開始、pコマンドで音声チャンク送信、eコマンドで終了するAmiVoice WebSocketプロトコルをTypeScriptでラップし、アプリ本体から切り離したamivoice-session.tsモジュールとして実装する。

sentence生成AIへの指示では「要約」ではなく「Issue下書き」を出力先として明示し、sourceQuotesフィールドに認識原文を必ず残すことで、LLMの補完と実際の発話内容を後から区別できるようにする。confidenceフィールドは「high/medium/low」の3値でLLMが自己評価し、レビュー優先度の判断に使う。

監査エージェント開発への示唆：監査手続きや指摘事項を音声で素早くメモし、確認項目・根拠・未確認事項が構造化された状態で出力される本パターンは、フィールド監査での記録作成に直接応用できる。音声→構造化JSONの変換パイプラインはLangGraphのノードとして組み込みやすく、ReActループでの証跡収集自動化にも転用可能。

## アイデア

- 音声認識の途中結果（partial）はUI表示専用、確定結果（final）だけをLLMへ渡すことでLLMの誤補完リスクを構造的に排除している
- LLMへの出力フォーマットをIssue下書きJSONに固定し、sourceQuotesで原文を保持することで「LLMが作った情報」と「人間が話した情報」を常に追跡可能にしている
- AmiVoiceのJSON出力（信頼度・発話時刻・単語単位情報）を前段で活用することで、後段LLMへの入力品質を高める2段階パイプライン設計

## 前提知識

- **WebSocket** → /deep_3238 Gemini Live APIを用いてAI架電アプリを作ってみた
- **音声PCMフォーマット** (TODO: 読むべき)
- **LLMプロンプト設計** → /deep_4901 アコーディオンパターン：巨大な単一LLMプロンプトをやめた理由と2段階分割アーキテクチャ
- **AmiVoice API** → /deep_7176 AmiVoice APIとLLMで作る声の公開レビューゲート
- **TypeScript** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説

## 関連記事

- /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_7176 AmiVoice APIとLLMで作る声の公開レビューゲート
- /deep_7834 AmiVoice API × LLMで採用面接の録音から構造化メモを自動生成してみた
- /deep_3512 50のフレームワークを物語に統合する — Learning Journeyシステムの設計

## 原文リンク

[音声メモをそのままチケットにしない — AmiVoice APIと生成AIで作る声のIssue下書き](https://zenn.dev/tp_li/articles/60f290eef01fb4)
