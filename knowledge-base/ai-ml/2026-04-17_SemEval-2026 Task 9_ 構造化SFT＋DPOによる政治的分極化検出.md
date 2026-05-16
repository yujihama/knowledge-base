---
title: "SemEval-2026 Task 9: 構造化SFT＋DPOによる政治的分極化検出"
url: "https://tldr.takara.ai/p/2604.11121"
date: 2026-04-17
tags: [DPO, SFT, LoRA, Qwen2.5, 分極化検出, SemEval, スロットフィリング, 偽陰性削減, 選好最適化]
category: "ai-ml"
related: [265, 1183, 405, 1397, 715]
memo: "[HF Daily Papers] BITS Pilani at SemEval-2026 Task 9: Structured Supervised Fine-Tuning with DPO Refinement for Polarization Detection"
processed_at: "2026-04-17T12:17:59.141351"
---

## 要約

本論文はSemEval-2026 POLAR共有タスク（オンライン上の政治的分極化の検出・分類）に対し、2段階の学習アプローチを提案する。

【背景・課題】オンライン上の政治的分極化の自動検出は、微妙なレトリック、暗黙的なフレーミング、および人間によるアノテーションコストの高さにより困難である。多言語・多文化・複数イベントにまたがる分類が求められる点もハードルを上げている。

【手法】第1段階として、Qwen 2.5-7B-InstructをLoRAで教師ありファインチューニング（SFT）する。その際、単純なラベル予測ではなく、「ターゲット・クレームタイプ・顕現化チェックリスト・理由付け」という4要素からなるスロットフィリングテンプレートを用いる構造化出力を採用。これにより中間推論を可視化し、解釈可能性を高めている。

第2段階では、自動生成した選好ペア（preferred/dispreferred）を使ってDirect Preference Optimization（DPO）を適用する。目的は偽陰性（実際は分極化しているのに見逃すケース）の削減であり、追加の人手アノテーションなしに実現する点が特徴。

【結果】英語開発セットにおいて、DPO適用後はRecallが0.5085から0.7797へ大幅に向上し、Macro-F1スコアも約5ポイント改善された。精度（Precision）とRecallのトレードオフを制御しつつ、偽陰性の削減という目的を達成している。

【監査エージェント開発への示唆】構造化スロットフィリングテンプレートは監査AIにおけるリスク分類や不正兆候検出にも応用可能。特に「ターゲット・クレームタイプ・根拠」という出力構造は、監査証跡の生成や判断根拠の説明責任確保に直接転用できる。また、自動生成選好ペアによるDPOは、高コストな人手アノテーションを削減しながら特定エラータイプ（偽陰性）を集中的に減らす手法として、内部統制違反の見逃し率低減に活用できる。

## アイデア

- スロットフィリングテンプレート（target/claim type/manifestation/justification）による構造化出力がモデルの解釈可能性を高め、単純なラベル分類より汎化性能が向上する可能性
- 自動生成選好ペアによるDPOで特定エラータイプ（偽陰性）を狙い打ちに削減できる点：ラベルコストを抑えながらRecallを0.51→0.78に改善した実証
- 2段階学習（SFTで構造理解→DPOで誤分類補正）という分離設計が、タスク特化LLMのファインチューニング戦略として汎用性を持つ

## 前提知識

- **DPO (Direct Preference Optimization)** (TODO: 読むべき)
- **LoRA** → /deep_20 Mellea 0.4.0 と Granite Libraries リリース：構造化・検証可能・安全性対応AIワークフローの新展開
- **SFT (教師ありファインチューニング)** (TODO: 読むべき)
- **Qwen 2.5** (TODO: 読むべき)
- **Recall / Macro-F1** (TODO: 読むべき)

## 関連記事

- /deep_265 RapidFire AIによるTRLファインチューニングの最大20倍高速化
- /deep_1183 オープンLLMによるConstitutional AI（憲法的AI）の実装
- /deep_405 UnslothとHugging Face Jobsで無料でAIモデルをファインチューニングする方法
- /deep_1397 StackLLaMA: RLHFでLLaMAをトレーニングするための実践ガイド
- /deep_715 Open R1 アップデート #3: OlympicCoderモデルとCodeForces-CoTsデータセットの公開

## 原文リンク

[SemEval-2026 Task 9: 構造化SFT＋DPOによる政治的分極化検出](https://tldr.takara.ai/p/2604.11121)
