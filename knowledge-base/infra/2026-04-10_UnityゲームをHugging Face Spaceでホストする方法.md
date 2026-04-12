---
title: "UnityゲームをHugging Face Spaceでホストする方法"
url: "https://huggingface.co/blog/unity-in-spaces"
date: 2026-04-10
tags: [HuggingFace, Unity, WebGL, Git-LFS, Static-HTML, Spaces, ゲームデプロイ]
category: "infra"
memo: "[HF Blog] How to host a Unity game in a Space"
processed_at: "2026-04-10T12:08:52.833209"
---

## 要約

Hugging Face Spacesは通常MLデモのホスティングに使われるが、UnityのWebGLビルドを使ったインタラクティブゲームのホスティングも可能であることを解説したチュートリアル記事（2023年4月公開）。手順は全11ステップで構成される。まずHugging Face Spacesで「Static HTML」テンプレートを選択してSpaceを作成し、Git経由でローカルにクローンする。次にUnityプロジェクトでビルドターゲットをWebGLに切り替え、Player SettingsからオプションとしてHugging Face製WebGLテンプレート（別途リポジトリからダウンロード）を適用することでSpace上での表示を最適化できる。重要な設定として、Publishing SettingsでCompression Formatを「Disabled」に変更する必要がある（これを怠るとブラウザでの読み込みが失敗する）。ビルド完了後、生成されたファイルをクローンしたリポジトリにコピーするが、WebGLビルドにはサイズの大きいファイルが含まれるためGit LFSを使用して大容量ファイルを追跡する必要がある（git lfs install / git lfs track Build/*）。最後にgit add・commit・pushでデプロイ完了。実例として「Huggy」「Farming Game」「Unity API Demo」の3つのゲームがSpace上で稼働している。インフラとして必要なのはHugging FaceアカウントとGit環境のみであり、サーバー管理やクラウドインフラのセットアップは不要。Static HTMLホスティングの仕組みを活用しているため、追加コストなくWebGLアプリを公開できる点が特徴。MLデモのプラットフォームとして普及しているHugging Face Spacesを、ゲームやインタラクティブシミュレーションのデプロイ基盤として転用できることを示した事例であり、強化学習環境の可視化やエージェントのデモ公開にも応用可能。

## アイデア

- ML用途に特化したHugging Face Spacesを、UnityのWebGLビルドという非ML用途に転用できる点は、プラットフォームの汎用性を示す好例
- Git LFSによる大容量ファイル管理をデプロイフローに組み込む手法は、モデルウェイトや大規模データを扱う他のプロジェクトにも応用可能
- Compression Formatを無効化しないとブラウザでの読み込みが失敗するという制約は、WebAssembly/WebGL系ビルドのデプロイ時に共通する注意点

## 原文リンク

[UnityゲームをHugging Face Spaceでホストする方法](https://huggingface.co/blog/unity-in-spaces)
