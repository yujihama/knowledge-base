---
title: "【備忘録】Web Agent SFT データパイプライン"
url: "https://zenn.dev/warabiimochi/articles/2b3569a867b216"
date: 2026-06-08
tags: [SFT, Web Agent, Mind2Web, WebLINX, OmniACT, HuggingFace Datasets, データパイプライン, マルチターン会話]
category: "ai-ml"
related: [1848, 1615, 1757, 826, 6269]
memo: "[Zenn LLM] 【備忘録】Web Agent SFT データパイプライン"
processed_at: "2026-06-08T21:02:05.353742"
---

## 要約

Web Agentのファインチューニング（SFT）に使用するデータパイプラインの構築手順を解説した備忘録。Mind2Web（osunlp/Mind2Web、約2,350件・400MB）、WebLINX（McGill-NLP/weblinx、約2,400件・800MB）、OmniACT（microsoft/OmniACT、約9,800件・3GB）の3つのHugging Faceデータセットを対象とする。パイプラインはraw保存→カラム確認→成形（formatted）→結合の4段階で構成される。

成形処理では各データセットの構造に合わせたmap関数を実装する。Mind2Webは「confirmed_task / website / actions」カラムを持ち、1軌跡をマルチターン会話形式（system/user/assistant）に変換する。各ステップでHTMLスニペット（最大500文字）をuserメッセージに含め、操作（click, typeなど）をassistantメッセージに格納する。WebLINXはutteranceをuser、actionをassistantに対応させるシングルターン変換。OmniActはスクリーンショットベースのタスクで、actions配列（type, text, x, y座標）をassistantの出力として整形する。

全データセットはconcatenate_datasets()で結合後にseed=42でシャッフルし、./data/formatted/combinedに保存。SFTTrainerにそのまま渡せる形式になっている。開発効率のため、まず100件のサンプルでカラム構造を確認してからmap関数を実装し、その後本番全件ダウンロードを行う2段階フローを採用している。Singularity経由のHPC環境での実行も考慮されており、--nvフラグによるGPUパススルーも示されている。

監査エージェント開発への示唆として、Web操作の軌跡データ（タスク→HTML状態→アクション）をマルチターン会話形式に変換するこのアプローチは、監査ワークフローのSFTデータ構築にも直接転用可能。特にMind2Webのステップ単位の状態管理パターンは、LangGraphベースの監査エージェントが取るアクション系列のログをSFTデータ化する際の設計参考になる。

## アイデア

- 100件サンプルでカラム確認→map関数修正→本番全件という2段階フローにより、データセットごとのカラム名の不一致リスクを最小化している
- Mind2Webの軌跡をステップ単位のマルチターン会話に変換する手法は、エージェントの中間状態（HTML断片）を観測として明示的にモデルに与えるため、単純なinput/output形式より状態依存の行動学習に適している
- 3データセット（Mind2Web/WebLINX/OmniACT）を統一的なmessages形式に正規化して結合することで、異なる操作モダリティ（DOM操作、発話指示、スクリーンショット座標）を単一モデルで学習可能にする設計

## 前提知識

- **SFT（Supervised Fine-Tuning）** (TODO: 読むべき)
- **SFTTrainer** → /deep_520 TRL v1.0: フィールドの変化に追従するポストトレーニングライブラリ
- **HuggingFace Datasets** → /deep_1488 音声データセット完全ガイド：HuggingFace Datasetsで音声データを効率的に扱う方法
- **マルチターン会話形式** (TODO: 読むべき)
- **Web Agent** (TODO: 読むべき)

## 関連記事

- /deep_1848 🤗 データ測定ツール紹介：データセット分析のためのインタラクティブツール
- /deep_1615 🤗 Datasetsにおける音声・画像データセット対応の新ドキュメント公開
- /deep_1757 🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_6269 開発しながらLoRAデータが自動で貯まる仕組み「M2LoRA」を作った

## 原文リンク

[【備忘録】Web Agent SFT データパイプライン](https://zenn.dev/warabiimochi/articles/2b3569a867b216)
