---
title: "Mambaの解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-12
tags: [Mamba, State Space Model, SSM, Selective SSM, S4, HiPPO, 長文脈モデル, 線形アテンション, RNN, シーケンスモデル]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [222, 833, 255, 201, 410]
processed_at: "2026-04-12T09:24:36.341382"
---

## 要約

MambaはAlbert GuとTri Daoが2023年に発表したState Space Model（SSM）ベースのシーケンスモデルで、Transformerの「二次的ボトルネック」を解消することを目的としている。Transformerのアテンション機構はトークン間のペアワイズ通信によりO(n²)の計算複雑度を持ち、KVキャッシュがO(n)のメモリを消費するため、長文脈での推論がスケール困難になる。Mambaはこの問題に対し、連続時間の状態空間モデル（h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)）を離散化（Zero-Order Hold法）して適用することで、線形スケーリングを実現する。

Mambaの核心的な革新は「選択的状態空間モデル（Selective SSM / S6）」にある。従来のSSM（S4など）では行列A・B・Cが入力に依存しない固定パラメータだったが、MambaではB・C・Δ（タイムステップ）を入力xの関数として動的に生成する。これにより「どの情報を記憶・忘却するか」を入力依存で制御でき、Transformerのソフトアテンションに相当する選択的な情報フィルタリングが可能となる。ただしこの選択性によりRNNのような並列畳み込み計算ができなくなるため、ハードウェアを意識したアルゴリズム（HiPPO理論に基づく初期化、並列スキャン、カーネルフュージョン）でGPU上での高速化を補っている。

性能面では、Mamba-3BはThe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。推論速度はTransformerの最大5倍、メモリ使用量も大幅に削減される。100万トークンの長文脈でも性能が向上し続けることが確認されている。言語・音声・ゲノミクスなど複数モダリティでSoTAを達成している。

解釈可能性の観点では、Mambaの固定サイズ隠れ状態は情報の「ロスレス」な保持を保証しない（情報のロッシー圧縮）ため、アテンションパターンの可視化のような解析手法が直接適用できない。これはAIセーフティ研究にとっての新たな課題となる。エージェントアーキテクチャへの応用可能性としては、長期的な文脈保持や状態追跡が必要なタスク（監査証跡の連続分析、長期会話エージェントなど）でTransformerの代替として有望。

## アイデア

- 選択的状態空間モデル（S6）における「入力依存ゲーティング」は、Transformerのソフトアテンションとは異なる情報選択機構であり、固定サイズ隠れ状態でどこまでコンテキストを保持できるかがエージェントの長期記憶設計に直結する
- RNNの逐次推論とCNNの並列学習を切り替えるデュアルモード動作（推論時はRNN形式でO(1)メモリ、訓練時はConv形式で並列処理）は、メモリ制約の厳しいエッジデバイス上でのエージェント展開に応用できる
- HiPPO理論に基づく行列Aの初期化（各時系列をルジャンドル多項式の係数として近似的に保持）は、長期依存を数学的に保証する設計であり、時系列の監査ログ解析への適用が考えられる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **State Space Model** → [Mamba解説：TransformerへのState Space Modelによる挑戦](../ai-ml/2026-04-02_Mamba解説：TransformerへのState Space Modelによる挑戦.md)
- **HiPPO理論** (TODO: 読むべき)
- **FlashAttention** → [Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版](../ai-ml/2026-04-03_Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版.md)

## 関連記事

- [Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線](../ai-ml/2026-04-03_Falcon-H1-Arabic_ ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前.md)
- [Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介](../ai-ml/2026-04-08_Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介.md)
- [Apriel-H1: 効率的な推論モデル蒸留の意外なカギ](../ai-ml/2026-04-04_Apriel-H1_ 効率的な推論モデル蒸留の意外なカギ.md)
- [【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜](../ai-ml/2026-04-02_【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えた.md)
- [Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応](../infra/2026-04-02_Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応.md)

## 原文リンク

[Mambaの解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
