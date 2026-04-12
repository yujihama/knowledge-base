---
title: "Synthetic Data Generator：自然言語でデータセットを構築するノーコードツール"
url: "https://huggingface.co/blog/synthetic-data-generator"
date: 2026-04-08
tags: [synthetic-data, distilabel, SFT, text-classification, Argilla, AutoTrain, HuggingFace, dataset-generation, LLM]
category: "ai-ml"
memo: "[HF Blog] Introducing the Synthetic Data Generator - Build Datasets with Natural Language"
processed_at: "2026-04-08T12:30:17.254620"
---

## 要約

HuggingFaceが2024年12月16日に公開した「Synthetic Data Generator」は、LLMを活用してコードなしでカスタムデータセットを生成できるWebアプリケーション。バックエンドはdistilabelフレームワークとHuggingFace無料テキスト生成APIで構成されており、ユーザーはUIの3ステップ（データセット説明→設定調整→生成・プッシュ）で作業を完結できる。

対応タスクはテキスト分類とチャット（SFT用）の2種類。テキスト分類では「多様なテキスト生成→ラベル付与」の2段階パイプラインを採用し、分速50サンプル生成が可能。チャットデータセットは分速20サンプルで、生成結果はArgillaとHugging Face Hubに直接保存される。

生成されたデータセットはArgilla（AIエンジニアとドメイン専門家向けデータ品質管理ツール）でセマンティック検索や複合フィルタを用いてレビュー・キュレーション可能。その後AutoTrainと組み合わせることで、コードなしでモデル訓練・デプロイまで完結する。argilla/synthetic-text-classification-newsデータセットを例に8クラス分類モデルをHugging Face CPU無料枠で数分以内に訓練できることが示されている。

上級者向け機能として、Spaceの複製とenv変数設定により、モデルをmeta-llama/Llama-3.1-70B-InstructやGPT-4oに変更したり、BATCH_SIZEを5から10に増やしてスループット改善が可能。プライベートArgillaインスタンスへの接続もARGILLA_URLとARGILLA_API_KEYで対応。ローカルデプロイはApache 2ライセンスのオープンソースとして提供され、pip install synthetic-dataset-generatorで導入可能。各パイプラインはdistilabelベースで構成されており、Pythonコードでのカスタマイズも可能。

## アイデア

- 「プロンプト→データセット→モデル」をノーコードで完結させるパイプライン設計は、データ収集コストが高い専門領域（監査・法務等）で特に有効
- distilabelをバックエンドに使いつつUIで抽象化することで、非エンジニアがLLMパイプラインを操作できる設計思想は、エージェントシステムのUI層設計に応用できる
- Argillaとの統合によりデータ生成→人間によるレビュー→ファインチューニングのループを構築しており、RLAIF的なフィードバックループのプロトタイプとして参考になる

## Yujiの取り組みへの示唆

監査エージェント開発において、監査手続きや内部統制評価のQ&Aペアや分類データセットをゼロから合成生成できる点が直接活用可能。特にLLM-as-judgeの評価データやReActエージェントのテストケース生成に、distilabelパイプラインをカスタマイズして使うユースケースが考えられる。GRPOやRLAIFの報酬モデル訓練用の初期合成データセット構築にも、このツールを起点として監査ドメイン特化のプロンプト設計を行う出発点として機能する。

## 原文リンク

[Synthetic Data Generator：自然言語でデータセットを構築するノーコードツール](https://huggingface.co/blog/synthetic-data-generator)
