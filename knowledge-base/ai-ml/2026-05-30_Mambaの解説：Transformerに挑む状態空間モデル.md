---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-30
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 長文脈, Parallel Scan, 選択性, 離散化]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-30T09:19:58.817455"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを克服することを目的としている。Transformerでは全トークン間のAttentionにより学習時O(n²)の計算量が発生し、自己回帰推論でも各ステップがO(n)となるため、長文脈では速度・メモリ双方が問題になる。Mambaはこれをコントロール理論由来の状態空間表現で代替する。基本的なSSMは連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表現され、「状態」はこれまでの入力の圧縮とみなせる。実装上はZero-Order Hold（ZOH）離散化により差分方程式へ変換し、行列A・B・Cをパラメータとして学習する。古典的SSM（S4等）では行列が入力に依存しない固定値であったため、「選択的な記憶」ができないという欠点があった。Mambaの核心的革新は「選択性（Selectivity）」であり、B・C・Δを入力xの関数として動的に生成することで、どの情報を状態に取り込み・捨てるかを制御できるようにした。これによりS4が苦手とした選択的コピーや誘導ヘッドの模倣が可能となった。しかし選択性の導入により畳み込み表現での並列計算が不可能になるため、代わりにParallel Scan（並列スキャン）アルゴリズムをHBM-SRAM間のI/Oを最小化するFlashAttentionライクな手法で実装し、学習効率を確保している。推論時はRNNと同様の逐次計算となり、シーケンス長に対して線形スケールで動作する。Mamba-3Bは同規模Transformerを上回り、2倍サイズのTransformerに匹敵する性能を示し、最大100万トークンの文脈長でも性能向上が確認されている。速度はTransformer比最大5倍。Mambaブロックはヘッドの代わりにSSMを用い、Transformerと同様にMLPによるトークン内計算を組み合わせる構造をとる。解釈可能性の面では、Mambaの状態は圧縮された過去情報であり、Transformerのより直接的なKV Cacheとは異なるため、Circuit分析等の手法の転用には課題がある。監査エージェント開発への示唆としては、長い監査ログや規程文書など長文脈の一括処理においてTransformerより低コストでのシーケンス処理が期待でき、リアルタイム審査エージェントへの応用可能性がある。

## アイデア

- 選択性（Selectivity）をB・C・Δを入力依存にすることで実現する設計は、RNNの固定ゲートとAttentionの全参照の中間に位置する新しいアーキテクチャパラダイムであり、「何を覚えるか」を動的に学習させる点が核心
- Parallel Scanによる学習の並列化とRNNモードによる推論の線形計算を両立させた実装戦略は、トレーニング効率と推論効率を同時に最適化する設計として、将来のシーケンスモデル全般に波及しうる
- 状態が「過去の圧縮」であるというSSMの性質は、無限の文脈長を有限メモリで近似するという哲学的に興味深い問いを提示しており、どの情報が圧縮・破棄されるかの解釈可能性研究が今後の重要課題になる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **離散化（ZOH）** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
