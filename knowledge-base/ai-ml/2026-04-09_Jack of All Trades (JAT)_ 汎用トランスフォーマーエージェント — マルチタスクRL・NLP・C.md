---
title: "Jack of All Trades (JAT): 汎用トランスフォーマーエージェント — マルチタスクRL・NLP・CVの統合"
url: "https://huggingface.co/blog/jat"
date: 2026-04-09
tags: [generalist-agent, transformer, multi-task-RL, Gato, GPT-Neo, imitation-learning, Atari, MuJoCo, Meta-World, BabyAI, multimodal]
category: "ai-ml"
memo: "[HF Blog] Jack of All Trades, Master of Some, a Multi-Purpose Transformer Agent"
processed_at: "2026-04-09T09:51:42.058920"
---

## 要約

JATはHugging Faceが公開したGato（DeepMind, 2022）のオープン再現を起点とする汎用エージェントプロジェクト。単一のTransformerネットワークで、Atari 57ゲーム・BabyAI（テキスト指示ナビゲーション）・Meta-World（ロボット操作26タスク）・MuJoCo（連続制御）の合計157タスクをこなす。アーキテクチャはEleutherAIのGPT-Neo実装をベースとし、観測・行動・報酬を時系列で交互にインターリーブするユニークな埋め込み機構を持つ。データモダリティに応じてCNN（画像）・線形層（連続ベクトル）・線形射影（離散値）を使い分け、出力側も同様に切り替える。損失関数はモダリティごとに計算（画像・連続値はMSE、離散値はクロスエントロピー）し平均化する。訓練データとして公開されたJATデータセットは、各環境でSoTA性能に達した専門家エージェントから収集した数十万件の軌跡を含む最初の汎用エージェント訓練用データセットであり、Wikipedia・Oscar・OK-VQA・Conceptual Captionsも含む。評価結果として、BabyAIでは専門家スコアの99.0%を達成、MuJoCoで84.8%、Meta-Worldで65.5%、Atari 57で14.1%（人間比37.6%、21ゲームで人間超え）となり、4ドメイン平均で専門家の65.8%に相当するパフォーマンスを単一ネットワークで実現した。また、観測予測損失の重みパラメータκを0.005に設定すると行動学習が改善するという副次的知見も得られており、世界モデル的な補助タスクがRL性能を向上させる可能性を示している。モデル・データセット・専門家エージェントはすべてHugging Face Hubで公開済み。

## アイデア

- 単一ネットワークで157タスクをこなす汎用エージェント設計：観測・行動・報酬をインターリーブする埋め込み機構が鍵であり、複数ドメインの異種データを統一的に扱うアーキテクチャ設計の参考になる
- 観測予測補助タスク（κ=0.005）がRL性能を向上させる知見：行動最適化に加えて環境のダイナミクスを予測させることで表現学習が改善し、サンプル効率が上がる可能性を示す実験設計
- 専門家軌跡データセットの公開：模倣学習・オフライン強化学習研究のベンチマーク基盤として、JATデータセット自体が今後の汎用エージェント研究の共通基盤になりうる
## 関連記事

- /deep_1057 臨床テキストだけで十分か？心不全患者の死亡予測に関するマルチモーダル研究
- /deep_739 深層強化学習の事前学習における進化戦略の有効性検証
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界

## 原文リンク

[Jack of All Trades (JAT): 汎用トランスフォーマーエージェント — マルチタスクRL・NLP・CVの統合](https://huggingface.co/blog/jat)
