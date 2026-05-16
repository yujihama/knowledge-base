---
title: "Claude CodeでAgentic Quality Gate Pluginを実装した話：Karpathyのいうアジェンティック・エンジニアリングをSI現場に落とし込む"
url: "https://zenn.dev/kiwiiosaru2024/articles/agentic-quality-gate-karpathy"
date: 2026-05-11
tags: [Claude Code, Agentic Engineering, 品質ゲート, Hook, Subagent, MCP, Living Spec, CVE自動取込, Human-in-Loop, SI品質保証]
category: "agent-arch"
related: [430, 2688, 4520, 2404, 2140]
memo: "[Zenn LLM] Claude Code で Agentic Quality Gate Plugin を実装した話"
processed_at: "2026-05-11T12:14:22.174485"
---

## 要約

Andrej Karpathyが提唱する「Agentic Engineering」の核心は「生産性は桁違いに上がるが、品質バーは絶対に下げるな」という命題にある。本記事はその命題をSI現場で実践するため、Claude CodeのSubagent・Hook・Skill・MCPを組み合わせた「自己進化する品質ゲート（Agentic Quality Gate）」をPlugin化し、実案件の提案書作成に適用した実装記録である。

Karpathyの3つの観察──①AI活用で生産性が10倍以上になる、②ボトルネックは打鍵からレビュー・意思決定する人間に移った、③Vibe codingを理由に脆弱性を入れることは許されない──を受け、SIerが直面する「生産性・品質・継続性の三点同時解決」という課題に対して4原則を設計した。①ルールをGit管理するLiving Spec（MarkdownでPR・revert可能）、②AI用自動判定と人間用チェックを同一ファイルに同居させるDual-Use設計、③NVD・GHSA・個人情報保護委員会・IPAなど外部DBを24時間以内に取り込むAuto-Update、④深刻度の高い変更には必ず人間承認を求め新ルールはShadow modeで1週間試すHuman-in-Loopである。

技術実装面では、観測→採点→ルール合成→PR生成という6層アーキテクチャを採用。log4shellクラスの脆弱性が朝公表されると夕方には該当リポジトリにルール更新PRが立つ仕組みになっている。ルール更新は即応型（CVE等、24時間以内）・定期型（月次）・ふりかえり型（インシデント後随時）の3モードで動く。開発ライフサイクル全7フェーズに専用チェックゲートを紐付け、現時点137項目（目標200項目）のチェックリストがフェーズ切替と同時に自動で適用される。

Claude Codeを選んだ理由はSubagent・Hook（PreToolUse / PostToolUse / Stop / SessionStart）・Skill・Slash Command・Plan Mode・Memory・MCP Serverが標準装備であり、「開発空間と品質ゲート空間を1つに置ける」点にある。物理レイアウトはユーザーレベル（組織共通）とプロジェクトレベル（案件別）の二階層構成。

実案件の提案書作成への適用結果は顕著で、計画書の致命的問題13件→0件を一晩で解消、Vibeコードと納品基準のギャップ8件を可視化した。富士通が2026年2月に発表したAI-DSDP（3人月→4時間の事例）との対比で、独自LLMや専用基盤を持てない中堅・中小SIerでも既存Claude Codeをベースに同等の仕組みを構築できることを示している。コードはApache-2.0でOSS公開済み（Claude Security連携は初版スケルトン、本実装は後続）。監査エージェント開発への示唆としては、フェーズ別チェックゲートの設計思想はLangGraphの状態遷移×条件分岐と親和性が高く、Human-in-LoopのShadow modeは本番投入前の誤検知評価フレームとして監査ルール自動化にそのまま転用できる。

## アイデア

- 品質ルールをMarkdown×Gitで管理し、AI用自動判定指示と人間用チェック項目を同一ファイルに同居させる『Dual-Use Living Spec』という設計思想は、チェックリストの陳腐化と人間・AI間の結論乖離を同時に解決する
- CVE公開から24時間以内にルール更新PRを自動生成する即応型更新ループは、年次更新型の静的チェックリストとの最大の差別化点であり、NVD・GHSA・政府機関通達を観測層として組み込むことで実現している
- 新ルールをまず『Shadow mode（判定はするがブロックしない）』で1週間稼働させてから本番投入する手順は、誤検知コストを定量化しながら段階的にガードを強化する実践的なRollout戦略であり、監査ルール自動化への転用価値が高い

## 前提知識

- **Claude Code Hooks** → /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- **Subagent** → /deep_43 AI社員8人で取締役会を開いたら、完全に人間の組織論だった件
- **MCP Server** → /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- **Living Spec** (TODO: 読むべき)
- **CVE/NVD** (TODO: 読むべき)

## 関連記事

- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2140 メルカリのClaude Codeセキュリティ設定を参考に、金融機関向けの方針を考えた

## 原文リンク

[Claude CodeでAgentic Quality Gate Pluginを実装した話：Karpathyのいうアジェンティック・エンジニアリングをSI現場に落とし込む](https://zenn.dev/kiwiiosaru2024/articles/agentic-quality-gate-karpathy)
