---
title: "Multiverse: 共有表現によるテキスト条件付きマルチゲームレベルブレンディング"
url: "https://arxiv.org/abs/2603.26782"
date: 2026-04-06
tags: [contrastive-learning, latent-space, multi-domain, procedural-content-generation, text-conditioned-generation, zero-shot, level-generation]
category: "ai-ml"
memo: "[arXiv cs.AI+cs.LG] Multiverse: Language-Conditioned Multi-Game Level Blending via Shared Representation"
processed_at: "2026-04-06T09:10:09.849037"
---

## 要約

本論文は、自然言語記述からゲームレベルを生成する「テキスト-to-レベル生成」をマルチゲーム対応に拡張するシステム「Multiverse」を提案する。従来のテキスト条件付きレベル生成器は単一ゲームドメインに限定されており、複数ゲームへの対応には異なるドメイン間での構造的関係を捉える共有表現学習が必要となる。Multiverseは、テキスト指示とレベル構造を整合させる共有潜在空間を学習し、そこにthreshold-based multi-positive contrastive supervision（閾値ベースの複数正例対照学習）を適用することで、ゲームをまたいで意味的に関連するレベル同士を結びつける。この表現学習により、異なるゲームのコンテンツを組み合わせる際にどの構造的特徴を保持すべきかをテキストで制御できるようになる。具体的な生成手法としては、潜在空間上での補間（latent interpolation）によるクロスゲームブレンディングと、組み合わせテキストプロンプトによるゼロショット生成の2つを実現している。実験では、学習済み表現がクロスゲームレベルブレンディングの制御性を支持し、同一ゲームジャンル内でのブレンディング品質を大幅に向上させることを示した。論文は8ページ・5図・4表の構成で、著者はIn-Chang Baekほか4名（韓国・セジョン大学のKyung-Joong Kim研究室系）。手法の核心はテキスト・レベル構造の共有潜在表現にあり、対照学習を複数正例に拡張することで異種ドメイン間のアライメントを実現している点が技術的に特徴的である。ゲームレベルという構造化データを横断的に扱う枠組みは、手続き型コンテンツ生成（PCG）の文脈で新しい方向性を示す。

## アイデア

- 閾値ベースの複数正例対照学習（threshold-based multi-positive contrastive supervision）により、異なるドメイン（ゲーム）間で意味的に類似したサンプルを同一潜在空間にアライメントする手法は、ドメイン横断的な表現学習の汎用パターンとして応用可能
- 潜在空間補間によるコンテンツブレンディングという概念は、ゲームに限らず「複数ポリシー・複数ドメインの知識を連続的に合成する」エージェント設計への示唆を持つ
- ゼロショット生成を組み合わせテキストプロンプトから実現する点は、未知ドメインへの汎化手法として、RAGやLLM-as-judgeシステムにおける「未知カテゴリへの適応」問題と構造的に類似している

## 関連記事

- /deep_930 Ultrasound-CLIP: 超音波画像テキスト理解のためのセマンティック対照事前学習
- /deep_302 SensorLM: ウェアラブルセンサーの言語を学習するマルチモーダル基盤モデル
- /deep_160 音声言語モデルにおけるプロンプト増幅とゼロショット後期融合による音声感情認識
- /deep_499 自己教師あり表現学習のためのガウス結合埋め込み（GJE/GMJE）
- /deep_1172 操舵可能な視覚表現（Steerable Visual Representations）

## 原文リンク

[Multiverse: 共有表現によるテキスト条件付きマルチゲームレベルブレンディング](https://arxiv.org/abs/2603.26782)
