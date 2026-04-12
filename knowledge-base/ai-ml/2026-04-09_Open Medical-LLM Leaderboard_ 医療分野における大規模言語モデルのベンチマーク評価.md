---
title: "Open Medical-LLM Leaderboard: 医療分野における大規模言語モデルのベンチマーク評価"
url: "https://huggingface.co/blog/leaderboard-medicalllm"
date: 2026-04-09
tags: [Medical-LLM, benchmark, USMLE, MedQA, MedMCQA, PubMedQA, MMLU, lm-evaluation-harness, GPT-4, Med-PaLM-2]
category: "ai-ml"
memo: "[HF Blog] The Open Medical-LLM Leaderboard: Benchmarking Large Language Models in Healthcare"
related: [23, 212, 1068, 902, 975]
processed_at: "2026-04-09T09:52:13.630799"
---

## 要約

Hugging Faceが2024年4月に公開したOpen Medical-LLM Leaderboardは、医療分野に特化したLLM評価プラットフォームである。医療AIの誤情報は患者ケアに直接影響するという実課題（例：GPT-3が妊婦にテトラサイクリンを誤推奨）を背景に、標準化された評価基盤の必要性から構築された。

評価データセットは以下の7種類：(1) MedQA（USMLE形式、テスト1,273問、4-5択）、(2) MedMCQA（インド医師国家試験AIIMS/NEET由来、187,000問以上、21医療科目）、(3) PubMedQA（PubMedアブストラクトを文脈とするYes/No/Maybe回答、1,000問）、(4)〜(9) MMLU医療・生物サブセット6種（臨床知識265問、医学遺伝学100問、解剖学135問、専門医学272問、大学生物学144問、大学医学173問）。評価指標は全て正解率（accuracy）で統一。

主な評価結果として、商用モデルのGPT-4-baseとMed-PaLM-2が全データセットで高精度を維持。オープンソースモデルでは7Bパラメータ規模のStarling-LM-7B、gemma-7b、Mistral-7B-v0.1、Hermes-2-Pro-Mistral-7Bが特定タスクで競争力ある性能を示した。Google Gemini Proは生物統計学・細胞生物学・産婦人科で高性能を発揮する一方、解剖学・心臓病学・皮膚科学では中〜低精度にとどまり、領域間のムラが顕在化した。

モデル提出要件はSafetensors形式への変換、HuggingFace AutoClasses（AutoConfig/AutoModel/AutoTokenizer）との互換性確保、Apache 2.0等のオープンライセンス設定の3点。評価はlm-evaluation-harnessフレームワーク上で実施され、few-shot設定（MedQA: 5-shot等）で統一されている。このリーダーボードは医療LLM開発者が自モデルの弱点領域を特定し、改善サイクルを回すための公開インフラとして機能する。

## アイデア

- 医療という高リスクドメイン特有のベンチマーク設計：汎用LLMベンチ（MMLU全体）から医療サブセットを抽出・組み合わせることで、ドメイン特化評価を低コストで構築できる設計思想は、監査・法務・会計など他の高信頼性ドメインへそのまま転用可能
- GPT-3の妊婦へのテトラサイクリン誤推奨事例のように、モデルが正しい禁忌知識を持ちながら最終推奨で矛盾を起こす『知識と推論の乖離』パターンは、LLM-as-judgeやファクトチェックエージェント設計時の重要な失敗モードとして参照価値が高い
- 7Bパラメータのオープンソースモデルが特定医療タスクで商用大型モデルに匹敵する結果は、ローカルLLMインフラ（RTX 3090等）での専門ドメインLLM運用の実現可能性を示す証拠として機能する
## 関連記事

- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_212 波形から知恵へ：聴覚知能の新ベンチマーク MSEB（Massive Sound Embedding Benchmark）
- /deep_1068 構造化生成によるプロンプト一貫性の改善
- /deep_902 日本語LLMオープンリーダーボードの公開
- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）

## 原文リンク

[Open Medical-LLM Leaderboard: 医療分野における大規模言語モデルのベンチマーク評価](https://huggingface.co/blog/leaderboard-medicalllm)
