---
title: "自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点"
url: "https://zenn.dev/analysis/articles/thought-analyzer-self-evolution"
date: 2026-04-15
tags: [AlphaEvolve, LLM wiki, 自己進化, 評価器独立性, agentic, 自己参照ループ, thought-analyzer]
category: "agent-arch"
related: [365, 1459, 722, 210, 322]
memo: "[Zenn LLM] 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点"
processed_at: "2026-04-15T12:41:56.778455"
---

## 要約

自己進化型AIシステムの成否を分ける根本的な条件として「評価器の独立性」を論じた考察記事。同週に話題になった2つの事例を対比軸に据える。

一方は、KarpathyのLLM wiki方式（raw/ディレクトリにソースを投入しLLMが自動整理・更新）をフロントエンド・CRMのコードベースに応用した試みだ。コードをLLMに入力→LLMがwikiを更新→wikiがコード改善提案を生む、という自己参照ループを設計した。しかしコメント欄の実験報告によれば、数回の更新サイクル後に「正しいものを自信を持って書き換え始める」という劣化が生じた。原因は評価器の不在：「この変更は改善か？」をLLM自身が判断するため、LLMは一貫して「良い変更だ」と確信し続け、誤った自己強化ループが走る。

もう一方はGoogle DeepMindのAlphaEvolve。ハイパーパラメータ調整ではなくアルゴリズム自体をLLMが書き換えて自律進化させるシステムで、数学的証明とベンチマークスコアという生成器から独立した評価器を持つ。この外部検証により、「LLMが改善と思うかどうか」に依存せず客観的な優劣判定が可能となり、人間の科学者を上回るアルゴリズムを生成した実績を持つ。

両者の構造的差異を表で整理すると：LLM wiki自己進化は生成器＝評価器（同一のLLM）、AlphaEvolveは生成器と評価器が独立。自己進化が機能するための最小条件は「評価器が生成器の認知構造から独立していること」であり、具体的な独立評価器の例として数学的証明、CI/CDパイプラインのテスト通過率・パフォーマンス指標、A/Bテストによる実ユーザー行動データが挙げられる。

この原則は人間×AI協働にも敷衍される。「最近うまく使えるようになった気がする」という主観的印象だけでは評価器が存在しないため、LLM wiki失敗例と同じ構造（生成側が生成側を評価）に陥る可能性がある。著者はthought-analyzerを提示し、会話ログからintegrative_complexityやspecification_precisionを定量測定することで「評価器を持つ」状態を作れると主張する。

監査エージェント開発への示唆：自己改善ループを持つエージェント設計においては、LLMによる自己評価だけでなくルールベースの検証・外部テストスイート・人間レビューなど独立評価器を必ずアーキテクチャに組み込む必要がある。評価器なしの自律改善は品質の見かけ上の向上と実際の劣化を区別できない。

## アイデア

- 「評価器が生成器から独立していること」が自己進化システムの成否を決める必要十分条件であるという定式化は、エージェント設計の原則として汎用性が高い
- AlphaEvolveの成功要因をアーキテクチャ構造の差として説明する比較フレームワークは、LLM-as-judgeの限界を明確に示す実例として有用
- 人間×AI協働における「改善の錯覚」問題をthought-analyzerで定量化するアプローチは、監査エージェントの品質保証設計（外部ベンチマーク・テストスイートの必須化）に直接応用できる

## 前提知識

- **AlphaEvolve** → /deep_175 スタートアップAxiom Mathが数学者の研究方法を変えようとしている——AIパターン探索ツール「Axplorer」
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **自己参照ループ** (TODO: 読むべき)
- **強化学習の報酬設計** (TODO: 読むべき)
- **評価器／生成器分離** (TODO: 読むべき)

## 関連記事

- /deep_365 数学者の研究手法を変えるAIツール「Axplorer」——Axiom MathがPatternBoostを民主化
- /deep_1459 数学者の研究を変えるAIツール「Axplorer」——PatternBoostをMac Pro上で動作させるAxiom Mathの取り組み
- /deep_722 数学者のやり方を変えようとするスタートアップ：Axiom MathのAxplorerとは
- /deep_210 数学者のための進化的パターン探索AI「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの新ツール
- /deep_322 数学者のための新AI探索ツール「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの挑戦

## 原文リンク

[自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点](https://zenn.dev/analysis/articles/thought-analyzer-self-evolution)
