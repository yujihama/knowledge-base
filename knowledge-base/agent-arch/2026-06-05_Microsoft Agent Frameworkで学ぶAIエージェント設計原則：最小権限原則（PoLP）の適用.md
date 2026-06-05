---
title: "Microsoft Agent Frameworkで学ぶAIエージェント設計原則：最小権限原則（PoLP）の適用"
url: "https://zenn.dev/naruaki/articles/af-design-08-least-privilege"
date: 2026-06-05
tags: [最小権限原則, PoLP, Microsoft Agent Framework, ツール制御, マルチエージェント, セキュリティ設計, SequentialBuilder]
category: "agent-arch"
related: [6846, 6359, 5793, 1641, 4753]
memo: "[Zenn LLM] 【第８回】Microsoft Agent Frameworkで学ぶAIエージェント設計原則：全 Agent に全ツールを渡すのをやめる"
processed_at: "2026-06-05T09:14:45.869969"
---

## 要約

本記事はMicrosoft Agent Frameworkを使ったAIエージェント設計における最小権限原則（PoLP: Principle of Least Privilege）の適用方法を解説する第8回。カスタマーサポートシステムを例に、全エージェントに全ツール（search_web, send_email, create_ticket, lookup_account）を渡す「アンチパターン」と、各エージェントに必要最小限のツールのみを割り当てる「改善パターン」を対比する。

アンチパターンでは、research_agent・support_agent・notify_agentの3エージェントすべてに4つのツールを渡す。動作はするが、どのエージェントも外部書き込み（メール送信・チケット作成）を行える状態になるため、プロンプトインジェクション攻撃を受けた場合に被害が全ツールに及ぶリスクがある。また各エージェントの実際の能力が不明確になり、デバッグや監査が困難になる。

改善パターンでは、client.as_agent()のtoolsパラメータを使い、research_agentには読み取り専用の[search_web, lookup_account]のみ、support_agentにはチケット作成のみの[create_ticket]、notify_agentはメール送信のみの[send_email]を割り当てる。これにより、侵害が発生しても影響範囲が1工程のツールセットに限定される。

ツール割り当ての設計指針として「工程の責務からツールを導く」「外部状態を変える書き込み系ツールは特に慎重に扱う」「ツールは与えるものではなく不要なものをあえて渡さないという発想で設計する」の3点を示す。

監査エージェント開発への示唆として、内部監査ワークフローにおいても同原則は直接適用可能。例えばデータ収集エージェントにDB書き込みツールを持たせない、レポート生成エージェントに外部送信ツールを渡さないといった設計が、誤操作・インジェクション攻撃による被害範囲の局所化につながる。LangGraphでのノード設計でも、各ノードが呼び出せるツールセットを明示的に制限することで、同様の効果が得られる。

## アイデア

- ツールは「与えるもの」ではなく「不要なものをあえて渡さない」という発想の転換は、LangGraphのノード設計やMCPのツール公開スコープ管理にも同様に適用できる
- 書き込み・送信・削除を伴う副作用ツールを持つエージェントを明示的に分離することで、プロンプトインジェクション攻撃の爆発半径（blast radius）を構造的に制限できる
- 各エージェントのtoolsリストが設計ドキュメントとして機能し、コードを読むだけでアーキテクチャの責務分離が確認できる自己文書化効果がある

## 前提知識

- **Principle of Least Privilege** (TODO: 読むべき)
- **LLMツール呼び出し** (TODO: 読むべき)
- **マルチエージェント設計** → /deep_5319 マルチエージェント設計の7原則：Factory「Missions」が16日間自律稼働を実現
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **SequentialAgent** (TODO: 読むべき)

## 関連記事

- /deep_6846 【第7回】Microsoft Agent FrameworkのFacadeパターン：workflow.as_agent()でワークフローをAgentとして公開する
- /deep_6359 仕様書に埋もれた「決まっていない意思決定」を、マルチエージェントで炙り出す
- /deep_5793 Microsoft Agent FrameworkのHandoffBuilderによるルーティング設計と開放閉鎖原則
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[Microsoft Agent Frameworkで学ぶAIエージェント設計原則：最小権限原則（PoLP）の適用](https://zenn.dev/naruaki/articles/af-design-08-least-privilege)
