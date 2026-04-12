---
title: "ScreenSuite - GUIエージェント向け最も包括的な評価スイート"
url: "https://huggingface.co/blog/screensuite"
date: 2026-04-07
tags: [GUI-Agent, VLM, ベンチマーク, smolagents, OSWorld, AndroidWorld, Qwen2.5-VL, vision-only, 評価フレームワーク, Docker]
category: "agent-arch"
memo: "[HF Blog] ScreenSuite - The most comprehensive evaluation suite for GUI Agents!"
related: [587, 1608, 305, 650, 522]
processed_at: "2026-04-07T21:01:09.731518"
---

## 要約

HuggingFaceが2025年6月に公開したScreenSuiteは、GUIエージェントの性能を多角的に評価するためのベンチマーク統合スイート。GUIエージェントとは、デスクトップやスマートフォンのGUI上でクリック・入力・スクロールなどの操作を行うAIエージェントであり、Claude Computer UseやOpen Computer Agent（Qwen2.5-VL-72B搭載）がその代表例。

ScreenSuiteは、GUI能力を「知覚（Perception）」「グラウンディング（Grounding）」「単一ステップ操作」「マルチステップ操作」の4カテゴリに分類し、13のベンチマークを統合する。具体的には、ScreenQA-Short（モバイル、8,400サンプル）・ScreenQA-Complex（11,800サンプル）・ScreenSpot-v2（デスクトップ、1,300サンプル）・ScreenSpot-Pro（1,600サンプル）・WebSRC（Web、52,000サンプル）・VisualWebBench（1,500サンプル）などの知覚・グラウンディング系、AndroidControl（モバイル、3,000サンプル）・Multimodal-Mind2Web（Web、6,400サンプル）などの単一ステップ系、そしてAndroidWorld・OSWorld（369タスク）・BrowseComp（1,270サンプル）・GAIA-Web（132サンプル）・Mind2Web-Live（208サンプル）のマルチステップ系が含まれる。

技術的な特徴として、評価はアクセシビリティツリーやDOMメタデータを一切使用せず「ビジョンのみ（vision-only）」で実施する点が重要。これにより既存のリーダーボードとスコアが異なる場合があるが、より現実的で難易度の高い評価環境を実現している。たとえばMind2Webは従来のelement-name選択方式からバウンディングボックス内クリック精度方式に変更し難易度を大幅に引き上げた。

マルチステップベンチマークの実行にはUbuntuデスクトップやAndroidの仮想環境が必要なため、E2BリモートサンドボックスおよびDocker上のカスタムコンテナを提供。エージェント実行フレームワークにはsmolagentsを採用している。

評価対象モデルはQwen-2.5-VLシリーズ（3B〜72B）、UI-Tars-1.5-7B（ByteDance）、Holo1-7B（H company）、GPT-4o。リポジトリはGitHubで公開され、`uv sync`で環境構築後`python run.py`のみで評価を開始できる設計になっている。

## アイデア

- vision-only評価という設計思想：アクセシビリティツリーやDOM等のメタデータを排除することで、モデルが人間と同様に視覚情報のみから操作を判断できるかを純粋に測定できる。これはエージェントの汎用性評価として本質的なアプローチ。
- 13ベンチマークを単一フレームワーク（smolagents）で統一したモジュール設計：各ベンチマークの前処理・実行・評価ロジックを一貫した形式に揃えることで、モデル間の公正な比較と再現性を担保している。Eleuther LM Evaluation Harnessのアプローチを視覚系エージェントに応用した構造。
- DockerによるUbuntu/Androidエミュレータのローカル展開：クラウド依存を排除し、マルチステップ評価をベアメタル環境でオンプレ実行できる設計は、セキュリティ要件の厳しい組織（金融・監査等）での活用にも適している。
## 関連記事

- /deep_587 Holo1: GUIエージェント「Surfer-H」を動かす新しいGUI自動化VLMファミリー
- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_305 オープンモデルでOCRパイプラインを強化する：VLMベースドキュメントAIの実践ガイド
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_522 TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク

## 原文リンク

[ScreenSuite - GUIエージェント向け最も包括的な評価スイート](https://huggingface.co/blog/screensuite)
