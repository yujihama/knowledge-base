---
title: "LLMの前段に「思考状態」を分離する — VLTE-BPTM の設計思想と正直な性能の現在地"
url: "https://zenn.dev/kota26/articles/vlte-bptm-thought-state-arch"
date: 2026-06-17
tags: [VLTE-BPTM, Semantic Routing, 責務分離, Thought Code, LLMコストゲート, 処理経路選択, Horizontal Mesh, llm_order, 追跡可能性, アーキテクチャ設計]
category: "agent-arch"
related: [1411, 6906, 3772, 485, 5165]
memo: "[Zenn LLM] LLMの前段に「思考状態」を分離する — VLTE-BPTM の設計思想と、正直な性能の現在地"
processed_at: "2026-06-17T09:04:26.414667"
---

## 要約

VLTE-BPTM v1.6（alpha）は、自然言語入力をLLMに直接渡す前に「どう考えるか」を決める薄い前段レイヤを挟むアーキテクチャ。入力を64bitの「Thought Code」（外部ルーティングキー）に変換し、意味抽出・経路選択・Unit実行・回答生成を独立したコンポーネントとして責務分離する設計。処理パイプラインは input → active_bits → selected_units → inhibition integration → horizontal mesh → action_vector → llm_order の順で流れ、各層が「やらないこと」によって契約的に境界を定義している（RouterはRAWプロンプトを解釈しない、CoreはLLMへの文章生成をしない等）。最も効果が顕著なのはコストゲート機能：「こんにちは」のような挨拶入力に対してLLM呼び出し（4〜6秒）を丸ごとスキップし、ローカルのgemma-4-12bとの比較で最大27,000倍の速度差を実現。これはRouterが賢いのではなく「呼ばずに済む」ことによる効果と筆者は明記している。回答品質の観点ではfrozen regressionで25/25（精度1.0）、foundation anchorsで58/58（精度1.0）を達成する一方、別系統のfixture交差評価ではCore→Router境界fixtureへの適用で9/25（macro-F1 0.364）まで落ち、汎化の限界を示している。最も重要な留保として、回答本文そのものの正しさを独立にblind評価したケース数は現時点で0件（independent_case_count=0, status=not_established）であり、現状は「回答を賢くする装置」ではなく「LLMをいつ・どう呼ぶかを決める追跡可能な前段レイヤ」という位置づけ。処理判断はJSONで完全ログ化されるため入力ごとの経路追跡が可能で、監査ログや制約注入（クラウド出力を学習に使わない等の構造的強制）として即時価値がある。今後はPattern Language Model・Processing Router・LLM Integrationの3トラックに分け、回答品質の独立blind評価確立を最優先課題としている。監査エージェント開発への示唆：入力ごとの処理経路をJSON追跡できる設計は、監査証跡の要件（why this input was processed this way）と親和性が高い。LLM呼び出しの前段でルールベースのコストゲートを設ける構造はLangGraphのconditional edgeと組み合わせ可能であり、重い推論を必要とする監査クエリとそうでないものを事前分離するレイヤとして応用を検討できる。

## アイデア

- 「やらないこと」で契約的に境界を定義する責務分離：RouterはRAWプロンプトを解釈しない、Coreは文章を生成しないという否定形の制約により、各層の独立評価・差し替えを可能にする設計哲学
- LLMを呼ぶ前に呼ばないと決めるコストゲート：入力の意味を軽量前段で判定し、挨拶のような単純入力でLLM呼び出しを完全スキップすることで最大27,000倍の速度差を実現するアプローチ
- 性能の正直な開示フレームワーク：frozen regression 100%・交差評価 36%・回答品質評価 0件という三層の指標を同等の熱量で並べ、「出ている数字」と「出ていない数字」を明示的に区別するエンジニアリング文化の実践

## 前提知識

- **LLMルーティング** → /deep_689 ParetoBandit: 非定常LLMサービングのための予算ペーシング適応型ルーティング
- **責務分離アーキテクチャ** (TODO: 読むべき)
- **Semantic Router** → /deep_6079 LLM / AIエージェント時代の安全設計：確率的推論と決定論的ガードレールの境界
- **LangGraph conditional edge** (TODO: 読むべき)
- **macro-F1スコア** (TODO: 読むべき)

## 関連記事

- /deep_1411 形状・対称性・構造：機械学習研究における数学の役割の変遷
- /deep_6906 形状・対称性・構造：機械学習研究における数学の変化する役割
- /deep_3772 ナラティブ駆動開発——LLMはなぜLLMであることを許されないのか
- /deep_485 なぜLLMにDSLを直接書かせないのか — Nia Drawing Languageの4層アーキテクチャ
- /deep_5165 RFPを貼るだけでAWSアーキテクチャ設計書が出てくるSaaSを個人開発した

## 原文リンク

[LLMの前段に「思考状態」を分離する — VLTE-BPTM の設計思想と正直な性能の現在地](https://zenn.dev/kota26/articles/vlte-bptm-thought-state-arch)
