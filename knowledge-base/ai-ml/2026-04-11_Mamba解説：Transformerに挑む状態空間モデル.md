---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-11
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 長文脈処理, 選択的メカニズム, ZOH離散化, Parallel Associative Scan]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-11T09:22:04.233833"
---

## 要約

MambaはAlbert GuとTri Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttention機構が持つO(n²)の計算量ボトルネックを解消することを目的としている。Transformerは各トークンが過去の全トークンを参照するためKVキャッシュがO(n)のメモリを消費し、長いコンテキストではGPUのOOMエラーが深刻な問題となる。Mambaはこれに対し、制御理論にインスパイアされたSSMを通信コンポーネントとして採用し、MLP系の射影を計算コンポーネントとして維持するブロック構造を取る。

SSMの基本は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される。ここでhは隠れ状態（過去の圧縮）、xは入力観測、yは出力である。実際の離散入力に対応するため、Zero-Order Hold（ZOH）離散化を用いてこれを差分方程式 h_t = Ā h_{t-1} + B̄ x_t、y_t = C h_t に変換する。

SSMは畳み込みとしても表現でき、学習時は並列畳み込みで高速化（O(n log n)）、推論時はRNN的な逐次計算で定数時間・定数メモリを実現する。この二重性がMambaの効率の核心である。

従来のSSM（S4等）はA・B・Cが入力に依存しない時不変（LTI）システムであったため、内容に基づく選択的な情報保持が困難だった。Mambaの最大の革新は「選択的メカニズム（Selective State Space）」で、B・C・Δを入力x_tの関数とすることでSSMをデータ依存にした点にある。これによりモデルは関連情報を保持し、不要な情報を破棄する選択を動的に行える。

ハードウェア面ではFlashAttentionに触発されたParallel Associative Scanを用いたカーネルフュージョンにより、HBMとSRAM間のメモリI/Oを削減し、Transformerに対して最大5倍の推論速度を達成する。Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pileベンチマーク等で示した。また百万トークン規模のシーケンス長でも性能が向上し続けることが確認されている。

デメリットとしては、選択的メカニズムによりSSMの並列畳み込み表現が使えなくなること、Transformerに比べてin-context learningが若干弱い可能性があること、解釈可能性の研究が発展途上であることが挙げられる。言語・音声・ゲノミクスなど複数モダリティでSOTAを達成しており、長文脈処理が必要なアプリケーションで特に有望とされる。

## アイデア

- 隠れ状態hが「過去の圧縮」として機能するという概念は、Agentの記憶設計（何を保持し何を捨てるか）に直接応用できる思考フレームワーク
- RNNとして推論・畳み込みとして学習という二重性は、学習効率と推論効率を両立させるアーキテクチャ設計の参考パターンとなる
- 入力依存のB・C・Δによる「選択的情報保持」はAttentionのソフト選択とは異なるアプローチで、注意機構の本質的な役割を再考させる
## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
