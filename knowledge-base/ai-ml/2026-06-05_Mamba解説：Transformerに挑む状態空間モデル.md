---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-05
tags: [Mamba, SSM, State Space Model, Transformer, 選択性メカニズム, S6, 線形計算量, 長文脈処理, 離散化, Hardware-Aware Algorithm]
category: "ai-ml"
related: [3105, 7117, 2480, 2510, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-05T09:11:29.746205"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのコアボトルネックである二次計算量（O(n²)）を線形計算量（O(n)）に削減する。Transformerでは全トークン間のAttentionによりKVキャッシュがO(n)のメモリを占有し、長文脈では速度・メモリ双方でスケールが悪化する。MambaはこれをControl Theory由来のSSMで代替し、最大100万トークンの長文脈でも推論が可能で、同サイズのTransformerと比較して最大5倍高速に動作する。

SSMの核心は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される状態遷移で、隠れ状態hが「過去の圧縮」として機能する。現実のディスクリートなデータに対してはZero-Order Hold（ZOH）離散化を適用し、差分方程式 h_{t+1} = Āh_t + B̄x_t に変換する。

しかし素朴なSSMには致命的な欠陥がある：パラメータA・B・Cが入力に依存しない（LTI: 線形時不変）ため、どの入力トークンを記憶・忘却するかを動的に制御できない。例えば「私はとても疲れている」と「私はとても興奮している」では同じ位置に異なる重みを付けるべきだが、LTI-SSMはこれができない。

Mambaの本質的な革新は「選択性メカニズム」（S6: Selective State Spaces）の導入だ。B・C・Δ（ステップサイズ）を入力依存のパラメータにすることで、モデルがコンテキストに応じて情報の取捨選択を動的に行えるようになる。Δが大きいトークンは状態に強く影響し、小さいトークンは素通りする形で選択的記憶が実現される。

ただし選択性の導入によりSSMの畳み込み表現が使えなくなり、並列計算が困難になる問題が生じる。これをHardware-Aware Algorithmで解決：再スキャンアルゴリズム（parallel scan）を用いてシーケンシャル計算を並列化し、中間状態はGPUのSRAM（L1キャッシュ相当）内で処理してHBM（VRAM）への書き戻しを最小化するFlashAttention類似の最適化を施している。

Mamba-3BモデルはオープンコーパスであるThe Pileでの評価において、同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能を示す。一方で、In-Context Learningや複数文書間の情報検索タスクではTransformerに劣るとの報告もあり、固定サイズの状態に全情報を圧縮することの限界も存在する。解釈可能性の観点では、Attentionヘッドのように可視化できる注意パターンがなく、内部状態の解釈が困難という課題がある。監査エージェント開発への示唆としては、長大な監査ログや取引履歴を低メモリ・高速に処理するバックボーンとして活用できる可能性がある一方、特定の証拠を正確に参照する能力はAttentionベースモデルに軍配が上がる点に注意が必要。

## アイデア

- 選択性メカニズム（S6）によりΔパラメータが入力依存になることで、LTI-SSMでは不可能だった動的な情報取捨選択が実現される点—これはAttentionのsoftmaxによる重み付けとは全く異なるメカニズムで同等の効果を達成している
- Parallel ScanとSRAM活用によるHardware-Aware Algorithmが、選択性導入による並列計算不可問題を回避している点—アルゴリズムとハードウェア特性の共同最適化がFlashAttentionと同様の思想で実装されている
- 固定サイズの隠れ状態が「過去の圧縮」として機能するため、無限の文脈長でもメモリが増加しないというトレードオフ—これはRAGや外部メモリなしで超長文脈を扱う新たなパラダイムを示唆する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **線形時不変システム（LTI）** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
