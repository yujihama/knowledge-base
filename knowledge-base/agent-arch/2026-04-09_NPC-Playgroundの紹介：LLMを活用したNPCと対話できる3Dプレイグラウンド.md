---
title: "NPC-Playgroundの紹介：LLMを活用したNPCと対話できる3Dプレイグラウンド"
url: "https://huggingface.co/blog/npc-gigax-cubzh"
date: 2026-04-09
tags: [LLM, NPC, function-calling, Phi-3, Mistral-7B, fine-tuning, Lua, game-AI, Hugging-Face-Spaces]
category: "agent-arch"
memo: "[HF Blog] Introducing NPC-Playground, a 3D playground to interact with LLM-powered NPCs"
related: [1449, 892, 800, 1266, 564]
processed_at: "2026-04-09T09:23:02.822317"
---

## 要約

CubzhとGigaxが共同開発した「NPC-Playground」は、LLM（大規模言語モデル）で動作するNPC（Non-Playable Character）とブラウザ上で直接対話できる3Dデモ環境。Hugging Face Spacesでホストされており、オープンソースとして公開されている。

技術スタックは3層構成。①CubzhはクロスプラットフォームのUGC（ユーザー生成コンテンツ）ゲームエンジンで、Robloxのオープンソース代替を目指す。Luaスクリプトによるゲームロジック記述、25,000以上のコミュニティ製ボクセルアイテムライブラリを持ち、Steam・Epic・iOS・Android・ブラウザで動作する。②GigaxはLLMを用いたNPC実行プラットフォームで、NPCの「function calling」原理に基づくファインチューニングモデルを提供。③Hugging Face Spacesがホスティング・実験環境を担う。

Gigaxのモデルアーキテクチャは入出力が明確に定義されている。入力は3Dシーンのテキスト説明・直近イベント記述・利用可能アクションリスト（`<say>`、`<jump>`、`<attack>`等）。出力はシーン内エンティティを参照するパラメータ付きアクション（例：`say NPC1 "Hello, Captain!"`）。Phi-3とMistral-7Bの2モデルをNPCインタラクション用にファインチューニングしており、どちらもHugging Face Hubで公開済み。

ユーザーはリポジトリをクローンし`cubzh.lua`を数行書き換えるだけでNPCに新スキルを追加できる。デモのカスタマイズ方法はHugging Faceの「ML for Games Course」チュートリアルで解説されている。2024年6月5日公開。

## アイデア

- NPCのアクションをfunction callingとして定式化し、3Dシーン記述＋直近イベント＋アクションリストを入力、構造化コマンドを出力するという設計は、監査エージェントにおける「状況認識→アクション選択」フローに直接応用可能なパターン
- Phi-3・Mistral-7Bをドメイン固有タスク（NPC対話）向けにファインチューニングすることで汎用LLMより低コスト・高精度なエージェント動作を実現している点は、特化型エージェントの設計思想として参考になる
- Lua数行でNPCスキルを拡張できるという「低コードでのエージェント能力拡張」設計は、監査エージェントのスキルモジュール化・ノーコード化の観点で示唆を与える
## 関連記事

- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_892 重み空間モデルマージによる大規模言語モデルの壊滅的忘却対策と指示追従能力の改善
- /deep_800 Foresight Learningによるサプライチェーン障害の予測
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由

## 原文リンク

[NPC-Playgroundの紹介：LLMを活用したNPCと対話できる3Dプレイグラウンド](https://huggingface.co/blog/npc-gigax-cubzh)
