---
title: "EgoCoT-Bench：マルチモーダル大規模言語モデルのための一人称視点・操作中心Chain-of-Thoughtベンチマーク"
url: "https://tldr.takara.ai/p/2605.19559"
date: 2026-05-25
tags: [EgoCoT-Bench, MLLM, egocentric video, Chain-of-Thought, spatio-temporal scene graph, benchmark, grounded reasoning, 手物体インタラクション]
category: "ai-ml"
related: [6130, 2789, 3381, 3921, 6294]
memo: "[HF Daily Papers] EgoCoT-Bench: Benchmarking Grounded and Verifiable Operation-Centric Chain of Thought Reasoning for MLLMs"
processed_at: "2026-05-25T09:11:37.671919"
---

## 要約

EgoCoT-Benchは、マルチモーダル大規模言語モデル（MLLM）を対象とした、一人称視点（egocentric）動画における操作中心の推論能力を評価するベンチマークである。既存の一人称視点動画ベンチマークは「根拠付きの推論評価（grounded rationale evaluation）」が不十分で、モデルが正解を出しても、その根拠が時空間的証拠と整合しているかを検証する仕組みに乏しかった。本ベンチマークはこの課題に対応するため、351本の一人称視点動画上に3,172件の検証可能なQAペアを構築し、4タスクグループ・12サブタスクグループに分類している。タスクは「知覚・回顧（perception and retrospection）」「予測（anticipation）」「高次推論（high-level reasoning）」を網羅する。構築手法として、時空間シーングラフ（Spatio-Temporal Scene Graph: STSG）によるQA生成フレームワークを採用し、自動生成後に人手アノテーターによる品質精製を経て、一人称視点への関連性と細粒度の品質を担保している。特筆すべき実験知見として、多くのMLLMが「答えは正しいが、推論根拠が答えと不整合」という現象を示すことが確認された。これはモデルが正答を偶然または近似的に導いており、時空間的な操作過程を真に理解した上での推論ではないことを示す。手と物体の相互作用の細粒度認識、物体の状態変化の時系列追跡、動的環境での操作プロセス推論といった能力を評価軸として設定しており、Chain-of-Thought（CoT）の各ステップに明示的な根拠アノテーションを付与している点が従来手法との差別化要素となっている。監査AIへの示唆としては、証拠と結論の整合性検証という問題意識が、監査エージェントにおける「証拠に基づく推論検証モジュール」の設計に直結する。監査エージェントが文書・映像・ログから推論を行う際、正答率だけでなく「根拠と結論の整合性」を評価する仕組みの重要性を示しており、LLM-as-judgeによる推論根拠の自動検証パイプライン設計の参考になる。

## アイデア

- 「正答だが根拠が不整合」という現象の定量的検出手法：MLLMが正解を出しつつ推論根拠が時空間証拠と矛盾するケースを3,172件のQAで体系的に測定しており、推論の信頼性評価の新たな軸を提示している
- 時空間シーングラフ（STSG）によるQA自動生成フレームワーク：動画内の操作イベントをグラフ構造で表現し、そこからverifiableな問題を生成するアプローチは、他の動画理解タスクや監査証拠からの自動問題生成への応用可能性がある
- 操作中心CoTの段階的根拠アノテーション：各推論ステップに明示的な時空間根拠を紐付ける設計は、監査エージェントにおける証拠追跡可能性（audit trail）の実装設計に直接応用できる概念

## 前提知識

- **MLLM（Multimodal LLM）** (TODO: 読むべき)
- **Chain-of-Thought推論** (TODO: 読むべき)
- **Scene Graph** → /deep_4591 グラフ世界モデル（GWM）：概念・分類・将来展望
- **egocentric video understanding** (TODO: 読むべき)
- **grounded reasoning** (TODO: 読むべき)

## 関連記事

- /deep_6130 EgoExoMem: 自己視点と外部視点の同期動画を横断するクロスビュー記憶推論ベンチマーク
- /deep_2789 VRAG-DFD: MLLMベースのディープフェイク検出のための検証可能な検索拡張
- /deep_3381 SurgCoT: Chain-of-Thoughtベンチマークによる外科手術動画の時空間推論の進化
- /deep_3921 SAKE: 根拠付きマルチモーダル固有表現認識のための自己認識型知識活用・探索フレームワーク
- /deep_6294 FruitEnsemble: 細粒度果物認識のためのMLLM誘導アービトレーションによる異種アンサンブル

## 原文リンク

[EgoCoT-Bench：マルチモーダル大規模言語モデルのための一人称視点・操作中心Chain-of-Thoughtベンチマーク](https://tldr.takara.ai/p/2605.19559)
