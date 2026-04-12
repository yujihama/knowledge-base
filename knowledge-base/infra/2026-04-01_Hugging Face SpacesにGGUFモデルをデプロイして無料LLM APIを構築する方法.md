---
title: "Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法"
url: "https://zenn.dev/pushmyheart/articles/ccbcd222244f71"
date: 2026-04-01
tags: [GGUF, llama.cpp, Hugging Face Spaces, FastAPI, Docker, llama-server, OpenAI互換API, CPU推論]
category: "infra"
memo: "[Zenn LLM] Hugging Face Spacesに小型LLMをあげて、夢の無料LLM-API を立てる方法"
related: [399, 1146, 647, 524, 390]
processed_at: "2026-04-01T21:10:44.669006"
---

## 要約

Hugging Face SpacesのCPU無料枠（Dockerランタイム）上に、llama.cppのllama-serverとFastAPIを組み合わせてGGUFモデルを動かし、OpenAI互換エンドポイントとして公開する構成の解説記事。著者はビルドエラーの解決に約3日を費やしており、その知見をコードベースとして残している。

構成は4ファイル（Dockerfile、README.md、main.py、requirements.txt）で完結する。Dockerfileはpython:3.11-slim-bookwormをベースに、llama-serverの実行に必要なlibgomp1とlibcurl4をaptインストールする。llama-serverのバイナリはコンテナビルド時ではなくFastAPIの起動イベント（on_event('startup')）内で動的にダウンロード・展開する設計を採用しており、これによりDockerイメージのビルドをシンプルに保っている。

最大のトラブルポイントは共有ライブラリの解決。GitHubからzip形式でバイナリを取得すると、libllama.soなどのシンボリックリンクが展開時に壊れてExec format errorやfile not foundが発生する。.tar.gz形式を使い展開後にchmod +xを適用することで回避できる。また起動時にLD_LIBRARY_PATH環境変数でBIN_DIRを明示的に指定することで、バイナリと同ディレクトリに配置した.soファイルを確実に参照させる。

モデルはHugging Face Hub上のGGUFリポジトリを-hfオプションで直接指定して起動する。FastAPIはllama-server（127.0.0.1:8080）へのリバースプロキシとして機能し、/v1/*エンドポイントをStreamingResponseで転送する。起動シーケンスは「FastAPI起動→バイナリ準備→llama-serverをサブプロセス起動→/healthポーリングで準備完了確認」の順序を厳守することで、Spaceが'Running'になった瞬間にAPIが利用可能な状態を保証する。

パフォーマンスの実測値は1秒あたり4〜7トークン（CPUのみ）。リアルタイムなチャットUIには不向きだが、バッチ処理や非同期ワークフローであれば実用範囲内との評価。

## アイデア

- ビルド時ではなくランタイム起動時にバイナリを動的ダウンロードする設計により、Dockerイメージのビルドを軽量に保ちながら任意バージョンのllama-serverを利用できる
- .zipではなく.tar.gzを使うことでシンボリックリンクの破損を回避するという、Linuxアーカイブ形式の特性に起因する実践的なトラブルシューティング知見
- FastAPIをプロキシ層として分離し推論をllama-serverに委譲する構成は、カスタムAPIロジック（認証・レート制限・前処理）とLLM推論を疎結合に保つアーキテクチャパターンとして汎用性がある
## 関連記事

- /deep_399 OpenClawエージェントをオープンモデルに移行する方法
- /deep_1146 1-bit Bonsai 8Bを触ってみた：爆速だが既存llama.cpp運用にはそのまま載らなかった
- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_390 Hugging Face Spacesの無料枠に小型LLMをデプロイしてAPIを立てる方法（非推奨）

## 原文リンク

[Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法](https://zenn.dev/pushmyheart/articles/ccbcd222244f71)
