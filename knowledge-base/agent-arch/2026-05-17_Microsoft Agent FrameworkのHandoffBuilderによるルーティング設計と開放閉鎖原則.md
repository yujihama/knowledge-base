---
title: "Microsoft Agent FrameworkのHandoffBuilderによるルーティング設計と開放閉鎖原則"
url: "https://zenn.dev/naruaki/articles/af-design-06-routing"
date: 2026-05-17
tags: [Microsoft Agent Framework, HandoffBuilder, マルチエージェント, OCP, SOLID原則, ルーティング, LLM, Python]
category: "agent-arch"
related: [3446, 5037, 5684, 2956, 108]
memo: "[Zenn LLM] 【第６回】Microsoft Agent Frameworkで学ぶAIエージェント設計原則：HandoffBuilder でルーティング設計"
processed_at: "2026-05-17T09:00:34.722326"
---

## 要約

本記事はMicrosoft Agent Frameworkを題材に、マルチエージェントシステムのルーティング設計にSOLID原則の「開放閉鎖原則（OCP）」を適用する方法を解説した連載第6回。

カスタマーサポートシステムを例に、問い合わせ内容に応じてtriage/return/billingの3エージェントを切り替える設計を検討する。

**改善前の問題点：if/elifによるルーティング**

従来のアプローチでは、triage_agentの出力テキストに「返品」「交換」「支払い」等のキーワードが含まれるかをPythonのif/elif文で判定し、対応エージェントにディスパッチしていた。この設計には2つの根本的欠陥がある。(1) エージェントを追加するたびにroute関数のelif節を修正する必要があり、既存コードへの変更が不可避。(2) キーワードマッチングはLLMの出力表現の揺れ（同義語・言い回しの変化）に脆弱で、運用中に静かに壊れる。

**HandoffBuilderによる解決**

Microsoft Agent FrameworkのHandoffBuilderを使うと、ルーティングロジックをコードから排除できる。各エージェントにdescriptionフィールドを付与し、HandoffBuilderのparticipantsリストに追加するだけで、LLM自身がdescriptionを参照して引き継ぎ先を動的に判断する。エージェント追加時はparticipantsに追記するだけで、既存コードの修正は不要。これはOCPの「拡張に対して開き、修正に対して閉じる」を実現している。

デフォルトではすべてのエージェント間でハンドオフ可能なメッシュトポロジーが構成されるが、add_handoff(source, targets)で引き継ぎ先を明示的に制限できる。例えば「triageはreturn/billingのみに引き継げる」「returnはbillingに引き継げる」という有向グラフ的な制約を設定可能。

**GroupChatBuilderとの対比**

類似コンポーネントのGroupChatBuilderとの設計上の違いも整理されている。HandoffBuilderは分散型トポロジーで各エージェントがツール呼び出しにより明示的に次のエージェントを指名する方式。一方GroupChatBuilderは中央集権型で、オーケストレーターが内部判断するため各エージェントは次を知らない。前者は問い合わせ対応・承認フローに、後者は調査・執筆・レビューなど複数エージェントが協調するタスクに適している。

**監査エージェントへの示唆**

監査エージェント開発では、リスク評価→証拠収集→判断→レポートといった段階的なハンドオフフローが自然に発生する。HandoffBuilderのパターンはこうした承認・エスカレーションフローの実装に直接応用可能。特にadd_handoffによる明示的なルーティング制約は、監査プロセスの手続き的完全性を担保するうえで有効なアーキテクチャパターンとなる。

## アイデア

- ルーティングロジックをコードのif/elifではなくLLMのdescription読み取りに委譲することで、エージェント追加がコード修正ゼロになる設計は、大規模エージェントシステムの保守性を根本的に変える
- add_handoff()による有向グラフ的なハンドオフ制約は、メッシュトポロジーの自由度と構造的制御のバランスを取る手法として、承認フローや監査プロセスの実装に直接応用できる
- HandoffBuilder（分散・明示的指名）とGroupChatBuilder（中央集権・オーケストレーター判断）という2種類のマルチエージェントトポロジーの使い分けは、タスクの性質（単線的 vs 協調的）に基づく設計判断として汎用的に活用できる

## 前提知識

- **SOLID原則** (TODO: 読むべき)
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **LLMツール呼び出し** (TODO: 読むべき)
- **Microsoft Agent Framework** (TODO: 読むべき)
- **オーケストレーションパターン** (TODO: 読むべき)

## 関連記事

- /deep_3446 表形式データの自動特徴量生成のためのメモリ拡張LLMベースマルチエージェントシステム（MALMAS）
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_5684 構文ガイドと意味認識を組み合わせた選好最適化によるコード翻訳の改善（CTO）
- /deep_2956 末梢神経AIと統合AIの分離設計 — 痛み閾値による自律制御
- /deep_108 局所整合から経路全体へ ― 意味の経路積分による生成AI挙動の数理的再解釈

## 原文リンク

[Microsoft Agent FrameworkのHandoffBuilderによるルーティング設計と開放閉鎖原則](https://zenn.dev/naruaki/articles/af-design-06-routing)
