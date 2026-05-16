---
title: "AutoNLPとProdigyによるアクティブラーニングパイプラインの構築"
url: "https://huggingface.co/blog/autonlp-prodigy"
date: 2026-04-14
tags: [AutoNLP, Prodigy, アクティブラーニング, NER, トークン分類, HuggingFace, spaCy, IOBタグ]
category: "ai-ml"
related: [1213, 1354, 1572, 1529, 1494]
memo: "[HF Blog] Active Learning with AutoNLP and Prodigy"
processed_at: "2026-04-14T12:10:11.760131"
---

## 要約

本記事は、Hugging FaceのAutoNLPとExplosion社のアノテーションツールProdigyを組み合わせたアクティブラーニングパイプラインの構築手順を、BBCニュース分類データセットを題材に解説したチュートリアルである。

アクティブラーニングとは、ラベル付きデータを反復的に追加し、モデルを再学習してエンドユーザーへ提供するサイクルを繰り返すプロセスであり、人間によるアノテーション作業が継続的に必要となる。

AutoNLPはHugging Faceが開発したノーコード・ローコードのモデル学習フレームワークで、Transformers・Datasetsなどのエコシステム上に構築されており、分類・トークン分類・QA・要約など多数のNLPタスクに対応する。1モデルあたり最低10ドルから利用可能で、ハイパーパラメータチューニングを自動で行う。

ProdigyはspaCyの開発元Explosionが提供する商用Webベースアノテーションツールで、NERやテキスト分類のほかコンピュータビジョンタスクにも対応し、カスタムタスク定義も可能。

実験ではまず既存カテゴリラベルを使いBBCニュースの多クラス分類モデルを構築し、15モデルを約15分で学習、最高精度98.67%を達成した。次にNERラベルが存在しなかった同データセットに対し、Prodigyで`prodigy ner.manual bbc blank:en BBC_News_Train.csv --label PERSON,ORG,PRODUCT,LOCATION`コマンドを用いてPERSON・ORG・PRODUCT・LOCATIONの4エンティティをアノテーション。ProdigyのDB出力をIOBタグ形式のJSONLに変換するスクリプトを介してAutoNLPへアップロードし、トークン分類モデルを反復学習させた。

サンプル数による性能推移は明確で、約20サンプル時点ではAccuracy約86%・Precision/Recall≒0、約70サンプルでAccuracy 92%・Precision 0.52・Recall 0.42、約150サンプルでAccuracy 95.7%・Precision 0.64・Recall 0.76、約250サンプルでAccuracy 95.9%・Precision 0.73・Recall 0.79と段階的に向上した。わずか250件のラベルで実用的なNERモデルが構築可能であることを示している。

監査エージェント開発への示唆として、監査文書・契約書・報告書を対象としたNER（組織名・金額・日付・リスク用語の抽出）パイプラインをアクティブラーニングで段階的に構築できる点が重要である。少量の人手アノテーションから始めてモデル精度を継続的に改善するこのアプローチは、専門ドメインのラベルデータが乏しい内部監査領域に直接適用可能であり、AutoNLPのAPI経由学習とProdigyのインタラクティブアノテーションを組み合わせることでアノテーションコストを最小化できる。

## アイデア

- 250サンプルという極めて少量のアノテーションでNERモデルのPrecision 0.73・Recall 0.79を達成しており、ドメイン特化NERの低コスト構築手法として監査文書解析に直接転用できる
- ProdigyのDBからIOB形式JSONLへの変換スクリプトが示すように、アノテーションツールと学習基盤の間のフォーマット変換がパイプラインのボトルネックになりやすく、この変換層の標準化が実用化の鍵となる
- 分類モデル（98.67%精度）とNERモデルを組み合わせることで、記事カテゴリ判定とエンティティ抽出を同時に行うハイブリッドな情報抽出システムが構築可能であり、構造化されていない監査証跡の自動解析に応用できる

## 前提知識

- **Named Entity Recognition** (TODO: 読むべき)
- **IOBタグ** (TODO: 読むべき)
- **Transformers fine-tuning** (TODO: 読むべき)
- **アクティブラーニング** → /deep_1213 Prodigy-HFの紹介：Hugging Faceとの直接統合
- **トークン分類** (TODO: 読むべき)

## 関連記事

- /deep_1213 Prodigy-HFの紹介：Hugging Faceとの直接統合
- /deep_1354 Hugging Face Hub：美術館・図書館・文書館・博物館（GLAM）向け活用ガイド
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[AutoNLPとProdigyによるアクティブラーニングパイプラインの構築](https://huggingface.co/blog/autonlp-prodigy)
