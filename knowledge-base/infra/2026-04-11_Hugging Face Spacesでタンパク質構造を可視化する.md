---
title: "Hugging Face Spacesでタンパク質構造を可視化する"
url: "https://huggingface.co/blog/spaces_3dmoljs"
date: 2026-04-11
tags: [3Dmol.js, Gradio, HuggingFace Spaces, タンパク質構造可視化, AlphaFold2, WebGL, PDB, gradio_molecule3d]
category: "infra"
memo: "[HF Blog] Visualize proteins on Hugging Face Spaces"
processed_at: "2026-04-11T21:04:59.136400"
---

## 要約

本記事は、Hugging Face SpacesとGradioを使ってタンパク質の3D構造をブラウザ上でインタラクティブに可視化する方法を解説している。主な技術スタックは3Dmol.js（Pittsburgh大学が開発するWebGL対応の分子ビューワー）とGradioのHTMLブロック（iframeラッパー経由）。

Gradioには3Dmol.jsの直接サポートがないため、`gr.HTML()`ブロックにiframeを埋め込む手法を採用している。iframeのsrcdoc属性にHTMLドキュメント全体を文字列として渡し、その中にPDBファイルの内容をJavaScriptテンプレートリテラルで直接埋め込む設計。ブラウザのセキュリティポリシー（Same-Origin Policy等）に対応するためのやや冗長な構造だが、外部依存を最小化できる。

入力はRCSB Protein Databank（PDB）の4文字コードまたはローカルPDBファイルのアップロードに対応。PDBコードが指定された場合はwgetでRCSBから直接ダウンロードする。表示スタイルはCartoon表現（whiteCarbonカラースキーム）がデフォルトで、3Dmol.jsのsetStyle APIから任意のスタイル（stick、sphere等）やcolorfunc（各原子のプロパティに基づくカスタム配色）に変更可能。

2024年5月のアップデートでは、`gradio_molecule3d`というGradioカスタムコンポーネントが公開され、`pip install gradio_molecule3d`で導入可能になった。repsパラメータでchain・style・colorを宣言的に指定できるため、よりシンプルな記述が可能。

実用例として、逆折りたたみモデルのProteinMPNNとAlphaFold2を組み合わせたSpaceが紹介されている。ユーザーがバックボーン構造をアップロード→ProteinMPNNが最適アミノ酸配列を予測→AlphaFold2で構造を検証→3Dmol.jsで可視化、というMLパイプラインが構築されている。このワークフローはAlphaFold2登場以降急増したOmegaFold・OpenFoldなどの構造予測モデルとの組み合わせを念頭に設計されている。

インフラとしてはHugging Face Spacesの無料ホスティングを利用し、CDN経由でjQuery 3.6.3と3Dmol-min.jsを読み込む。特別なGPUリソースは不要で、可視化自体はクライアントサイドのWebGLで処理される。

## アイデア

- iframeのsrcdocにHTMLを文字列として直接埋め込む手法は、ブラウザセキュリティを回避しながら任意のJSライブラリをGradioに統合する汎用パターンとして応用できる
- colorfuncを使って原子ごとのプロパティ（例: pLDDTスコア、リガンド結合確率）を色でエンコードする手法は、モデル出力の信頼度や重要度をそのまま構造に重ねて可視化するUI設計として有効
- PDBコード入力→外部API取得→表示というパターンは、外部データソース連携を持つ任意のMLデモアプリの雛形として転用しやすい

## 関連記事

- /deep_45 Daggr：Pythonコードでワークフローを定義し、自動生成されるビジュアルキャンバスで検査・デバッグするオープンソースライブラリ
- /deep_1304 AI WebTV：テキスト・トゥ・ビデオモデルを使ったリアルタイムストリーミングシステムの構築
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_1392 UnityゲームをHugging Face Spaceでホストする方法

## 原文リンク

[Hugging Face Spacesでタンパク質構造を可視化する](https://huggingface.co/blog/spaces_3dmoljs)
