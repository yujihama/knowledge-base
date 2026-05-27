---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-27
tags: [自動運転, LLM, Vision Transformer, Perception, Planning, エンドツーエンド学習, GPT-4V, DriveVLM, PromptTrack]
category: "ai-ml"
related: [716, 5220, 1266, 1760, 1449]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-27T09:24:38.919667"
---

## 要約

本記事は、LLM（大規模言語モデル）が自動運転の課題をどのように解決しうるかを解説した入門的な技術解説記事である。自動運転の従来アーキテクチャは「モジュール型」と「エンドツーエンド学習」の2種類に分類される。モジュール型はPerception・Localization・Planning・Controlという4つのモジュールを独立して設計するアプローチで、解釈性は高いが複雑性が増すという課題がある。一方、エンドツーエンド学習は単一ニューラルネットワークでステアリングと加速を直接予測するが、ブラックボックス問題を抱える。LLMの基礎としてTokenization（テキストを数値トークンに変換する処理）とTransformerアーキテクチャ（Encoder-Decoderまたはデコーダー専用のGPT型）を説明したうえで、自動運転への応用可能性を4つの領域に整理している。①Perception：GPT-4 VisionやHiLM-D、MTD-GPT等が画像から物体・レーン検出を行い、PromptTrackはDETRオブジェクト検出器とLLMを組み合わせて追跡IDを付与する。②Planning：DriveVLMやDriveWithLLaMA等がBEV（鳥瞰図）入力から車線変更・停車等の行動決定を自然言語で推論する。③Generation：拡散モデルを用いたトレーニングデータの合成生成やエッジケースシナリオの自動生成。④Q&A：シナリオに対して自然言語で問い合わせ可能なチャットインターフェース。記事後半では、自動運転にLLMを適用する際の技術的課題として推論レイテンシ（リアルタイム要件との不整合）、センサーデータのトークン化コスト、ハルシネーションによる安全リスクが挙げられている。監査エージェント開発への示唆として、LLMを既存の判断モジュールに「アドオン」する形（知覚結果を自然言語に変換してLLMへ渡す設計）は、監査証跡の生成や異常説明の自動化に直接応用可能なパターンである。また、モジュール型とエンドツーエンドのトレードオフは、監査エージェントにおけるLangGraph的なルール明示フローとLLMによる暗黙推論の統合設計と本質的に同じ問題構造を持つ。

## アイデア

- センサーデータ（LiDAR点群・カメラ画像）をトークン化してTransformerに入力する設計は、監査データ（仕訳・契約書・ログ）をLLMに渡す前処理パイプラインと同一の抽象構造を持つ
- PromptTrackのようにDETR等の専門モデルとLLMを組み合わせるハイブリッドアーキテクチャは、監査エージェントにおけるルールベース検出器＋LLM説明生成の設計パターンに直接対応する
- ハルシネーションが安全クリティカルな判断（ステアリング指示）を誤る可能性は、監査判断の誤りが法的リスクに直結する文脈と同様であり、LLM-as-judgeやReActによる自己検証ループの必要性を示唆する

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **Tokenization** → /deep_39 エージェンティックコマースは「真実」と「コンテキスト」によって動く
- **BEV (Bird's Eye View)** (TODO: 読むべき)

## 関連記事

- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_5220 AIエージェントの用語まとめ：基礎から計画・メモリ・ツール使用まで
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
