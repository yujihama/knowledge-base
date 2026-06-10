---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-10
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形スケーリング, Selective SSM, Hardware-Aware Parallel Scan, 長文脈処理]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-10T09:23:11.604542"
---

## 要約

Mambaは、Gu and Dao（2023）が提案した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttention機構が持つO(n²)の計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりKVキャッシュがO(n)のメモリを消費し、長文脈での推論が困難だが、MambaはSSMを用いて線形スケーリングを実現する。Mamba-3BモデルはThe Pileベンチマークにおいて同サイズのTransformerを上回り、2倍のサイズのTransformerと同等の性能を示す。

技術的な核心は、制御理論由来の状態空間表現にある。隠れ状態h(t)を微分方程式 h'(t) = Ah(t) + Bx(t)、出力を y(t) = Ch(t) + Dx(t) で定義し、連続時間系を離散化（Zero-Order Hold法）することで実装する。古典的なSSMとの最大の違いは「選択的状態空間（Selective SSM / S6）」で、パラメータB・C・ステップサイズΔを入力xに依存させることで、トークンごとに何を状態に記憶し何を忘れるかを動的に制御できる。これによりTransformerのAttentionに近いコンテンツ依存フィルタリングが可能になる。

効率的な計算を実現するためにHardware-Aware Parallel Scanを採用。通常の逐次スキャンはO(n)時間だが並列化できないため、GPUに不向き。Mambaはプレフィックスサムの並列アルゴリズムでO(log n)の並列処理を実現し、SRAMを活用したFlashAttention的アプローチでHBMへのアクセスを最小化する。これによりTransformerより最大5倍高速な推論を達成する。

アーキテクチャはMambaブロックを積み重ねた構造で、各ブロックは1D畳み込み・選択的SSM・SiLU活性化・スキップ接続から構成される。トークン間通信はSSMが担い、トークン内計算はMLP的な射影層が担う点でTransformerブロック（Attention + MLP）と対応する。

解釈可能性の観点では、Attention HeadはInduction HeadやPrevious Token Headなど役割分担が明確だが、MambaのSSM状態は連続的な「過去の圧縮」であり解析が難しい。一方、Mambaは任意の過去トークンを明示的に参照できないため、精密なルックアップが必要なタスクでは劣る可能性がある。監査エージェント開発への示唆として、長文書（監査調書・規制文書）の文脈理解において、TransformerのOOM問題を回避しつつ百万トークン規模を処理できる点は実用的価値が高い。ただし特定の過去トークンへの精密な参照が求められる構造化データ処理では注意が必要。

## アイデア

- 選択的SSM（S6）は入力依存のパラメータB・C・Δを持つことで、静的フィルタだった古典的SSMに「何を記憶するか」の動的制御を加えた点が本質的革新。これはAttentionのソフトアドレッシングとは異なるアプローチで情報選択を実現している
- 状態空間の隠れ次元数がTransformerのKVキャッシュに相当するが、固定サイズに圧縮される点が鍵。推論時はO(1)メモリで逐次処理でき、学習時はParallel Scanで並列化できるという二重の効率性を持つ
- Temple Runのアナロジーが示す通り、SSMは「画面全体を記憶する」のでなく「状態という圧縮表現＋新規観測」で動作するため、過去全体への参照が不要なタスクではTransformerより効率的だが、精密なルックアップが必要なタスクでは構造的限界がある

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **離散化・Zero-Order Hold** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
