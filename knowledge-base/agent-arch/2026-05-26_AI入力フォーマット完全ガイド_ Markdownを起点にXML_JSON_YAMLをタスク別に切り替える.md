---
title: "AI入力フォーマット完全ガイド: Markdownを起点にXML/JSON/YAMLをタスク別に切り替える"
url: "https://zenn.dev/motowo/articles/ai-prompt-markup-markdown-xml-json-yaml"
date: 2026-05-26
tags: [prompt-engineering, Claude Code, YAML, XML, JSON, Markdown, format-tax, プロンプトインジェクション, RAG, マルチエージェント]
category: "agent-arch"
related: [4520, 1045, 3638, 6070, 2821]
memo: "[Zenn LLM] AI 入力フォーマット完全ガイド: Markdown を起点に XML/JSON/YAML をタスク別に切り替える"
processed_at: "2026-05-26T21:03:44.660752"
---

## 要約

Claude Codeのマルチエージェント環境（.claude/agents/に13体構成）での実運用経験をもとに、LLMへの入力フォーマット（Markdown/XML/JSON/YAML/TOON/CSV）の選択戦略を体系化した記事。

LLMの推論精度は「構文ノイズの少なさ」「学習データ上の出現頻度」「フォーマット制約による思考阻害（format tax）」の3軸で決まる。トークン量の比較ではMarkdownはJSON比で34〜38%少なく、XMLはMarkdown比で80%多い。EMNLP 2024の論文「Let Me Speak Freely?」によると、JSON-mode強制でClaude-3-HaikuはGSM8Kで86.51%→23.44%（-63.07pt）と大幅に精度が低下する。

タスク別の最適フォーマット選択指針は以下の通り:
- **Markdown**: RAG・ナレッジベース・長文ガイドライン。LangChainのMarkdownHeaderTextSplitterで見出し境界をチャンキングに活用できる
- **YAML**: 3階層以上の深いネスト推論。Improving Agentsの独立ベンチ（1,000問・ネストQA）でGPT-5 NanoはYAML 62.1%/JSON 50.3%（+11.8pt）
- **XML**: プロンプトインジェクション対策・指示と外部入力の境界明示。Anthropic公式も`<untrusted_user_input>`タグによる境界明示を推奨。ただし疑似タグ閉じやEmoji Smuggling（U+FE00〜FE0F）による突破手法も報告されており「確率的減衰」止まり
- **JSON**: Tool Use・API I/Oなど機械連携が必要な場面のみ
- **TOON**: 一様な配列・ログデータ。JSON比-39.9%トークンで精度は同等だが、仕様v3.3 Working Draftの個人プロジェクトで標準化未完了

HTML→Markdown変換によるトークン80〜90%削減（Microsoft MarkItDown利用）も重要な最適化手法として言及。監査エージェント開発への示唆として、エージェントへの指示はYAML（設定・依存関係の記述）とXML（外部入力の境界明示）を組み合わせ、Tool Use出力はJSONで受け取る設計が合理的。

## アイデア

- JSON強制（Constrained Decoding）でClaude-3-HaikuのGSM8K精度が86.51%→23.44%に激減するという実測値は、監査エージェントの出力設計において推論精度を犠牲にしないフォーマット選択が不可欠であることを示している
- XMLタグによるプロンプトインジェクション対策は「完全防御」ではなく「確率的減衰」であり、</untrusted_user_input>の偽閉じタグやEmoji Smuggling（不可視文字埋め込み）で突破される手法が存在する——アプリ側サニタイズとの多層防御が前提
- YAMLのネストQA精度がJSONより11.8pt高い（GPT-5 Nano: 62.1% vs 50.3%）という結果は、LangGraphの複雑なエージェント設定ファイルやReActのthought/action/observationサイクルの記述をYAMLで行う設計根拠になる

## 前提知識

- **Constrained Decoding** → /deep_4869 NeocorRAG：証拠チェーンによる無関連情報の削減・明示的根拠の強化・効果的な想起の実現
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **Tool Use** → /deep_3094 LLMに図面情報を全部見せる設計をやめた話
- **LangChain** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術

## 関連記事

- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_3638 NIM + Docker ではじめる NeMo Agent Toolkit ハンズオン
- /deep_6070 AIに人格をロードする ── 記憶と人格を分離する設計思想
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話

## 原文リンク

[AI入力フォーマット完全ガイド: Markdownを起点にXML/JSON/YAMLをタスク別に切り替える](https://zenn.dev/motowo/articles/ai-prompt-markup-markdown-xml-json-yaml)
