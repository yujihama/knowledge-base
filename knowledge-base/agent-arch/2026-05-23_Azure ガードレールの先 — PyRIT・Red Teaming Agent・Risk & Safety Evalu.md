---
title: "Azure ガードレールの先 — PyRIT・Red Teaming Agent・Risk & Safety Evaluators・Agent Governance Toolkit・Defender for Cloud による多層AIセキュリティ"
url: "https://zenn.dev/headwaters/articles/fb0b48788a914b"
date: 2026-05-23
tags: [PyRIT, AI Red Teaming, Azure AI Foundry, Risk and Safety Evaluators, Agent Governance Toolkit, XPIA, OWASP Agentic AI, Defender for Cloud, adversarial testing, LLMセキュリティ]
category: "agent-arch"
related: [6121, 2841, 5077, 2693, 2543]
memo: "[Zenn LLM] Azure ガードレールの先 — PyRIT・Red Teaming Agent・Risk & Safety Evaluators・Defe"
processed_at: "2026-05-23T09:06:30.249212"
---

## 要約

本記事は、Azure AI エコシステムにおける LLM セキュリティを「runtime ガードレール」の外側まで拡張し、開発→CI→runtime monitoring→SOC の全ライフサイクルを Microsoft ツール群で繋ぐ設計を解説する。

**PyRIT（Python Risk Identification Tool）**は Microsoft OSS の adversarial testing フレームワークで、Crescendo/TAP/Skeleton Key 等のマルチターン攻撃戦略を標準搭載。OpenAI/Azure/Anthropic/Google など任意 HTTP ターゲットに対応し、SQLite または Azure SQL に結果を保存・エクスポートできる。

**AI Red Teaming Agent（preview）**は PyRIT のクラウド自動化版で、Foundry プロジェクト内でエージェントに対し自動 adversarial probing を実行する。curated seed prompts とリスクカテゴリ別 taxonomy を同梱し、fine-tuned adversarial LLM が攻撃シミュレーションと採点を担う。Attack Success Rate（ASR）を指標として出力し、pre-deployment の大規模実行と post-deployment のスケジュール実行を分けて設計されている。現時点では Foundry hosted agents のみサポートで、テキスト専用・Python 3.9 以上が要件。

**Risk and Safety Evaluators**は CI ゲート用採点器で、Hate/Violence/Sexual/Self-harm、Indirect Attack（XPIA）、Protected materials、Code vulnerability（path-injection/sql-injection 等 7 言語対応）、Ungrounded attributes、Prohibited actions（agents only）、Sensitive data leakage（agents only）の各カテゴリをスコア化する。prohibited_actions と sensitive_data_leakage はツール呼び出し情報（tool_calls）が必要なためエージェント専用。XPIA は Manipulated content／Intrusion／Information gathering の 3 サブカテゴリで判定される。

**Agent Governance Toolkit（AGT）**は 2026-04 公開の MIT ライセンス OSS で、OWASP Agentic AI Top 10 の全 10 項目に対応する初のツールキットと位置付けられる。Policy engine は LLM 判定でなく deterministic に sub-millisecond で policy 評価し、Zero-trust identity でエージェント単位の暗号学的 ID を付与、ツール実行の Execution sandboxing、Audit logging/SRE、Agent Mesh による複数エージェント間ガバナンスを提供する。

**Defender for Cloud AI threat protection**は runtime で漏れた攻撃を検知・可視化し、Defender XDR/Microsoft Sentinel と連携して SOC の XDR/SIEM 相関・インシデント化まで繋ぐ。

監査エージェント開発への示唆：CI パイプラインに ASR 閾値ゲートを組み込み、prohibited_actions ヒット時にツール権限を自動見直す仕組みは、LangGraph ベースの監査エージェントの権限昇格リスクを事前検出する設計パターンとして直接応用できる。また AGT の deterministic policy engine は、LLM 非依存で監査ツール呼び出しを制御する HITL ゲートとして有効。

## アイデア

- AGT の Policy engine が LLM 判定でなく deterministic に sub-millisecond で評価する点：LLM ベースのガードレールは攻撃者に bypass されるリスクがあるが、deterministic policy は原理的に予測不能な LLM 応答に依存しないため、エージェントのツール呼び出し制御において確実性が格段に高い
- prohibited_actions と sensitive_data_leakage がエージェント専用評価カテゴリである理由：tool_calls を入力として必要とするため bare model には適用不可という設計制約は、エージェント評価と model 評価のアーキテクチャ的差異を明確に示しており、監査エージェントの評価設計で見落とされがちな盲点
- XPIA（cross-domain prompt injected attacks）の 3 サブカテゴリ分解：Manipulated content／Intrusion／Information gathering という分類は、RAG パイプラインや添付文書処理を持つ監査エージェントにとって攻撃面の体系的な棚卸しに直接使えるフレームワークとなる

## 前提知識

- **Prompt Injection** → /deep_1740 AIエージェントの安全性は『モデルの注意力』ではなく『ハーネスの設計』で守る
- **Azure AI Foundry** (TODO: 読むべき)
- **OWASP Top 10** (TODO: 読むべき)
- **Red Teaming** → /deep_5571 ブレーキを壊せ、ホイールは壊すな：エントロピー最大化による非ターゲット型ジェイルブレイク
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_6121 システムプロンプトって漏れるの？LLM07 System Prompt Leakageを初心者向けに解説
- /deep_2841 サラミスライシング脅威：LLMシステムにおける累積リスクの悪用
- /deep_5077 アライメントだけでは不十分：LLMエージェントへのレスポンスパス攻撃
- /deep_2693 そのプロンプト、本当に 
- /deep_2543 【実装】あなたのAIアシスタント、一文でハイジャックされてます——PythonでPrompt Injection検出ゲートを作る

## 原文リンク

[Azure ガードレールの先 — PyRIT・Red Teaming Agent・Risk & Safety Evaluators・Agent Governance Toolkit・Defender for Cloud による多層AIセキュリティ](https://zenn.dev/headwaters/articles/fb0b48788a914b)
