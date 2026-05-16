---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-26
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 長コンテキスト, 選択メカニズム, FlashAttention, 離散化, ZOH, 並列スキャン]
category: "ai-ml"
related: [2510, 222, 2480, 1837, 833]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-26T12:14:19.430723"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを解消することを目的としている。Transformerのアテンション機構はトークン間の全対全通信を行うためO(n²)の時間計算量とO(n)の空間計算量（KVキャッシュ）を要し、長いコンテキスト（100万トークン規模）では実用上の限界がある。

MambaはこれをSSMで置き換える。SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、制御理論に由来する。状態hは過去の情報を圧縮した表現であり、新しい観測xと組み合わせることで次の出力yを決定する。実際のデータは離散的なため、Zero-Order Hold（ZOH）離散化を用いて差分方程式に変換する。

SSMは畳み込みとしてトレーニング（並列処理可能）し、再帰として推論（一定の状態サイズで高速）できる二面性を持つ。これにより訓練効率と推論効率を両立する。

しかし古典的なSSMには「input-independence」という問題がある。行列A、B、Cが入力xに依存せず固定されているため、コンテキストに応じた動的な情報選択ができない。Mambaはこれを「選択メカニズム（Selection Mechanism）」で解決する。B、C、Δ（ステップサイズ）を入力依存にすることで、関連情報を保持し不要情報を無視するフィルタリングが可能になる。これはTransformerのソフトアテンションに対応する動的な選択能力に相当する。

ただしこの入力依存化によって畳み込み計算ができなくなるため、代わりにHardware-Aware Parallel Scanアルゴリズムを用いてGPU SRAM上で効率的に計算するFlashMamba的な実装を行っている。これによりTransformerより最大5倍の速度を実現し、Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を達成している。

解釈可能性の観点では、MambaはTransformerより状態サイズが小さいため情報のボトルネックが生じやすく、逆に状態の解析が容易になる可能性がある。一方でアテンション行列のような直接的な解釈ツールは存在しない。AI安全性の観点では、KVキャッシュが増大しないため悪意あるプロンプトの蓄積リスクが低い可能性がある。監査AIへの示唆として、長文書（契約書、監査報告書）の処理に必要な超長コンテキスト処理をTransformerより低コストで実現できる点が有望である。

## アイデア

- SSMは訓練時は畳み込み（並列処理）・推論時は再帰（定常メモリ）という二面性を持ち、TransformerのKVキャッシュ問題を根本から回避する設計が巧妙
- 選択メカニズムによる入力依存パラメータ（B, C, Δ）の導入がSSMをLLMとして機能させる鍵であり、これがアテンションの「どのトークンに注目するか」という動的選択と機能的に対応する
- 状態hは「過去の圧縮」であるためSSMは本質的に有損失な記憶構造を持つ。Transformerはlosslessにすべてのトークンを保持するのと対照的で、何を圧縮・捨象するかをモデルが学習する点が興味深い

## 前提知識

- **Transformer・アテンション機構** (TODO: 読むべき)
- **RNN・再帰型ニューラルネット** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **制御理論・状態空間表現** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
