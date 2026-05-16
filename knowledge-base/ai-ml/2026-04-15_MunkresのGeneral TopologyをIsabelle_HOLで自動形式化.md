---
title: "MunkresのGeneral TopologyをIsabelle/HOLで自動形式化"
url: "https://tldr.takara.ai/p/2604.07455"
date: 2026-04-15
tags: [autoformalization, Isabelle/HOL, LLMエージェント, 定理証明, 形式検証, sledgehammer, 数学形式化, Claude Opus]
category: "ai-ml"
related: [976, 935, 1483, 631, 566]
memo: "[HF Daily Papers] Munkres' General Topology Autoformalized in Isabelle/HOL"
processed_at: "2026-04-15T12:45:14.784194"
---

## 要約

本論文は、LLM支援による数学テキストの自動形式化（autoformalization）実験を報告する。対象はJames Munkresの教科書「Topology」（第2〜8章、一般位相幾何学）の全39節であり、成果物は85,000行超のIsabelle/HOLコードとなった。形式化を担ったLLMベースのコーディングエージェントは、当初ChatGPT 5.2、途中からClaude Opus 4.6に切り替えて使用され、実作業期間は24日間。

形式化の完全性が特筆される。806件の定理・補題がすべて「sorry（未証明プレースホルダ）」ゼロで証明済みとなっており、Tychonoffの定理、Baireのカテゴリー定理、Nagata–Smirnov・Smirnovの距離化定理、Stone–Čechコンパクト化、Ascoliの定理、空間充填曲線（Peano曲線）などの主要結果を含む。

方法論の核心は「sorry-first」宣言型証明ワークフローとsledgehammer（Isabelleの自動証明タクティク）の大量活用の組み合わせである。sorry-firstとは、まず定理の主張（statement）を形式的に記述してsorriesでスタブを埋め、その後sledgehammer等で自動証明を充填していく手順を指す。この2段階アプローチにより、人間の監督コストを抑えつつ形式化の進行速度を高めることができた。

セッションログから人間–LLM間のインタラクションパターンも分析されており、LLMがコード生成・証明探索の主体となりつつも、一部の難所では人間の介入が有効だったことが示されている。比較対象としてMegalodon、HOL Light、Naproche等の関連形式化プロジェクトとの対比も行われている。

監査エージェント開発への示唆としては、「sorry-first」ワークフローはLLMによる段階的タスク分解と自動検証の組み合わせパターンとして注目できる。監査手続の形式化・自動検証（例: 内部統制要件の形式仕様記述と自動チェック）においても、まず要件の骨格を宣言的に記述し、個別の証明ステップをLLM＋自動ツールで充填する手順が有効な可能性がある。また、大量のドメイン知識（806件）を低コスト・短期間で形式化できた点は、GRC領域の規則体系の機械可読化にも応用できる。

## アイデア

- sorry-firstワークフロー：定理の主張を先に形式化してプレースホルダで埋め、後からsledgehammer等で自動証明を充填する手順が、LLM補助形式化の進行速度を大幅に改善する
- 24日・85,000行・sorry-ゼロという定量的成果が示すように、標準的な数学教科書レベルの形式化はLLM+証明支援ツールで既に「安価かつ高速」に実現可能な段階に達している
- 監査や規制対応の文脈で、ドメイン知識の形式仕様化（コンプライアンス要件→証明可能な命題）にsory-firstパターンを転用できる可能性がある

## 前提知識

- **Isabelle/HOL** (TODO: 読むべき)
- **定理証明支援系** (TODO: 読むべき)
- **sledgehammer** (TODO: 読むべき)
- **autoformalization** (TODO: 読むべき)
- **LLMコーディングエージェント** (TODO: 読むべき)

## 関連記事

- /deep_976 型検査によるコンプライアンス：Lean 4定理証明を用いた金融エージェントシステムの決定論的ガードレール
- /deep_935 高次元空間から安全クリティカルなAIシステムのための検証可能なODDカバレッジへ
- /deep_1483 構文は簡単、意味論は難しい：LLMによるLTL変換の評価
- /deep_631 ドメイン固有言語とSpeed-of-Light誘導を用いたGPUカーネル最適化エージェントの効率改善
- /deep_566 ドメイン固有言語とSpeed-of-Light誘導によるGPUカーネル最適化エージェントの効率改善

## 原文リンク

[MunkresのGeneral TopologyをIsabelle/HOLで自動形式化](https://tldr.takara.ai/p/2604.07455)
