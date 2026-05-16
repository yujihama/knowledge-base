---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-30
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, Zero-Order Hold, Selective SSM, 長文脈]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-30T12:51:54.426183"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算コスト問題を解消することを目的としている。Transformerでは全トークン間のペア演算によりO(n²)の計算複雑性とO(n)のKVキャッシュメモリが必要となるが、MambaはSSMを用いて線形スケーリングを実現する。アーキテクチャの核心は制御理論に由来する微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、現在の隠れ状態と新規入力から次の出力を予測する。この連続時間方程式をZero-Order Hold（ZOH）離散化によって離散化し、実データ処理に適用できる差分方程式へ変換する。重要な革新点は行列A・B・CをSelective State Space（S6）として入力依存にした点であり、従来のS4モデルが固定パラメータだったのに対しMambaは動的に選択的な情報フィルタリングを行う。これによりモデルは関連情報を保持し不要情報を捨てる判断を文脈に応じて行える。並列学習のためにはConv1Dやスキャン演算を用いたHardware-Aware Parallel Algorithmを採用し、逐次推論時は圧縮された隠れ状態のみを持ち回るため定数メモリで動作する。Mamba-3BはThe Pileデータセットにおいて同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能を示した。推論速度はTransformerの最大5倍。100万トークン級の超長文脈でも現実的な計算コストで処理可能な点が最大の強みである。一方で弱点として、In-Context Learningにおける選択的コピーやリコールタスクでTransformerより劣る実験結果も報告されており、固定サイズの隠れ状態に情報を圧縮する構造上、Transformerのような「全過去トークンへの完全アクセス」は原理的に不可能である。解釈可能性・AIセーフティの観点では、Transformerとは異なるアテンションパターン構造を持つため、既存のMechanistic Interpretability手法の直接適用が難しく新たな解析手法の開発が必要とされる。監査エージェント開発への示唆として、長大な監査ログや取引履歴を扱う際に線形スケーリングのMambaはコスト効率で優位性を持つ可能性があるが、特定トークンへの精密な参照が必要なタスクでは現時点ではTransformerハイブリッド構成が現実的な選択肢となる。

## アイデア

- 隠れ状態を『過去の圧縮』と定義することで、Transformerの全トークン参照を不要にする設計思想は、ストリーミングデータや無限長コンテキストへの対応を理論的に可能にする
- 行列A・B・Cを入力依存（Selective）にするだけで、固定SSMから動的フィルタリング能力が生まれる点は、パラメータ効率と表現力のトレードオフを示す好例
- 並列学習と逐次推論を同一モデルで切り替えるHardware-Aware設計は、訓練効率と推論速度を両立させるアーキテクチャ工学の工夫として他モデルへの応用可能性がある

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **離散化（ZOH）** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
