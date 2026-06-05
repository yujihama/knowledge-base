---
title: "NVIDIA LocateAnything-3B を試してみた：マルチモーダル物体位置特定モデルの実装レポート"
url: "https://zenn.dev/hitoruna/articles/9494c8dbdc7c40"
date: 2026-06-05
tags: [NVIDIA, LocateAnything-3B, VLM, 物体検出, Hugging Face, マルチモーダル, BoundingBox, transformers]
category: "ai-ml"
related: [21, 1709, 1707, 2511, 1669]
memo: "[Zenn 機械学習] NVIDIA Locate Anything-3Bを試してみました"
processed_at: "2026-06-05T09:21:32.258992"
---

## 要約

NVIDIAが公開したビジョン言語モデル「LocateAnything-3B」をGoogle Colab上で実際に動作させた実践レポート。モデルはHugging Faceで公開されており、transformers 4.57.1（v5は非対応）とdecord、lmdbを依存ライブラリとして使用する。

処理フローは以下の通り。AutoTokenizerとAutoProcessorで`nvidia/LocateAnything-3B`をロードし、入力画像とテキストプロンプトをマルチモーダル対話形式に構造化する。processor.apply_chat_templateでOpenAI互換のchat template形式（im_start/im_endトークン）を適用し、processorがinput_ids（トークン化テキスト）・attention_mask・pixel_values（正規化画像テンソル）の3要素を含む入力辞書を生成する。

モデルはAutoModel.from_pretrainedでbfloat16精度・GPU実行でロードし、model.generateにinput_ids・attention_mask・pixel_values・image_grid_hwsを渡して推論を実行。max_new_tokensは64に設定。

出力はBBox座標を`<box><x1><y1><x2><y2></box>`形式のXMLライクなトークン列として返す。座標値は0〜1000のスケールで正規化されており、実際のピクセル座標への変換は「座標値 / 1000 × 画像幅（高さ）」で計算する。変換後、PIL ImageDrawでバウンディングボックスを赤枠として描画することで検出結果を可視化する。

実験では犬と猫が写った画像（800×534px）を使用し、「Locate the animals on the image」というシンプルな自然言語プロンプトで複数の動物を同時に位置特定することに成功している。

監査エージェント開発への示唆としては、自然言語プロンプトで任意オブジェクトの位置特定が可能な点が注目される。監査現場での証憑書類中の特定項目（印鑑・署名・金額欄等）の自動検出パイプラインに応用できる可能性があり、VLMベースの文書解析エージェントのコンポーネントとして組み込む際の参考実装として有用。

## アイデア

- BBox座標を0〜1000スケールのトークン列として出力する設計により、座標予測をテキスト生成タスクとして扱い、decoder-onlyアーキテクチャで物体検出を実現している点
- image_grid_hwsパラメータを別途渡す設計から、画像を固定グリッドに分割してパッチ埋め込みする処理が推測され、高解像度画像への対応と位置情報保持の両立を図っている点
- transformers 4.57.1でのみ動作しv5が非対応である点は、trust_remote_codeで読み込むカスタムモデリングコードがAPIの破壊的変更に依存していることを示しており、本番利用時の依存管理の難しさを示唆する

## 前提知識

- **Vision Language Model (VLM)** (TODO: 読むべき)
- **Hugging Face transformers** → /deep_1573 Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する
- **Chat Template** (TODO: 読むべき)
- **Bounding Box正規化座標** (TODO: 読むべき)
- **AutoModel / AutoProcessor** (TODO: 読むべき)

## 関連記事

- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）
- /deep_1707 機械学習によるカスタマーサービスの強化：HuggingFaceエコシステムを使った感情分析パイプラインの実装
- /deep_2511 患者教育をマルチターン・マルチモーダルインタラクションとして再考する
- /deep_1669 倫理原則を研究ライフサイクルの核心に据える：Hugging Face マルチモーダルプロジェクトの倫理憲章

## 原文リンク

[NVIDIA LocateAnything-3B を試してみた：マルチモーダル物体位置特定モデルの実装レポート](https://zenn.dev/hitoruna/articles/9494c8dbdc7c40)
