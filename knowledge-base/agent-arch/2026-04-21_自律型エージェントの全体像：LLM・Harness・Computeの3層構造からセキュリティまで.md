---
title: "自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで"
url: "https://zenn.dev/k_k_p/articles/autonomous-agent-overview"
date: 2026-04-21
tags: [自律型エージェント, Harness, MCP, Agent Skills, マルチエージェント, サンドボックス, OWASP, 状態管理, Progressive Disclosure, Sub-agent]
category: "agent-arch"
related: [88, 628, 68, 2249, 2102]
memo: "[Zenn LLM] 自律型エージェントの全体像"
processed_at: "2026-04-21T12:39:16.862631"
---

## 要約

本記事は自律型エージェントの全体像を体系的に整理した解説記事。従来の1ショットLLM利用との違いから始まり、エージェントを構成する3要素（LLM・Harness・Compute）、ツール/プロトコル層、マルチエージェント設計、セキュリティ、状態管理までを網羅する。

【3層構造】Harnessはツール定義・ループ制御・ガードレール・権限管理を担う「台座」であり、モデルの能力向上とともに責務を削減していく「引き算設計」が原則。ComputeはOS-ネイティブ（Seatbelt/bubblewrap）・コンテナ（Docker/gVisor）・MicroVM（Firecracker）の3分離レベルで実装される非特権サンドボックス。

【ツール/プロトコル】MCP（Model Context Protocol）はJSON-RPC 2.0ベースのオープン標準で、Tools・Resources・Promptsの3プリミティブを定義。エージェント内部ロジックには関与しない割り切りにより、Claude Code Agent SDK・OpenAI Agents SDK・OpenHandsなど主要SDKすべてが対応。MCPの上位概念としてAgent Skillsがあり、「何ができるか」ではなく「どうやるか・なぜそう判断するか」という手続き知識をYAMLフロントマターでProgressive Disclosure方式に提供する。

【マルチエージェント】OrchestratorパターンはClaude Managed Agentsが実装。Advisor Strategy（上位モデルが方針、下位モデルが実行）でコスト最適化が可能。HiClawはMatrixプロトコルベースの分散協調パターンで、WorkerはクレデンシャルをHigress AI Gatewayにプロキシ委譲し保持しない設計。Sub-agentは実行時に動的生成され、BrowseCompベンチマークで単一エージェント比+2.8%改善。

【セキュリティ】OWASP Top 10 for Agentic Applications (2026)がASI01〜ASI10を体系化。主要脅威はプロンプトインジェクション（ASI01）・権限濫用（ASI03）・サプライチェーン汚染（ASI04）・サンドボックス脱出（ASI05）。防御は特権分離・サンドボックス・ガードレール・Egress制御の4層で構成。Anthropic未リリースモデルClaude Mythos Previewが主要OS全域で数千件のゼロデイ脆弱性を自律発見したProject Glasswingが攻撃側ポテンシャルの実証として言及される。

【状態管理】In-context（セッション内）・External（検索要）・Episodic（FTS5+LLM要約）・Checkpointing（Issue記録）の4メカニズムを区別。コンテキスト設計は「Static first, dynamic last」（変化しない情報を先頭固定）でprompt cache効率を最大化。監査エージェント開発観点では、特権分離・ガードレール・Human-in-the-Loopの設計パターンが内部統制の証跡可視性と直結する。

## アイデア

- Harnessの「引き算設計」思想：モデル能力向上に伴い責務をモデルに委譲し続けるという設計哲学は、エージェント開発の長期的アーキテクチャ判断に直接影響する
- HiClawのゲートウェイ型クレデンシャル管理：WorkerがConsumer Tokenのみ保持しHigress AI Gatewayが実API認証をプロキシする設計は、監査エージェントの権限最小化に転用できる実装パターン
- Agent SkillsのProgressive Disclosure：YAMLフロントマターのみを事前ロードし本体は使用時に取得する遅延読み込みは、コンテキスト窓の効率的管理と動的な手続き知識拡張を両立する

## 前提知識

- **LLM推論ループ** (TODO: 読むべき)
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **サンドボックス分離** (TODO: 読むべき)
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **OWASP Top 10** (TODO: 読むべき)

## 関連記事

- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- /deep_68 Claudeは明日もあなたを忘れる — MCP Memory Server cpersona 設計と実践
- /deep_2249 Claude Codeの設定はどこに書くべきか ― プロンプト・RULES・スキル・エージェントの使い分け
- /deep_2102 Clade v1.14.5 ── Claude Code上のフレームワークを他の構成と正直に比べてみた

## 原文リンク

[自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで](https://zenn.dev/k_k_p/articles/autonomous-agent-overview)
