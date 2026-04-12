---
title: "Vision Language Models（より良く、より速く、より強く）- 2025年最新動向"
url: "https://huggingface.co/blog/vlms-2025"
date: 2026-04-07
tags: [VLM, multimodal, MoE, RLVR, RLAIF-V, SmolVLM, Qwen2.5-VL, ColPali, multimodal-RAG, multimodal-agent, VLA, reasoning-model]
category: "ai-ml"
memo: "[HF Blog] Vision Language Models (Better, faster, stronger)"
related: [522, 587, 1608, 819, 975]
processed_at: "2026-04-07T21:37:27.445965"
---

## 要約

Hugging Faceによる2025年版VLM総括ブログ。2024年4月の前回投稿以降の主要な進展を体系的にまとめている。

【新モデルトレンド】
1. **Any-to-anyモデル**: テキスト・画像・音声を相互変換。Qwen2.5 Omniは「Thinker-Talker」アーキテクチャを採用し、テキスト生成とストリーミング音声出力を分離。DeepSeekのJanus-Pro-7Bは理解と生成で視覚エンコーダを分離する構造を採用。
2. **推論モデル**: QVQ-72B-previewに続き、Moonshot AIのKimi-VL-A3B-ThinkingがMoEデコーダ（総16B/実効2.8Bパラメータ）＋長Chain-of-Thought＋強化学習アライメントで登場。長尺動画・PDF・スクリーンショット対応のエージェント機能も持つ。
3. **小型高性能モデル**: SmolVLM2（256M/500M/2.2B）はiPhoneアプリ「HuggingSnap」で動画理解を実証。Gemma3-4b-itは128kコンテキスト・140言語対応の最小級マルチモーダルモデル。Qwen2.5-VL-3Bは物体検出・文書理解・エージェントタスクを32kコンテキストで処理。
4. **MoEデコーダ**: 代表例はKimi-VL-A3B（2.8B active/16B total）。稀にしか使われないエキスパートをオフロードすることで推論速度と効率を両立。
5. **Vision-Language-Action（VLA）モデル**: ロボティクスへの応用。π0、OpenVLA-OFT、RoboVLMsなどが台頭。

【専門的能力の拡張】
- 物体検出・セグメンテーション・カウント（Qwen2.5-VL、Molmo等）
- マルチモーダル安全モデル（Llama Guard 4、WildGuard等）
- マルチモーダルRAG（ColPali: パッチレベルの視覚埋め込みによるPDF検索、DSE等）
- マルチモーダルエージェント（UI-TARS: スクリーンショットのみでGUIを操作）
- 動画言語モデル（Qwen2.5-VL、LLaVA-Video、長尺動画対応モデル）

【新アライメント手法】
- RLAIF-V、RLVR（Qwen2.5-VLで採用）、LLaVA-RLHF、VLFeedbackなど視覚特化のRL手法が整備されつつある。

【新ベンチマーク】
- MMT-Bench: 32種タスク・162スキルをカバーするマルチタスク評価
- MMMU-Pro: 図表理解の難易度を引き上げた強化版MMMU

## アイデア

- ColPaliのパッチレベル視覚埋め込みによるPDF検索は、監査調書・財務報告書のような図表混在ドキュメントに対するRAGの精度を根本的に改善できる可能性がある
- RLVR（Reinforcement Learning from Verifiable Rewards）をVLMに適用するアプローチは、正誤が明確な監査チェック（数値照合・基準適合性判定）タスクへの報酬設計に直接転用できる
- UI-TARSのようなスクリーンショットのみでGUI操作を行うエージェントは、ERP・GRCシステムへのエージェントアクセスをAPIなしで実現する手段として注目に値する
## 関連記事

- /deep_522 TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク
- /deep_587 Holo1: GUIエージェント「Surfer-H」を動かす新しいGUI自動化VLMファミリー
- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_819 外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline
- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）

## 原文リンク

[Vision Language Models（より良く、より速く、より強く）- 2025年最新動向](https://huggingface.co/blog/vlms-2025)
