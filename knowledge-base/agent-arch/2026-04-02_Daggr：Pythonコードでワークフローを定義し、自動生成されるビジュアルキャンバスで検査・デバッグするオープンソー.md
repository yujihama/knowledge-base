---
title: "Daggr：Pythonコードでワークフローを定義し、自動生成されるビジュアルキャンバスで検査・デバッグするオープンソースライブラリ"
url: "https://huggingface.co/blog/daggr"
date: 2026-04-02
tags: [Daggr, Gradio, ワークフローオーケストレーション, HuggingFace Spaces, DAG, パイプラインデバッグ, ビジュアルキャンバス, InferenceProviders]
category: "agent-arch"
memo: "[HF Blog] Introducing Daggr: Chain apps programmatically, inspect visually"
related: [1571, 1304, 88, 1619, 701]
processed_at: "2026-04-02T12:01:02.516845"
---

## 要約

DaggrはHugging Faceチーム（Gradioチーム）が開発したオープンソースのPythonライブラリで、AIワークフローを構築・可視化するためのツールである。pip installで導入でき、Python 3.10以上が必要。

コア設計思想は「コードファースト＋自動ビジュアル生成」。LangGraphのようにグラフ構造でワークフローを定義するが、ドラッグ&ドロップのGUI編集ではなく、Pythonコードでノード間の接続を記述すると、ポート7860にビジュアルキャンバスが自動生成される。キャンバス上では各ノードの中間出力を検査し、特定のステップのみを再実行することが可能。10ステップのパイプラインでステップ7が失敗した場合、ステップ7単体をリランできる。

サポートするノードタイプは3種類。GradioNodeはHugging Face Spacesのエンドポイントを呼び出す。run_locally=Trueを指定するとSpaceをローカルにクローンして分離された仮想環境で起動し、失敗時はリモートAPIにフォールバックする。FnNodeは任意のPython関数をラップしてノード化する。InferenceNodeはHugging Face Inference Providersを通じてmoonshotai/Kimi-K2.5などのモデルを呼び出す。

ノード間の接続はbg_remover.inputs['image'] = image_gen.imageのように出力参照を渡すだけで確立される。グラフはGraph(name='...', nodes=[...])でインスタンス化し、graph.launch()で起動する。share=Trueでトンネリング経由の公開URLも生成可能。

ステート管理として、ワークフローの状態・入力値・キャッシュ結果・キャンバス位置を自動保存する。「シート」機能により同一アプリ内で複数のワークスペースを管理できる。

エンドツーエンドの例として、画像→背景除去（BiRefNetをローカル実行）→ダウンスケール（FnNode）→3Dアセット風スタイル変換（Flux.2-klein-4B via InferenceNode）→3D生成（Trellis.2 Space）というパイプラインが示されており、異なるノードタイプの組み合わせ方が具体的に確認できる。

## アイデア

- 「コードファーストでビジュアルを自動生成」するアプローチは、LangGraphのグラフ定義と同じ哲学。コードがソース・オブ・トゥルースのままビジュアライズできるため、バージョン管理と視認性を両立できる
- ステップ単位の再実行（部分リラン）は監査ワークフローのデバッグに直接応用可能。10段階の監査チェックパイプラインで特定チェックのみ再実行するユースケースに合致する
- GradioNodeのフォールバック機構（ローカル失敗→リモートAPI）はエージェントアーキテクチャにおける「バックアップノード」概念として興味深い。モデルやSpaceを差し替え可能にすることでレジリエンスを担保するパターン
## 関連記事

- /deep_1571 Hugging Face Spacesでタンパク質構造を可視化する
- /deep_1304 AI WebTV：テキスト・トゥ・ビデオモデルを使ったリアルタイムストリーミングシステムの構築
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）
- /deep_701 分散コンピューティングを用いた検出器設計最適化のためのスケーラブルなAI支援ワークフロー管理

## 原文リンク

[Daggr：Pythonコードでワークフローを定義し、自動生成されるビジュアルキャンバスで検査・デバッグするオープンソースライブラリ](https://huggingface.co/blog/daggr)
