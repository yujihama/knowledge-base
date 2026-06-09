---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-09
tags: [Mamba, SSM, 状態空間モデル, Selective SSM, 線形スケーリング, 長文脈, RNN, 並列スキャン, Hardware-Aware]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-09T09:22:18.011438"
---

## 要約

MambaはAlbert GuとTri Daoが開発した、Transformerの代替となる状態空間モデル（SSM）ベースのアーキテクチャ。Transformerの最大の欠点であるAttentionのO(n²)計算複雑度を克服し、シーケンス長に対して線形スケーリングを実現する。Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。推論速度はTransformerの最大5倍。

【コア技術：SSMの仕組み】連続時間の状態方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を基礎とする。状態hは過去の情報を圧縮したもの（マルコフ決定過程的）で、新規入力xと組み合わせて次の出力yを決定する。実装にあたってはZero-Order Hold（ZOH）離散化でこれを離散差分方程式に変換する。

【線形注意との違い：選択的SSM】従来のSSMは行列A・B・Cが入力に依存しない線形時不変（LTI）システムだったため、フィルタとして畳み込みで効率的に計算できるが、文脈に応じた選択的な情報保持ができなかった。Mambaの革新は「選択機構（Selective SSM）」の導入で、B・C・Δを入力xの関数にすることで内容依存のフィルタリングを実現。これにより選択的コピーや誘導ヘッドのようなタスクをこなせるようになった。一方、選択機構の導入で畳み込み表現が使えなくなるため、推論時は再帰（RNN的）、学習時はHardware-Aware Parallel Scan（CUDA上での並列スキャン）で効率を担保する。

【ハードウェア最適化】FlashAttentionと同様の発想で、HBM（高帯域幅メモリ）ではなくSRAM（オンチップ）で主要計算を行い、メモリ転送コストを削減するカーネル融合を実装。

【Mambaブロック構成】入力→線形投影→選択的SSM（+ Conv層）→SiLU活性化→ゲート付き出力。Transformerのようにブロックを積み重ねる形式。

【解釈可能性・安全性への含意】Transformerの解釈可能性研究（回路分析、Induction Heads等）はAttentionパターンの可視化に依存しており、SSMへの直接移植は困難。SSMの隠れ状態は連続値ベクトルであり、Attentionのように「どのトークンを参照したか」が明示的でない。

【監査エージェント開発への示唆】長大なドキュメント（監査調書、法令全文等）を処理するRAGパイプラインにおいて、Mambaの線形スケーリングはコンテキスト長1Mトークン超の処理を現実的なコストで実現する可能性がある。ただし現時点ではエコシステム（ツール、ファインチューニング事例）でTransformerに大きく劣る。

## アイデア

- 選択機構（B・C・Δを入力依存化）によってLTIの限界を克服しつつ、学習時はParallel Scan、推論時はRNN的再帰という二重表現で効率を両立する設計は、アーキテクチャ設計のトレードオフ管理の好例
- 隠れ状態hが「過去の圧縮」としてマルコフ性を持つという定式化は、エージェントの作業記憶（Working Memory）設計に応用可能──長い対話履歴を固定サイズの状態ベクトルに圧縮し続けるエージェント記憶アーキテクチャが考えられる
- 解釈可能性研究がAttention可視化に依存していることの指摘は重要で、SSMが主流化した場合に監査・説明可能AI（XAI）の手法が根本から再構築を迫られる可能性を示している

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
