---
title: "StarCoder2-Instruct: 完全透明・許諾自由なコード生成のための自己アライメント"
url: "https://huggingface.co/blog/sc2-instruct"
date: 2026-04-09
tags: [self-alignment, instruction-tuning, StarCoder2, OSS-Instruct, execution-guided-validation, code-generation, SFT, LLM-as-judge]
category: "ai-ml"
memo: "[HF Blog] StarCoder2-Instruct: Fully Transparent and Permissive Self-Alignment for Code Generation"
processed_at: "2026-04-09T09:50:39.477950"
---

## 要約

StarCoder2-15B-Instruct-v0.1は、GPT-4などの独自大規模LLMへの蒸留や人手アノテーションを一切使わず、StarCoder2-15B自身が生成したデータのみでファインチューニングされた初のコードLLM。パイプラインは3段階で構成される。①The Stack V1から高品質なPython関数をシードとして抽出（500万関数中、Pyright静的型チェック・ベンチマーク汚染除去・StarCoder2-15B自身によるdocstring品質フィルタリング・MinHashによる近似重複除去を経て25万件に絞り込み）。②Self-OSS-Instructにより、各シード関数からコード概念（パターンマッチング、データ型変換など）を抽出し、16-shotのin-context learningで多様な指示を自動生成（23.8万件）。③実行ベースの自己検証：各指示に対しStarCoder2-15Bが(自然言語回答, テストコード)のペアを10サンプル生成し、サンドボックス実行でテストをパスしたもののみを採用。238k×10=240万サンプルから50万件がテストを通過し、重複除去後5万件をSFTデータセットとして使用。評価結果として、HumanEvalで72.6点を達成しCodeLlama-70B-Instruct（72.0点）を上回る。LiveCodeBenchでは同サイズモデル中トップを記録し、GPT-4蒸留データで訓練したOpenCodeInterpreter-SC2-15Bをも超える。EvalPlusベンチマークでは許諾自由モデルの中で首位となり、Grok-1・DBRX・Command-R+を上回る。特筆すべき知見は「教師モデルの分布とは異なる蒸留データより、自分自身の分布内データから学ぶ方が効果的」という点で、モデル間の分布ギャップが蒸留の効果を制限することを実証した。完全オープンソース・Apache 2.0ライセンスで商用利用・蒸留も許容される。

## アイデア

- 自己検証ループ（Self-Validation）: モデルが回答と同時にテストコードを生成し、実行結果でフィルタリングする手法は、LLM-as-judgeの代替として低コストかつ客観的な品質保証を実現する
- 分布内学習の優位性: 蒸留元モデルとの分布ギャップがむしろ学習を阻害するという実証結果は、小規模モデルの自己改善設計において重要な示唆を持つ
- コード概念の明示的抽出: 「再帰」「データ直列化」などの概念をラベルとして中間表現に持つことで、指示の多様性を構造的に担保する設計が興味深い
## 関連記事

- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_251 証明可能なプライバシーを保証するAI利用インサイト取得システム（Google Research）
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ

## 原文リンク

[StarCoder2-Instruct: 完全透明・許諾自由なコード生成のための自己アライメント](https://huggingface.co/blog/sc2-instruct)
