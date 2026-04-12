---
title: "EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合"
url: "https://tldr.takara.ai/p/2603.21332"
date: 2026-04-02
tags: [3D Gaussian Splatting, NeRF, FLAME, talking head synthesis, few-shot learning, emotion recognition, audio-driven, facial animation]
category: "ai-ml"
memo: "[HF Daily Papers] EmoTaG: Emotion-Aware Talking Head Synthesis on Gaussian Splatting with Few-Shot Personalization"
processed_at: "2026-04-02T09:05:12.968756"
---

## 要約

EmoTaGは、音声駆動の3Dトーキングヘッド合成において、感情表現の正確さと幾何学的安定性を両立させるフレームワーク。従来のNeRF（Neural Radiance Fields）や3DGS（3D Gaussian Splatting）ベースの手法では、豊かな表情動作時に幾何学的不安定性（Gaussian の直接変形による崩れ）と音声・感情のミスマッチが発生する問題があった。

EmoTaGの核心的なアプローチは「Pretrain-and-Adapt」パラダイムで、事前学習済みの豊富なプライアを活用し、数秒程度の短い動画から即座に個人化（フューショット）できる点にある。最大の技術的革新は、3D Gaussianを直接変形させる代わりに、FLAME（顔の3Dパラメトリックモデル）パラメータ空間でモーション予測を再定式化したこと。FLAMEは頭部形状・表情・姿勢を分離したパラメータで記述する標準モデルであり、これを介することで明示的な幾何学的プライアが導入され、モーションの安定性が向上する。

主要コンポーネントとして「Gated Residual Motion Network（GRMN）」を提案。GRMNは音声から感情プロソディ（抑揚・リズムに基づく感情情報）を抽出しながら、音声だけでは捉えられない頭部姿勢や上顔面（眉・目など）の動きを補完する設計になっている。ゲート機構により、音声由来の信号と補完信号の統合バランスを動的に調整し、表情豊かで一貫したモーション生成を実現する。

実験評価では、感情表現力・口形同期精度・視覚的リアリズム・モーション安定性の4軸でState-of-the-Artを達成したと報告されている。フューショット設定（数秒の動画）での即時個人化能力により、大規模な個人専用学習データなしに特定人物のトーキングヘッドを生成できる実用性を持つ。

## アイデア

- FLAME パラメータ空間でモーション予測を行うことで、Gaussian 直接変形より幾何的に安定した表現が得られるという設計思想は、他の3D生成タスクにも転用可能な汎用的知見
- Gated Residual Motion Network が「音声にない情報（頭部姿勢・上顔面）」を補完するアーキテクチャは、モダリティ欠損を明示的に扱うマルチモーダル設計の好例
- フューショット個人化と事前学習プライアの組み合わせ（Pretrain-and-Adapt）は、少データ環境での高品質生成という現実的制約への解答として、エージェント系のパーソナライズ機能設計にも示唆を持つ

## 原文リンク

[EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合](https://tldr.takara.ai/p/2603.21332)
