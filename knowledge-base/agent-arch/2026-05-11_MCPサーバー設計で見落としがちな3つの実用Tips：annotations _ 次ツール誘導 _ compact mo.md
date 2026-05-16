---
title: "MCPサーバー設計で見落としがちな3つの実用Tips：annotations / 次ツール誘導 / compact mode"
url: "https://zenn.dev/kanseilink/articles/kanseilink-mcp-builder-tips-20260428"
date: 2026-05-11
tags: [MCP, MCPサーバー設計, annotations, エージェントフレンドリー, TypeScript, トークン最適化, マルチステップワークフロー]
category: "agent-arch"
related: [430, 2365, 2405, 3898, 2953]
memo: "[Zenn LLM] MCPサーバー設計で見落としがちな3つの実用Tips：annotations / 次ツール誘導 / compact mode"
processed_at: "2026-05-11T12:00:32.684130"
---

## 要約

156サービス・21ツールのMCPインテリジェンスレイヤー「KanseiLink」の運用から得た、エージェントフレンドリーなMCPサーバー設計の3つの実践的Tipsを紹介する記事。

Tip1はannotationsの明示的な設定。registerToolの第2引数にannotationsフィールドを渡すことで、エージェントがツール呼び出しの安全性を判断できるようになる。readOnlyHint: trueを設定した読み取り専用ツールはタイムアウト時に安全にリトライ可能と判断され、idempotentHint: falseを持つ書き込み系ツールにはエージェントが慎重に振る舞う。annotationsが未設定だと多くのエージェントは保守的に1回しかツールを呼ばず、本来取得できる情報を逃す。

Tip2はレスポンス内への「次に呼ぶべきツール」の明示的な埋め込み。suggested_next_toolフィールドにtool名・args（service_idなどの具体的な引数値まで）・reason・flow_position（「4ステップ中の2番目」など）を返すことで、エージェントは次のツール呼び出しをそのままコピーして実行できる。引数を省略すると再推論が必要になるが、argsまで埋めることで多段ワークフローの貫通率が体感で大きく向上した。

Tip3はcompactパラメータによるトークン削減。エージェントは1ツール呼び出しごとにレスポンス全文をコンテキストに積むため、冗長なJSONはそのままトークンコストになる。inputSchemaにcompact: z.boolean().optional()を追加し、compact: trueの場合はフィールドを必要最小限（id, name, grade等）に絞り、さらにJSON.stringifyのインデントをゼロにすることで実測50%以上のトークン削減が可能。キー名を1文字に短縮するなど、人間の可読性より圧縮を優先した設計がエージェント向けAPIでは合理的。

3つのTipsはいずれもregisterToolのスキーマ変更かレスポンス側の数行追加で実装可能。エージェント時代のMCPサーバーは「人間が読むREST API」とは設計思想が異なり、再試行安全性・フロー誘導・トークン効率を最優先に設計する必要がある。監査エージェント開発においても、複数ツールの連鎖実行が前提となるReActループのフロー貫通率向上に直接応用できる観点。

## アイデア

- suggested_next_toolでargsまで具体値を埋めて返すことで、エージェントの再推論コストをゼロにしてワークフロー貫通率を高める設計パターンは、LangGraphのedge定義と相補的に使える
- readOnlyHint / idempotentHintのようなセマンティクスヒントをツール側が宣言することで、エージェントのリトライ戦略を暗黙の保守的デフォルトから引き出す仕組みは、APIのべき等性設計と同じ思想
- 人間可読性を犠牲にしてトークン圧縮を優先するcompact modeの設計は、エージェント専用API（Agent API）と人間向けAPIを分離すべきという設計指針の具体的実装例

## 前提知識

- **Model Context Protocol** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **registerTool API** (TODO: 読むべき)
- **Zod スキーマ** (TODO: 読むべき)
- **LLMコンテキスト管理** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2365 kintoneのAPIドキュメントは1ページ53,600トークン — AIエージェントのトークン浪費を実測した
- /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証

## 原文リンク

[MCPサーバー設計で見落としがちな3つの実用Tips：annotations / 次ツール誘導 / compact mode](https://zenn.dev/kanseilink/articles/kanseilink-mcp-builder-tips-20260428)
