---
title: "Transformers.jsでMLパワードWebゲームを作る方法"
url: "https://huggingface.co/blog/ml-web-games"
date: 2026-04-10
tags: [Transformers.js, MobileViT, ONNX, ブラウザ推論, Web Workers, ファインチューニング, Quick Draw, Vite, React]
category: "ai-ml"
memo: "[HF Blog] Making ML-powered web games with Transformers.js"
related: [1, 1529, 1310, 1480, 1169]
processed_at: "2026-04-10T09:17:19.742793"
---

## 要約

本記事は、HuggingFaceのエンジニアがTransformers.jsを用いてブラウザ完結型のMLゲーム「Doodle Dash」を構築した手順を解説したチュートリアルである。

ゲームの概要は、Google Quick, Draw!に着想を得たスケッチ認識ゲームで、プレイヤーが60秒間でできるだけ多くのお題を描き、モデルが正解すれば次のお題に進む仕組み。1秒間に60回以上のリアルタイム推論をブラウザ上で実現している。

技術スタックは以下の通り。モデルにはapple/mobilevit-smallを採用。パラメータ数5.6M・ファイルサイズ約20MBの軽量Vision Transformerで、ImageNet-1kで事前学習済み。Google Quick, Draw!データセット（345カテゴリ・500万件超）のサブセットでファインチューニングし、Hugging Face Hub上に公開（Xenova/quickdraw-mobilevit-small）。

ブラウザ実行にはTransformers.jsを使用。内部的にONNX Runtimeを利用するため、PyTorchモデルをONNXに変換する必要がある。変換はHugging Face Optimumライブラリのconvertスクリプトで対応。フロントエンドはVite + Reactで構築し、推論処理はWeb Workers APIを用いてメインスレッドから分離することでUI描画をブロックしないよう設計されている。

worker.js内ではpipeline('image-classification', 'Xenova/quickdraw-mobilevit-small', {quantized: false})でモデルをロードし、RawImage.read()で画像を取得、grayscale()変換後に分類推論を実行する。出力例は[{label: 'skateboard', score: 0.998}]のようなラベルとスコアの配列。

ゲームデザイン面では、リアルタイム推論の特性を活かし、誤判定が続く場合は上位n件のラベルスコアを逓減させる仕組みを導入。また、モデルが苦手な一部クラスを除外してユーザー体験を改善し、最終的に100クラスに絞り込んでいる。スキップ機能（3秒ペナルティ）も実装。

監査エージェント開発への直接的な示唆は薄いが、サーバーレスML推論のパターンとして参考になる。特に、重いモデル処理をWorkerスレッドに分離してメインスレッドの応答性を維持する設計は、UIを持つエージェントシステムの非同期処理設計に応用できる。

## アイデア

- ONNXランタイムを用いることでPyTorchモデルをサーバーレスでブラウザ実行可能にする変換パイプライン（Optimum → ONNX → Transformers.js）は、エッジデプロイの標準的なワークフローとして汎用性が高い
- Web Workers APIによる推論スレッド分離パターンは、UIを持つエージェントアプリケーションで推論待ちによるフリーズを防ぐ非同期設計の実装モデルになる
- 5.6MパラメータのMobileViTが60fps超のリアルタイム推論を達成している点は、軽量モデルのエッジ活用可能性を示す具体的なベンチマークとして参照価値がある

## 関連記事

- /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_1480 推論とデュアルメモリの共同最適化による自己学習型診断エージェント（SEA）
- /deep_1169 広範な探索から安定した生成へ：自己回帰画像生成のためのエントロピー誘導最適化

## 原文リンク

[Transformers.jsでMLパワードWebゲームを作る方法](https://huggingface.co/blog/ml-web-games)
