---
title: "「人間はコードを書かない・レビューもしない」を5ヶ月やった話──OpenAI Frontierの極限harness"
url: "https://zenn.dev/aiwatch_jp/articles/openai-frontier-extreme-harness"
date: 2026-06-06
tags: [harness, CI, multi-agent, Codex, spec-driven, 自己改善, PRレビューagent, 観測ファースト, on-policy設計]
category: "agent-arch"
related: [7504, 599, 65, 70, 38]
memo: "[Zenn LLM] 「人間はコードを書かない・レビューもしない」を5ヶ月やった話──OpenAI Frontierの極限harness"
processed_at: "2026-06-06T09:06:44.833345"
---

## 要約

OpenAI FrontierのRyan Lopopoloが3人チームで5ヶ月間、「人間がコードを書かない・事前レビューもしない」という条件で内部プロダクトを開発した実験の詳細報告。成果は100万行超・約1500PR・1日10億トークン（市場価格で日$2〜3k相当）。崩壊しなかった理由は「harness（足場）」の多層構造にある。

具体的な仕組みは以下の通り。①CI強制：「CI has to pass」をプレーンテキストの方針として明文化し、flakyテストやマージ衝突はエージェントが自律修正する。②観測ファースト：Jaeger/Prometheusのトレースをエージェントが直接クエリして障害を自己検知する。③レビューエージェントの合議：別プロンプトのPRレビューagentが「P2以上の問題のみ報告・マージ寄り」で動作し、著者agentとレビューagentが人間の裁定なしに交渉・合意する。④tech tracker：markdownの表に業務ロジックのガードレールを列挙し、agentが自己監査する。

コードベース設計も特徴的。500個のNPMパッケージで厳格なアーキを採用（各人間が10〜50体のagentとして振る舞うため衝突防止）。ドキュメントはspec.md・agent.md・core_beliefs.mdの3層構造で「非機能要件をagentにprompt-injectする空間」として機能。スキルは6個に限定し、inner-loopビルドは絶対1分以内を死守（Make→Bazel→Turbo→NXと移行）。MCPには懐疑的で、代わりに数行の薄いshim CLIを使用。

harnessの自己改善機能も実装。個人レベルではCodexに自分のセッションログを読ませて改善点を抽出。チームレベルでは全員のagent軌跡をblob storageに収集し、毎日agentループを回してリポジトリに還元する（L7相当の組織規模実装）。

課題も正直に開示：Codex Miniの初月は人間比10倍遅い、greenfield（更地）限定でレガシー環境には非適用、0→1の新規発明はまだ人間操舵が必要、チームのagent同士の調整に毎日45分のスタンドアップが必要。

核心的主張：「ガードレールをモデルがすでに生成しているコードにネイティブな形で組み込むこと」でモデル進化との摩擦を避ける。プロンプト芸や特殊なscaffoldはモデルが賢くなるほど陳腐化するが、「CIが通る・テストが増える・specから再生成できる」構造はモデルが強くなるほど効果が増す。監査エージェント開発への示唆：CI/観測/合議型レビューの多層ガードレールは、LangGraphベースのReActエージェントにも直接適用可能。特にレビューagentの敵対的合議パターンは監査判断の品質保証に転用できる。

## アイデア

- レビューagent合議パターン：著者agentとレビューagentを別プロンプトで対立させ、人間の裁定なしに交渉・合意させることでコードの質を担保する「敵対的検証」の実装
- agent軌跡の自動還元：チーム全員のagent実行ログをblob storageに集約し、毎日agentループで「チームとしての改善点」を抽出してリポジトリに書き戻すL7相当の組織学習ループ
- on-policy harness設計：ガードレールをプロンプト芸でなくモデルが生成するコードそのものに組み込むことで、モデルの能力向上と共にharnessの効果も増大する構造的アーキテクチャ

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **CI/CDパイプライン** (TODO: 読むべき)
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **OpenTelemetry/Jaeger** (TODO: 読むべき)
- **spec駆動開発** → /deep_6078 Spec駆動開発×LLMエージェントで挑む、次世代の分析基盤構築

## 関連記事

- /deep_7504 エージェントに「脆弱性を探して」はなぜ失敗するのか──CloudflareのProject Glasswingが示したharnessの正体
- /deep_599 OpenAIが全力投資する「完全自動化研究者」AIの構想
- /deep_65 OpenAIが全力投球する「完全自動化AIリサーチャー」構想：2026年インターン、2028年マルチエージェント研究システムへのロードマップ
- /deep_70 OpenAIが全力投入する「完全自動化された研究者」構築計画
- /deep_38 OpenAIが全力投入する「完全自動化AI研究者」構築計画

## 原文リンク

[「人間はコードを書かない・レビューもしない」を5ヶ月やった話──OpenAI Frontierの極限harness](https://zenn.dev/aiwatch_jp/articles/openai-frontier-extreme-harness)
