---
title: "1行のコードでHugging Faceデータセットをインタラクティブに探索する"
url: "https://huggingface.co/blog/scalable-data-inspection"
date: 2026-04-09
tags: [Hugging Face, datasets, Renumics Spotlight, データ可視化, 埋め込みベクトル, ViT, CIFAR-100, データ検査, モデルデバッグ]
category: "ai-ml"
memo: "[HF Blog] Interactively explore your Huggingface dataset with one line of code"
processed_at: "2026-04-09T21:23:28.426408"
---

## 要約

Renumics Spotlightは、Hugging Faceの`datasets`ライブラリと直接統合し、`spotlight.show(ds)`の1行でMLデータセットのインタラクティブな可視化を実現するツール。70,000以上の公開データセットに対応し、画像・音声・動画・テキスト等のマルチモーダルデータを統一的に扱える。技術的な特徴として、Arrowテーブル形式のタブラーデータはメモリにロードしてクライアントサイドで効率的な分析を行い、音声・画像等のメモリ集約型データはオンデマンドで遅延ロードする設計を採用。データ型・ラベルマッピングはデータセットのfeatureから自動推論される。モデル結果（予測値・埋め込みベクトル）をデータセットに結合して可視化する機能が強力で、例えばCIFAR-100に対してViT（Vision Transformer）モデル`Ahmed9275/Vit-Cifar100`で768次元の埋め込みと予測を計算し、類似マップ・混同行列・Inspectorウィジェット等で失敗事例のクラスタを特定できる。`datasets.concatenate_datasets`でモデル結果を元データに横結合し、`spotlight.layouts.debug_classification`レイアウトで分類デバッグ用の標準UIを即座に構築可能。レイアウトはGUIで動的変更・保存・ロードでき、Python APIからも定義可能なため、EDA・モデルデバッグ・モデルモニタリングのワークフローをコード化して再現性を確保できる。Hugging Face Spacesと連携してデータセット・モデル結果の公開展示にも利用可能。`pip install renumics-spotlight datasets transformers[torch]`で導入できる。Greg Brockmanの「手動データ検査はMLにおいて最高のコスパを持つ活動」という言葉を引用し、データ検査のスケーラビリティ向上を主眼に置いたツールとして位置づけられている。

## アイデア

- モデルの埋め込みベクトルを使った類似マップで失敗事例クラスタを視覚的に特定する手法は、LLM-as-judgeの評価結果を可視化してエラーパターンを発見するのに応用できる
- データセットにモデル予測・埋め込みを横結合して一元管理するパターンは、エージェントの中間出力や評価スコアをトレース・検査するための設計パターンとして参考になる
- Python APIでレイアウトを定義しコード化することで、データ品質チェックやモデルモニタリングのワークフローを再現可能な形で標準化できる

## Yujiの取り組みへの示唆

監査エージェント開発において、LangGraphエージェントの中間出力・判定結果・埋め込みをHugging Face datasets形式で管理し、Spotlightで可視化するワークフローが構築できる。特にLLM-as-judgeの評価結果を埋め込みと組み合わせて類似マップ表示することで、エージェントの判断失敗パターンをクラスタ単位で特定しやすくなる。Pydanticで型付けした出力をdatasetsのfeaturesにマッピングする設計も親和性が高い。

## 原文リンク

[1行のコードでHugging Faceデータセットをインタラクティブに探索する](https://huggingface.co/blog/scalable-data-inspection)
