---
title: "長距離Transformerの読書会：Longformer・Compressive Transformer・Linformer・Performerの比較"
url: "https://huggingface.co/blog/long-range-transformers"
date: 2026-04-14
tags: [Longformer, Compressive Transformer, Linformer, Performer, 長距離注意, Efficient Transformer, 自己注意の線形化, 低ランク近似, カーネル近似, FAVOR+]
category: "ai-ml"
related: [1449]
memo: "[HF Blog] Hugging Face Reads, Feb. 2021 - Long-range Transformers"
processed_at: "2026-04-14T12:52:14.643115"
---

## 要約

Hugging Faceが2021年2月に開催した読書会の記録。Transformerのシーケンス長に対する二次計算コスト問題を解決する4つのアプローチを取り上げている。

【Longformer】通常の全自己注意をウィンドウ型ローカル注意と少数のグローバル注意の組み合わせに置き換える。メモリ消費をn²からwn+gn（w=ウィンドウ幅、g=グローバルトークン数）に削減し、シーケンス長に対して線形スケールを実現。オートレグレッシブLMにはdilated windowed注意を、エンコーダ事前学習にはlocal+globalの双方向注意を使用。既存の事前学習済みモデルをfine-tuneで転用可能な点が実用上の強み。

【Compressive Transformer】Transformer-XLの過去activationキャッシュ機構を拡張し、廃棄予定の古いactivationを圧縮して「圧縮メモリ」に格納する。圧縮関数fcとして畳み込み・平均プーリング・最大プーリング・MLPを比較検証。圧縮率cを設定し、O(n²+nnm)の計算量を保ちつつより長い過去文脈にアクセスを可能にした。PG-19データセット（Project Gutenbergの書籍）でSOTA達成。また「予測の忘却」のみが真の長期記憶を必要とする指標になるという観察も報告。

【Linformer】自己注意行列がlow-rankであるという観察に基づき、n×dのキー・バリュー行列をk×dに射影する低ランク近似を適用。計算量をO(n²)からO(nk)に削減。kはシーケンス長に対して対数または線形でスケール可能。ただし固定長の射影行列を前提とするため、学習時と異なるシーケンス長への汎化に課題があり、自己回帰デコーダへの直接適用も困難。

【Performer】注意スコアexp(q·k/√d)をランダム特徴量マップを使ってカーネル近似し（FAVOR+アルゴリズム）、行列積の順序を変えることでO(n²d)をO(nd²)に削減。近似誤差に関する理論的保証があり、softmax注意の近似精度が他手法より高い。既存のTransformerから再学習なしに変換可能（プリトレーニング済みモデルへの近似適用）。

4手法の共通課題として、標準的なTransformerとの性能差・汎化性の検証不足、異なるシーケンス長への対応、TPU等の特定ハードウェアでの実装効率の問題が挙げられる。Long Range Arenaベンチマークでは全手法が標準Transformerを上回るが、実タスクでの優位性は限定的。監査エージェント開発への示唆としては、長文契約書・監査報告書・規制文書を処理するLLMの設計時に、Longformerのようなローカル+グローバル注意の組み合わせが実用的な出発点となりうる。

## アイデア

- dilated windowed注意のウィンドウサイズを層が深まるにつれ拡大する設計がCNNの受容野拡大と対応しており、視覚・言語を横断する設計原則の共通性を示唆している
- Compressive Transformerの圧縮メモリは「何を忘れるか」を学習させるアプローチであり、人間の記憶の圧縮・忘却メカニズムとの類比からエージェントのメモリ管理設計に応用できる可能性がある
- Performerのランダム特徴量によるsoftmax近似（FAVOR+）は理論的誤差保証を持ちながら既存モデルへのドロップイン置換が可能という点で、実用性とエレガンスを両立した設計として注目に値する

## 前提知識

- **Transformer自己注意機構** (TODO: 読むべき)
- **Transformer-XL** (TODO: 読むべき)
- **BERT/GPT-2** (TODO: 読むべき)
- **カーネル法** → /deep_213 生成AIに入れて学ぶ：高校数学からカーネル法・関数解析・信号処理
- **低ランク行列近似** (TODO: 読むべき)

## 関連記事

- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[長距離Transformerの読書会：Longformer・Compressive Transformer・Linformer・Performerの比較](https://huggingface.co/blog/long-range-transformers)
