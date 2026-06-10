---
title: "LLMのIn-Context Learningによる世論調査データの欠損値補完"
url: "https://tldr.takara.ai/p/2606.09351"
date: 2026-06-10
tags: [In-Context Learning, 欠損値補完, 世論調査, MICE PMM, MNAR, gpt-oss-120b, American Trends Panel, sklearn API]
category: "ai-ml"
related: [1641, 369, 3516, 7386, 4840]
memo: "[HF Daily Papers] In-Context Learning for the Imputation of Public Opinion Data with Large Language Models"
processed_at: "2026-06-10T21:20:18.798103"
---

## 要約

世論調査データにおける欠損値補完（Imputation）にLLMのIn-Context Learning（ICL）を適用した研究。従来の統計的補完手法であるMICE PMM（Predictive Mean Matching）との比較評価を、American Trends Panelの15波・150の意見変数を対象に実施した。

欠損メカニズムは3種類を対象とする：完全ランダム欠損（MCAR）、ランダム欠損（MAR）、非ランダム欠損（MNAR）。MNARはデータの欠損がその値自体に依存するため、統計的手法では仮定が成立しにくく最も難しいケース。ICLアプローチはすべての欠損メカニズムにおいてMICE PMMより絶対誤差を一貫して低減し、特にMNARで最大の改善を示した。

最良構成はgpt-oss-120b（100件のin-contextサンプル）で、95%水準に近い名目上のカバレッジを達成しつつ、信頼区間の幅はMICE PMMの2〜5分の1まで縮小した。信頼区間が狭くてもカバレッジが維持されることは、単なる予測精度向上ではなく、不確実性推定の質の向上を意味する。

技術的なポイントとして、ICL設計の選択肢（コンテキスト例の数、サンプリング戦略等）を体系的に比較しており、100件のin-context examplesが最適であることを示した。また、本手法はscikit-learn互換のAPIを持つPythonパッケージとして公開されており、ローカルLLM・プロプライエタリLLM双方での利用が可能。

監査AI観点では、企業内調査・アンケートデータや内部統制評価における回答欠損への応用が考えられる。特にMNARのケース（例：不正に関わる従業員ほど回答を避ける傾向）では、統計手法より優れた補完精度が期待でき、監査サンプリングの品質向上に寄与しうる。

## アイデア

- MNAR（非ランダム欠損）でICLが最も効果を発揮する点：欠損が値依存である場合、LLMの持つ常識的知識や文脈理解が統計的仮定を超えられることを示唆する
- 信頼区間をMICE PMMの2〜5分の1に縮小しながら95%カバレッジを維持：予測精度と不確実性定量化を両立するICLの潜在力
- sklearn互換APIでローカルLLMにも対応：オープンソース実装により、センシティブな調査データをクラウドに送らずに補完できるプライバシー保護の実用性

## 前提知識

- **In-Context Learning (ICL)** (TODO: 読むべき)
- **MICE PMM** (TODO: 読むべき)
- **欠損メカニズム (MCAR/MAR/MNAR)** (TODO: 読むべき)
- **信頼区間・カバレッジ** (TODO: 読むべき)
- **sklearn API** (TODO: 読むべき)

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_369 視覚的In-Contextデモンストレーション選択の学習
- /deep_3516 見えないものを見る：シンボリック推論におけるTransformerの汎化能力について
- /deep_7386 文脈内演算子学習のスペクトル監査：ヤコビアンに基づく局所的演算子忠実性の評価
- /deep_4840 形状・対称性・構造：機械学習研究における数学の変化する役割

## 原文リンク

[LLMのIn-Context Learningによる世論調査データの欠損値補完](https://tldr.takara.ai/p/2606.09351)
