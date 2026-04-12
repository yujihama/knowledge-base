---
title: "HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に"
url: "https://huggingface.co/blog/community-tools"
date: 2026-04-08
tags: [HuggingChat, Tool Calling, Gradio, RAG, マルチモーダル, LLMツール統合, Spaces]
category: "agent-arch"
memo: "[HF Blog] Introducing Community Tools on HuggingChat"
processed_at: "2026-04-08T21:36:20.675490"
---

## 要約

HuggingFaceは2024年9月16日、HuggingChatに「Community Tools」機能をリリースした。この機能により、HuggingFace上の任意の公開SpaceをHuggingChat内でLLMが直接呼び出せるツールとして登録・利用できるようになった。

技術的な仕組みとして、SpaceのURLを入力するだけで利用可能な関数とパラメータが自動検出される。各ツールには「Tool Description」（LLMへの説明文）、「AI Function Name」（関数名）、「Arguments」（必須・任意・固定の3種類）を設定する。LLMはこれらの定義をもとにツールを呼び出すタイミングと引数を判断する。

対応モダリティが拡張され、テキストに加えて画像理解、動画生成、テキスト読み上げ（TTS）が利用可能となった。たとえばDamarJati/FLUX.1-RealismLoraのような画像生成SpaceをそのままツールとしてHuggingChatに組み込める。

カスタムツールの作成も容易で、Gradioの基本的なapp.pyを書くだけで独自ツールを構築できる。サンプルとして示されたダイスロールツールは、LLMが本質的に苦手なランダム数生成をPythonのrandom.randint()に委譲する実装例で、Gradioのgr.Interfaceを使ってSpace化し、HuggingChatのツールとして登録する流れが示された。

アシスタントへの統合も可能で、ツール呼び出し対応モデルを使ったアシスタント作成時に最大3つのツールを選択できる。システム命令フィールドでモデルにいつツールを使うかを指示できる。

さらにRAGツールのテンプレートSpaceも公開されており、Spaceを自分のアカウントにデュプリケートしてsources/フォルダにファイルを配置するだけで、自分のドキュメントへのQ&AツールをHuggingChat上に構築できる。この機能はまだ実験的な段階とされている。

## アイデア

- GradioのSpaceを関数定義として自動解析しツール化する仕組みは、任意のPythonコードをLLMのツール空間に動的に追加するローコードなMCPに近い発想
- ツール引数をRequired/Optional/Fixedの3種類に分けることで、LLMの自由度と制御のバランスを設計段階で明示的に制御できるスキーマ設計
- RAGツールをSpaceとして外部化し、ファイルをsources/に置くだけで更新できる構成は、ツールのステートフルな拡張（知識ベースの差し替え）を軽量に実現している

## Yujiの取り組みへの示唆

監査エージェント開発においてLangGraphのノードに外部ツールを組み込む際、GradioベースのSpaceをツール化するこのアーキテクチャは、監査手続き（証憑取得・分類・照合）を個別Spaceとして実装し動的に呼び出すパターンの参考になる。特にRAGツールをSpaceとして独立させ差し替え可能にする設計は、監査証拠のナレッジベースを更新しながらエージェントを動かす構成に応用できる。ツール引数のRequired/Fixed設計は、Pydanticのフィールド制約と対応関係があり、エージェントへのツールスキーマ定義設計の参考になる。

## 原文リンク

[HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に](https://huggingface.co/blog/community-tools)
