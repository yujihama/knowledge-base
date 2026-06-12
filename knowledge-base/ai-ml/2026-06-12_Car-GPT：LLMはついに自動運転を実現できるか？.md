---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-06-12
tags: [LLM, 自動運転, Vision Transformer, Perception, End-to-End学習, Diffusion Model, Planning, GPT-4 Vision, PromptTrack, DriveDreamer]
category: "ai-ml"
related: [3717, 3260, 3353, 3453, 3559]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-06-12T09:26:39.428555"
---

## 要約

本記事は、自動運転におけるLLM（大規模言語モデル）の応用可能性をThe Gradientが解説したサーベイ的論考（2024年3月）。従来の自動運転システムは、Perception・Localization・Planning・Controlの4モジュールに分割するモジュラー型アーキテクチャが主流であり、2010年代を通じてWebサーチや点群認識など各モジュールの精度向上が図られてきた。一方で2020年代に入り、単一ニューラルネットワークがステアリングと加速度を直接予測するEnd-to-End学習への関心が高まっているが、ブラックボックス問題が残課題となっている。

LLMの基礎として、本記事はTokenization（テキストを数値列に変換する工程）、Transformer（Encoder-Decoderアーキテクチャ、Multi-Head Attention、Next-Word Predictionを中核とする構造）、そして言語処理の仕組みを平易に解説している。GPTは純粋なDecoder型であり、BERTはEncoder型という区分も示している。

自動運転への適用では、入力をVision Transformer（ViT）でトークン化し、センサーデータ（LiDAR点群、RADARデータ）や画像をTransformerに通すことで、各自動運転タスクをLLMに解かせるアプローチが紹介されている。研究が活発な領域は4つに整理される。

① **Perception**：GPT-4 Visionが画像中の物体を列挙できることを示す事例のほか、HiLM-D・MTD-GPT・PromptTrack（DETR+LLMで物体にユニークIDを付与する4D的トラッキング）といったモデルが紹介される。

② **Planning**：DriveVLMやLMDrive、SurrealDriver、VisionLLMなど、鳥瞰図や自然言語インストラクションをもとに「車線変更すべきか」等の行動計画を出力するモデル群が紹介される。GPT-4に「交差点でどう進むか」を問いかける事例では、人間的な逐次推論が得られることが示されている。

③ **Generation（データ生成）**：拡散モデル（Diffusion Model）を用いたDriveDreamer・MagicDrive・DriveXなどが、Waymoの現実走行データを基にレアシナリオ（夜間・悪天候）を合成し、学習データを拡張する手法として紹介される。

④ **Q&A / Chat Interface**：DriveLikeAHuman・DiMA・LanguageMPCなどが対話型インターフェースを通じてシナリオ解釈や意思決定の説明を可能にすることが示される。

課題として、LLMはリアルタイム推論（数十ms以内）が困難であること、センサーモダリティのトークン化コストが高いこと、ハルシネーション（誤った知覚出力）が安全上の致命的リスクになり得ることが指摘される。記事全体として、LLMは自動運転の「銀の弾丸」ではなく、既存モジュールを補完・強化するコンポーネントとしての活用が現実的であるという立場で締めくくられている。

## アイデア

- LLMのTokenization概念をLiDAR点群・RADARデータにも拡張し、マルチモーダルトークンとしてTransformerに入力するアーキテクチャは、監査エージェントにおける構造化データ（財務数値・ログ）と非構造化データ（テキスト報告書）の統合処理に直接応用できる設計パターン
- DriveDreamerなどの拡散モデルによるレアシナリオ合成（夜間・悪天候）は、監査領域での不正シナリオ・例外ケース不足に対する合成訓練データ生成手法として転用可能
- PromptTrackがDETR＋LLMでオブジェクトに一意IDを付与してトラッキングするアプローチは、監査エージェントが取引エンティティや証跡をセッション横断で追跡する際のエンティティ解決（Entity Resolution）設計のヒントになる

## 前提知識

- **Vision Transformer (ViT)** (TODO: 読むべき)
- **Transformer Encoder-Decoder** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **Diffusion Model** → /deep_357 データ制約のある空間トランスクリプトミクスにおける遺伝子発現予測改善のためのCentral-to-Local適応型生成拡散フレームワーク
- **LiDAR点群処理** (TODO: 読むべき)

## 関連記事

- /deep_3717 今AIで重要な10のこと：LLMs+時代の到来
- /deep_3260 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3353 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3453 LLMs+：今AIで重要な10のこと（MIT Technology Review）
- /deep_3559 LLMs+：今AIで重要な10のこと（MIT Technology Review）

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
