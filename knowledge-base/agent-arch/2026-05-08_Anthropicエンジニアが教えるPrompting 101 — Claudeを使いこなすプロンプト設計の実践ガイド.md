---
title: "Anthropicエンジニアが教えるPrompting 101 — Claudeを使いこなすプロンプト設計の実践ガイド"
url: "https://zenn.dev/bokuno_log/articles/anthropic-prompting-101"
date: 2026-05-08
tags: [prompt-engineering, Claude, Anthropic, XML-tags, few-shot, pre-fill, extended-thinking, structured-output, prompt-caching, system-prompt]
category: "agent-arch"
related: [2958, 593, 1407, 1679, 1629]
memo: "[Zenn LLM] Anthropic エンジニアが教える Prompting 101 — Claude を使いこなすプロンプト設計の実践ガイド"
processed_at: "2026-05-08T21:33:59.162328"
---

## 要約

AnthropicのApplied AIチームのHannah MoranとChristian Ryanが、プロンプトエンジニアリングのベストプラクティスを実際のコンソールデモを交えて解説したセッションの書き起こし。題材はスウェーデン語の自動車事故報告書（17項目チェックボックス＋手書きスケッチ）から過失車両を判定するシステムで、V1〜V5の5段階でプロンプトを段階的に改善していく過程が示される。

Anthropicが推奨するプロンプトの基本構造は①タスク説明、②動的コンテンツ、③詳細な手順、④例示（Few-shot）、⑤重要事項の再掲の5要素。情報整理にはXMLタグを推奨し、Markdownより境界が明確でトークン効率が良いとされる。

V1では背景情報ゼロのため「Chapman Gotham通りでスキー事故が発生した」という誤認出力。V2でタスクコンテキスト（自動車保険クレーム処理システム、スウェーデン語フォームという背景）とトーン（確信がない場合は判定しない）を追加し、車の事故として認識するようになった。V3ではフォームの構造情報（2列構成、左右が車両A・B、各行の意味）をシステムプロンプトに記述し、「車両Bが過失」という明確な判定が初めて得られた。V4では処理順序を明示的に指定——「まずフォームを丁寧に読んでチェック済みボックスをリストアップし、その後スケッチを分析する」という人間の作業順序を再現することで分析精度が向上。V5では出力フォーマットを`<final_verdict>`タグで指定し、アプリケーションが必要な情報だけをパースできる構造化出力を実現した。

追加テクニックとして、Pre-fill（Assistantロールに出力開始文字列を設定することでJSONや特定タグから出力を強制）、Extended Thinking（Claude 3.7以降でthinkingタグに推論過程を出力、デバッグやシステムプロンプト改善に活用）、Few-shot例示（Base64エンコード画像を含む実ケースを数十〜数百件追加可能）が紹介される。プロンプトキャッシングは静的なシステムプロンプト情報に適用するとコスト効率が高い。監査エージェント開発において、チェックボックス形式の構造化文書（例：内部統制チェックリスト）を処理する際に処理順序の明示とXMLタグによる出力構造化が直接応用できる。

## アイデア

- 処理順序の明示が精度を左右する：スケッチより先にフォームを読む指示が、人間の認知順序を再現し判定精度を向上させた点は、複数ドキュメントを扱う監査エージェント設計にそのまま転用できる
- XMLタグによる出力の構造化がアプリ統合コストを下げる：`<final_verdict>`タグで囲むだけで後続システムが必要な情報だけをパースできるようになり、LLM出力とシステム統合の境界設計として汎用性が高い
- Extended Thinkingをデバッグツールとして使い、思考過程をシステムプロンプトの指示に落とし込むことでトークン効率を維持しながら同等品質を達成できるという逆算的アプローチ

## 前提知識

- **System Prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **Few-shot learning** → /deep_189 EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合
- **Prompt caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- **Extended Thinking** → /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- **XML tags** (TODO: 読むべき)

## 関連記事

- /deep_2958 なぜOpus 4.7は「禁止ルール」を削ったのか：Claude system prompt 4.6→4.7の差分分析
- /deep_593 国防総省のAnthropicに対するカルチャーウォー戦術は裏目に出た
- /deep_1407 ペンタゴンのAnthropicへのカルチャー戦争戦術は裏目に出た
- /deep_1679 ペンタゴンのAnthropicへのカルチャーウォー戦術は裏目に出た
- /deep_1629 ペンタゴンのAnthropicへの「文化戦争」戦術は裏目に出た

## 原文リンク

[Anthropicエンジニアが教えるPrompting 101 — Claudeを使いこなすプロンプト設計の実践ガイド](https://zenn.dev/bokuno_log/articles/anthropic-prompting-101)
