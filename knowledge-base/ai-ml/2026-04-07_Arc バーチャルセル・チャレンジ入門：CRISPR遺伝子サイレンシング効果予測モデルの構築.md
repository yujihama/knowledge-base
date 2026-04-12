---
title: "Arc バーチャルセル・チャレンジ入門：CRISPR遺伝子サイレンシング効果予測モデルの構築"
url: "https://huggingface.co/blog/virtual-cell-challenge"
date: 2026-04-07
tags: [single-cell-RNA-seq, CRISPR, perturbation-modeling, ESM2, transformer, MMD, cell-embedding, protein-language-model, context-generalization]
category: "ai-ml"
memo: "[HF Blog] Arc Virtual Cell Challenge: A Primer"
processed_at: "2026-04-07T12:19:52.178054"
---

## 要約

Arc Instituteが公開した「Virtual Cell Challenge」の技術解説。目標は、CRISPRによる遺伝子サイレンシングが細胞に与える影響を予測するモデルの訓練であり、特に未知の細胞タイプへの汎化（context generalization）が評価軸となる。

データセットは約30万件のシングルセルRNAシーケンシングプロファイルで構成され、訓練セットは22万細胞のトランスクリプトーム（各遺伝子のRNA分子数を示すスパース行列）を含む。うち約3.8万件は未摂動のコントロール細胞。転写産物の計測が細胞を破壊するという観察者効果的問題があるため、摂動前後の同一細胞を比較することができず、コントロール細胞の集団を基準として摂動効果を推定する必要がある。

Arcが提供するベースラインモデルはSTATE（State Transition and Embedding）であり、2つのトランスフォーマーモデルから構成される。State Transition Model（ST）はLlamaバックボーンを持つトランスフォーマーで、共変量マッチしたコントロール細胞のトランスクリプトームおよびワンホットエンコードされた摂動ベクトルを入力とし、最大平均差異（MMD）損失で訓練される。State Embedding Model（SE）はBERT類似のオートエンコーダで、ESM2（FAIRの150億パラメータタンパク質言語モデル）によるアミノ酸配列埋め込みからgene embeddingを生成し、対数倍率発現量上位2048遺伝子を「細胞文」として処理してcell embeddingを得る。代替スプライシングによって生じる複数のタンパク質アイソフォームも考慮し、平均プーリングで統合する。

評価はPearsonデルタスコアを用い、コントロールとの差分（デルタ）の予測精度を測る。これにより絶対的な発現量予測ではなく、摂動効果そのものの予測精度が評価される。未見の細胞タイプへの汎化能力が問われる構成となっており、Kaggle等を通じた競技形式で公開されている。

## アイデア

- 「転写産物計測が細胞を破壊する」という観察者効果的制約により、同一細胞の前後比較ができず、集団統計からシグナルを分離するモデル設計が必要になる点は、ノイズの多い実世界データから因果効果を推定するという汎用的な問題構造と同型
- ESM2（150億パラメータのタンパク質言語モデル）を特徴量エンコーダとして固定し、遺伝子埋め込みを生成してからトランスクリプトーム予測モデルに接続するアーキテクチャは、大規模基盤モデルの埋め込みを下流タスクに転用するパターンの生物学への応用例
- Pearsonデルタスコア（絶対値でなく変化量の相関）を評価指標とすることで、ベースラインのばらつきを除去し摂動効果そのものを評価する設計は、比較対照が必要な実験的評価設計の参考例

## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_328 食物アレルギーのためのAI：オープンコミュニティ研究ラボの取り組み
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_370 設計段階でのスパース化によるクロスモダリティ予測：信頼性と効率的学習のためのL0ゲート表現

## 原文リンク

[Arc バーチャルセル・チャレンジ入門：CRISPR遺伝子サイレンシング効果予測モデルの構築](https://huggingface.co/blog/virtual-cell-challenge)
