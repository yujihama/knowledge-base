---
title: "Nested Learning：継続学習のための新しいMLパラダイム"
url: "https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/"
date: 2026-04-03
tags: [Nested Learning, Continual Learning, Catastrophic Forgetting, Associative Memory, Titans, Transformer, NeurIPS 2025, 自己修正アーキテクチャ, Continuum Memory System]
category: "ai-ml"
memo: "[Google AI Blog] Introducing Nested Learning: A new ML paradigm for continual learning"
related: [938, 199, 1494, 113, 216]
processed_at: "2026-04-03T21:00:32.476980"
---

## 要約

Googleリサーチ（Ali Behrouz, Vahab Mirrokni）がNeurIPS 2025で発表した「Nested Learning」は、機械学習モデルを「相互に入れ子になった複数の最適化問題の集合」として捉え直すパラダイムである。従来のディープラーニングでは、モデルのアーキテクチャ（ネットワーク構造）と最適化アルゴリズム（学習ルール）を別々のものとして扱ってきたが、Nested Learningはこの二つを「更新頻度の異なる同一概念の異なるレベル」として統一的に定式化する。

核心的な洞察は、バックプロパゲーション自体を連想記憶（Associative Memory）としてモデル化できるという点にある。Transformerのアテンション機構や全結合層も同様に連想記憶モジュールとして定式化され、それぞれが異なる「更新頻度レート」を持つ最適化レベルとして階層化される。この視点により、既存のモデルは実質的に内部コンテキストフローを「圧縮」しているに過ぎないことが示される。

このパラダイムから派生した実用的な貢献が2つある。第一に「Deep Optimizers」：従来のmomentumベースの最適化器をL2回帰損失ベースで再定式化することで、不完全なデータに対してより頑健な更新則を導出する。第二に「Continuum Memory System（CMS）」：標準TransformerのFFN（長期記憶）とSequence Model（短期記憶）という二層構造を、異なる更新頻度を持つメモリモジュールのスペクトラムに拡張した概念。

プルーフオブコンセプトとして設計された「Hope」は、Titansアーキテクチャをベースにした自己修正型リカレントアーキテクチャ。Titansは「意外性」に基づいてメモリを優先する長期記憶モジュールだが、パラメータ更新が2レベルに限定されているため1次のin-context learningしか行えない。Hopeはこれを無限レベルの自己参照的学習に拡張し、CMSブロックで大規模コンテキストウィンドウにも対応する。

実験結果では、Hopeは言語モデリング・常識推論・継続学習・知識組み込みタスクにおいて、現代のリカレントモデルおよび標準Transformerを上回るperplexityと精度を達成。特に継続学習タスクでCatastrophic Forgettingを大幅に軽減することが示された。

## アイデア

- アーキテクチャと最適化アルゴリズムを『更新頻度の異なる同一概念』として統一する視点は、エージェント設計における短期ワーキングメモリ・長期知識ストア・メタ学習層の階層化に直接応用可能
- Continuum Memory System（CMS）の『異なる頻度で更新されるメモリスペクトラム』という概念は、RAGシステムのキャッシュ戦略（ホット/コールドデータの分離）の理論的根拠として活用できる
- バックプロパゲーションを連想記憶として再定式化するアプローチは、LLM-as-judgeにおけるフィードバック信号の処理メカニズムを新たな角度から分析する視座を提供する
## 関連記事

- /deep_938 精度は一致、幾何学は異なる：LLMポストトレーニングにおける進化戦略とGRPOの比較
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界

## 原文リンク

[Nested Learning：継続学習のための新しいMLパラダイム](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/)
