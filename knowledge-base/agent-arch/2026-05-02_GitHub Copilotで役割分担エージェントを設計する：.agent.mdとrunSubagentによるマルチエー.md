---
title: "GitHub Copilotで役割分担エージェントを設計する：.agent.mdとrunSubagentによるマルチエージェント構成"
url: "https://zenn.dev/tsukitsukiss/articles/copilot-role-agents"
date: 2026-05-02
tags: [GitHub Copilot, マルチエージェント, .agent.md, runSubagent, 関心の分離, System Prompt, Tool Use, オーケストレーター]
category: "agent-arch"
related: [3241, 1966, 1641, 16, 21]
memo: "[Zenn LLM] GitHub Copilotで役割分担エージェントを設計する"
processed_at: "2026-05-02T12:41:28.935021"
---

## 要約

本記事は、GitHub Copilotのカスタムエージェント機能（.agent.md）とサブエージェント呼び出し（agent/runSubagent）を使い、複数の役割を持つLLMエージェントを順番に呼び出して意見を統合するマルチエージェント構成を実践した報告である。

題材として「野外活動サークルの会議」を採用し、司会役（nokuru_meeting）・企画主導役（kaede）・体験提案役（hinata）・現実調整役（satsuki）・装備確認役（yuki）の5エージェントを.vscode/agents/以下に配置した。各.agent.mdファイルにはname・description・toolsのフロントマターと、性格・話し方・判断スタンスを記述したシステムプロンプトを定義する。司会エージェントは`tools: ["agent/runSubagent"]`を宣言し、kaede→hinata→satsuki→yukiの順で`#tool:agent/runSubagent`を呼び出してそれぞれの回答を取得、最後に統合して返答する。

技術的な本質として3点が整理されている。①関心の分離：1つの巨大プロンプトに全人格を混在させず、役割ごとに判断軸を切り分けることで出力の一貫性と再利用性が向上する。②Tool Useによる制御：司会エージェントがrunSubagentを関数呼び出しのように実行し、引数（prompt）と戻り値（各エージェントの回答）を制御する。③文脈のリレー：LLMは永続記憶を持たないため、司会役がそれまでの議論を要約しながら次エージェントへ文脈を引き継ぐことで、独立回答の寄せ集めではなく連続した議論を成立させる。

ソフトウェア開発への応用として、main_orchestrator・spec_writer・implementer・reviewerの4エージェント構成が提案される。要件整理エージェントの出力をrequirements.mdの原稿として、実装エージェントの出力をコードとテストとして、レビューエージェントの出力を修正タスクリストとして接続することで、会議結果が直接開発資産になるワークフローを実現できる。

著者は自作のMultiRoleChat.pyで同様の試みをしており、GitHub Copilotでも近いことが実現可能になったと評価している。実行環境の制約からサブエージェントの直接呼び出しが一部解決できなかったケースも報告されており、現時点の機能境界も率直に示されている。監査エージェント開発への示唆として、spec_writer→implementer→reviewerという分業フローは、LangGraphベースの監査ワークフローにおける要件定義・実装・品質確認の各ノード設計と直接対応しており、各ノードに独立した判断軸を持たせることで監査証跡の透明性と責務分離を両立できる構成として参考になる。

## アイデア

- .agent.mdによる役割定義は「判断軸の明示」であり、キャラクター性ではなく責務分離が本質という整理は、LangGraphのノード設計原則と直接対応する
- 司会エージェントが文脈を要約しながら次エージェントへリレーする構造は、LLMの無記憶性を明示的な文脈伝達で補う設計パターンとして汎用的
- マルチエージェントの出力を「読むための議事録」ではなく「次工程への入力ドキュメント」として扱う発想は、エージェントパイプラインの中間成果物設計に応用できる

## 前提知識

- **System Prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **Tool Use** → /deep_3094 LLMに図面情報を全部見せる設計をやめた話
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **オーケストレーターパターン** (TODO: 読むべき)
- **GitHub Copilot Agent** (TODO: 読むべき)

## 関連記事

- /deep_3241 VSCodeリリースノートで追うGitHub Copilot進化史 (v1.86 → v1.116)
- /deep_1966 AIエージェントと組んだら、データサイエンスプロジェクトはどう変わる？実験してみた（前半戦）
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_16 長期実行アプリケーション開発のためのハーネス設計
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読

## 原文リンク

[GitHub Copilotで役割分担エージェントを設計する：.agent.mdとrunSubagentによるマルチエージェント構成](https://zenn.dev/tsukitsukiss/articles/copilot-role-agents)
