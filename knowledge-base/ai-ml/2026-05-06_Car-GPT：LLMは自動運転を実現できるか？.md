---
title: "Car-GPT：LLMは自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-06
tags: [LLM, 自動運転, Vision Transformer, End-to-End学習, マルチモーダル, Perception, Planning, GPT-4V, 拡散モデル, Hallucination]
category: "ai-ml"
related: [3785, 111, 3582, 1912, 1835]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-06T12:16:54.974869"
---

## 要約

本記事は、大規模言語モデル（LLM）を自動運転システムへ応用する可能性をサーベイ形式で解説したThe Gradientの2024年3月掲載記事である。

自動運転の従来アプローチは「モジュール型」と「End-to-End学習」の2系統に大別される。モジュール型はPerception・Localization・Planning・Controlの4モジュールを独立設計する手法で、解釈性が高い反面、モジュール間の誤差伝播が課題。End-to-End学習は単一ニューラルネットワークで操舵・加速を直接予測するが、ブラックボックス問題が残る。LLMはこれらの課題を補完する「第三の候補」として注目されている。

LLMの自動運転への適用にあたっては、入力をトークン化する必要がある。画像はVision Transformer（ViT）、LiDAR点群やRADARデータも同様にトークン列へ変換可能であり、Transformerコア自体は入力モダリティに依存しない。出力はシーン記述・走行指示・Q&A応答など複数のタスク形式で設計できる。

研究が活発な領域は主に4つ。①Perception：GPT-4 VisionやHiLM-D、MTD-GPTがマルチビュー画像から物体検出・追跡（PromptTrackはDETRとLLMを統合してID管理）を実施。②Planning：DriveLikeAHuman、DriveVLM、GPT-Driverなどがシーン記述から走行判断（車線変更・停止等）を生成。DriveVLMはBEV（Bird's Eye View）表現を活用して空間推論を強化。③データ生成：拡散モデルと組み合わせて代替シナリオや学習データを生成し、ロングテールな稀有シーン（霧・夜間・逆光等）への対応データを補完。④Q&A・説明性：DrivGPTやLingoQAは「なぜ今ブレーキをかけたか」を自然言語で説明し、監査・信頼性確保の観点から重要。

LLM導入の主なメリットは3点：(1) 事前学習済みの世界知識（交通法規・物理常識）をゼロショットで転用できる、(2) テキスト・画像・センサーを統合したマルチモーダル推論が可能、(3) 判断根拠を自然言語で説明できる。一方、課題はリアルタイム推論の計算コスト（自動車では100ms以下の応答が要求される）、センサーデータの精密なトークン化設計、および安全クリティカルな判断における幻覚（Hallucination）リスクである。

監査エージェント開発への示唆：LLMが判断根拠を自然言語で説明するアーキテクチャ（DrivGPT型）は、監査AIにおける「判断トレーサビリティ」設計と直接対応する。Perceptionモジュールの出力をLLMのコンテキストとして渡すパイプライン構成は、ReActエージェントにおけるツール結果のコンテキスト注入と同型であり、設計パターンとして参照価値が高い。

## アイデア

- DrivGPT・LingoQAのような「判断根拠を自然言語で説明するPlanning LLM」は、自動運転だけでなく監査AIの説明性要件（なぜそのリスク判定をしたか）にそのまま転用できる設計パターンである
- LiDAR点群・RADAR・カメラ映像を統一的にトークン化してTransformerに入力するマルチモーダルパイプラインは、異種データ（財務数値・テキスト報告書・ログ）を扱う監査エージェントのコンテキスト設計に応用できる
- 稀有シーン（霧・夜間等）の学習データ不足を拡散モデルで補う手法は、監査で頻度の低い不正パターンへの対応データ拡張戦略として参考になる

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **Vision Transformer (ViT)** (TODO: 読むべき)
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **マルチモーダルLLM** → /deep_171 MedGemma 1.5による次世代医療画像解析と音声認識モデルMedASRの公開
- **BEV (Bird's Eye View)** (TODO: 読むべき)

## 関連記事

- /deep_3785 遮蔽に強い3D人体メッシュ復元のための識別・生成シナジーフレームワーク
- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_1912 ハルシネーションの構造的解明：認識の失敗からフレームの誤作動へ
- /deep_1835 【実録】GeminiはGoogle自社サービスの夢を見るか？ ―― ハルシネーションの実例・傾向・対策

## 原文リンク

[Car-GPT：LLMは自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
