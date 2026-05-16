---
title: "AI評価が専門家と一般人で大きく乖離する理由：Stanford AI Index 2026が示す「ジャギー・フロンティア」の現実"
url: "https://www.technologyreview.com/2026/04/13/1135720/why-opinion-on-ai-is-so-divided/"
date: 2026-04-26
tags: [Stanford AI Index, jagged frontier, LLM評価, Gemini Deep Think, Claude Code, AI認識格差, TSMC]
category: "ai-ml"
related: [2889, 2574, 2275, 2771, 2036]
memo: "[MIT Technology Review AI] Why opinion on AI is so divided"
processed_at: "2026-04-26T12:09:03.711597"
---

## 要約

Stanford AI Index 2026の発表を受け、MIT Technology ReviewのコラムニストがAIに対する認識の分断構造を分析した記事。最も際立つ統計は、AIの雇用への影響について「肯定的」と答えた米国専門家が73%であるのに対し、一般市民はわずか23%という50ポイントもの乖離だ。同様の格差は経済・医療分野でも確認されている。

記事はこの乖離を「jagged frontier（ジャギー・フロンティア）」の概念で説明する。最新LLMはコーディングや数学など正解が明確なタスクでは飛躍的に性能が向上している一方、それ以外のオープンエンドなタスクでは依然として凡ミスを犯す。具体例として、Google DeepMindのGemini Deep ThinkがInternational Math Olympiadで金メダル相当のスコアを達成しながら、アナログ時計の読み取りを50%の確率で失敗するという非対称性が挙げられている。

AI研究者Andrej Karpathyの指摘も引用されており、月200ドルを払ってClaude Codeを使うパワーユーザーと、半年前に無料版で結婚式の計画を立てようとした一般ユーザーとでは、実質的に異なる技術を経験しており、両者は「話が噛み合っていない（speaking past each other）」状態にあると分析する。

ハードウェア面では、TSMCが主要AIチップのほぼすべてを製造しているという極端な集中リスクも指摘。米国のデータセンター数は5,427拠点と、2位の国の10倍以上であることも示されている。

監査エージェント開発への示唆としては、AIシステムの能力評価に「どのタスク領域か」を明示することが重要であり、コーディング・数学などの定型タスクと、監査判断・リスク評価などのオープンエンドタスクでは性能の信頼性が大きく異なる点を設計段階で考慮すべきという点が挙げられる。エージェントの適用領域をjagged frontierの「得意な斜面」に集中させる設計判断が実用上の鍵となる。

## アイデア

- 「jagged frontier」の概念：LLMはコーディング・数学など検証可能なタスクで極めて高性能だが、アナログ時計読み取りのような一見簡単なタスクでも50%失敗するという非対称性は、エージェント設計でのタスク選定基準として直接応用できる
- 専門家vs一般市民の73% vs 23%という認識ギャップは、AIツールの使用強度（特にコーディング用途）と相関しており、評価者バイアスを考慮したAI導入効果測定の必要性を示す
- TSMCへの一極集中というサプライチェーンリスクは、AIインフラの地政学的脆弱性を定量的に示す事例であり、AIシステムの事業継続計画（BCP）設計に組み込むべき外部リスク要因

## 前提知識

- **LLM (Large Language Model)** (TODO: 読むべき)
- **jagged frontier** → /deep_1982 AI評価がこれほど二極化する理由：専門家と一般公衆の間の50ポイントギャップ
- **Stanford AI Index** → /deep_1983 AIの現状を理解するためのデータ：Stanford AI Index 2026の主要チャート解説
- **TSMC / AI chip supply chain** (TODO: 読むべき)
- **Gemini Deep Think** → /deep_1982 AI評価がこれほど二極化する理由：専門家と一般公衆の間の50ポイントギャップ

## 関連記事

- /deep_2889 現在のAIの状況を理解するためのチャート集：Stanford AI Index 2026レポート解説
- /deep_2574 AIの現状を理解するためのデータ：Stanford AI Index 2026の主要チャート解説
- /deep_2275 AIの現状を理解するためのデータ集：Stanford AI Index 2026の主要ポイント
- /deep_2771 AIの現状を理解するためのチャート集：スタンフォード2026 AIインデックス解説
- /deep_2036 AIの現状を理解するためのチャート集：Stanford AI Index 2026年版の主要知見

## 原文リンク

[AI評価が専門家と一般人で大きく乖離する理由：Stanford AI Index 2026が示す「ジャギー・フロンティア」の現実](https://www.technologyreview.com/2026/04/13/1135720/why-opinion-on-ai-is-so-divided/)
