---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-12
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 選択的状態空間, 線形スケーリング, 長コンテキスト, S4, ZOH離散化, Hardware-Aware]
category: "ai-ml"
related: [2510, 222, 2480, 1837, 3105]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-12T21:16:54.850845"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つO(n²)の計算複雑性問題を解消する。Transformerでは全トークン間のペアワイズ通信（KVキャッシュ）により、長いコンテキストでメモリと計算量が二次関数的に増大するが、MambaはSSMを使いシーケンス長に対して線形スケーリングを実現する。

理論的基盤は制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、「状態」は過去の圧縮表現として機能する。この連続時間表現をZero-Order Hold（ZOH）離散化によって差分方程式に変換し、実際のシーケンス処理に適用する。

古典的なS4等のSSMとMambaの最大の違いは「選択的状態空間（Selective SSM / S6）」機構にある。従来のSSMでは行列A・B・Cが入力に依存せず固定されていたため、時間・内容を選択的に記憶・忘却することができなかった。Mambaでは入力xに応じてB・C・Δが動的に変化し、重要な情報を選択的に保持できる。たとえば「The company...it」という文脈では、「it」が何を指すかを動的に解決できる。

ハードウェア最適化として、MambaはKernel Fusionと並列スキャンアルゴリズムを組み合わせた「Hardware-Aware Parallel Algorithm」を採用。再帰的な計算をGPUのSRAM上で効率的に処理し、推論速度はTransformerの最大5倍を達成。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能をThe PileベンチマークとThe Pile以外のダウンストリームタスクで示した。

アーキテクチャ上、MambaブロックはTransformerブロックのAttention層をSSM層に置き換え、MLP部分は維持する構造。Transformerのように「全過去トークンを参照」するのではなく、隠れ状態hに過去を圧縮して持ち歩く点でRNNに近いが、並列学習が可能な点が異なる。

解釈可能性・AIセーフティ観点では、Transformerに比べて内部状態の解析が困難な課題がある。また「無限コンテキスト」は理論上可能だが実際には有限の隠れ状態に全情報を圧縮するため、超長期依存の保持には限界もある。監査エージェント開発への示唆として、長大なログ・監査証跡を低コストで処理する際のバックボーンアーキテクチャ候補として有望。特に監査証跡のような長期シーケンスデータを扱うReActエージェントのメモリ機構として、Mambaの線形スケーリング特性は実装上の利点となり得る。

## アイデア

- 「状態は過去の圧縮」というフレームワーク：隠れ状態hが過去全体を有限ベクトルに圧縮するという設計思想は、RNNとTransformerの中間的な立ち位置であり、無限コンテキストを扱う際のトレードオフ（何を忘れるか）を明示的に制御できる点が新しい
- 入力依存の選択性（S6）：行列B・C・Δを入力xの関数とすることで、固定パラメータのSSMが抱えていた「全トークンを均等に処理してしまう」問題を解決。コンテンツベースの選択的記憶はアテンション機構に近い表現力を線形コストで実現する
- Hardware-Aware Parallel Algorithm：再帰計算とKernel Fusionを組み合わせることで、理論上は逐次的なSSMをGPUで並列実行する実装上の工夫。アルゴリズムの数学的性質とハードウェア特性の両方を意識した設計が5倍高速化を可能にしており、理論と実装の橋渡し事例として参考になる

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル (S4)** (TODO: 読むべき)
- **離散化 / ZOH** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
