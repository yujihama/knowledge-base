---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-08
tags: [Mamba, SSM, 状態空間モデル, Transformer, 選択的状態空間, 線形スケーリング, 長文コンテキスト, HiPPO, 並列スキャン]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-08T12:09:45.397829"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算ボトルネックを解消することを目的としている。Transformerはアテンション機構において全トークン間のペアワイズ通信を行うため、訓練時O(n²)、推論時O(n)の時間計算量となり、長文コンテキスト（例：100万トークン）での利用が困難だった。MambaはこのアテンションをSSMで置き換え、線形スケーリングを実現する。

SSMの基本方程式はh'(t) = Ah(t) + Bx(t)（状態遷移）およびy(t) = Ch(t) + Dx(t)（出力）で表される連続時間微分方程式であり、これをZero-Order Hold（ZOH）離散化によって差分方程式へ変換して実装する。離散化後の方程式はh_t = Āh_{t-1} + B̄x_tおよびy_t = Ch_tとなる。この構造により、過去の全情報を固定サイズの隠れ状態hに圧縮しながら逐次処理が可能になる。

従来のSSM（S4等）との最大の差異は「選択的状態空間」の導入にある。従来のSSMでは行列A・B・Cが入力に依存しない固定パラメータだったが、Mambaでは行列B・C・ステップサイズΔを入力x_tの関数として動的に決定する。これにより、モデルが現在の入力に応じて「何を記憶し何を忘れるか」を自律的に制御できる。ただし、選択的SSMは並列スキャンの単純な適用が困難になるため、カーネル融合・並列スキャン・再計算を組み合わせたHardware-Aware Parallel Algorithmを採用し、GPUのSRAMとHBM間の帯域幅ボトルネックを回避している。

性能面では、Mamba-3BがThe Pileベンチマークにおいて同サイズのTransformerを上回り、2倍サイズのTransformerと同等のパフォーマンスを示した。推論速度はTransformerの最大5倍。一方、現時点での弱点として、In-Context Learning能力がTransformerより劣ること、固定サイズの隠れ状態への圧縮により非常に長い依存関係の保持が困難なこと、Retrieval・Copying等のタスクで劣後することが指摘されている。解釈可能性研究においても、アテンションヘッドという解析単位がなくなるため既存の手法がそのまま適用できない課題がある。

## アイデア

- 固定サイズの隠れ状態への圧縮という設計思想は「効率的な情報圧縮」の問題であり、何を記憶すべきかを入力依存で動的に決定する選択機構がRAGの検索判断やエージェントのコンテキスト管理に応用できる可能性がある
- HiPPO理論（高次多項式射影演算子）により行列Aを初期化することで長期依存関係を保持する仕組みは、時系列監査データ（ログ・トランザクション系列）の効率的なエンコードに応用できる
- Hardware-Aware Parallel Algorithmとして「どのデータをGPUのSRAMに置くか」を数学的に最適化する手法は、LLM推論インフラ設計においてメモリ階層を意識したシステム設計の重要性を示す好例
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
