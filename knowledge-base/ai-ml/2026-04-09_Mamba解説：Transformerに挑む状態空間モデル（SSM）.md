---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-09
tags: [Mamba, SSM, State Space Model, Transformer, 線形アテンション, 長文脈, 選択的状態空間, ZOH離散化, シーケンスモデル]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [199, 222, 833, 255, 1494]
processed_at: "2026-04-09T21:18:44.005699"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンションメカニズムが持つO(n²)の計算複雑性問題を解決することを目指している。Transformerでは全トークン間のペアワイズ通信が必要なためKVキャッシュがO(n)のメモリを消費し、長文脈での推論が困難だが、MambaはSSMを用いることで系列長に対して線形スケーリングを実現する。

理論的背景はControl Theory（制御理論）に基づく微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去情報の圧縮として機能する。連続時間の微分方程式はZero-Order Hold（ZOH）離散化によって差分方程式に変換され、実際のトークン列処理に対応する。

従来のSSM（S4等）との最大の違いは「選択的状態空間（Selective State Space）」機構にある。S4ではA・B・Cが入力に依存しない固定パラメータだったが、Mambaでは各トークンの入力に応じてB・C・Δ（タイムステップ）が動的に変化する。これにより「どの情報を状態に保持し、どの情報を忘れるか」を入力に基づいて選択できるようになり、LSTMのゲート機構に類似した選択性を持つ。

実装面では、この選択性が原因でParallel Scanアルゴリズムの単純な適用が困難になるが、FlashAttentionのようなカーネルフュージョン技術（Flash State Space Model）とハードウェアアウェアな実装により計算効率を確保している。ベンチマーク結果では、Mamba-3BはThe Pileでの事前学習・下流評価の両方において同サイズのTransformerを上回り、2倍のサイズのTransformerと同等の性能を示した。推論速度はTransformerより最大5倍高速。

アーキテクチャ上の位置づけとしては、Transformerの「Attention（トークン間通信）＋MLP（トークン内計算）」に対し、MambaはSSM（通信）＋MLP（計算）という構造を持つ。解釈可能性の観点では、隠れ状態の次元がボトルネックとなり、Transformerのように任意の過去トークンに直接アクセスできないため、一部の解釈可能性研究手法が適用困難になる課題がある。また選択的な記憶・忘却の特性が事実の上書きや誤情報問題に対してTransformerと異なるリスクプロファイルを持つ可能性が指摘されている。

## アイデア

- 選択的状態空間（Selective SSM）により「入力に応じて何を記憶し何を忘れるか」を動的に決定できる点は、LSTMゲートの一般化として捉えられ、固定メモリ制約下での情報取捨選択の原理として興味深い
- 系列長に対して線形スケーリング（O(n)）を実現しつつ、Transformerと同等のスケーリング則を示した点は、アーキテクチャ選択がスケーリング特性に与える影響の観点から重要な実証データ
- 隠れ状態が過去全体の固定次元圧縮である制約が解釈可能性研究の困難さにつながる点は、モデルの内部表現と説明可能性のトレードオフを考える上での具体的事例になる
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
