---
title: "Snowball Fight ☃️ 紹介：Hugging FaceによるML-Agents初のカスタム深層強化学習環境"
url: "https://huggingface.co/blog/snowball-fight"
date: 2026-04-14
tags: [深層強化学習, Unity ML-Agents, Hugging Face Spaces, マルチエージェント, MA-POCA, カスタム環境, ゲームAI]
category: "ai-ml"
related: [1641, 16, 21, 931, 88]
memo: "[HF Blog] Introducing Snowball Fight ☃️, our first ML-Agents environment"
processed_at: "2026-04-14T12:12:19.308331"
---

## 要約

Hugging Faceが2021年12月に公開した、Unity ML-Agentsを用いた初のカスタム深層強化学習（Deep RL）環境「Snowball Fight」の紹介記事。Snowball Fightは1vs1の雪合戦ゲームで、プレイヤーが深層強化学習エージェントと対戦する形式。ゲームはHugging Face Spacesでホストされ、ブラウザ上でそのままプレイ可能。Unity Machine Learning Agents Toolkit（ML-Agents）はUnityエンジン上でゲームやシミュレーション環境を構築し、それをインテリジェントエージェントの学習環境として活用できるオープンソースライブラリ。Hugging Faceはこの取り組みを皮切りに、Deep RLコミュニティ向けのエコシステム構築を目指している。具体的には3つの機能に注力する：①カスタム環境の構築と公開（雪合戦、レーシング、パズルなど、すべてオープンソースでHugging Face Hubにホスト）、②Hugging Face Hub上でのモデル保存・共有の容易化（学習環境「Snowball Fight training environment」はすでにHub上に公開済み）、③Hugging Face Spacesを活用したデモのホスティングと成果共有。今後の展開としては、ML-Agentsのテクニカルチュートリアルの執筆、Snowball Fight 2vs2バージョンの開発（チーム協調行動を学習するMA-POCA：Multi-Agent POsthumous Credit Assignmentアルゴリズムを活用予定）、新カスタム環境の追加が予定されている。DiscordサーバーにDeep Reinforcement LearningとML-Agents専用チャンネルが追加されており、コミュニティでの情報交換の場も整備されつつある。監査エージェント開発への直接的な示唆は薄いが、Unity上のシミュレーション環境を用いた協調マルチエージェント学習（MA-POCA）の考え方は、複数エージェントが協調して監査タスクをこなすアーキテクチャ設計の参考になりうる。

## アイデア

- Hugging Face Spacesをゲームデモのホスティング基盤として使うことで、学習済みモデルをインタラクティブに公開・評価できる仕組みが低コストで実現できる
- MA-POCA（Multi-Agent POsthumous Credit Assignment）によるチーム協調行動の学習は、複数エージェントが役割分担しながら共通目標に向かうマルチエージェントシステムの設計に直接応用可能
- Unity MLAgentsのような物理シミュレーション環境をHugging Face Hubと統合することで、環境・モデル・デモの三点セットを一元管理するDeep RLエコシステムのプロトタイプとなっている

## 前提知識

- **深層強化学習（Deep RL）** (TODO: 読むべき)
- **Unity ML-Agents** → /deep_1301 オープンソースAIゲームジャム第1回結果発表
- **MA-POCA** (TODO: 読むべき)
- **Hugging Face Hub** → /deep_187 Community Evals: ブラックボックスリーダーボードから脱却するHugging Faceの分散型評価システム
- **マルチエージェント強化学習** → /deep_1432 TwinLoop: オンラインマルチエージェント強化学習のためのシミュレーション・イン・ザ・ループ型デジタルツイン

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_16 長期実行アプリケーション開発のためのハーネス設計
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ
- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法

## 原文リンク

[Snowball Fight ☃️ 紹介：Hugging FaceによるML-Agents初のカスタム深層強化学習環境](https://huggingface.co/blog/snowball-fight)
