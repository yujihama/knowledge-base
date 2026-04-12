---
title: "Claude Code × Google Colab 第3弾：PyTorch LSTMで東京の気温7日間予測（GPU使用）"
url: "https://zenn.dev/niikun/articles/1a6d62e5869373"
date: 2026-04-07
tags: [PyTorch, LSTM, 時系列予測, Google Colab, Claude Code, スライディングウィンドウ, MinMaxScaler, GPU]
category: "ai-ml"
memo: "[Zenn 機械学習] Claude Code × Google Colab 第3弾 PyTorch LSTMが怖くなかった話 GPUで気温予測"
related: [113, 828, 26, 415, 116]
processed_at: "2026-04-07T12:02:44.093203"
---

## 要約

気象庁オープンデータ（東京の日別気温2016〜2025年）を用いて、PyTorch LSTMで翌7日間の気温を多ステップ予測するモデルをGoogle Colab T4 GPU上で構築した実践記録。Claude Codeをナビゲーターとして活用し、複数の技術的障壁を乗り越えた過程が詳述されている。

モデル構成はPyTorch LSTM（2層、hidden_size=64）、入力は過去30日のシーケンス、出力は翌7日分の気温。データ前処理ではMinMaxScalerをtrainデータのみでfitし（データリーク防止）、スライディングウィンドウ（seq_len=30, pred_len=7）でシーケンスを生成している。GPU切り替えはtorch.device('cuda')で対応し、Colab T4（VRAM 15.6GB）を使用。

評価結果はMAE 2.12℃、RMSE 2.72℃。ステップ別MAEは翌1日目1.59℃から翌7日目2.37℃へ単調増加し、予測困難度が時間とともに増す自然な挙動を確認。50エポックの学習曲線はtrain/valがほぼ重なって下降し、過学習なしの安定した学習を達成。

ノートブックは01_eda（データ可視化・ACF確認）→02_preprocess（スケーリング・DataLoader）→03_model（LSTM定義・GPU学習）→04_predict（推論・逆変換・評価）の4本に分割。ACFグラフで365日周期の自己相関を確認し、seq_len=30〜60の妥当性を根拠付けた点が実践的。

Claude Codeの貢献として、気象庁CSVのParserError（skiprows=5、header=Noneで解決）の診断、スケーラーのfitルールの説明、LSTMゲート構造の解説など、「なぜそうするのか」という設計根拠の言語化が学習効果を高めた点が強調されている。

## アイデア

- スケーラーをtrainデータのみでfitするデータリーク防止の原則：val/testで値が0〜1をわずかにはみ出すのは正しい挙動であるという明示的な説明が、初学者の誤解を防ぐ実用的なポイント
- ACF（自己相関関数）グラフからseq_lenを設定する根拠ベースのアプローチ：365日周期の確認によってハイパーパラメータ選択に統計的根拠を持たせる手法
- ノートブックを機能単位（EDA→前処理→モデル→推論）に分割する構成：各ステップの責務を明確化し、デバッグや再実験を容易にするパイプライン設計パターン
## 関連記事

- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_828 PyTorchにおけるGPUメモリの可視化と理解
- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_415 Claude Code × Google Colab 第2弾——MLの出力をClaudeが読んで改善提案してくれた話
- /deep_116 AIを活用した都市型鉄砲水（フラッシュフラッド）予測システムの展開

## 原文リンク

[Claude Code × Google Colab 第3弾：PyTorch LSTMで東京の気温7日間予測（GPU使用）](https://zenn.dev/niikun/articles/1a6d62e5869373)
