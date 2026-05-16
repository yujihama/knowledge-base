---
title: "Mamba解説：State Space ModelがTransformerに挑む"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-10
tags: [Mamba, SSM, State Space Model, Transformer, 長文コンテキスト, 選択的状態空間, ZOH離散化, S4, 線形計算量, Mechanistic Interpretability]
category: "ai-ml"
related: [3105, 2480, 2510, 2577, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-10T21:44:52.604877"
---

## 要約

MambaはAlbert GuとTri Daoが2023年に発表したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量の問題を解決することを目指している。Transformerはトークン間通信にAttentionを使うため、訓練時にO(n²)の時間複雑度、推論時のKVキャッシュにO(n)の空間複雑度が必要になる。これにより長文コンテキスト（100万トークン規模）での処理が現実的でなくなる。

Mambaの核心はSSMにある。状態空間モデルは制御理論由来の数式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、隠れ状態hが過去情報の圧縮として機能する。連続時間の微分方程式を離散時間の差分方程式に変換（離散化）するためにZero-Order Hold（ZOH）手法を使用。これによりA・Bは時間ステップΔに依存したĀ・B̄に変換される。

S4と呼ばれる先行SSMとMambaの最大の違いは「選択的状態空間」の導入にある。S4のA・B・Cは入力に依存しない定数だったが、Mambaではこれらを入力xに依存させることで、どの情報を記憶・忘却するかを動的に制御できる。これによりコンテキストに応じた情報フィルタリングが可能になり、Induction HeadパターンやSentiment課題など、選択的記憶を要するタスクでのパフォーマンスが大幅に向上した。

ハードウェア最適化として、GPUのHBM（高帯域幅メモリ）とSRAMの帯域差を活用したKernel Fusionを適用。A・B・C・Δの計算とScan演算を単一カーネルで実行し、中間状態をSRAMに保持することでメモリ転送コストを削減。これによりTransformerより最大5倍の推論高速化を実現している。

実験結果として、Mamba-3BモデルはThe PileベンチマークでTransformer 3Bを上回り、6Bモデルと同等のperplexityを達成。選択的コピーやInduction Headなどの合成タスクでもSSMの中でダントツの性能を示した。ゲノム（DNA配列）・音声・言語の複数モダリティで最先端性能を達成している。

解釈可能性の観点では、MambaにはTransformerのAttention行列のような「どのトークンを見ているか」を可視化する手段が存在しない。隠れ状態による情報圧縮はブラックボックス的であり、Mechanistic Interpretabilityの適用が困難。安全性の面では、隠れ状態が将来のトークン生成に使用される情報を明示的に示さないため、透明性に課題がある。監査エージェント開発への示唆として、Mambaの選択的情報フィルタリング機構は長期監査ログの処理やコンテキスト管理に応用可能な概念であり、「何を記憶し何を忘却するか」を学習で最適化する設計は監査エージェントのメモリ管理設計に参考になる。

## アイデア

- 選択的SSM：入力xに応じてA・B・CとΔを動的に変化させることで「何を記憶し何を忘却するか」をモデル自身が学習するアーキテクチャは、監査エージェントの証跡フィルタリングや長期コンテキスト管理に応用可能な設計原則を提供する
- 状態は過去の圧縮：Mambaの隠れ状態hは過去全トークンの情報を固定サイズのベクトルに圧縮する。Transformerが全KVキャッシュを保持するのと対照的に、このMarkov的な状態表現は推論時の定数空間複雑度を実現しており、リソース制約環境でのLLMデプロイに重要な設計思想
- 解釈可能性のトレードオフ：Attention行列という可視化可能な情報経路を持つTransformerと異なり、Mambaはどのトークンがどのトークンに影響しているかを直接読み取る手段がなく、Mechanistic Interpretabilityの観点では後退しており、安全性重視の応用では課題となる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **State Space Model (SSM)** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2577 因果的跳ね橋：TransformerLMにおける統語的アイランドの勾配ブロッキングの特性化
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：State Space ModelがTransformerに挑む](https://thegradient.pub/mamba-explained/)
