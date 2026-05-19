---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-19
tags: [Mamba, SSM, State Space Model, Transformer, 線形時不変システム, 選択的SSM, 並列スキャン, 長コンテキスト, ZOH離散化]
category: "ai-ml"
related: [3105, 222, 2480, 2510, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-19T21:32:44.600106"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルであり、Transformerが抱える二次計算コストの問題を克服することを目的とする。Transformerのアテンション機構はすべてのトークン間のペアワイズ通信を行うためO(n²)の時間計算量と O(n)の空間計算量（KVキャッシュ）を必要とし、長いコンテキスト（例：100万トークン）では実用上の限界がある。

Mambaはこの問題をSSMで解決する。SSMの核心は、連続時間の微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) で表される状態遷移にある。ここでhは隠れ状態（過去の圧縮表現）、xは入力、yは出力、A/B/C/Dはパラメータ行列である。この連続方程式はZero-Order Hold（ZOH）離散化によって離散差分方程式に変換され、実際のトークン列に適用される。

従来のSSM（S4等）は行列A/B/Cが入力に依存しない線形時不変（LTI）システムであったが、これはコンテキストに依存した選択的な情報保持ができないという欠点を持つ。Mambaの最大の革新は「選択的SSM（S6）」であり、B・C・Δ（ステップサイズ）を入力xの関数として動的に変化させる仕組みを導入した点にある。これにより、関連トークンを選択的に記憶・忘却することが可能になり、実質的にTransformerのソフトアテンションに相当する選択性を達成する。

ただし、この入力依存性によりバッチ計算が困難になる。Transformerの畳み込み的な並列計算（カーネル計算）が使えなくなるため、Mambaは「Hardware-Aware Parallel Scan（並列スキャン）」をGPUのSRAM上で実装する独自のCUDAカーネルで効率化を図る。結果として推論時はO(1)空間（固定サイズの隠れ状態のみ）・O(n)時間、訓練時もスキャンアルゴリズムによって並列化が可能となる。

Mamba-3BはThe Pileベンチマークにおいて同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。推論速度はTransformerの最大5倍高速。ただしMambaの隠れ状態は固定サイズのため情報の圧縮損失が生じ、「In-Context Learning（ICL）」や複雑な検索タスクではTransformerに劣る可能性がある。また、Transformerのアテンションマップのような解釈可能性の手法がMambaには直接適用できないため、AIセーフティ・解釈可能性研究の観点では新たな課題となる。

監査エージェント開発への示唆として、長いトランザクションログや監査証跡（数万〜数十万トークン規模）を低コストで処理する基盤モデルとしてMambaアーキテクチャを活用できる可能性がある。ただしICLの弱さは少数事例によるルール適用に影響するため、Fine-tuningを前提とした設計が必要となる。

## アイデア

- 選択的SSM（S6）でB・C・Δを入力依存にすることで、固定ステートマシンを「動的なソフトアテンション」に昇格させる発想が巧妙。Transformerとの性能差を埋めた核心部分
- 隠れ状態が固定サイズである点は「状態は過去の圧縮」という情報理論的な制約を明示しており、モデルが何を忘れ何を保持するかを学習する必要がある——これは人間の記憶モデルに近い
- GPUのHBM（高帯域メモリ）ではなくSRAM（共有メモリ）上でカーネルを融合させるHardware-Aware設計は、アルゴリズムとハードウェア特性を同時最適化するFlashAttentionと同じ設計思想であり、今後のアーキテクチャ競争のトレンドを示唆する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **State Space Model（SSM）** (TODO: 読むべき)
- **微分方程式の離散化** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **並列スキャンアルゴリズム** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
