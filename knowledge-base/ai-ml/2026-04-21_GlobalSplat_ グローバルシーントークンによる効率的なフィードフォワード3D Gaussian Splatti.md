---
title: "GlobalSplat: グローバルシーントークンによる効率的なフィードフォワード3D Gaussian Splatting"
url: "https://tldr.takara.ai/p/2604.15284"
date: 2026-04-21
tags: [3D Gaussian Splatting, novel-view synthesis, feed-forward inference, coarse-to-fine curriculum, scene representation, RealEstate10K, ACID]
category: "ai-ml"
related: [1053, 2076, 2005, 130, 353]
memo: "[HF Daily Papers] GlobalSplat: Efficient Feed-Forward 3D Gaussian Splatting via Global Scene Tokens"
processed_at: "2026-04-21T12:18:25.879296"
---

## 要約

GlobalSplatは、3D Gaussian Splatting（3DGS）における「プリミティブの空間割り当て」問題を根本から解決するフィードフォワード推論フレームワーク。従来手法（反復最適化型・フィードフォワード型）は、ピクセルアライン型またはボクセルアライン型のローカルなヒューリスティック割り当て戦略に依存しており、入力視点数が増えるにつれ表現サイズが膨張し（representation bloat）、グローバル一貫性が崩れる問題があった。GlobalSplatは「align first, decode later」の原則に基づき設計されている。複数視点の入力をコンパクトなグローバル潜在シーン表現にエンコードし、クロスビュー対応関係（cross-view correspondences）を解決してから明示的な3D幾何学をデコードする。これにより、事前学習済みのピクセル予測バックボーンや密なベースラインの潜在特徴の再利用なしに、コンパクトかつグローバルに一貫した再構成を実現する。学習戦略として「coarse-to-fine training curriculum（粗から細へのカリキュラム学習）」を採用し、デコードキャパシティを段階的に増加させることで表現の膨張をネイティブに防止する。性能面では、RealEstate10KおよびACIDデータセットにおいて競争力のある新規視点合成（novel-view synthesis）性能を達成しつつ、使用するGaussian数はわずか16K個（密なパイプラインと比較して大幅に少ない）、モデルフットプリントは4MBと軽量。推論速度は単一フォワードパスで78ミリ秒未満と、ベースライン手法より大幅に高速。監査AIや内部統制への直接的な関連は薄いが、コンパクトなシーン表現の学習戦略（グローバル文脈を先に解決してからデコード）は、エージェントが環境状態を効率的に表現・推論する設計思想と共通点がある。

## アイデア

- 「align first, decode later」の原則：クロスビュー対応をデコード前に解決するアーキテクチャ設計は、マルチモーダル入力を統合してから推論するLLMエージェントの設計思想と類似しており、状態表現の圧縮戦略として参考になる
- coarse-to-fineカリキュラム学習でrepresentation bloatをネイティブに防止する手法：段階的なキャパシティ増加は、過学習・過複雑化を防ぐ正則化として機能しており、エージェントのツール数・コンテキスト量の段階的拡張戦略にも応用可能
- 16K Gaussiansと4MBという極めてコンパクトな表現で競争力を維持：密な表現から疎なグローバルトークンへの圧縮率の高さは、RAGや長期記憶設計における情報圧縮・要約の品質評価指標として示唆を与える

## 前提知識

- **3D Gaussian Splatting** → /deep_130 ガウシアンを減らし、テクスチャを増やす：4Kフィードフォワードテクスチャードスプラッティング
- **novel-view synthesis** (TODO: 読むべき)
- **feed-forward inference** (TODO: 読むべき)
- **NeRF** → /deep_189 EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？

## 関連記事

- /deep_1053 高品質なプリミティブベース神経再構成のためのNeural Harmonic Textures
- /deep_2076 反復的ガウシアン概要によるIterative Gaussian Synopsisを用いた3D Gaussian Splattingの段階的展開
- /deep_2005 パーツレベル3Dガウシアン車両生成：関節・ヒンジ軸推定による可動モデル合成
- /deep_130 ガウシアンを減らし、テクスチャを増やす：4Kフィードフォワードテクスチャードスプラッティング
- /deep_353 カテゴリレベル3DGSアライメント：幾何学的特徴誘導による異インスタンスGaussian Splattingの位置合わせ

## 原文リンク

[GlobalSplat: グローバルシーントークンによる効率的なフィードフォワード3D Gaussian Splatting](https://tldr.takara.ai/p/2604.15284)
