---
title: "Holo1: GUIエージェント「Surfer-H」を動かす新しいGUI自動化VLMファミリー"
url: "https://huggingface.co/blog/Hcompany/holo1"
date: 2026-04-07
tags: [VLM, GUI-agent, UIローカライゼーション, Qwen2.5-VL, web-automation, multimodal, Surfer-H, WebClick]
category: "agent-arch"
memo: "[HF Blog] Holo1: New family of GUI automation VLMs powering GUI agent Surfer-H"
related: [1608, 650, 522, 584, 819]
processed_at: "2026-04-07T21:02:40.524889"
---

## 要約

H CompanyがHolo1を発表した。これはWeb UI理解と精密なUI要素ローカライゼーション（画面上の座標特定）に特化したAction VLM（行動可能なビジョン言語モデル）のオープンソースファミリーである。モデルはHolo1-3BとHolo1-7Bの2種類があり、Holo1-7BはUIローカライゼーションの主要ベンチマーク平均で76.2%の精度を達成し、小型モデルの中では最高性能を記録した。アーキテクチャはQwen2.5-VLベースで、HuggingFace Transformersと完全互換。flash_attention_2対応でbfloat16推論が可能。

合わせてWebClickベンチマークも公開された。これは1,639件の人間的なUIタスクから構成されるマルチモーダルなUI操作評価セットである。

Holo1を基盤として動作するWebエージェントがSurfer-Hである。Surfer-Hはブラウザ上でのWeb自動化タスクを人間と同様の操作（クリック、スクロール、タイピング等）でこなすモジュラーアーキテクチャを採用している。内部は3つの独立コンポーネントで構成される：(1) Policyモデル（計画立案・行動駆動）、(2) Localizerモデル（視覚的UI理解・精密インタラクション）、(3) Validatorモデル（タスク完了確認）。カスタムAPIやDOMラッパーに依存せず、純粋にブラウザ操作のみで動作する点が特徴的である。

WebVoyagerベンチマークにおいて実世界のWebタスクで92.2%の精度を達成し、タスクあたりのコストは$0.13という低コスト。これはコスト効率とパフォーマンスのパレートフロンティアを更新するものとして位置づけられている。ライセンスはApache 2.0であり商用利用も可能。

## アイデア

- Policy/Localizer/Validatorを独立したモデルに分離するモジュラー設計は、各コンポーネントを個別にファインチューニング・置換できる柔軟性をもたらす。監査エージェントでも同様の役割分離（判断・証跡取得・検証）が設計指針になり得る
- UIの視覚的ローカライゼーション（スクリーン座標のClick(x,y)出力）という単純なインターフェース設計により、ブラウザDOM構造やカスタムAPIへの依存を排除している。これは脆弱なセレクタベースの自動化と対照的な堅牢なアプローチ
- Validatorモデルを独立させることでタスク完了の自己評価をエージェントループに組み込む構造は、LLM-as-judgeの実装パターンとして参考になる
## 関連記事

- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_522 TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク
- /deep_584 ScreenSuite - GUIエージェント向け最も包括的な評価スイート
- /deep_819 外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline

## 原文リンク

[Holo1: GUIエージェント「Surfer-H」を動かす新しいGUI自動化VLMファミリー](https://huggingface.co/blog/Hcompany/holo1)
