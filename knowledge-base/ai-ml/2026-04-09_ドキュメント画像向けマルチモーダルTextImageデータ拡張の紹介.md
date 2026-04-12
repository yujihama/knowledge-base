---
title: "ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介"
url: "https://huggingface.co/blog/doc_aug_hf_alb"
date: 2026-04-09
tags: [VLM, データ拡張, Albumentations, OCR, ドキュメント理解, マルチモーダル, SynthDOG, ファインチューニング]
category: "ai-ml"
memo: "[HF Blog] Introducing TextImage Augmentation for Document Images"
processed_at: "2026-04-09T09:04:32.352664"
---

## 要約

HuggingFaceとAlbumentations AIの共同開発による、ドキュメント画像専用のデータ拡張パイプライン「TextImage Augmentation」の解説記事。Vision Language Model（VLM）のファインチューニング時に限られたデータセットへ対応するための技術で、画像とテキストアノテーションを同時に変換する「マルチモーダル」拡張を実現する。

従来の画像変換（リサイズ、ブラー、背景色変更）はOCRや文字認識精度を低下させる問題があったが、本手法はテキストの整合性を保ちながらデータを増幅できる点が特徴。具体的な処理フローとしては、(1) ドキュメント内の行をランダム選択（`fraction_range`ハイパーパラメータで制御）、(2) 対象テキストにRandom Deletion・Random Swap・Stopword Insertionのいずれかを適用、(3) テキスト挿入箇所の画像をブラックアウトしてインペイントし、`font_size_fraction_range`でバウンディングボックス高さに対するフォントサイズ比率を指定する流れ。

主な機能は2つ。1つ目は任意テキストのオーバーレイで、ランダム背景画像に新規テキストを描画して合成データを生成するSynthDOG類似の手法。2つ目は既存テキストの拡張で、前述3種の変換を施したテキストを元のバウンディングボックスに再描画する。どちらも変換後のテキストとバウンディングボックスを取得して学習に利用可能。

Albumentations の `A.TextImage` クラスとして実装されており、`A.PlanckianJitter`（色バランス調整）や `A.Affine`（スケール・回転・平行移動）といった他の画像変換と `A.Compose` でパイプライン化できる。入力データとしてIDLおよびPDFAデータセット（行単位のバウンディングボックス付き）を想定しており、正規化Pascal VOC形式のバウンディングボックスを前処理して `textimage_metadata` として渡す実装例も掲載されている。なお初期バージョンに含まれていた同義語置換（Synonym Replacement）は処理時間のオーバーヘッドが大きいため削除された。インストールはpillow・albumentations・nltk（stopwords）で完結する。

## アイデア

- テキストと画像アノテーションを同時に変換する「マルチモーダル拡張」の考え方は、単一モダリティの拡張では破綻しがちな整合性問題を根本解決する設計として汎用性が高い
- バウンディングボックスをフォントサイズの代理変数として使うインペイント手法は、ラベル付きデータから自然な外観の合成データを生成する低コストな近似として実用的
- Random Deletion・Swap・InsertionというNLPの古典的テキスト拡張をビジョンパイプラインに統合した点が、テキストリッチな画像ドメインへの適用を広げる橋渡しになっている
## 関連記事

- /deep_305 オープンモデルでOCRパイプラインを強化する：VLMベースドキュメントAIの実践ガイド
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_1117 WebSightデータセット：スクリーンショットからHTMLコードへの変換を実現する大規模合成データセット
- /deep_234 VOLMO: 眼科特化型汎用オープン大規模マルチモーダルモデル
- /deep_1257 Saliency-R1: 顕著性マップ整合報酬によるVLMの解釈可能性と忠実性の強化

## 原文リンク

[ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介](https://huggingface.co/blog/doc_aug_hf_alb)
