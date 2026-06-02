---
title: "Agentの基本定義：なぜ一文のPromptではないのか？"
url: "https://zenn.dev/lienjack/articles/00-01-agent-not-a-prompt"
date: 2026-06-02
tags: [Agent, ReAct, Harness, LLM Runtime, ツール呼び出し, 状態管理, ループ, Policy Decision]
category: "agent-arch"
related: [2550, 6484, 63, 5311, 5563]
memo: "[Zenn LLM] Agent の基本定義：なぜ一文の Prompt ではないのか？"
processed_at: "2026-06-02T09:07:26.738139"
---

## 要約

本記事は、LLMアプリケーションにおける「Prompt」と「Agent」の本質的な違いを、CLIデバッグアシスタントを例に体系的に整理したエンジニアリング解説記事である。

核心的な主張は「AgentはPromptの延長ではなく、モデル＋ループ＋ツール＋状態によって構成される実行プロセスである」という点だ。一回のLLM呼び出しはテキストを生成できるが、実タスク（例：テスト失敗の修正）には「ファイルを実際に読む」「コマンドを実行する」「結果を次のラウンドへ引き継ぐ」という多段階の前進が必要であり、これはPromptだけでは実現できない。

記事はAgentが解くべき問題の連鎖を明示する：①一回のモデル呼び出しは回答しか生成できない → ②実タスクには多段階の前進が必要 → ③多段階にはループが必要 → ④ループは外部世界に触れるためツールが必要 → ⑤ツール結果は状態として保持する必要がある → ⑥状態・ツール・ループが実環境に触れると、モデル外部の制御システム（Harness）が必要になる。

Agentのエンジニアリング規律として特に強調されるのは、「モデルが言ったこと」「システムがしたこと」「外部世界が返したこと」の三者を明確に区別することだ。モデルが「テストは通りました」と出力しても、それは証拠ではない。証拠はtool_executionイベントの終了コード・stdout/stderrである。この区別を怠ると、AgentはRuntimeではなく「作業報告を書くのがうまいチャット欄」に退化する。

ループ（ReAct的な観測→判断→行動→観測の繰り返し）を実装する際、各ラウンドのイベントは6段階に分解される：Model Event（assistant messageの生成）→ Tool Intent（tool_useブロックの解析）→ Policy Decision（権限・安全性の判定）→ Tool Execution（実行）→ Observation（結果のシリアライズ）→ State Update（messages・workspace・予算記録の更新）。この境界が明確であれば、「Agentが動かない」という曖昧な障害を「Tool IntentのJSON解析失敗」「Policy Decisionによる拒否」「State Updateの欠落」と正確に分類してデバッグできる。

Promptの役割は「生成側の制約」（口調・形式・優先順位）に留まり、事実源の管理・実行権・検証権・ガバナンス権の四つはRuntime＋Harnessが担う。この設計分離こそが、デモでは動くが本番で崩壊するAgentとプロダクションレベルのAgentを分ける根本だと結論づけている。

監査エージェント開発への示唆：証跡（Tool Execution・Observationのイベントログ）をシステムとして記録する設計は、監査AI文脈での「AIが何をしたか」の説明責任に直接対応する。LangGraphでState Updateを構造化し、各ノードのtool_eventを台帳として保持する設計が有効。

## アイデア

- 「モデルが言ったこと」「システムがしたこと」「外部世界が返したこと」の三者区別という台帳モデルは、監査AIにおける操作ログ・証跡設計に直接応用できる
- Agent障害を「モデルが賢くない」と一括りにせず、6段階イベント境界（Model Event→Tool Intent→Policy Decision→Tool Execution→Observation→State Update）で分類することで、デバッグの焦点が明確になる
- Promptは「タスク説明書」、Agent Runtimeは「実行現場」という役割分離の明確化は、システム設計時のPrompt最適化とRuntime最適化のトレードオフ判断基準を提供する

## 前提知識

- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Tool Use / Function Calling** (TODO: 読むべき)
- **LLM Context Window** (TODO: 読むべき)
- **System Prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **State Machine** → /deep_6414 Agent開発における「No disclaimer by design」という考え方

## 関連記事

- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで
- /deep_6484 prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先
- /deep_63 NVIDIAがDGX SparkとReachy Miniでエージェントを現実世界に具現化
- /deep_5311 LLMエージェントはなぜ壊れるのか ——モデル性能に依存しない自律型ワークフローの構築
- /deep_5563 LGSS（ライフサイクル統治型セマンティックシステム）：長期LLM推論の安定化のための制約蓄積モデル

## 原文リンク

[Agentの基本定義：なぜ一文のPromptではないのか？](https://zenn.dev/lienjack/articles/00-01-agent-not-a-prompt)
