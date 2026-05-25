---
title: "prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先"
url: "https://zenn.dev/biscuit/articles/llm-engineering-layers-bottleneck-shift"
date: 2026-05-25
tags: [LLM-engineering, harness, context-engineering, prompt-engineering, ReAct, LLM-as-judge, eval, governance, A2A, RAG]
category: "agent-arch"
related: [5472, 6276, 112, 2563, 1247]
memo: "[Zenn LLM] prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先"
processed_at: "2026-05-25T09:05:28.655701"
---

## 要約

LLM engineeringの進化を「ボトルネックの外側への移動」というメタ法則で整理した考察記事。4つのエンジニアリング層を系譜として読む。

【prompt engineering】GPT-3のfew-shot learningやChain-of-Thought（CoT）が代表技法。しかしWharton GenAI Labsの調査でreasoning model（o3-mini、o4-mini）へのCoT追加は大幅な時間コスト増の割に改善が限定的と報告。Khanの"Prompting Inversion"研究では、gpt-4oで有効だったSculpting技法がgpt-5では逆効果（94% vs standard CoT 96%）になる現象を定式化。モデルの能力向上で入力の言い回しへの依存度が低下した。

【context engineering】コンテキストウィンドウが100万トークン規模に拡大しても、情報を詰め込むと性能が落ちる。Microsoft/Salesforceの共同研究でマルチターン会話で平均-39%の性能劣化、o3でさえ98.1%→64.1%に低下。Anthropicは2025年9月にcontext engineeringを「推論時の最適なトークン集合を選別・維持する戦略群」と定義し、Compaction・Structured note-taking・Sub-agent architecturesの3技法を提示。RAGやContext pruningもコミュニティ技法として定着。

【agent engineering】ReAct（Reasoning+Acting交互ループ）が基本形となり、OpenAI Assistants APIやAnthropic tool use APIで標準化。observe→think→actの自律ループ設計が中心課題となった。

【harness engineering】Philipp Schmid（HuggingFace/Google DeepMind）がModel=CPU、Context Window=RAM、Agent Harness=OS、Agent=Applicationという比喩を提示。Böckelerはharness構成要素をGuides/Sensors×Computational/Inferentialの4象限で分類。Harvey（リーガルAI）はモデル変更なしでharness改修のみで精度を大幅向上、Legal Agent Benchmark（LAB）として1200以上のタスク・24法務領域をOSS化。OpenAI Codexチームは5ヶ月で100万行超・約10億トークン消費、エンジニアの役割が「コードを書く」から「環境設計・意図の明文化・フィードバックループ構築」に移行。

【次のボトルネック：eval と governance】Anthropic Claude Managed AgentsやLangGraph PlatformなどPaaS化でharnessがcommodity化しつつある。次の焦点は(1)eval：Galileoが「Eval Engineering」としてCI/CDへの統合を推進、Amazon Bedrock AgentCoreはOpenTelemetry連携でLLM-as-a-Judgeを実装。LLM-as-a-Judgeのposition bias/length bias等の再帰的問題も顕在化。(2)governance：Graviteeの調査（919人）でA2A通信にfull visibilityを持つ組織はわずか24.4%、エージェントidentity管理・監査ログ・権限動的制御が未解決。監査エージェント開発への示唆：eval設計とA2A通信の可視化・権限管理は、内部統制・GRC文脈での監査エージェント設計において特に重要な要素となる。

## アイデア

- Prompting Inversionの概念：モデルが賢くなるほど精緻なprompt技法が逆効果になる現象は、監査エージェント設計においてプロンプト過剰設計のリスクとして直接応用できる
- Böckelerの4象限（Guides/Sensors×Computational/Inferential）はharness設計の分業フレームワークとして実用的。監査エージェントのコントロール設計に転用可能
- eval自体のバイアス（position bias、length bias）という再帰問題：LLM-as-judgeで監査エージェントの出力品質を評価する際、judge自体の信頼性検証が必要になるという構造的課題

## 前提知識

- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **Chain-of-Thought** → /deep_59 EcoThink: 持続可能でアクセスしやすいエージェントのためのグリーン適応的推論フレームワーク
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **OpenTelemetry** → /deep_1349 ALTK-Evolve: AIエージェントのオンザジョブ学習システム

## 関連記事

- /deep_5472 LLMエンジニアとして最初の3ヶ月に何をするべきか：ロードマップと優先順位
- /deep_6276 製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_2563 文字通りの要約を超えて：医療SOAPノート評価におけるハルシネーションの再定義
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷

## 原文リンク

[prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先](https://zenn.dev/biscuit/articles/llm-engineering-layers-bottleneck-shift)
