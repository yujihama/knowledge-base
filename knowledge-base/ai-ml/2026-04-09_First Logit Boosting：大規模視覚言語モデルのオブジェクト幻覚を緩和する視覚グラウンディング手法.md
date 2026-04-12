---
title: "First Logit Boosting：大規模視覚言語モデルのオブジェクト幻覚を緩和する視覚グラウンディング手法"
url: "https://tldr.takara.ai/p/2604.00455"
date: 2026-04-09
tags: [LVLM, Object Hallucination, Contrastive Decoding, Logit Manipulation, Visual Grounding, Training-Free, Multimodal LLM]
category: "ai-ml"
memo: "[HF Daily Papers] First Logit Boosting: Visual Grounding Method to Mitigate Object Hallucination in Large Vision-Language Models"
related: [369, 641, 352, 493, 197]
processed_at: "2026-04-09T12:53:16.944701"
---

## 要約

大規模視覚言語モデル（LVLM）において、実際には存在しないオブジェクトを出力してしまう「オブジェクト幻覚（Object Hallucination）」は長年の課題である。本論文では、この問題に対してトレーニング不要な手法「First Logit Boosting（FLB）」を提案している。

既存のアプローチとして、再トレーニングや外部グラウンディングモデルの利用があるが、データコストや構造的複雑さという問題を抱える。トレーニング不要な手法としてContrastive Decoding（CD）が提案されているが、CDは「長期減衰（long-term decay）」という問題を持つ。これは、トークン生成が進むにつれて視覚情報への注意が弱まり、言語の事前確率（language prior）が支配的になる現象である。

FLBの仕組みはシンプルで、最初に生成されたトークンのロジット（logit）を保存し、それを後続のトークン予測に加算する。これにより、最初のトークンに埋め込まれた視覚情報が生成全体を通じて持続される。さらに、英語文の冒頭に頻出する「The」トークンの安定化効果により、幻覚的な単語の出力が抑制されるという副次的効果も観察されている。

実験では、CHAIR、POPE、MMHalBenchなど複数の幻覚評価ベンチマークにおいて、FLBが幻覚を大幅に削減することを確認。また、LLaVA、InstructBLIPなど複数のバックボーンモデルにわたって効果が確認されており、汎用性が高い。推論オーバーヘッドはほぼゼロであるため、リアルタイムのマルチモーダルシステムへの適用が容易である点も実用上の大きな利点である。コードはGitHubで公開されている（https://github.com/jiwooha20/FLB）。

## アイデア

- 最初のトークンのロジットを再利用するだけで視覚情報の長期減衰を防げるという、極めてシンプルかつ効果的なアイデアは、デコーディング戦略の設計において「初期状態の情報を後続ステップに引き継ぐ」という一般化可能な原則を示している
- 「Theトークンの安定化効果」という副次的発見は、言語モデルの内部表現における文頭トークンの特殊な役割を示唆しており、LLMのデコーディング機構の解釈可能性研究への新たな切り口となりうる
- トレーニング不要でオーバーヘッドがほぼゼロという特性は、本番環境のマルチモーダルシステムに対して既存モデルを変更せず品質向上できるプラグイン的アプローチの可能性を示す
## 関連記事

- /deep_369 視覚的In-Contextデモンストレーション選択の学習
- /deep_641 トレーニング不要なエキスパート言語モデルの動的アップサイクリング
- /deep_352 TED: マルチモーダル推論のためのトレーニング不要な経験蒸留
- /deep_493 TED: マルチモーダル推論のためのトレーニング不要な経験蒸留
- /deep_197 MuRF: ビジョン基盤モデルのマルチスケールポテンシャルを解放する

## 原文リンク

[First Logit Boosting：大規模視覚言語モデルのオブジェクト幻覚を緩和する視覚グラウンディング手法](https://tldr.takara.ai/p/2604.00455)
