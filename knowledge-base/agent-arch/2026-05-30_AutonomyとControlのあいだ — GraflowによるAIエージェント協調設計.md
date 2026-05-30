---
title: "AutonomyとControlのあいだ — GraflowによるAIエージェント協調設計"
url: "https://zenn.dev/myui/articles/c195b671ca9202"
date: 2026-05-30
tags: [Graflow, LangGraph, Harness Engineering, Autonomy Slider, Define-by-run, PydanticAI, Google ADK, Controlled Autonomy, Ralph-loop, Multi-agent]
category: "agent-arch"
related: [564, 41, 745, 526, 857]
memo: "[Zenn LLM] AutonomyとControlのあいだ — Graflowで記述するAIエージェント協調"
processed_at: "2026-05-30T09:07:37.943769"
---

## 要約

本記事は、2026年5月15日開催の第5回AIエージェントソフトウェア開発勉強会での登壇内容をまとめたもの。著者が開発するOSS「Graflow」（Apache-2.0）のコンセプトと、エージェント設計における「Autonomy Slider」という思想を解説する。

Andrej Karpathyが示す枠組みを援用し、エージェントの自律性を「Deterministic（Airflow/Dagster）」から「Fully Autonomous（Claude Code/Devin）」までの連続スライダーとして捉える。Graflowが狙うのはその中間帯「Controlled Autonomy」——人間がワークフロー全体を設計しつつ、個々のタスクでLLMが自律する領域。

Graflowの設計上のコアは3点。①Pythonic DSL：`>>`で逐次、`|`で並列を表現し、LangGraphの`add_edge`より大幅に記述量を削減。②Define-by-run：LangGraphがDefine-and-compile（TF1.x流）であるのに対し、PyTorch流の実行時グラフ構築を採用。分岐は通常の`if`文で記述可能で、`pdb`によるデバッグも素直に動く。③SuperAgent as Fat Node：ReActループはADK/PydanticAI/OpenAI Agents SDKなどBest-of-Breedに委譲し、Graflowはワークフロー編成に集中する関心分離。

もう一つの論点が「Harness Engineering」。モデル単体の性能差が縮小する中、差別化要因は「モデルを取り囲む環境・記憶・道具・反復ループ」の設計品質にシフトしつつあるという観測。構成要素はSkills（ドメイン特化知識の動的装着）、Context Engineering（情報注入・トリミング・要約）、Agent Memory（短期/長期/エピソード）、Ralph-loop（Critique→Reviseの自己改善ループ）の4つ。Google ADKは`google.adk.skills.load_skill_from_dir`でスキルディレクトリを動的ロード、PydanticAIは`pydantic_ai_skills`パッケージの`SkillsCapability`で対応しており、これらはフレームワーク標準機能になる方向性。

Graflowのロードマップは、ADKとPydanticAIの両エージェントが同一skillディレクトリを参照できる統合層の提供、Context Engineering、Agent Memory統合、Ralph-loop first-class対応。監査エージェント開発との関連では、「東証上場企業で過去2年連続赤字」という同一プロンプトでも参照ソースや結果件数が変わる非決定性の問題を、Controlled Autonomyで抑制できる点が示唆に富む。複数フレームワークを組み合わせたワークフロー全体のライフサイクル管理（Skill A/Bテスト、HITLによる段階ロールアウト等）はワークフロー層を持つメリットが出る領域として言及される。

## アイデア

- 自律性を「Deterministic〜Fully Autonomous」の連続スライダーとして定量的に捉え、ユースケースごとに最適点を選ぶという設計思想は、監査エージェントのように決定的挙動が求められる場面と探索的推論が必要な場面を同一ワークフロー内で使い分ける際に直接応用できる
- Define-by-runアーキテクチャにより、LangGraphのcompile時グラフ定義と異なり実行時の動的分岐をネイティブな`if`文で記述できる点は、実行ステップ数・依存関係が事前に確定しない監査調査タスクのオーケストレーションに適合する
- Harness Engineeringの観点で「モデル性能差よりも周辺設計品質が差別化要因になる」という命題は、LLM-as-judgeやRLAIF評価ループの設計において、どのモデルを使うかよりも評価基準・メモリ・コンテキスト注入の品質をどう工学的に担保するかに注力すべきことを示唆する

## 前提知識

- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **ReActループ** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Define-by-run** (TODO: 読むべき)
- **PydanticAI** → /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】
- **Multi-agent Orchestration** (TODO: 読むべき)

## 関連記事

- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由
- /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- /deep_745 ケース適応型マルチエージェント審議による臨床予測：CAMP
- /deep_526 Consilium: 複数LLMが協調して意思決定するマルチLLMプラットフォーム
- /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】

## 原文リンク

[AutonomyとControlのあいだ — GraflowによるAIエージェント協調設計](https://zenn.dev/myui/articles/c195b671ca9202)
