---
title: "Mamba解説：TransformerのAttentionに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-15
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形計算量, 選択的SSM, 離散化, ZOH, Hardware-Aware, 長文脈]
category: "ai-ml"
related: [1837, 222, 833, 255, 410]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-15T12:38:13.953843"
---

## 要約

MambaはGu・Dao両氏が提案した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、Transformerが持つ二次計算量（O(n²)）のボトルネックを線形計算量（O(n)）で置き換える。Transformerでは全トークン間のAttentionを計算するため、シーケンス長nに対してトレーニングはO(n²)、自己回帰推論はO(n)の時間計算量とO(n)のメモリ（KVキャッシュ）が必要となり、超長文脈（例：100万トークン）での利用が現実的でない。Mambaはこの問題をControl Theory（制御理論）由来のSSMで解決する。基本方程式は h'(t) = Ah(t) + Bx(t)（状態遷移）と y(t) = Ch(t) + Dx(t)（出力）の連立微分方程式で、「隠れ状態h」が過去の文脈を圧縮して保持する。連続時間の微分方程式はZero-Order Hold（ZOH）離散化によって差分方程式へ変換され、離散パラメータ Ā・B̄ を用いた漸化式 h_t = Āh_{t-1} + B̄x_t として実装される。重要な革新点はS4からMambaへの進化にある「選択的状態空間（Selective SSM）」で、従来のSSMがA・B・Cを入力に依存しない時不変パラメータとしていたのに対し、MambaではB・C・∆（ステップサイズ）を入力x_tの関数として動的に変化させる。これにより無関係なトークンを「忘却」し、重要な情報を選択的に保持する能力を獲得する。例えば「Harry Potter」の後に「is」が来た場合、∆を大きくして「Harry Potter」を強く状態に書き込み、一方「the」などの無関係なトークンでは∆を小さくしてほぼスルーする振る舞いが可能になる。実装上の難点として、選択的SSMはB・Cが時変になるためFFT畳み込みによる並列化が不可能になる問題があり、これをHardware-Aware Parallel Scanningで解決している。具体的にはAHW（シーケンス長）のスキャン操作をGPUのSRAMで効率的に実行し、HBMへの読み書き回数を最小化するFlashAttentionに類似の手法を採用する。性能面では、Mamba-3BモデルがThe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を達成。推論速度はTransformerの最大5倍速い。ただし現状の限界として、In-Context Learning（ICL）やPrompt Engineeringとの相性がAttentionより劣る可能性、Multi-head Attentionのような豊富なヘッド構造を持たないことによる解釈可能性の低さが課題として残る。監査エージェント開発への示唆として、長大なログや監査証跡（数万行規模）を処理するシーケンスモデルとして、Mambaの線形スケーリング特性は実用的な優位性を持つ。また「重要情報を選択的に保持し無関係情報を圧縮する」選択的SSMの設計思想は、監査エージェントのメモリ管理・コンテキスト圧縮戦略に直接応用可能な概念である。

## アイデア

- 選択的SSMにおける∆（ステップサイズ）の動的制御は「情報の選択的記憶・忘却」を実現する機構であり、Transformerのsoftmax Attentionとは根本的に異なるアプローチで同等の情報選択を達成している点が興味深い
- 連続時間微分方程式→ZOH離散化→差分方程式という変換パイプラインにより、物理・制御理論の枠組みをシーケンスモデルに持ち込んでいる点は、今後の物理インフォームドAIとの融合可能性を示唆する
- Parallel Scanを使ってGPUのSRAMで計算を完結させるHardware-Aware設計は、アルゴリズムとハードウェア特性を共同最適化するFlashAttentionの思想を継承しており、モデル設計においてハードウェア意識が必須になりつつある潮流を示している

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **RNN/LSTM** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応

## 原文リンク

[Mamba解説：TransformerのAttentionに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
