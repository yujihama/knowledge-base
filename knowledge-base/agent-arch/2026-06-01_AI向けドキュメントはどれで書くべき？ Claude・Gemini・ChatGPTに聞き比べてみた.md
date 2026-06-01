---
title: "AI向けドキュメントはどれで書くべき？ Claude・Gemini・ChatGPTに聞き比べてみた"
url: "https://zenn.dev/shomitei/articles/ai-doc-format-3models"
date: 2026-06-01
tags: [Markdown, XML, JSON, プロンプトエンジニアリング, MCP, RAG, Structured Outputs, llms.txt, Agent間通信, トークン効率]
category: "agent-arch"
related: [6605, 7003, 3514, 5913, 4520]
memo: "[Zenn LLM] AI向けドキュメントはどれで書くべき？ Claude・Gemini・ChatGPTに聞き比べてみた"
processed_at: "2026-06-01T09:02:44.601618"
---

## 要約

LLMに渡すドキュメントのフォーマットとして、Markdown・XML・JSON・HTMLの4種を比較検討した記事。3つのAIモデル（Claude、Gemini、ChatGPT）に同じ質問を投げ、各社の設計思想が回答に反映されている点を考察している。

4フォーマットの役割分担はレイヤーで整理される。プロンプト構造層（境界・役割定義）にXML、コンテンツ層（人間も読む本文）にMarkdown、データ層（構造化・スキーマ付きデータ）にJSON、Web取り込みの一次形式としてHTMLを使い、最終的にMDへ変換するのが現実解とされる。MarkdownはトークンコストがHTMLの20〜30%削減できるという報告があり、RAGソースやCLAUDE.md・AGENTS.md等の指示書にほぼ標準的に採用されている。XMLはClaudeの訓練データに含まれており、Anthropic公式もタグ構造（`<document>`, `<instructions>`）を推奨。プロンプトインジェクション対策としても有効。JSONはFunction CallingやTool Use、Agent間通信の実質的な標準であり、OpenAIのStructured Outputs（strict mode）、GoogleのVertex AI response_schema、AnthropicのToolベース強制と、各社とも機械処理にはJSONを中心に据えている。

3モデルの回答比較では、レイヤー分けとAgent間通信のJSON本命については全モデルが一致。ただしXMLへの肯定度はClaude＞ChatGPT＞Geminiの順で、ClaudeはXMLの訓練データ親和性から推奨、GeminiはMarkdownの区切りだけで十分（長コンテキスト前提）と主張、ChatGPTはClaudeの影響でXML利用者増加を予測するという三者三様の立場を示した。将来予測では「MarkdownとJSONの二極化」で一致したが、XMLの扱いのみ見解が分かれた。

実プロジェクト規模別の推奨は、小規模では`ai-context.md`1枚のMarkdownのみ、中規模ではMarkdown＋JSON（設計思想はMD、厳密データはschema/*.json）、複数AgentではプロンプトにMarkdown、境界制御にXML、Agent通信にJSONの組み合わせ。「MD一本完結」も「全部XML/JSON」も過剰であり、レイヤーに合わせて使い分けることが結論。

監査エージェント開発への示唆として、LangGraphなどのエージェントフレームワークにおいてツール呼び出し定義にはJSON Schema、システムプロンプトにはMarkdownまたはXML、Agent間通信にはJSONという設計方針はそのまま適用可能。特にClaudeをジャッジや推論エンジンとして使う場合、システム指示をXMLタグで囲む手法はプロンプトインジェクション対策としても機能するため、マルチエージェント構成での入力境界設計に活用できる。

## アイデア

- AIモデルへの質問に対して「誰が」答えているかで回答が変わる点—ClaudeはXMLを推し、GeminiはMarkdownで十分と言い、ChatGPTは中庸路線をとるという、訓練方針と設計思想がそのまま出力に反映される現象
- HTMLをMarkdownに変換するだけでトークン消費が20〜30%削減できるという定量的知見—RAGパイプラインのコスト最適化における前処理設計の重要性
- llms.txt（2024年提唱、Jeremy Howard）という新標準—サイトルートにMarkdownファイルを置いてAIにサイト地図を渡す発想で、2026年時点ではAnthropicとPerplexityが対応表明済みだが主要プラットフォームの正式採用はまだ

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Function Calling / Tool Use** (TODO: 読むべき)
- **JSON Schema** → /deep_6556 RustでLLMコードレビューエージェントを作った
- **Model Context Protocol (MCP)** (TODO: 読むべき)
- **Structured Outputs** → /deep_6485 LLMワークフローにおける決定論という罠

## 関連記事

- /deep_6605 AI入力フォーマット完全ガイド: Markdownを起点にXML/JSON/YAMLをタスク別に切り替える
- /deep_7003 ファインチューニングの前に、まず汎用AIにつなぐ時代になってきたのか
- /deep_3514 AIとAIをつなぐ意味のパイプライン設計：会話ではなく、正典・制約・実ファイルで状態を継承する
- /deep_5913 視覚化された哲学者の思考から問いに繋げるアプリを作ってみた
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[AI向けドキュメントはどれで書くべき？ Claude・Gemini・ChatGPTに聞き比べてみた](https://zenn.dev/shomitei/articles/ai-doc-format-3models)
