---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-30
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, DriveGPT, Perception, Planning, 拡散モデル, マルチモーダル]
category: "ai-ml"
related: [3785, 4441, 3582, 4900, 1347]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-30T21:24:05.534107"
---

## 要約

本記事は、自動運転へのLLM適用可能性をPerception・Planning・Generation・Q&Aの4領域に分けて解説する入門的サーベイである。

自動運転の従来アーキテクチャは「モジュラー型」（Perception→Localization→Planning→Controlの独立モジュール）であり、2010年代を経てEnd-to-Endアプローチ（単一NNでステアリング・加速度を直接予測）へ移行しつつあるが、ブラックボックス問題が残る。LLMはこの課題に対する「第三の道」として注目されている。

**Perception領域**では、GPT-4 Visionが画像から物体を記述できることを皮切りに、HiLM-DやMTD-GPTがマルチビュー映像での検出・予測を実現。PromptTrackはDETRとLLMを組み合わせ、物体に一意IDを付与するトラッキングを実現している。

**Planning領域**では、DriveGPTやDriveVLMなどがBEV（Bird's Eye View）や複数カメラ入力から行動計画を生成。SurrealDriverはLLMをドライバー「ペルソナ」として機能させ、GPT-4がSimCity的シミュレーション環境での安全判断に高精度を示した実験も紹介される。

**Generation領域**では、DriveDreamer・WoVogenのような拡散モデル系手法が、テキスト条件付きで走行シナリオの合成データを生成し、エッジケースの学習データ不足問題への対処として機能する。

**Q&A領域**では、DriveLM・NuScenesQA・NuPlanQA等のデータセットが整備され、「なぜこの操作を選んだか」を自然言語で説明できる解釈性向上が実用上の強みとなる。

LLMの主要な利点として、①Few-shot/Zero-shot汎化（未見シナリオへの対応）、②自然言語による説明生成（規制対応・乗客への説明）、③マルチモーダル入力の統合処理が挙げられる。一方、リアルタイム推論の遅延、幻覚リスク、安全認証の困難さが実用化上の課題である。

監査エージェント開発への示唆：DriveGPTのように「行動とその根拠を自然言語で出力する」設計は、監査エージェントのReAct実装に直接応用可能。意思決定トレースの自然言語化は、LLM-as-judgeによる監査証跡の自動生成とも親和性が高い。

## アイデア

- DriveGPTのように行動根拠を自然言語で出力する設計は、監査エージェントのReActトレース記録と同一構造であり、説明可能なエージェント設計の参照アーキテクチャとなる
- Generation領域の拡散モデルによるシナリオ合成（DriveDreamer等）は、監査エージェントの訓練用エッジケースシナリオ生成にも転用できる可能性がある
- PromptTrackのように既存検出器（DETR）とLLMを組み合わせるハイブリッド構成は、既存ルールベース監査ロジックとLLMを段階的に統合する際の設計パターンとして参考になる

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **BEV（鳥瞰図表現）** (TODO: 読むべき)
- **拡散モデル** → /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成
- **Transformer Attention** (TODO: 読むべき)

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
