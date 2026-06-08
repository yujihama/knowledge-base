---
title: "AmiVoice API × LLMで採用面接の録音から構造化メモを自動生成してみた"
url: "https://zenn.dev/fsgesaiyo/articles/a00bf5180b86e0"
date: 2026-06-08
tags: [AmiVoice, 音声認識, 構造化出力, TypeScript, zod, OpenAI互換API, CLIツール, 面接メモ自動化]
category: "agent-arch"
related: [7068, 7176, 6838, 7596, 3903]
memo: "[Zenn LLM] AmiVoice API × LLMで採用面接の録音から構造化メモを自動生成してみた"
processed_at: "2026-06-08T21:03:02.082935"
---

## 要約

採用面接の録音音声をAmiVoice API（日本語特化の音声認識サービス）で文字起こしし、その結果をLLMに渡して構造化した面接メモを自動生成するCLIツールの実装記事。技術スタックはNode.js 20系 + TypeScript 5系。

処理フローは、(1) 音声ファイルをAmiVoice APIの同期HTTPインタフェース（`https://acp-api.amivoice.com/v1/recognize`）にFormDataで送信、(2) レスポンスのトップレベル`text`フィールドを取得、(3) そのテキストをOpenAI互換のChat Completions API形式でLLMに送信し、temperature=0.2で低温生成、(4) JSON出力をzodスキーマ（`InterviewNoteSchema`）でバリデーション、(5) JSONとMarkdownの2形式でファイル出力（`output/interview-note.json`、`output/interview-note.md`）——という構成。

LLMに渡すプロンプトでは「文字起こしに存在しない情報は推測せず不明とする」「合否判定しない」「懸念点は発言根拠とセットで出す」という制約を明示し、幻覚（ハルシネーション）を抑制している。出力スキーマは`candidateSummary`、`experienceSkills`（配列）、`careerReason`、`desiredConditions`（配列）、`concerns`（point/evidence/nextCheckの構造体配列）、`nextInterviewQuestions`（配列）、`handoffMemo`、`unknowns`（配列）の8フィールド。

長時間音声への対応として、非同期HTTPインタフェースや話者分離の検討が必要と明記。APIキーは`.env`管理、LLM_API_URLを環境変数で切り替えることでOpenAI互換の任意LLMエンドポイントに対応できる設計。

監査AI・エージェント開発への示唆として、この構成（専用APIで入力を正規化→LLMで業務ロジックに沿って構造化→zodでスキーマ検証）は監査エージェントにおける証跡音声・会議録の自動要約・リスク抽出パイプラインに直接応用可能。特にzodによる出力スキーマ強制とプロンプトでの根拠付き懸念点出力の設計パターンは、監査調書の自動生成における事実と推論の分離要件に適合する。

## アイデア

- 音声認識とLLMの役割を明確に分離（AmiVoice=文字起こし専用、LLM=業務ロジック整理）することで、各コンポーネントを独立して差し替え可能な設計になっている
- zodスキーマによるLLM出力のバリデーションで、JSON構造の不正・欠損フィールドを実行時に検出する堅牢なパイプラインを実現している
- プロンプトに「根拠付き懸念点」「不明点の明示」を強制することで、LLMの幻覚を業務上安全なレベルに抑制するパターンは、監査調書や法的文書の自動生成にも応用できる

## 前提知識

- **AmiVoice API** → /deep_7176 AmiVoice APIとLLMで作る声の公開レビューゲート
- **Chat Completions API** (TODO: 読むべき)
- **zod** → /deep_1911 2026年、現場エンジニアが押さえておくべきAI技術トレンド5選
- **FormData** (TODO: 読むべき)
- **TypeScript** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説

## 関連記事

- /deep_7068 AmiVoiceとLLMで音声情報を取得・要約する実装ガイド（Next.js BFF構成）
- /deep_7176 AmiVoice APIとLLMで作る声の公開レビューゲート
- /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- /deep_7596 Pi Agent SDKを触ってみたメモ：LM Studio連携とカスタムプロバイダ実装
- /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた

## 原文リンク

[AmiVoice API × LLMで採用面接の録音から構造化メモを自動生成してみた](https://zenn.dev/fsgesaiyo/articles/a00bf5180b86e0)
