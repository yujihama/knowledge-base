---
title: "agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた"
url: "https://zenn.dev/7788/articles/ecc67394fd6ff0"
date: 2026-04-08
tags: [agency-agents, Claude Code, システムプロンプト, マルチエージェント, プロンプトエンジニアリング, LLMエージェント]
category: "agent-arch"
memo: "[Zenn LLM] agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた"
processed_at: "2026-04-08T21:52:26.673156"
---

## 要約

GitHubリポジトリ「msitarzewski/agency-agents」は、Claude Codeをはじめとする主要AIコーディングツール向けに144種類の専門エージェント用システムプロンプトを提供するコレクションである。Redditスレッド発祥で、公開後12時間で50件超のリクエストが集まったコミュニティ主導プロジェクト。12部門（Engineering 26、Marketing 27、Game Development 18、Specialized 28など）に分類され、各エージェントはMarkdown形式で「Identity & Memory」「Core Mission」「Critical Rules」「Technical Deliverables」「Workflow Process」「Success Metrics」の6要素を持つ構造化されたプロンプトとして設計されている。

実用性が高い領域はエンジニアリング部門で、Frontend DeveloperはCore Web Vitals（LCP < 2.5s、FID < 100ms、CLS < 0.1）の具体的目標値と@tanstack/react-virtualを使った実装例を内包する。Code ReviewerとReality Checkerの組み合わせで「実装→品質チェック」ループが構成可能。テスト部門ではEvidence Collector（スクリーンショットによる証跡収集）とReality Checker（本番リリース前品質ゲート）が「証拠ベースのQA」哲学を体現し、他プロンプト集にない特徴となっている。ゲーム開発部門はUnity・Unreal・Godot・Blender・Robloxをカバーし、インディー開発者向けにパイプライン全体をチームとして組める。

一方、Sales Data Extraction AgentやReport Distribution Agentのような自動化エージェントは、単体では機能せずn8nやMake等のオーケストレーション基盤が別途必要。Accounts Payable Agent（暗号通貨・法定通貨での自律支払い実行）は安全上の理由から実用困難。Legal Compliance Checker（SOC 2・HIPAA・PCI-DSS）やCivil Engineerは「下書きを作る副操縦士」として有資格者レビュー前提での利用が現実的。

インストールは./scripts/install.shで対話的に行え、Claude Code・GitHub Copilot・Cursor・Gemini CLI・Aider・Windsurf・Qwen Code・Kimi Code・OpenCodeなど11ツールに対応。MVP開発チームとして「Rapid Prototyper→Backend Architect→Frontend Developer→Reality Checker→Growth Hacker」というエージェント切り替えワークフローが典型的な活用パターンとして提示されている。評価はClaudeでのPR・コードレビュー補助が★5、自律的な外部API操作・金融処理が★1。本質は「自律ボット」ではなく「高品質なシステムプロンプト集」であり、144個全部より自分のワークフローに直結する10〜20個を深く活用するアプローチが費用対効果最大とされる。

## アイデア

- 単なるロールプレイ指示ではなく「Identity・Mission・Critical Rules・Technical Deliverables・Workflow・Success Metrics」の6要素で構造化することで、再現性ある成果物を引き出す設計思想が参考になる
- Code ReviewerとReality Checkerのような「実装エージェント＋検証エージェント」の二重構造は、LLM-as-judgeパターンのシステムプロンプトレベルでの実装例として捉えられる
- Evidence Collector（視覚的証拠を要求するQAエージェント）という概念は、AIによるテストに「証明責任」を持たせる哲学的アプローチであり、監査領域のエビデンス収集と構造的に同型
## 関連記事

- /deep_108 局所整合から経路全体へ ― 意味の経路積分による生成AI挙動の数理的再解釈
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_1684 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- /deep_1643 Claude Codeの「アドバイザー」と「サブエージェント」── Maxプランでの使い方
- /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 原文リンク

[agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた](https://zenn.dev/7788/articles/ecc67394fd6ff0)
