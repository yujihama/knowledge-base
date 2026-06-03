---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-03
tags: [LLM, 自動運転, Vision Transformer, エンドツーエンド学習, Perception, Planning, マルチモーダル, PromptTrack, DriveVLM]
category: "ai-ml"
related: [4441, 3582, 4900, 716, 1527]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-03T09:24:51.900691"
---

## 要約

本記事はThe Gradientに掲載された解説記事で、LLM（大規模言語モデル）を自動運転に応用する研究動向を体系的に整理している。

自動運転の開発史として、2010年代の「モジュラーアプローチ」（Perception・Localization・Planning・Controlの4モジュール）から、単一ニューラルネットワークで操舵・加速を予測するエンドツーエンド学習への移行を概説。そこにLLMという第三の潮流が合流しつつある。

LLMの基礎として、テキストを数値トークンに変換するTokenization、Encoder-Decoder構造のTransformer、次単語予測（Next-Word Prediction）の3要素を説明。自動運転への適用では、入力をカメラ画像・LiDARポイントクラウド・RADARデータ・アルゴリズム出力に置き換え、Vision Transformer（ViT）でトークン化することで既存のTransformerアーキテクチャをほぼそのまま流用できる。

2023年時点の主要研究領域は4つ。(1) Perception：GPT-4 Visionによる物体記述、HiLM-D・MTD-GPTによるマルチビュー物体検出、PromptTrackによるDETR+LLMの物体追跡とID付与。(2) Planning：DriveVLMやDriveWithLLMなどが鳥瞰図や認識結果を入力として「車線変更すべき」等の行動決定を出力。(3) データ生成：Diffusionモデルとの組み合わせによる訓練データや代替シナリオの自動生成。(4) Q&A：シナリオをLLMに問い合わせるチャットインターフェース。

課題として、(1) ハルシネーション（LLMが誤った情報を自信を持って出力する問題）、(2) リアルタイム処理のレイテンシ（GPT-4のような大型モデルは推論遅延が大きい）、(3) エッジケース対応（訓練データに存在しない稀な状況への汎化）、(4) 説明可能性の担保が挙げられている。

記事の結論は、LLMは自動運転の「銀の弾丸」ではなく、既存のモジュラー・エンドツーエンド手法を補完する有力な要素技術として位置づけられるという点。特にPlanningとQ&Aにおけるコモンセンス推論能力は従来手法では実現が難しく、LLMの強みが活きやすい。監査エージェント開発への示唆としては、複数センサ・複数モダリティの入力をトークン化して統一Transformerに投入するアーキテクチャは、監査における多種類ドキュメント（財務データ・契約書・ログ）の統合処理にも転用可能な設計思想である。

## アイデア

- テキスト・画像・LiDARポイントクラウドをすべてトークン列に変換することで、モダリティを問わず同一のTransformerアーキテクチャを適用できるという設計の汎用性
- LLMのコモンセンス推論能力をPlanningモジュールに組み込むことで、ルールベースでは定義困難なエッジケース（歩行者の意図推定等）に対処する方向性
- Diffusionモデルと組み合わせたデータ拡張（実世界で発生頻度の低い危険シナリオを合成生成して訓練データを補完する手法）は、監査異常検知の少数事例問題にも応用できる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **トークン化** → /deep_1002 エージェンティックコマースは真実性とコンテキストで動く
- **エンドツーエンド学習** → /deep_354 ガイダンス付き予測：時系列予測のための表現レベル監督（ReGuider）
- **マルチモーダルLLM** → /deep_6132 SVFSearch: ゲーム縦型ドメインにおける短尺動画フレーム検索のマルチモーダル知識集約型ベンチマーク

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_716 LeRobotが自動車教習所へ：世界最大のオープンソース自動運転データセット「L2D」
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
