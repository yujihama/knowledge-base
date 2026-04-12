---
title: "NPC-Playgroundの紹介：LLMを活用したNPCと対話できる3Dプレイグラウンド"
url: "https://huggingface.co/blog/npc-gigax-cubzh"
date: 2026-04-09
tags: [LLM, NPC, function-calling, Phi-3, Mistral-7B, fine-tuning, Lua, game-AI, Hugging-Face-Spaces]
category: "agent-arch"
memo: "[HF Blog] Introducing NPC-Playground, a 3D playground to interact with LLM-powered NPCs"
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

## Yujiの取り組みへの示唆

GigaxのNPCアーキテクチャは「シーン状態＋利用可能アクションリストをプロンプトに含め、構造化アクションを出力させる」という設計で、YujiのReActベース監査エージェントにおけるツール選択・アクション実行フローと構造的に同一。特に監査手続きを`<say>`のようなアクションとして列挙し、LLMに選択させるfunction calling的アプローチはLangGraphのノード設計に転用できる。ただしゲームNPCと監査エージェントでは信頼性・説明可能性の要求水準が大きく異なるため、直接の技術移転より設計パターンの参考にとどめるのが適切。

## 原文リンク

[NPC-Playgroundの紹介：LLMを活用したNPCと対話できる3Dプレイグラウンド](https://huggingface.co/blog/npc-gigax-cubzh)
