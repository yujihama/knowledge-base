---
title: "Dehaze-then-Splat: 物理インフォームド3D Gaussian Splattingによるスモーク除去と新規視点合成"
url: "https://tldr.takara.ai/p/2604.13589"
date: 2026-04-21
tags: [3D Gaussian Splatting, Novel View Synthesis, Dehazing, Dark Channel Prior, NTIRE 2026, Nano Banana Pro, PSNR, 深度監視, 生成的画像修復]
category: "ai-ml"
related: [2076, 130, 1053, 2005, 353]
memo: "[HF Daily Papers] Dehaze-then-Splat: Generative Dehazing with Physics-Informed 3D Gaussian Splatting for Smoke-Free Novel View Synthesis"
processed_at: "2026-04-21T12:01:50.826298"
---

## 要約

NTIRE 2026 3D Restoration and Reconstruction ChallengeのTrack 2向けに開発された、マルチビュー煙除去と新規視点合成（Novel View Synthesis）のための2段階パイプライン。

【第1段階：生成的デヘイジング】
Nano Banana Proを使用したフレーム単位の生成的デヘイジングにより、擬似クリーン画像（pseudo-clean images）を生成する。その後、輝度正規化を適用することで画像品質を均一化する。生成モデルによるフレームごとの処理は高品質な単一フレームの修復を実現する一方、視点間の一貫性（cross-view consistency）を保証しない点が根本的な課題となる。

【第2段階：物理インフォームド3DGS学習】
擬似クリーン画像を用いて3D Gaussian Splatting（3DGS）を学習する際、以下の3つの補助損失を導入してビュー間不整合を補償する：
1. **深度監視（Depth Supervision）**：擬似深度とのPearson相関を用いた深度整合性の強制
2. **ダークチャネル事前正則化（Dark Channel Prior Regularization）**：霧・煙の物理モデルに基づくヘイズ抑制
3. **デュアルソース勾配マッチング（Dual-Source Gradient Matching）**：複数ソースからの勾配を整合させ構造安定性を向上

【主要な知見】
MCMCベースの密度化（densification）とアーリーストッピングを組み合わせることで、フレーム単位処理に起因するブラーやStructural Instabilityを効果的に軽減できることを示した。Dehaze-then-Reconstruct型パイプラインの本質的なジレンマとして「単一フレームの修復品質の高さがマルチビュー一貫性を保証しない」という問題を明確に定式化している点が新規性の一つ。

【定量評価】
Akakazeバリデーションシーンにて、PSNR 20.98 dB・SSIM 0.683を達成。正則化なしのベースラインに対して+1.50 dBのPSNR改善を確認。

監査AIへの直接的示唆は限定的だが、「生成モデルによる前処理＋物理制約を持つ後段モデル」という2段階パイプライン設計は、不完全・ノイジーなデータを扱うエージェントシステムの品質保証アーキテクチャに参考となる。

## アイデア

- フレーム単位の生成修復とマルチビュー3D再構成の間に本質的なトレードオフ（品質 vs 一貫性）が存在し、これを物理ベースの補助損失で橋渡しするアプローチは、他の「生成前処理→3D/4D再構成」パイプライン全般に応用可能な設計原則
- Dark Channel Priorという古典的な物理モデルをディープラーニングの正則化項として再利用することで、ドメイン知識をデータ効率よく組み込む手法——ニューラルネットワークと物理モデルのハイブリッド正則化の好例
- MCMCベースの密度化＋アーリーストッピングという学習戦略が、ビュー不整合ノイズに対してロバストな3DGS構築に寄与する点は、ノイジーな監督信号下でのNeRF/3DGS学習全般への示唆となる

## 前提知識

- **3D Gaussian Splatting (3DGS)** (TODO: 読むべき)
- **Novel View Synthesis** → /deep_130 ガウシアンを減らし、テクスチャを増やす：4Kフィードフォワードテクスチャードスプラッティング
- **Dark Channel Prior** (TODO: 読むべき)
- **Generative Dehazing** (TODO: 読むべき)
- **PSNR / SSIM** (TODO: 読むべき)

## 関連記事

- /deep_2076 反復的ガウシアン概要によるIterative Gaussian Synopsisを用いた3D Gaussian Splattingの段階的展開
- /deep_130 ガウシアンを減らし、テクスチャを増やす：4Kフィードフォワードテクスチャードスプラッティング
- /deep_1053 高品質なプリミティブベース神経再構成のためのNeural Harmonic Textures
- /deep_2005 パーツレベル3Dガウシアン車両生成：関節・ヒンジ軸推定による可動モデル合成
- /deep_353 カテゴリレベル3DGSアライメント：幾何学的特徴誘導による異インスタンスGaussian Splattingの位置合わせ

## 原文リンク

[Dehaze-then-Splat: 物理インフォームド3D Gaussian Splattingによるスモーク除去と新規視点合成](https://tldr.takara.ai/p/2604.13589)
