---
title: "Claude Codeを自律エージェント基盤として運用する — context rotから逆算する設計"
url: "https://zenn.dev/yutabeee/articles/claude-code-autonomous-agent-platform"
date: 2026-06-06
tags: [Claude Code, コンテキストウィンドウ, Hooks, サブエージェント, Dynamic Workflows, CLAUDE.md, 自律エージェント, Auto Memory, PreToolUse, コスト管理]
category: "agent-arch"
related: [2961, 2055, 6004, 5029, 5970]
memo: "[Zenn LLM] Claude Codeを自律エージェント基盤として運用する — context rotから逆算する設計"
processed_at: "2026-06-06T21:16:31.168489"
---

## 要約

Claude Codeを「補完ツール」ではなく「自律エージェント基盤」として運用するための設計論。すべての問題（CLAUDE.mdが守られない・セッション後半で精度が落ちる・コストが急増する）は「コンテキストウィンドウは有限で収穫逓減する」という1つの制約に起因する。

**CLAUDE.md設計**: 公式推奨は1ファイル200行未満。CLAUDE.mdはシステムプロンプトではなく「ユーザーメッセージとして後注入」されるため、遵守は確率的にしかならない。長くなると指示が埋もれる。削除基準は「その行を削ったらClaudeが間違えるか」のみ。トークン節約には @importではなくjust-in-time取得（glob/grep）やAuto Memory（MEMORY.md先頭200行/25KB）を活用する。

**Hooks設計**: CLAUDE.mdの指示はadvisory（確率的）、HooksはCI相当のdeterministic（決定論的）な強制力を持つ。PreToolUseのexit 2でツール実行をブロックし、stderrがClaudeへのフィードバックになる。最小安全装置は「.envの保護」と「rm -rfのブロック」の2本。PostToolUseでEdit/Writeにマッチさせ自動Prettier整形も実装できる。SessionStartフックでgitブランチ・差分・GitHub Issueをコンテキストへ自動注入可能。

**並列化の選択軸**: 「中間結果（計画）をどこに保持するか」が唯一の判断基準。単発はメインコンテキスト、2〜4本の比較はサブエージェント（隔離コンテキスト）、相互依存タスクはAgent Teams（共有タスクリスト）、10本以上のファンアウトはDynamic Workflows（スクリプト変数に外部化）と使い分ける。サブエージェントはネスト不可で、Dynamic Workflowsは同時16エージェント/総計1,000が上限。

**コスト管理**: 2026年6月15日からclaudeのプログラム的利用（-p/Agent SDK/GitHub Actions）は対話的利用と別クレジット枠で課金される。サブエージェントのモデルをHaiku/Sonnetに落とすコスト階層化、/compactとmax_turns制御による暴走防止、並列数の絞り込みが必要。

監査エージェント開発への示唆: HooksのPreToolUse/PostToolUse構造はLangGraphのノード前後処理と同概念。「advisory指示 vs deterministic強制」の分離は監査チェックリストの必須項目・推奨項目の区別と対応する。Dynamic Workflowsの計画外部化は、LangGraphのstate管理をエージェント間で共有するパターンそのもの。

## アイデア

- CLAUDE.mdはシステムプロンプトではなくユーザーメッセージとして後注入されるため遵守が確率的になるという構造的制約——「守られない理由」が実装レベルで説明される
- 並列化の選択基準を「計画をどこに保持するか」という1軸に還元することで、新機能が出ても位置づけが即判断できる設計思想
- HooksのPreToolUse/PostToolUseを「CI相当の決定論的強制」として使うことで、LLMのハルシネーションが入り込めない安全境界をコード層で実現する発想

## 前提知識

- **コンテキストウィンドウ** → /deep_1422 一時的な閉世界——コンテキストウィンドウとSmalltalkの50年
- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **サブエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Hooks（Claude Code）** (TODO: 読むべき)

## 関連記事

- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_2055 Claude Codeのトークン消費を半分にする——800時間の運用データから見つけた実践テクニック
- /deep_6004 Claude Codeで大規模コードベースを扱うベストプラクティス
- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間

## 原文リンク

[Claude Codeを自律エージェント基盤として運用する — context rotから逆算する設計](https://zenn.dev/yutabeee/articles/claude-code-autonomous-agent-platform)
