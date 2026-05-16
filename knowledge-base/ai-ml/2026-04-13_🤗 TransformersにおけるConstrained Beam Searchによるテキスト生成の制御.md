---
title: "🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御"
url: "https://huggingface.co/blog/constrained-beam-search"
date: 2026-04-13
tags: [Constrained Beam Search, テキスト生成, Hugging Face Transformers, ニューラル機械翻訳, DisjunctiveConstraint, PhrasalConstraint, force_words_ids, T5, GPT-2, デコーディング戦略]
category: "ai-ml"
related: [1616, 1531, 1489, 706, 518]
memo: "[HF Blog] Guiding Text Generation with Constrained Beam Search in 🤗 Transformers"
processed_at: "2026-04-13T12:35:24.616346"
---

## 要約

Hugging Face Transformersに実装されたConstrained Beam Search（制約付きビームサーチ）の仕組みと使い方を解説したブログ記事。通常のビーム探索では出力に特定の単語やフレーズを含めることを保証できないが、本機能により`force_words_ids`引数を通じて生成テキストに必ず含まれるべき単語・フレーズを指定できるようになる。

【問題の背景】ニューラル機械翻訳などのタスクでは、辞書引きにより出力に含めるべき単語が事前にわかっている場合がある。また同じ確率スコアを持つ候補でも、フォーマル/インフォーマルなど文脈によって望ましさが異なるケースがある。これらを生成後フィルタリングではなく、生成段階で制御するのがConstrained Beam Searchの目的。

【技術的難しさ】ビームサーチはトークンを1つずつ逐次生成するため、将来のステップで特定トークンを出力すべきことを現在のステップで判断するのが困難。さらに複数制約の同時充足、制約間の優先順位付け、「いずれか1つを含む」ような選言的（Disjunctive）制約など、要件が複雑になると組み合わせ爆発が生じる。

【実装の仕組み】解決策として「制約状態機械（Constraint State Machine）」を各ビームに紐付ける方式を採用。各ビームがどの制約をどこまで充足しているかを追跡し、ビームステップごとに制約の進捗に基づいてトークン候補を絞り込む。制約を完全充足した完成ビームと未充足のビームをバンクで管理し、探索の効率化を図る。

【サポートする制約タイプ】(1) PhrasalConstraint: 特定のトークン列（フレーズ）を順序通り含めることを強制。(2) DisjunctiveConstraint: 複数の単語候補リストから少なくとも1つを含めることを強制。例えば「raining/rained/rains」のような語形変化を許容した制約が可能。

【使用例】T5-baseを用いた英独翻訳タスクで`force_words_ids=[tokenizer(['Sie']).input_ids]`を指定することで、通常の出力「Wie alt bist du?（インフォーマル）」を「Wie alt sind Sie?（フォーマル）」に誘導できることを示す。GPT-2を使った文章生成でも「scared」と「scream/screams/screaming/screamed」のいずれかを同時に含む文を生成させるデモを提供。

【監査エージェントへの示唆】監査レポート生成や根拠文書の要約において、必ず特定の規制用語・基準番号（例:「IAS 36」「IFRS 9」）を出力に含めることを保証するための制御機構として活用できる。LLM-as-judgeで評価基準となるキーワードを生成結果に強制包含させることで、評価の一貫性向上にも応用可能。

## アイデア

- 制約状態機械（Constraint State Machine）をビームごとに保持することで、逐次生成の中でも複数フレーズの充足状況を追跡できる設計は、エージェントの出力検証ループにも応用できる
- DisjunctiveConstraintにより語形変化（raining/rained/rains）を許容しながら意味的制約を課せる点は、多言語対応RAGシステムでの検索クエリ生成に活用できる
- 生成後フィルタリングではなく生成ステップ内に制約を組み込むアーキテクチャは、コスト・レイテンシの削減につながり、リアルタイム監査レポート生成における実用性が高い

## 前提知識

- **Beam Search** (TODO: 読むべき)
- **Seq2Seq / Encoder-Decoder** (TODO: 読むべき)
- **Tokenizer / input_ids** (TODO: 読むべき)
- **Transformers generate()** (TODO: 読むべき)
- **デコーディング戦略（greedy/sampling）** (TODO: 読むべき)

## 関連記事

- /deep_1616 TensorFlowとXLAによる高速テキスト生成
- /deep_1531 🤗 EvaluateライブラリによるLLMバイアス評価
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_706 バイリンガルBabyLMの育成：小規模モデルを用いた多言語言語習得の研究
- /deep_518 TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化

## 原文リンク

[🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御](https://huggingface.co/blog/constrained-beam-search)
