---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-25
tags: [自動運転, LLM, Vision Transformer, Perception, Planning, エンドツーエンド学習, マルチモーダル, 拡散モデル, PromptTrack, DriveVLM]
category: "ai-ml"
related: [3785, 4441, 3582, 4900, 1347]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-25T21:13:42.720060"
---

## 要約

本記事は、自動運転へのLLM（大規模言語モデル）応用を解説した入門的技術解説記事である。自動運転の従来アプローチとして、Perception・Localization・Planning・Controlの4モジュールに分割する「モジュラー方式」と、単一ニューラルネットワークで操舵・加速を直接予測する「エンドツーエンド学習」が紹介されている。LLMの基礎として、テキストを数値トークンに変換するTokenization、EncoderとDecoderからなるTransformerアーキテクチャ、そして次単語予測（Next-Word Prediction）の仕組みが説明される。

自動運転へのLLM適用においては、入力を画像・LiDARポイントクラウド・RADARデータなどに拡張し、Vision Transformer（ViT）経由でトークン化することで、既存Transformerモデルを再利用できる点が強調されている。主要な研究領域は4つ：①Perception（環境認識）、②Planning（行動計画）、③生成（学習データ・シナリオ生成）、④Q&A（対話インターフェース）。

Perceptionでは、GPT-4 Visionによる物体検出、HiLM-D・MTD-GPTによるマルチモーダル検出、PromptTrack（DETRとLLMを組み合わせた物体追跡・ID付与）が具体例として挙げられている。Planningでは、SurrealDriver・DriveVLMなどのモデルが鳥瞰図や画像入力から「車線変更」「徐行」などの行動を自然言語で推論する。生成タスクでは、WoVogenやMagicDriveが拡散モデルを利用して自動運転用の合成トレーニングデータを生成し、データ不足問題への対処が図られている。Q&Aアプローチとして、NuScenesデータセットを用いたSurroundQAが示されている。

LLMの自動運転への適用は研究段階にあり、実用化には推論速度・センサーフュージョン精度・安全保証などの課題が残る。監査AI観点では、LLMが複数モジュールの意思決定を統合して自然言語で説明可能な推論を行う点は、判断根拠のトレーサビリティ確保という監査要件と親和性が高く、エージェントシステムにおける説明可能性設計への示唆がある。

## アイデア

- LLMの自然言語推論能力をPlanningモジュールに適用することで、ルールベースでは記述困難なエッジケース（歩行者の曖昧な行動、複雑な交差点）への対応が期待できる
- WoVogenやMagicDriveのような生成モデルによる合成シナリオ生成は、希少・危険シナリオのデータ収集コスト問題を根本から回避する手法であり、監査エージェントの異常シナリオ学習にも転用可能
- PromptTrackのようにDETR等の特化モデルとLLMをハイブリッド接続する設計は、既存モジュールの精度を活かしつつLLMの文脈理解を付加するアーキテクチャパターンとして汎用性が高い

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **拡散モデル (Diffusion Model)** (TODO: 読むべき)
- **DETR** → /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1347 SEM-ROVER: セマンティックボクセル誘導拡散による大規模走行シーン生成

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
