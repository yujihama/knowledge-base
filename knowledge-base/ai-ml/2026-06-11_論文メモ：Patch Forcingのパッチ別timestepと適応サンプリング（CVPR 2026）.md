---
title: "論文メモ：Patch Forcingのパッチ別timestepと適応サンプリング（CVPR 2026）"
url: "https://zenn.dev/kas_blog/articles/20260610-patch-forcing-adaptive-sampling"
date: 2026-06-11
tags: [Patch Forcing, Diffusion Transformer, Flow Matching, 適応サンプリング, LTG sampler, difficulty head, AdaLN, CVPR2026, 画像生成, SiT]
category: "ai-ml"
related: [6324, 6771, 2147, 5771, 492]
memo: "[Zenn 機械学習] 論文メモ：Patch Forcingのパッチ別timestepと適応サンプリング"
processed_at: "2026-06-11T12:18:06.770009"
---

## 要約

Patch Forcing（PFT）は、Diffusion TransformerおよびFlow Matchingモデルにおける画像生成フレームワークで、CVPR 2026採択論文「Denoising, Fast and Slow」で提案された。従来の拡散モデルは画像内の全パッチに同一のtimestep（ノイズレベル）を適用するが、空・壁などの低周波領域と文字・細線・遮蔽境界などの高周波領域では生成難易度が大きく異なる。PFTはこの前提を覆し、パッチごとに異なるtimestep t_i ∈ ℝ^{(H/p)×(W/p)} を与えることで、簡単なパッチを先に低ノイズ状態へ進め、その完成済み表現を難しいパッチの文脈として活用する設計を採る。

アーキテクチャ面では、DiT系モデルのAdaLN機構にスカラーtimestep埋め込みをtoken単位へ拡張することで対応し、追加パラメータはdifficulty headを含めても0.01%未満に抑えている。

学習時の課題として、各パッチを独立にU(0,1)からtimestepを抽出すると、パッチ数が多い画像では常にt_i≈1のほぼ完成した領域が学習文脈として存在するtrain-test mismatch（推論はすべてノイズ状態から開始するため）が生じる。これを解決するLTG（Logit-Normal Truncated Gaussian）samplerは、最大timestep t_maxをLogit-Normal分布から生成し、各パッチのt_iをt_max以下に制限するlower-half Gaussianで従属サンプリングすることで、学習時の文脈クオリティを制御する。

推論時には、モデルがvelocityに加えてパッチごとの標準偏差σ_θを予測するdifficulty headを使い、相対的な生成難易度を推定する。t=0.6時点での検証誤差との相関はR=0.52と実用的な精度を持ち、生成が進むほど難易度判定が安定する。この予測を用いた適応サンプリング戦略として、(1) dual-loop（低難易度パッチを大ステップで先進め、高難易度パッチを小ステップで複数回更新）と(2) look-ahead（低難易度パッチを一時的に未来の低ノイズ状態へ投影し、その表現を高難易度パッチの文脈として注入）の2手法を提案する。

ImageNet 256×256のFIDでの実験結果：SiT-B/2（130M）がFID 33.0のところ、PFT-B/2がFID 27.9、+dual-loopで26.0、+look-aheadで24.2を達成。PFT-XL/2+look-ahead（675M）ではFID 9.8を記録し、SiT-XL/2の17.2から大幅に改善。REPA併用では2.00も報告されており、既存のguidance手法とも組み合わせ可能。なお著者らはPFTを高速化手法ではなく、固定NFE（Number of Function Evaluations）・固定計算予算での品質向上フレームワークとして位置づけており、wall-clock latencyはNFEと一致しない点に注意が必要。

## アイデア

- 外部アノテーションや深度マップを使わず、モデル自身が先に生成した低難易度パッチの表現を文脈として再利用するself-contextual設計は、追加モダリティ不要でパッチ間の依存関係を活用できる点が興味深い
- LTG samplerによる最大timestep t_maxの制御でtrain-test mismatchを緩和するアプローチは、マルチエージェント系での「学習環境と推論環境の分布ずれ」問題と構造的に類似しており、ReAct/LangGraphエージェントの学習設計にも示唆がある
- difficulty headで予測した生成難易度（標準偏差σ_θ）を不確実性指標として使いながら、t=0.6でR=0.52・t=0.2でR=0.11と生成後期に精度が安定する知見は、動的な計算リソース配分のタイミング設計に応用できる

## 前提知識

- **Flow Matching** → /deep_204 テキストから画像への生成モデルのトレーニング設計：アブレーション実験から得られた知見
- **Diffusion Transformer (DiT)** (TODO: 読むべき)
- **AdaLN** (TODO: 読むべき)
- **timestep embedding** (TODO: 読むべき)
- **FID** → /deep_204 テキストから画像への生成モデルのトレーニング設計：アブレーション実験から得られた知見

## 関連記事

- /deep_6324 Diffusion Transformerにおけるクロスレイヤー情報ルーティングの再考
- /deep_6771 SoftCap: Diffusion Transformerの推論高速化のためのソフト予算制御
- /deep_2147 長期モーション埋め込み学習による効率的な運動生成
- /deep_5771 言語生成を最適制御として再定式化：潜在制御空間における閉ループ拡散
- /deep_492 視覚的インコンテキスト学習におけるデモンストレーション選択の学習

## 原文リンク

[論文メモ：Patch Forcingのパッチ別timestepと適応サンプリング（CVPR 2026）](https://zenn.dev/kas_blog/articles/20260610-patch-forcing-adaptive-sampling)
