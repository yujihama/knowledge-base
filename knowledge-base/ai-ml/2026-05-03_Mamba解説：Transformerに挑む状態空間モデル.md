---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-03
tags: [Mamba, SSM, State Space Model, Transformer代替, 選択的状態空間, 線形スケーリング, 長文脈, Hardware-Aware, Parallel Prefix Scan, ZOH離散化]
category: "ai-ml"
related: [2480, 2510, 3105, 222, 833]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-03T12:34:56.236360"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つ二次計算量ボトルネックを克服することを目的とする。Transformerはすべてのトークン間のペアワイズ通信（O(n²)の時間計算量）とKVキャッシュ（O(n)のメモリ）を必要とするため、長いコンテキストウィンドウで極めて非効率になる。Mambaはこれに対し、制御理論由来の連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) をベースとするSSMを通信コンポーネントとして採用し、計算コンポーネントにはMLPスタイルの射影を維持する構成を取る。連続時間方程式はZero-Order Hold（ZOH）法で離散化され、実際のシーケンスデータに適用可能にする。従来のSSM（S4等）はパラメータ行列A・B・Cが入力に依存しない線形時不変（LTI）系であったため、コンテキスト依存の選択的情報処理が不可能だったが、Mambaはこれらのパラメータを入力依存（セレクティブSSM）にすることで選択的な記憶・忘却を実現する。ただしこの変更により畳み込み表現が使えなくなるため、代わりにParallel Prefix Scanアルゴリズムを採用し、GPUハードウェアに最適化したHardware-Aware Selective Scanをカーネルフュージョンとrecomputationで実装している。Mamba-3Bモデルは同サイズのTransformerと同等以上、2倍サイズのTransformerと同程度の性能をThe Pile上で達成し、Transformerの最大5倍の推論速度と100万トークンまでの線形スケーリングを実現する。隠れ状態サイズが固定のため情報の圧縮・選択が必須であり、Transformerのように全過去情報を保持できない点は本質的なトレードオフとなる。解釈可能性の観点では、Transformerのアテンションパターン分析手法がSSMに直接適用できないため、メカニスティック解釈可能性研究に新たな課題をもたらす。監査エージェント開発への示唆として、長大なログ・ドキュメントストリームをO(n)メモリで逐次処理できるアーキテクチャは、監査証跡の継続的監視や長期セッション管理において実用的な選択肢となりうる。

## アイデア

- 入力依存パラメータ（セレクティブSSM）にすることで「何を記憶し何を忘れるか」を動的に制御できる点が、固定圧縮の旧来SSMとの本質的な差異であり、RNNの課題（固定隠れ状態サイズ）をより柔軟に扱う設計思想
- Parallel Prefix ScanによりRNN的な再帰構造をGPU並列計算に変換している点：逐次的な依存関係をツリー状の並列演算に変換することで訓練効率とハードウェア活用を両立させる工夫
- 状態は「過去の圧縮」であるという定式化から、固定サイズ隠れ状態に何を詰め込むかという情報理論的トレードオフが生じ、Transformerの「忘れない」設計と対比してコンテキスト選択の重要性が浮き彫りになる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（S4）** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **並列プレフィックススキャン** → /deep_881 Hawkesプロセスの大規模並列厳密推論

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
