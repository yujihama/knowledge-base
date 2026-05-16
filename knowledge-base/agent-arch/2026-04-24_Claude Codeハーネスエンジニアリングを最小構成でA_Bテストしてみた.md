---
title: "Claude Codeハーネスエンジニアリングを最小構成でA/Bテストしてみた"
url: "https://zenn.dev/yohei_data/articles/3900a223fe9378"
date: 2026-04-24
tags: [Claude Code, ハーネスエンジニアリング, PostToolUse Hook, CLAUDE.md, ESLint, TypeScript, A/Bテスト, bigint, ISO 8601, 自己修正ループ]
category: "agent-arch"
related: [2547, 1789, 1788, 94, 2250]
memo: "[Zenn LLM] Claude Codeハーネスエンジニアリングを最小構成でA/Bテストしてみた"
processed_at: "2026-04-24T12:31:38.154397"
---

## 要約

ハーネスエンジニアリングとは、CLAUDE.mdへの「お願い」だけに頼るのではなく、周辺の仕組み（フック・リンター等）でAIの行動を物理的に制約するアプローチ。本記事ではClaude Code（Opus 4.7 xhigh）を使い、「ハーネスなし（baseline）」と「ハーネスあり（harnessed）」の2条件で同一タスク（時給計算関数の実装）を実行し、出力品質を比較検証した。

ハーネスの構成は5層モデルで整理される：①ルール層（CLAUDE.md）、②コンテキスト層（MEMORY.md）、③フック層（PostToolUse Hook）、④スキル層（SKILL.md）、⑤エージェント・MCP層。今回の検証ではルール層とフック層のみを実装した最小構成を採用。

CLAUDE.mdには「金額計算はnumberではなく文字列ベース（浮動小数NG）」「日時はISO 8601文字列で受け渡す」「any型禁止・unknownを使う」「node:fs/promisesを使う」等のルールを記述。.claude/settings.jsonのPostToolUse HookにESLintを仕込み、Edit/Writeツール使用後に自動実行されるよう設定した。

結果として、harnessed側はbaseline比で実装行数が89行→最大261行（約3倍）に増加し、テスト数も13→19〜22件に増加、思考時間も27秒→約4分に延びた。品質面では、金額計算においてbaseline側がnumber（浮動小数）を使ったのに対し、harnessed側はbigintを用いた文字列ベースの精度保証実装を選択。日時処理もnew Date()からISO 8601＋タイムゾーン処理に変化した。また、harnessed側ではエージェントが負の値を許容する正規表現（/^-?\d+$/）を書いた直後に自発的に修正（/^\d+$/）する「自己修正ループ」も観察された。これはCLAUDE.mdの「エッジケース（負の値）を必ずカバー」というルールが影響した可能性が高い。

トレードオフとして、ルール遵守により低レベル関数（parseMoney/formatMoney/divRoundHalfUp等）を自作する実装コストが跳ね上がる点が挙げられ、既存ライブラリ優先の例外ルールを追加する余地がある。また、Opus 4.7は素の状態でも性能が高いため、差異が見えにくく、ハーネスの真価はSonnet/Haikuなど下位モデル使用時・同一タスクの繰り返し実行時・大規模リファクタリング時に顕在化すると考察されている。

実装上のハマりどころとして、pnpm approve-buildsでの誤操作によるブロック、旧仕様の$CLAUDE_FILE_PATHS（現行v2.1.114ではstdin JSONをjqで抽出が正）、/hooksの複数ページ構成、HookコマンドでのCDパス指定の必要性が記録されている。監査エージェント開発への示唆として、エージェントの出力に一貫性・精度・型安全性を要求する場面（例：金額・日時を扱う監査計算ロジック）では、CLAUDE.md＋PostToolUse Hookの組み合わせが有効な品質ガードとして機能する。

## アイデア

- PostToolUse HookでESLintを自動発火させることで、プロンプトによる『お願い』を物理的な強制力に昇格させる構造は、監査エージェントの出力検証（計算精度・型安全性）にそのまま応用可能
- CLAUDE.mdのルールが自己修正ループを誘発する副次効果（負値バリデーションの自発的修正）は、エージェントの自律的な品質向上メカニズムとして興味深く、ReActサイクルへの統合可能性がある
- ハーネスの真価が下位モデル（Sonnet/Haiku）使用時・大規模タスク時に顕在化するという知見は、コスト最適化を図りながら品質を維持する本番設計において、モデル選択とハーネス強度のトレードオフを定量的に評価する必要性を示唆している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **PostToolUse Hook** (TODO: 読むべき)
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **ESLint** (TODO: 読むべき)
- **TypeScript bigint** (TODO: 読むべき)

## 関連記事

- /deep_2547 【Claude Code】コマンドは3つだけ！ハーネスエンジニアリング実践編：log → distill → promote
- /deep_1789 Claude Code 基礎ガイド：AIの全体像からMCP活用まで
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_2250 Karpathyが指摘したLLMコーディングの失敗パターンと、コミュニティが作ったCLAUDE.mdの全貌

## 原文リンク

[Claude Codeハーネスエンジニアリングを最小構成でA/Bテストしてみた](https://zenn.dev/yohei_data/articles/3900a223fe9378)
