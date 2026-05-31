---
title: "Arcaの探索グラフ：探索の記録をリポジトリに残すためのscaffold設計"
url: "https://zenn.dev/sisiodos/articles/c11580fb40978a"
date: 2026-05-31
tags: [exploratory-graph, scaffold, LLM-agent, knowledge-management, context-graph, YAML, Markdown, decision-traceability, Arca]
category: "agent-arch"
related: [6554, 6605, 609, 5219, 1058]
memo: "[Zenn LLM] Arca の探索グラフ：探索の記録を repo に残すための scaffold"
processed_at: "2026-05-31T09:06:58.939496"
---

## 要約

Arcaというエージェント開発プロジェクトにおいて、「なぜその判断に至ったか」という探索プロセスの記録が残らない問題を解決するために、exploratory graph（探索グラフ）という仕組みを設計・実装した経緯を記述した記事。

Stage 8でroadmapからタスクを自動生成する仕組みが完成した後、次のgoal選択という探索プロセスが人間の頭の中やセッションログにしか残らないという問題が浮上した。却下した候補・リスク・発見の根拠がどこにも記録されず、次のagentが同じ探索をやり直すリスクがあった。

設計の核心は二層分離構造にある。`graph.yaml`が機械可読なグラフトポロジー（ノードID・エッジ・ステータス）を保持し、`nodes/*.md`が各ノードのMarkdown本文（観察・発見・理由・open question）を保持する。これによりLLMなしでトポロジーを走査でき、必要なノードだけを選択的に読み込める。

初期のノードタイプは8種類（question/source/finding/candidate/decision/risk/rejected/next）、エッジタイプは9種類（derived_from/supports/weakens/contradicts/led_to/answers/selects/defers/blocked_by）という最小vocabularyから始めた。「vocabulary を小さく保つ」方針はrole分離を細分化してから再統合した過去の失敗から来ている。

schema version 2では`title`フィールドをtop-levelから削除し、root node idのみを残した。グラフの意味はroot nodeのMarkdown本文が持つという原則を徹底した。

グラフが増えるにつれ一覧性の問題が生じたため、`catalog.yaml`をdiscovery indexとして追加。整合性検証用の`run-exploration-check.sh`も実装した。agent がグラフを参照するタイミングを制御するため`context-reading.md` skillを追加し、task intake段階で「グラフを使うか・既存グラフに追記するか・なぜ使わないか」を明示する設計に変更した。

Stage 9が落ち着くとplanningの記録も同じ構造で扱えると気づき、`arca/explorations/`から`arca/contexts/`へ改名、IDも`EXP-*`から`CTX-*`へ変更した。explorationとplanningで共通vocabularyを使うため分離する意味がなかった。

重要な設計思想として、グラフを「探索が終わってから結果を整理するもの」にしないことを強調している。rejected/risk/nextノードをfirst-classに扱い、探索しながらリアルタイムにノードを追加することで、結論だけでなく過程が記録に残る。

監査エージェント開発への示唆：判断根拠のトレーサビリティはaudit trailの本質であり、この「操作の記録 vs 要約」という区別はLangGraphベースの監査エージェントにおけるstate管理・handoff設計にも直接応用できる。なぜその判断に至ったかを機械可読な形でリポジトリに残す仕組みは、LLM-as-judgeの評価ログやReActの思考ステップ保存と組み合わせることで、監査エージェントの説明可能性を大幅に向上させる可能性がある。

## アイデア

- 「グラフをworkflow authorityにしてはならない」という制約を先に明示するアプローチ：新しいartifactが既存のworkflowを乗っ取るリスクを設計初期に制限する手法は、多エージェントシステムの責務分離設計に応用できる
- graph.yaml（機械可読トポロジー）とnodes/*.md（人間可読本文）の二層分離：LLMなしでグラフ走査が可能になり、必要なノードだけを選択的に読み込む「全量読む必要をなくす」設計は、長大なcontext windowを節約するRAGの代替戦略として有効
- グラフを「操作の記録」として機能させるためにrejected/risk/nextノードをfirst-classに扱う設計：結論だけでなく却下候補・残存リスク・保留事項を記録することで、次のagentが同じ探索をやり直すコストを削減できる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **scaffold設計** (TODO: 読むべき)
- **グラフトポロジー** (TODO: 読むべき)
- **context window管理** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_6554 Arcaの観察：役割分離がエージェントの振る舞いを変え始めた
- /deep_6605 AI入力フォーマット完全ガイド: Markdownを起点にXML/JSON/YAMLをタスク別に切り替える
- /deep_609 将軍の城をシンデレラの城に改装した — OSSマルチエージェントフレームワークをフォークしてアイドル達を住まわせた話
- /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- /deep_1058 メタサーフェス逆設計のための自己進化型エージェントフレームワーク

## 原文リンク

[Arcaの探索グラフ：探索の記録をリポジトリに残すためのscaffold設計](https://zenn.dev/sisiodos/articles/c11580fb40978a)
