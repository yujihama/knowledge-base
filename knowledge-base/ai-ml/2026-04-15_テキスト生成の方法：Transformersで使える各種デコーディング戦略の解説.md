---
title: "テキスト生成の方法：Transformersで使える各種デコーディング戦略の解説"
url: "https://huggingface.co/blog/how-to-generate"
date: 2026-04-15
tags: [デコーディング, Greedy Search, Beam Search, Top-K Sampling, Top-p Sampling, Nucleus Sampling, temperature, GPT-2, テキスト生成, Transformers, HuggingFace]
category: "ai-ml"
related: [1529, 1758, 1760, 1709, 1755]
memo: "[HF Blog] How to generate text: using different decoding methods for language generation with Transformers"
processed_at: "2026-04-15T12:49:02.408947"
---

## 要約

本記事はHugging Face公式ブログ（2020年3月公開、2023年7月更新）で、GPT-2を例に自己回帰型言語生成における主要なデコーディング手法を実装付きで解説する。

**自己回帰生成の基礎**：テキスト生成は条件付き次トークン確率の積として定式化される。P(w_{1:T}|W_0) = ∏P(w_t|w_{1:t-1}, W_0) であり、EOSトークンが生成されるまでトークンを逐次サンプリングする。

**Greedy Search**：各タイムステップで最高確率のトークンを選ぶ最もシンプルな手法。実装は`model.generate(**inputs, max_new_tokens=40)`のみ。欠点は低確率トークンの背後に隠れた高確率系列を見逃す点（例："dog"→"has"の確率0.9が"nice"→"woman"の確率0.4に負ける）と、繰り返しが発生しやすいこと。

**Beam Search**：num_beams個の仮説を並列に保持し、最終的に最高スコアの系列を選ぶ。num_beams=5でGreedy Searchより高確率な出力を得られるが、それでも繰り返しが発生する。`no_repeat_ngram_size=2`でn-gramペナルティを設定し同一2-gramの再出現を禁止することで改善可能。また`num_return_sequences`で複数候補を返すことができる。Beam Searchの本質的な問題として、人間のテキストは最高確率の系列ではなく、適度な「驚き」（低確率トークン）を含む点が挙げられ、機械翻訳・要約等のターゲットが明確なタスクには有効だが、open-ended生成には不向き。

**Sampling**：次トークンをその確率分布に従ってランダムに選ぶ手法。`do_sample=True, top_k=0`で有効化。`temperature`パラメータ（例：0.7）で分布をシャープ化し、低確率トークンの選択確率を下げられる。ただし完全なサンプリングでは稀に突飛な単語が選ばれる問題がある。

**Top-K Sampling**：確率上位K個のトークンのみに絞ってサンプリング。`top_k=50`が典型値。ただしKが固定のため、分布が均一な場合も急峻な場合も同じK個に制限される問題がある。

**Top-p（Nucleus）Sampling**：累積確率がp以上になるまでトークンを追加し、その集合からサンプリング。`top_p=0.92`等を設定。分布形状に応じて集合サイズが動的に変わるため、Top-Kより柔軟。Top-KとTop-pを組み合わせることも可能（両方設定した場合、どちらか小さい側のフィルタが適用される）。

実践的には`top_k=50, top_p=0.95, temperature=0.7`の組み合わせが広く使われる。監査エージェント開発では、ラベル生成・要約・根拠テキスト生成において、Greedy/Beamは再現性が高く、Sampling系は多様な説明候補生成に有用であり、タスク目的に応じた使い分けが重要。

## アイデア

- 人間の書くテキストは最高確率系列ではなく適度な「驚き」を含むという観察は、Beam Searchの限界を本質的に説明しており、open-ended生成でのサンプリング優位の根拠として重要
- Top-p（Nucleus）Samplingは語彙サイズ固定のTop-Kに対し、確率分布の形状に応じて動的に候補集合を変えるため、文脈依存の多様性制御としてより原理的
- temperatureによる分布のシャープ化・フラット化は、監査レポート生成のような正確性重視タスクと、アイデア出しのような多様性重視タスクの切り替えに直接応用できる

## 前提知識

- **自己回帰言語モデル** (TODO: 読むべき)
- **Softmax / 確率分布** (TODO: 読むべき)
- **GPT-2 / Transformer** (TODO: 読むべき)
- **トークナイザー** → /deep_158 翻訳か暗唱か？極低リソース言語の機械翻訳評価スコアの較正
- **HuggingFace Transformers** → /deep_1394 TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1758 🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）
- /deep_1755 カスタムデータセットでセマンティックセグメンテーションモデルをファインチューニングする

## 原文リンク

[テキスト生成の方法：Transformersで使える各種デコーディング戦略の解説](https://huggingface.co/blog/how-to-generate)
