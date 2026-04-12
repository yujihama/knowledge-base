---
title: "StarCoder2とThe Stack v2：次世代オープンコードLLMの公開"
url: "https://huggingface.co/blog/starcoder2"
date: 2026-04-09
tags: [StarCoder2, コードLLM, Fill-in-the-Middle, Grouped Query Attention, The Stack v2, BigCode, オープンソース, 事前学習データ]
category: "ai-ml"
memo: "[HF Blog] StarCoder2 and The Stack v2"
related: [365, 722, 210, 322, 1216]
processed_at: "2026-04-09T12:24:23.977245"
---

## 要約

BigCode（Hugging FaceとServiceNowの共同研究組織）が2024年2月28日にStarCoder2を公開した。StarCoder2は3B・7B・15Bの3サイズのオープンコードLLMファミリーで、全モデルが新しいコードデータセット「The Stack v2」で学習されている。

【モデル仕様】全サイズでGrouped Query Attention（GQA）を採用し、コンテキストウィンドウ16,384トークン（スライディングウィンドウ注意機構4,096トークン）を持つ。学習目標はFill-in-the-Middle（FIM）。StarCoder2-3BはServiceNowが学習（17言語、3兆トークン以上）、StarCoder2-7BはHugging Faceが学習（17言語、3.5兆トークン以上）、StarCoder2-15BはNVIDIAがNeMoフレームワークとNVIDIAインフラを用いて学習（600言語以上、4兆トークン以上）。StarCoder2-15Bは同サイズクラスで最高性能を示し、33B以上のモデルと同等の評価結果を多数達成。StarCoder2-3BはStarCoder1-15Bと同等の性能を発揮する。

【The Stack v2】Software Heritageアーカイブ（InriaとUNESCOの非営利ソフトウェアアーカイブ）を基盤とした最大のオープンコードデータセット。v1比較でフルデータ6.4TB→67.5TB、重複排除後2.9TB→32.1TB、学習用トークン数約2,000億→約9,000億と大幅に拡張。言語・ライセンス検出手法の改善、フィルタリングヒューリスティクスの強化、リポジトリ単位でのグルーピング（リポジトリコンテキストを活用した学習が可能）が特徴。

【公開物】モデル（全3サイズ）、データセット（The Stack v2）、データ処理コード、学習コード、論文、VSCode拡張機能、コード全文検索ツール、学習データ包含確認ツールをすべてオープンに公開。ライセンスはBigCode OpenRAIL-M v1。

## アイデア

- リポジトリ単位でグルーピングされた学習データにより、ファイル間の依存関係やコンテキストを保持したコード生成が可能になる設計思想
- 3B〜15Bの3サイズを異なる組織（ServiceNow・HuggingFace・NVIDIA）が分担学習することで、各社のインフラ最適化手法を実証する分散開発モデル
- Software Heritageという非営利の文化財アーカイブをLLM学習の基盤とすることで、ライセンスコンプライアンスと大規模データ収集を両立するアプローチ
## 関連記事

- /deep_365 数学者の研究手法を変えるAIツール「Axplorer」——Axiom MathがPatternBoostを民主化
- /deep_722 数学者のやり方を変えようとするスタートアップ：Axiom MathのAxplorerとは
- /deep_210 数学者のための進化的パターン探索AI「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの新ツール
- /deep_322 数学者のための新AI探索ツール「Axplorer」——PatternBoostをMac Pro上で動作させたAxiom Mathの挑戦
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法

## 原文リンク

[StarCoder2とThe Stack v2：次世代オープンコードLLMの公開](https://huggingface.co/blog/starcoder2)
