---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-11
tags: [Mamba, SSM, State Space Model, Selective SSM, 線形RNN, 長コンテキスト, シーケンスモデル, アテンション代替]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-11T21:20:18.646234"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを回避しながら同等の性能を実現する。Transformerはアテンション機構において全トークン間のペアワイズ通信を行うため、訓練時はO(n²)の時間計算量、推論時はKVキャッシュによりO(n)の空間計算量が必要となる。Mambaはこれをゼロ次ホールド（ZOH）離散化を用いた線形差分方程式に置き換え、隠れ状態h_t = Ā·h_{t-1} + B̄·x_t、出力y_t = C·h_tで表現する。

Mambaの最大の革新は「選択的状態空間モデル（Selective SSM / S6）」にある。従来のSSM（S4等）では行列A・B・Cが入力に依存しない固定パラメータであったが、Mambaでは入力x_tに応じてB・C・Δ（タイムステップ）を動的に変化させる。これにより「どの情報を記憶・忘却するか」を文脈に応じて選択でき、例えば「The State of the Union is…」という文で「Union」が国家の意味か労働組合の意味かを文脈から判断して適切に状態に格納できる。この選択性こそがTransformerの内容ベースアドレッシング（アテンション）に相当する機能を実現する。

実装面では「ハードウェアアウェアアルゴリズム」として、FlashAttentionに倣いHBM（高帯域幅メモリ）とSRAM（オンチップキャッシュ）間のメモリ転送を最小化する並列スキャンアルゴリズムを採用。訓練時は並列畳み込みモード、推論時は再帰モードに切り替えることでそれぞれ最適化される。Mamba-3Bモデルは同サイズのTransformerを性能で上回り、2倍サイズのTransformerに匹敵する。推論速度はTransformer比最大5倍。

スケーリング則についても、Mamba論文はTransformerと同等の法則に従うことを示しており、長期的な競合モデルとして注目される。一方でMambaの限界として、固定長の隠れ状態（圧縮された記憶）を使うため、Transformerのように過去の全トークンを正確に参照することはできず、「What was the first word I said?」のような正確な過去参照タスクでは劣る可能性がある。解釈可能性の観点では、隠れ状態の意味解釈がTransformerのアテンションヘッドよりも難しく、メカニスティック解釈可能性の研究は黎明期にある。

## アイデア

- 選択的状態空間（S6）は「入力に応じてΔ・B・Cを動的生成する」という設計で、固定遷移行列の従来SSMとTransformerのアテンション機構の中間的な表現力を実現している点が巧妙
- 訓練時に並列畳み込み、推論時に再帰処理と動的にモードを切り替えるハードウェアアウェア設計は、理論的効率性を実際のGPU性能に落とし込む実装哲学として参考になる
- 固定長隠れ状態による「過去の圧縮」という設計思想は、無限の記憶を持つTransformerとは異なる認知モデルを示唆しており、人間の作業記憶（ワーキングメモリ）の計算論的モデルとしても解釈できる
## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
