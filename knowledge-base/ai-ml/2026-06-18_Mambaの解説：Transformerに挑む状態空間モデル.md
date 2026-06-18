---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-18
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, parallel scan, 選択的SSM, S4, S6, Zero-Order Hold]
category: "ai-ml"
related: [2510, 3105, 7961, 2480, 7597]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-18T21:10:30.220122"
---

## 要約

Mambaは、Transformerの二次計算量ボトルネックを克服することを目的とした状態空間モデル（SSM）ベースのアーキテクチャである。Gu and Daoによって開発され、100万トークン規模の長いシーケンス長においてもTransformerと同等の性能とスケーリング則を実現し、推論速度はTransformerの最大5倍に達する。

**Transformerの問題点**：Attentionメカニズムはすべてのトークン間のペアワイズ通信を行うため、訓練時のforward passはO(n²)の時間計算量を持つ。また、KVキャッシュはO(n)のメモリを要し、長いコンテキストではCUDA OOMエラーが現実的な脅威となる。Sliding Window AttentionやFlashAttentionなどの緩和策はあるが、超長文脈には根本的な代替手段が必要である。

**SSMの仕組み**：MambaはControl Theory（制御理論）に基づくSSMをAttentionの代替として採用する。連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) として定式化され、状態hは過去の圧縮表現として機能する。これはMarkov Decision Processへの変換に相当し、過去全体を参照せずとも未来の予測が可能になる。

**離散化（Zero-Order Hold）**：実際の離散時間データを扱うため、ZOH法を用いて連続微分方程式を差分方程式へ変換する。その結果、行列A・BはΔ（タイムステップ）によってスケールされたĀ・B̄に変換される。

**SSMの計算モード**：訓練時は畳み込み（Convolution）として並列計算が可能（効率的）。推論時はRNN的な再帰（Recurrence）として逐次計算し、O(1)のメモリで動作する。この二重性がMambaの実用的強みである。

**選択的SSM（S6）**：古典的なS4モデルの問題は、A・B・Cが入力に依存しない点（線形時不変）にあり、選択的フィルタリングができない。Mambaはこれを解決するため、Δ・B・Cを入力xの関数として学習させ、コンテキストに応じた情報選択（何を記憶し何を忘れるか）を実現する。

**ハードウェア最適化（parallel scan + kernel fusion）**：選択的SSMでは並列畳み込みが使えないため、parallel scanアルゴリズムをHBM/SRAMのカーネルフュージョンと組み合わせてGPUメモリ転送を最小化する。これによりnaiveな実装より高速な計算を実現している。

**Mamba-3Bの評価**：The Pileベンチマークにおいて、同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を発揮する。言語・音声・ゲノム等の複数モダリティでState-of-the-Artを達成している。

**解釈可能性・安全性への含意**：TransformerのAttentionパターンは可視化による解釈が可能だが、MambaのSSM内部状態は連続的・圧縮的であり、解釈が困難である。これはCircuit-level interpretabilityの手法が適用しにくいことを示唆する。監査エージェント開発においては、長文書・監査証跡の長文脈処理にMambaベースアーキテクチャの活用が候補となりうるが、内部状態の解釈可能性確保は課題として残る。

## アイデア

- SSMが訓練時は畳み込み、推論時はRNNとして動作する二重性により、並列訓練と定数メモリ推論を両立している点は、長文監査ログ処理への応用で特に魅力的
- 選択的SSM（S6）が入力依存のΔ・B・Cを学習することで「何を記憶し何を忘れるか」を動的に決定する仕組みは、ReActエージェントのコンテキスト管理と概念的に対応しており、エージェント設計への示唆がある
- TransformerのAttentionと異なりMambaの内部状態が解釈困難であることは、監査・説明責任が求められる領域での採用に際してinterpretability研究の空白地帯を示しており、LLM-as-judgeとの組み合わせ検討が必要

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / 再帰ニューラルネット** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込み（Convolution）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7961 LLMに「睡眠」が必要な理由 ― 論文「Language Models Need Sleep」解説
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_7597 深層学習・生成AIの全体像を「3つの問い」で整理する｜CNNから拡散モデル・Mambaまで

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
