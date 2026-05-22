---
title: "Nemotron 3 Nano Omni：効率的なオープンマルチモーダルLLM（NVIDIA）"
url: "https://zenn.dev/team_nishika/articles/fc597b5f983199"
date: 2026-05-22
tags: [Nemotron, multimodal, MoE, NVFP4, GSPO, Conv3D, EVS, vLLM, llama.cpp, NVIDIA]
category: "ai-ml"
related: [4060, 5157, 5969, 152, 650]
memo: "[Zenn LLM] 【Nishika 論文サク読み 第10回】Nemotron 3 Nano Omni"
processed_at: "2026-05-22T09:07:34.305257"
---

## 要約

NVIDIAが2026年4月27日に発表したNemotron 3 Nano Omniは、テキスト・画像・動画・音声の4モダリティをネイティブに処理するオムニモーダルモデル。バックボーンにMoE型のNemotron 3 Nano 30B-A3B（活性パラメータ3B）を採用し、前世代のDense型12Bから切り替えることで長いマルチモーダル系列の処理効率を向上させた。視覚エンコーダーにC-RADIOv4-H、音声エンコーダーにParakeet-TDT-0.6B-v2を組み合わせてマルチモーダル入力を実現している。コンテキスト長は128Kから256Kトークンに拡張。

学習は7ステージのSFTと5ステージのRLの2フェーズ構成。SFTではモダリティを段階的に追加しながらコンテキスト長を16K→48K→256Kと伸ばし、壊滅的忘却を防ぎつつ434.1Mサンプル・466.9Bトークンを学習。RLフェーズではGSPO（Group Sequence Policy Optimization）の改良版を使用し、MPO・Text RL（2回）・ImageRL・Omni RLの5ステージで推論能力・指示追従・安全性を強化した。Text RLを2回実施する構成が特徴的。

推論効率の主な技術として、Conv3D＋EVS（Early Video Sampling）による動画トークン削減がある。Conv3Dで時間方向を2倍圧縮し、EVSで空間トークンを枝刈りすることで、512フレーム動画の入力トークンを約141Kから約42Kへ70%削減。TTFTを7,969msから5,313msへ33%短縮し、平均精度低下は約0.5ポイントに抑えた。量子化はBF16（61.5GB）→FP8（32.8GB）→NVFP4（20.9GB）の3段階で、NVFP4はBF16比で最大7.5倍のスループットを実現しつつ精度低下は-0.40ポイント未満。

B200単一GPU上でシングルストリーム500トークン/s超（Qwen3-Omni比2.5倍）、高並行時は長時間動画タスクでQwen3-Omni比最大9倍のスループットを達成。精度面でも全モダリティで前世代V2 VLを上回り、特にGUI操作タスクで劇的な向上を示した。ローカル実行ではGGUFのQ4_K_XL量子化（unsloth経由）でGeneration 98.4 t/sを確認。

監査エージェント開発への示唆として、長時間文書・音声・動画を統合処理できるオムニモーダル能力は監査証跡の多様な入力形式に対応するうえで有用。256Kコンテキスト対応と段階的なモダリティ追加学習の設計は、複雑なRAGパイプラインの削減につながる可能性がある。

## アイデア

- SFTでモダリティとコンテキスト長を段階的に拡張する7ステージ設計により、壊滅的忘却を抑制しながら複数モダリティの精度を同時に向上させる学習パイプラインの有効性
- Conv3D（時間圧縮）＋EVS（空間枝刈り）の組み合わせで動画トークンを70%削減しながら精度低下を0.5ポイント以内に抑えたトークン効率化手法
- RLフェーズでText RLを2回（ステージ2と5）実施し、マルチモーダルRL後の最終仕上げとしてテキスト推論能力を再強化するという構成

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **SFT・RLHF** (TODO: 読むべき)
- **GRPO/GSPO** (TODO: 読むべき)
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク
- **量子化（FP8/NVFP4）** (TODO: 読むべき)

## 関連記事

- /deep_4060 NVIDIA Nemotron 3 Nano Omni：文書・音声・動画エージェント向け長コンテキストマルチモーダルモデル
- /deep_5157 GRPOが真のon-policyになれない理由 —— 訓練・推論の不一致の根底にあるロジック
- /deep_5969 初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する
- /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向

## 原文リンク

[Nemotron 3 Nano Omni：効率的なオープンマルチモーダルLLM（NVIDIA）](https://zenn.dev/team_nishika/articles/fc597b5f983199)
